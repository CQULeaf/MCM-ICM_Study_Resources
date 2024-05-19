import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置全局字体为Palatino Linotype
mpl.rcParams['font.family'] = 'Palatino Linotype'

file_path = 'Wimbledon_featured_matches_momentum.csv'
data = pd.read_csv(file_path)

# 确保点号（point_no）和盘号（set_no）已经正确排序
data.sort_values(by=['match_id', 'set_no', 'point_no'], inplace=True)

# 选取Carlos Alcaraz和Novak Djokovic之间的比赛
selected_data = data[(data['player1'] == 'Carlos Alcaraz') & (data['player2'] == 'Novak Djokovic')]

# 设置绘图大小
plt.figure(figsize=(14, 6))

# 定义一个颜色列表，用于绘制不同的set
colors = ['#EAAA60', '#E68B81', '#B7B2D0', '#7DA6C6', '#84C3B7']

# 使用groupby按match_id和set_no分组
for (match_id, set_no), group in selected_data.groupby(['match_id', 'set_no']):
    # 根据set_no选择颜色，注意set_no可能从1开始，所以需要做一些调整来匹配颜色列表的索引
    color = colors[(set_no-1) % len(colors)]  # 使用取模操作确保索引不会超出颜色列表的范围
    # 绘制每一组的数据，使用选定的颜色
    plt.plot(group['point_no'], group['momentum_value_diff_cumsum'], label=f'Set {set_no}', linewidth=2, marker='o', color=color, markersize=4)

# 将y=0这一条线加粗使之更加明显
plt.axhline(y=0, color='black', linewidth=1.5)

# 设置图例
plt.legend(loc='upper left', fontsize=16)
plt.xlabel('Point Number', fontsize=20)
plt.ylabel('Momentum Value Difference', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.grid(True)
plt.show()