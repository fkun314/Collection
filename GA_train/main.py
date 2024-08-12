import random
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
import glob
import imageio
import pandas as pd

    
# 遺伝的アルゴリズムのパラメータ
# population_size = 540
# generations = 2
# mutation_rate = 0.01
# crossover_rate = 0.7
notch_positions = [1, 2, 3, 4, 0, -1, -2, -3, -4, -5, -6, -7]
speed_positions = [0.8, 1.5, 2.5, 3.3, 0, -0.8, -1.5, -2.5, -3.3, -4.0, -4.5, -5.0]

# 制約条件
max_speed = 105  # km/h
distance = 6.3  # km
target_time = 340  # seconds

def simulate_with_position_tracking(individual, max_speed, distance):
    """
    鉄道の走行時間をシミュレートし、速度と位置の変化を記録する関数。

    :param individual: ノッチの配列
    :param max_speed: 最高速度 (km/h)
    :param distance: 目的地までの距離 (km)
    :return: 所要時間 (秒), 速度の記録, 位置の記録
    """
    notch_acceleration = {
        4: 3.3, 3: 2.8, 2: 2.4, 1: 1.8, 0: 0,
        -1: -0.8, -2: -1.5, -3: -2.5, -4: -3.3, -5: -4.0, -6: -4.5, -7: -5.0
    }

    current_speed = 0.0  # 現在の速度 (km/h)
    total_distance = 0.0  # 累積距離 (km)
    total_time = 0.0  # 累積時間 (秒)
    speed_tracking = []  # 速度の記録
    position_tracking = []  # 位置の記録

    max_speed_mps = max_speed * 1000 / 3600

    for notch in individual:
        # 加減速度を m/s² に変換
        acceleration = notch_acceleration[notch] * 1000 / 3600

        # 加減速
        current_speed += acceleration * 1.0  # 1.0秒ごとの加減速

        # 最高速度の制約を適用
        if current_speed > max_speed_mps:
            current_speed = max_speed_mps
        elif current_speed < 0:
            current_speed = 0

        # 距離と時間の更新
        total_distance += current_speed * 1.0  # 1.0秒ごとの距離
        total_time += 1.0
        speed_tracking.append(current_speed * 3600 / 1000)  # m/sをkm/hに変換して記録
        position_tracking.append(total_distance / 1000)  # mをkmに変換して記録

        # 目的地に到達した場合
        if total_distance >= distance * 1000:  # kmをmに変換
            break

    return total_time, speed_tracking, position_tracking



def parse_genetic_information(genetic_string):
    """
    文字列形式の遺伝子情報を数値のノッチ情報に変換する関数。
    '4'はノッチ4、'-'は減速を表し、例えば'-4'はノッチ-4を意味する。

    :param genetic_string: 文字列形式の遺伝子情報
    :return: 数値のノッチ情報のリスト
    """
    notch_info = []
    i = 0
    while i < len(genetic_string):
        if genetic_string[i] == '-':
            # 減速ノッチ
            notch_info.append(-int(genetic_string[i+1]))
            i += 2
        else:
            # 加速ノッチ
            notch_info.append(int(genetic_string[i]))
            i += 1
    return notch_info

def plot_speed_and_position(genetic_string, max_speed, distance, directory_path, generation):
    """
    文字列形式の遺伝子情報から速度と位置の変化をグラフで表示する関数。

    :param genetic_string: 文字列形式の遺伝子情報
    :param max_speed: 最高速度 (km/h)
    :param distance: 目的地までの距離 (km)
    :param directory_path: 保存先のディレクトリパス
    :param generation: 世代数
    """
    #リスト形式で入力された場合は文字列の遺伝子情報に変換
    if type(genetic_string) == list:
        genetic_string = ''.join([str(n) for n in genetic_string])
    
    # 遺伝子情報を解析
    individual = parse_genetic_information(genetic_string)

    # シミュレーションを実行
    simulated_time, speed_tracking, position_tracking = simulate_with_position_tracking(individual, max_speed, distance)

    # テスト
    score = evaluate_performance_adjusted(simulated_time, speed_tracking[-1], position_tracking[-1])
    print("Score:", score)
    
    distance = 6.3  # km
    target_time = 340  # seconds
    
    # # 速度と位置の変化をプロット
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(range(len(speed_tracking)), speed_tracking)
    plt.title("Speed Changes During Simulation")
    plt.ylabel("Speed (km/h)")
    
    # target_timeの線を引く
    plt.vlines(target_time, 0, max(speed_tracking), linestyle='dashed', color='red')
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(range(len(position_tracking)), position_tracking)
    plt.title("Position Changes During Simulation")
    plt.xlabel("Time (s)")
    plt.ylabel("Position (km)")
    
    # x軸に目標時間を設定
    plt.vlines(target_time, 0, max(position_tracking), linestyle='dashed', color='red')
    plt.grid(True)

    plt.tight_layout()
    # plt.show()
    if(not os.path.exists(directory_path)):
        os.makedirs(directory_path)
    plt.savefig(os.path.join(directory_path, f"generation_{generation}.png"))
    
    if generation == 99:
        # 最終の遺伝子のspeed_trackingとposition_trackingをCSVファイルに保存
        df = pd.DataFrame({
            "speed": speed_tracking,
            "position": position_tracking
        })
        df.to_csv(os.path.join(directory_path, "speed_and_position.csv"), index=False)
    
    
