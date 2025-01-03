import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置全局字体为Palatino Linotype
mpl.rcParams['font.family'] = 'Palatino Linotype'

file_path_1 = 'Djere_vs_Tsitsipas_set1.csv'
file_path_2 = 'Djere_vs_Tsitsipas_set2.csv'
file_path_3 = 'Djere_vs_Tsitsipas_set3.csv'

data_1 = pd.read_csv(file_path_1)
data_2 = pd.read_csv(file_path_2)
data_3 = pd.read_csv(file_path_3)

# 计算性能指标
def calculate_performance(row):
    p1_performance = p2_performance = 0
    # 设置性能权重
    if row['server'] == 1:
        p1_performance_weight = 0.4
        p2_performance_weight = 0.6
    else:
        p1_performance_weight = 0.6
        p2_performance_weight = 0.4

    # 根据点数胜者设置性能
    if row['point_victor'] == 1:
        p1_performance = 1 * p1_performance_weight
        p2_performance = 0 * p2_performance_weight
    elif row['point_victor'] == 2:
        p1_performance = 0 * p1_performance_weight
        p2_performance = 1 * p2_performance_weight

    return pd.Series([p1_performance, p2_performance, p1_performance - p2_performance])

# 应用计算函数
data_1[['p1_performance', 'p2_performance', 'performance_diff']] = data_1.apply(calculate_performance, axis=1)
data_2[['p1_performance', 'p2_performance', 'performance_diff']] = data_2.apply(calculate_performance, axis=1)
data_3[['p1_performance', 'p2_performance', 'performance_diff']] = data_3.apply(calculate_performance, axis=1)

# 将'performance_diff'累加
data_1['performance_diff'] = data_1['performance_diff'].cumsum()
data_2['performance_diff'] = data_2['performance_diff'].cumsum()
data_3['performance_diff'] = data_3['performance_diff'].cumsum()

# 设置绘图大小
plt.figure(figsize=(14, 6))

# 绘制 performance_diff 随 point_no 的变化,一张图里面5条曲线
plt.plot(data_1['point_no'], data_1['performance_diff'], label='Set 1', linewidth=2, marker='o', color = '#A2AFC4', markersize=3)
plt.plot(data_2['point_no'], data_2['performance_diff'], label='Set 2', linewidth=2, marker='o', color = '#78837E', markersize=3)
plt.plot(data_3['point_no'], data_3['performance_diff'], label='Set 3', linewidth=2, marker='o', color = '#b4a992', markersize=3)

# 设置图例
plt.legend(loc='upper left', fontsize=16)
plt.xlabel('Point Number', fontsize=20)
plt.ylabel('Performance Difference', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.grid(True)
plt.show()