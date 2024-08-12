import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('hoge.csv')

# data = pd.read_csv(file_path)

# データセットの分離
data1 = data[['time[s]', 'speed[km/h]']].dropna()
data2 = data[['time[s].1', 'speed[km/h].1']].rename(columns={'time[s].1': 'time[s]', 'speed[km/h].1': 'speed[km/h]'}).dropna()

plt.figure(figsize=[12,4.2])

# データセット1のプロット
plt.scatter(data1['time[s]'], data1['speed[km/h]'], color='red', label='real data')

# データセット2のプロット
plt.scatter(data2['time[s]'], data2['speed[km/h]'], color='blue', label='simulated data')

# グラフのタイトルと軸ラベルの設定
plt.title("Real and Simulated Data")
plt.xlabel("Time [s]")
plt.ylabel("Speed [km/h]")
plt.legend()
plt.grid(True)
# plt.show()

plt.savefig('hoge.png')