def evaluate_performance_adjusted(simulated_time, final_speed, final_position, target_time=340, target_distance=6.4, perfect_score=10000, time_penalty=200, distance_penalty=1000, speed_tolerance=0.8):
    """
    シミュレーション結果を評価する関数。到着時の速度が0.8km/h以内は0km/hとみなす。

    :param simulated_time: シミュレートされた所要時間 (秒)
    :param final_speed: 最終速度 (km/h)
    :param final_position: 最終位置 (km)
    :param target_time: 目標時間 (秒)
    :param target_distance: 目標距離 (km)
    :param perfect_score: 完璧な到着に対するスコア
    :param time_penalty: 時間のずれに対するペナルティ
    :param distance_penalty: 距離のずれに対するペナルティ
    :param speed_tolerance: 速度の許容誤差 (km/h)
    :return: 評価スコア
    """
    
    
    score = 0
    if type(final_speed) == list:
        # 全ての速度の差分を取得
        speed_difference = [abs(speed - target_time) for speed in final_speed]
        # ２乗して平均を取る
        speed_difference = np.mean(np.array(speed_difference)**2)
        # score -= speed_difference * 1
        final_speed = final_speed[-1]
    if type(final_position) == list:
        final_position = final_position[-1]
        
    score_time = 0
    score_distance = 0
    score_stopped = 0

    # 時間の精度評価
    time_difference = abs(simulated_time - target_time)
    score_time += perfect_score - time_difference * time_penalty
    # score += time_penalty * time_difference

    # debug
    # print("simulated_time シミュレートされた所要時間 (秒):", simulated_time)
    # print("time_difference 到着した時間のズレ（秒）:", time_difference)
    # print("score_time:", score_time)
    
    
    # 距離の精度評価
    distance_difference = abs(final_position - target_distance)
    score_stopped += perfect_score - distance_difference * distance_penalty
    
    # debug
    # print("target_distance 目標距離 (km):", target_distance)
    # print("distance_difference 目標位置とのズレ（km）:", distance_difference)
    # print("score_stopped:", score_stopped)
    
    
    # score += distance_penalty * distance_difference
    
    score = score_time + score_stopped
    

    # 速度が許容誤差内でなければ減点
    if final_speed > 0:
        score -= 20 * abs(final_speed)
        

    return score


# # # テスト用の遺伝子情報
# genetic_string_test = "44444444444400000000000000000000000" * 10  # 遺伝子情報を10回繰り返す

