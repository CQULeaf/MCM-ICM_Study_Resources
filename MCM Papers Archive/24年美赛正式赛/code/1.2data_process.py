import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置全局字体为Palatino Linotype
mpl.rcParams['font.family'] = 'Palatino Linotype'

file_path = 'Wimbledon_featured_matches.csv'
data = pd.read_csv(file_path)

# 为避免除以0的情况，先处理rally_count为0的情况
data.loc[data['rally_count'] == 0, 'rally_count'] = np.nan

# 计算每个回合的平均运动距离
data['p1_avg_distance_per_rally'] = data['p1_distance_run'] / data['rally_count']
data['p2_avg_distance_per_rally'] = data['p2_distance_run'] / data['rally_count']

# 基本统计分析来查看分布，以便确定阈值
avg_distance_per_rally_stats = data[['p1_avg_distance_per_rally', 'p2_avg_distance_per_rally']].describe()

# 计算阈值：平均值加上2倍标准差
threshold_p1 = avg_distance_per_rally_stats.loc['mean', 'p1_avg_distance_per_rally'] + 3 * avg_distance_per_rally_stats.loc['std', 'p1_avg_distance_per_rally']
threshold_p2 = avg_distance_per_rally_stats.loc['mean', 'p2_avg_distance_per_rally'] + 3 * avg_distance_per_rally_stats.loc['std', 'p2_avg_distance_per_rally']

# 识别异常值
abnormal_p1 = data[data['p1_avg_distance_per_rally'] > threshold_p1]
abnormal_p2 = data[data['p2_avg_distance_per_rally'] > threshold_p2]

# 异常值数量
abnormal_count_p1 = len(abnormal_p1)
abnormal_count_p2 = len(abnormal_p2)

# 输出异常值数量
print(abnormal_count_p1)
print(abnormal_count_p2)

import matplotlib.pyplot as plt

# 假定data是你的数据集变量名，threshold_p1和threshold_p2是之前计算的上限阈值
# 调整后的绘图代码
plt.figure(figsize=(14, 7))

# 定义颜色
color1 = '#316357'  
color2 = '#af9476'  
color3 = '#3C5840'  

# 使用条件列表推导式为点着色，同时绘制所有点
plt.scatter(data.index, data['p1_avg_distance_per_rally'], c=[color1 if x > threshold_p1 else color2 for x in data['p1_avg_distance_per_rally']], alpha=[1 if x > threshold_p1 else 0.3 for x in data['p1_avg_distance_per_rally']], s=10)

# 绘制用于图例的不可见点
plt.scatter([], [], color=color1, alpha=0.3, s=10, label='Player 1: Abnormal Avg Distance')
plt.scatter([], [], color=color2, alpha=0.3, s=10, label='Player 1: Normal Avg Distance')

# 绘制阈值线
plt.axhline(y=threshold_p1, color=color3, linestyle='--', label=f'Threshold: {threshold_p1:.2f} meters')

# 标题和标签
plt.xlabel('Point Index', fontsize=20)
plt.ylabel('Avg Distance (meters)', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=16, loc='upper right')

# 显示图表
plt.tight_layout()
plt.show()

# # 定义颜色
# color1 = '#11659A'  
# color2 = '#F8DF70'  
# color3 = '#3C5840'  

# # 使用条件列表推导式为点着色，同时绘制所有点
# plt.scatter(data.index, data['p2_avg_distance_per_rally'], c=[color1 if x > threshold_p2 else color2 for x in data['p2_avg_distance_per_rally']],alpha=[1 if x > threshold_p2 else 0.3 for x in data['p2_avg_distance_per_rally']], s=10)

# # 绘制用于图例的不可见点
# plt.scatter([], [], color=color1, alpha=0.3, s=10, label='Player 2: Abnormal Avg Distance')
# plt.scatter([], [], color=color2, alpha=0.3, s=10, label='Player 2: Normal Avg Distance')

# # 绘制阈值线
# plt.axhline(y=threshold_p1, color=color3, linestyle='--', label=f'Threshold: {threshold_p2:.2f} meters')

# # 标题和标签
# plt.xlabel('Point Index', fontsize=20)
# plt.ylabel('Avg Distance (meters)', fontsize=20)
# plt.xticks(fontsize=20)
# plt.yticks(fontsize=20)
# plt.legend(fontsize=16)

# # 显示图表
# plt.tight_layout()
# plt.show()