import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置全局字体为Palatino Linotype
mpl.rcParams['font.family'] = 'Palatino Linotype'

file_path_1 = 'Alcaraz_vs_Djokovic_set1.csv'
file_path_2 = 'Alcaraz_vs_Djokovic_set2.csv'
file_path_3 = 'Alcaraz_vs_Djokovic_set3.csv'
file_path_4 = 'Alcaraz_vs_Djokovic_set4.csv'
file_path_5 = 'Alcaraz_vs_Djokovic_set5.csv'

data_1 = pd.read_csv(file_path_1)
data_2 = pd.read_csv(file_path_2)
data_3 = pd.read_csv(file_path_3)
data_4 = pd.read_csv(file_path_4)
data_5 = pd.read_csv(file_path_5)

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
data_4[['p1_performance', 'p2_performance', 'performance_diff']] = data_4.apply(calculate_performance, axis=1)
data_5[['p1_performance', 'p2_performance', 'performance_diff']] = data_5.apply(calculate_performance, axis=1)

# 将'performance_diff'累加
data_1['performance_diff'] = data_1['performance_diff'].cumsum()
data_2['performance_diff'] = data_2['performance_diff'].cumsum()
data_3['performance_diff'] = data_3['performance_diff'].cumsum()
data_4['performance_diff'] = data_4['performance_diff'].cumsum()
data_5['performance_diff'] = data_5['performance_diff'].cumsum()

# 将'performance_diff'输出到新建的csv文件中
data_1.to_csv('Alcaraz_vs_Djokovic_set1_new.csv', index=False)
data_2.to_csv('Alcaraz_vs_Djokovic_set2_new.csv', index=False)
data_3.to_csv('Alcaraz_vs_Djokovic_set3_new.csv', index=False)
data_4.to_csv('Alcaraz_vs_Djokovic_set4_new.csv', index=False)
data_5.to_csv('Alcaraz_vs_Djokovic_set5_new.csv', index=False)

# 设置绘图大小
plt.figure(figsize=(14, 6))

# 绘制 performance_diff 随 point_no 的变化,一张图里面5条曲线
plt.plot(data_1['point_no'], data_1['performance_diff'], label='Set 1', linewidth=2, marker='o', color = '#EAAA60', markersize=3)
plt.plot(data_2['point_no'], data_2['performance_diff'], label='Set 2', linewidth=2, marker='o', color = '#E68B81', markersize=3)
plt.plot(data_3['point_no'], data_3['performance_diff'], label='Set 3', linewidth=2, marker='o', color = '#B7B2D0', markersize=3)
plt.plot(data_4['point_no'], data_4['performance_diff'], label='Set 4', linewidth=2, marker='o', color = '#7DA6C6', markersize=3)
plt.plot(data_5['point_no'], data_5['performance_diff'], label='Set 5', linewidth=2, marker='o', color = '#84C3B7', markersize=3)

# 将y=0这一条线加粗使之更加明显
plt.axhline(y=0, color='black', linewidth=1.5)

# 设置图例
plt.legend(loc='upper left', fontsize=16)
plt.xlabel('Point Number', fontsize=20)
plt.ylabel('Performance Value Difference', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.grid(True)
plt.show()