# # # グラフ表示関数を実行
# plot_speed_and_position(genetic_string_test, max_speed, distance)
# 可視化用の関数
def visualize_evolution(scores, best_genes, gene_length, directory_path):
    filenames = []

    for i, (score, gene) in enumerate(zip(scores, best_genes)):
        # スコアのグラフ
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.plot(scores[:i+1])
        plt.title("Score Evolution")
        plt.xlabel("Generation")
        plt.ylabel("Score")

        # 遺伝子のグラフ
        plt.subplot(1, 2, 2)
        plt.bar(range(gene_length), gene)
        plt.title("Gene at Generation " + str(i+1))
        plt.xlabel("Gene Index")
        plt.ylabel("Value")

        # 一時ファイルに保存
        filename = f'generation_{i+1}.png'
        plt.savefig(filename)
        filenames.append(filename)
        plt.close()

    # GIFアニメーションを作成
    with imageio.get_writer(os.path.join(directory_path, "evolution.gif"), mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
            os.remove(filename)


def create_individual(gene_length):
    """
    新しい個体（遺伝子）を生成する。

    :param gene_length: 遺伝子の長さ
    :return: 新しい個体（遺伝子）
    """
    # ノッチは[-7, -6, ..., 4]の範囲でランダムに選択
    i = random.choice(range(-7, 9))
    if i > 4:
        i -= 4
    return [i for _ in range(gene_length)]

def mutate(individual, mutation_rate):
    """
    個体を突然変異させる。

    :param individual: 個体（遺伝子）
    :param mutation_rate: 突然変異率
    :return: 突然変異した個体
    """
    j = random.choice(range(-7, 9))
    if j > 4:
        j -= 4
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = j
    return individual

def crossover(parent1, parent2, crossover_rate):
    """
    二つの個体を交叉させる。

    :param parent1: 親個体1
    :param parent2: 親個体2
    :param crossover_rate: 交叉率
    :return: 二つの子個体
    """
    if random.random() < crossover_rate:
        # crossover_point = random.randint(1, len(parent1) - 1)
        crossover_point = 170
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    else:
        return parent1, parent2
    
    # crossover_point = 170
    # # crossover_point = random.randint(1, len(parent1) - 1)
    # child1 = parent1[:crossover_point] + parent2[crossover_point:]
    # child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


def tournament_selection(population, tournament_size):
    """
    トーナメント選択を用いて次世代の個体を選択する。

    :param population: 現世代の個体群
    :param tournament_size: トーナメントのサイズ
    :return: 選択された個体
    """
    chosen = []
    for _ in range(len(population)):
        competitors = random.sample(population, tournament_size)
        chosen.append(max(competitors, key=lambda ind: ind['fitness']))
    return chosen

def genetic_algorithm(gene_length, population_size, generations, mutation_rate, crossover_rate, tournament_size, elite_size ,directory_path):
    # 初期個体群を生成
    population = [{'gene': create_individual(gene_length), 'fitness': float('-inf')} for _ in range(population_size)]
    
    scores = []  # スコアを記録するリスト
    best_genes = []  # 最高スコアの遺伝子を記録するリスト


    for generation in range(generations):
        # 各個体の適応度を評価
        for individual in population:
            # 適応度評価関数をここで呼び出す
            individual['fitness'] = evaluate_performance_adjusted(*simulate_with_position_tracking(individual['gene'], max_speed, distance))
            pass

        # 世代ごとの最高スコアを出力
        best_individual = max(population, key=lambda ind: ind['fitness'])
        print(f"Generation {generation + 1}: Best Score = {best_individual['fitness']}")
        
         # 世代ごとの最高スコアと遺伝子を記録
        best_individual = max(population, key=lambda ind: ind['fitness'])
        scores.append(best_individual['fitness'])
        best_genes.append(best_individual['gene'])
        
        # 最終の遺伝子の情報をグラフに表示
        plot_speed_and_position(best_individual['gene'], max_speed, distance, directory_path, generation)

        # エリート個体を選定
        elites = sorted(population, key=lambda ind: ind['fitness'], reverse=True)[:elite_size]

        # 次世代の個体群を選択
        selected = tournament_selection(population, tournament_size)

        # 交叉と突然変異により次世代を生成
        next_generation = elites.copy()  # エリート個体を次世代にコピー
        while len(next_generation) < population_size:
            # 交叉と突然変異を行う
            parent1, parent2 = random.choice(selected)['gene'], random.choice(selected)['gene']
            child1, child2 = crossover(parent1, parent2, crossover_rate)
            next_generation.append({'gene': mutate(child1, mutation_rate), 'fitness': float('-inf')})
            next_generation.append({'gene': mutate(child2, mutation_rate), 'fitness': float('-inf')})

        population = next_generation

    return max(population, key=lambda ind: ind['fitness']), scores, best_genes

def make_gif(directory_path):
    # GIFアニメーションを作成
    filenames = glob.glob(os.path.join(directory_path, "*.png"))
    with imageio.get_writer(os.path.join(directory_path, "generation.gif"), mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
            # os.remove(filename)


# 遺伝的アルゴリズムの実行（適応度評価関数と遺伝子の長さ等のパラメータを設定して使用）
gene_length = 340
population_size = 1000
generations = 100
mutation_rate = 0.02
crossover_rate = 1.0
tournament_size = 100
elite_size = 30

directory_path = datetime.now().strftime("%Y%m%d_%H%M%S")

best_individual, scores, best_genes = genetic_algorithm(gene_length, population_size, generations, mutation_rate, crossover_rate, tournament_size, elite_size,directory_path)
visualize_evolution(scores, best_genes, gene_length, directory_path)
make_gif(directory_path)
print("Best Individual:", best_individual)

# 100世代目のbest_individualの速度と位置をグラフに表示
plot_speed_and_position(best_individual['gene'], max_speed, distance, directory_path, generations)


import pandas as pd
import os


# パラメータのDataFrameを作成
df_params = pd.DataFrame({
    "gene_length": [gene_length],
    "population_size": [population_size],
    "generations": [generations],
    "mutation_rate": [mutation_rate],
    "crossover_rate": [crossover_rate],
    "tournament_size": [tournament_size],
    "elite_size": [elite_size]
})


# CSVファイルに保存
df_params.to_csv(os.path.join(directory_path, "result.csv"), index=False)
