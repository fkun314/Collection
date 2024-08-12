`create_individual(gene_length`

遺伝子の生成

gene_lengthは遺伝子の長さを指定し、遺伝子は-7から4までの整数からランダムに選ばれた数値のリストとして生成される。
``
mutate(individual, mutation_rate)``

この関数は個体に突然変異を適用する。

mutation_rateは突然変異の発生確率を指定し、この確率に従って個体の遺伝子がランダムに変更される。
``
crossover(parent1, parent2, crossover_rate)``

この関数は二つの個体（親）から交叉を行い、二つの子個体を生成する。
crossover_rateは交叉が発生する確率。

交叉点はランダムに選ばれ、その点を基に親の遺伝子が組み合わされて子個体が生成される。

``
tournament_selection(population, tournament_size)``

この関数はトーナメント選択を用いて次世代の個体を選択する。
トーナメント選択は、ランダムに選ばれた一定数の個体（tournament_size）の中から最も適応度の高い個体を選ぶ方法。