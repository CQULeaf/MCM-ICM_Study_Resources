import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置全局字体为Palatino Linotype
mpl.rcParams['font.family'] = 'Palatino Linotype'

# 加载数据文件
file_paths = ['Alcaraz_vs_Djokovic_set1.csv', 'Alcaraz_vs_Djokovic_set2.csv', 'Alcaraz_vs_Djokovic_set3.csv', 'Alcaraz_vs_Djokovic_set4.csv', 'Alcaraz_vs_Djokovic_set5.csv']
datasets = [pd.read_csv(file_path) for file_path in file_paths]

def calculate_performance_with_weights(data, p1_weight_server, p2_weight_server, p1_weight_receiver, p2_weight_receiver):
    def calculate_performance(row):
        if row['server'] == 1:
            p1_performance_weight = p1_weight_server
            p2_performance_weight = p2_weight_server
        else:
            p1_performance_weight = p1_weight_receiver
            p2_performance_weight = p2_weight_receiver

        if row['point_victor'] == 1:
            p1_performance = 1 * p1_performance_weight
            p2_performance = 0 * p2_performance_weight
        elif row['point_victor'] == 2:
            p1_performance = 0 * p1_performance_weight
            p2_performance = 1 * p2_performance_weight

        return pd.Series([p1_performance, p2_performance, p1_performance - p2_performance])

    data[['p1_performance', 'p2_performance', 'performance_diff']] = data.apply(calculate_performance, axis=1)
    data['performance_diff'] = data['performance_diff'].cumsum()
    return data

plt.figure(figsize=(14, 6))

weight_combinations = [
    (0.4, 0.6, 0.6, 0.4, 'Original', 'black'),
    (0.45, 0.55, 0.55, 0.45, 'Adjusted', 'red'),
    (0.35, 0.65, 0.65, 0.35, 'Equal', 'blue'),
    (0.3, 0.7, 0.7, 0.3, 'Extreme', 'green')
]

line_styles = ['-', '--', '-.', ':']

for i, (p1w_s, p2w_s, p1w_r, p2w_r, label, color) in enumerate(weight_combinations):
    for j, data in enumerate(datasets):
        data_copy = calculate_performance_with_weights(data.copy(), p1w_s, p2w_s, p1w_r, p2w_r)
        plt.plot(data_copy['point_no'], data_copy['performance_diff'], line_styles[i % len(line_styles)], color=color, label=f'{label} Set {j+1}', linewidth=2)

plt.axhline(y=0, color='black', linewidth=1.5)
plt.xlabel('Point Number', fontsize=20)
plt.ylabel('Performance Value Difference', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.grid(True)
plt.show()
