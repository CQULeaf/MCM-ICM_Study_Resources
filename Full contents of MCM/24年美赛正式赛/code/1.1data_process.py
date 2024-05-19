import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置全局字体为Palatino Linotype
mpl.rcParams['font.family'] = 'Palatino Linotype'

file_path = 'Wimbledon_featured_matches.csv'
data = pd.read_csv(file_path)

# 计算两名运动员运动距离的差异，并添加到新列
data['distance_difference'] = np.abs(data['p1_distance_run'] - data['p2_distance_run'])

# 计算差异的基本统计量
distance_diff_stats = data['distance_difference'].describe()

# 计算阈值：平均差异加上2倍标准差
threshold = distance_diff_stats['mean'] + 3 * distance_diff_stats['std']

# # 识别超过阈值的记录
# abnormal_index = data[data['distance_difference'] > threshold].index

# # 输出超过阙值最大的10个记录的match_id与distance_difference
# print(data.loc[abnormal_index, ['match_id', 'elapsed_time', 'distance_difference']].nlargest(10, 'distance_difference'))

# 创建散点图
plt.figure(figsize=(10, 6))

# 定义颜色
color1 = '#BC3823'  
color2 = '#5AA4AE'  
color3 = '#3C5840' 

# 使用条件列表推导式为点着色，同时绘制所有点
plt.scatter(data.index, data['distance_difference'], 
            c=[color1 if x > threshold else color2 for x in data['distance_difference']],
            alpha=[1 if x > threshold else 0.3 for x in data['distance_difference']],
            s=10)

# 绘制用于图例的不可见点
plt.scatter([], [], color=color1, s=10, label='Abnormal Distance Difference')
plt.scatter([], [], color=color2, alpha=0.3, s=10, label='Normal Distance Difference')

# 绘制阈值线
plt.axhline(y=threshold, color=color3, linestyle='--', label=f'Threshold: {threshold:.2f} meters')

# 标题和标签
plt.xlabel('Point Index', fontsize=20)
plt.ylabel('Distance Difference (meters)', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=16)

# 显示图表
plt.tight_layout()
plt.show()