import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import warnings

warnings.filterwarnings('ignore')

file_path = 'Problem_C_Data_Wordle.xlsx'
data = pd.read_excel(file_path, header = 1)  # Assuming the second row contains the column names

# Dropping the first unnamed column if it's entirely empty
if data.columns[0].startswith('Unnamed'):
    data = data.drop(data.columns[0], axis = 1)

# Renaming columns
data.columns = [
    'Date', 
    'Contest number', 
    'Word', 
    'Number of reported results', 
    'Number in hard mode', 
    'Percent in 1 try', 
    '2 tries', 
    '3 tries', 
    '4 tries', 
    '5 tries', 
    '6 tries', 
    '7 or more tries (X)'
]

data['Date'] = pd.to_datetime('1899-12-30') + pd.to_timedelta(data['Date'], unit='D')

# 困难模式选择人数占总人数的比例
plt.figure(figsize = (10, 6))
plt.title('Number in hard mode as a percentage of Number of reported results')
plt.xlabel('Date')
plt.ylabel('Percentage')
plt.plot(data['Date'], data['Number in hard mode'] / data['Number of reported results'])
plt.show()

# 每日参与人数
plt.figure(figsize = (10, 6))
plt.title('Number of reported results')
plt.xlabel('Date')
plt.ylabel('Number')
plt.plot(data['Date'], data['Number of reported results'], label = 'Number of reported results')
# plt.plot(data['Date'], data['Number in hard mode'], label = 'Number in hard mode')
# plt.legend()
plt.show()

# # 每日参与人数优化

max_reported_date = data.loc[data['Number of reported results'].idxmax(), 'Date']

# Plotting the graph with the new stabilization point and colored regions only below the curve
plt.figure(figsize=(12, 6))
plt.title('Number of Reported Results Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Reported Results')
plt.plot(data['Date'], data['Number of reported results'], label='Number of Reported Results')

# x坐标只显示起始日期，结束日期，以及两个峰值日期，同时将日期字体调小一点
plt.xticks([data['Date'].min(), max_reported_date, pd.Timestamp('2022-07-01'), data['Date'].max()], fontsize=6)

# Find the value of "Number of reported results" on max_reported_date
max_reported_value = data.loc[data['Date'] == max_reported_date, 'Number of reported results'].values[0]

# Find the value of "Number of reported results" on 2022-07-01
stabilization_value = data.loc[data['Date'] == pd.Timestamp('2022-07-01'), 'Number of reported results'].values[0]

# Adding vertical lines for max reported date and new stabilization point
plt.plot([max_reported_date, max_reported_date], [0, max_reported_value], color='red', linestyle='--', label='Max Reported Date') 
plt.plot([pd.Timestamp('2022-07-01'), pd.Timestamp('2022-07-01')], [0, stabilization_value], color='red', linestyle='--', label='Stabilization Point')

# Filling regions only below the curve
plt.fill_between(data['Date'], data['Number of reported results'], where=(data['Date'] <= max_reported_date), color='skyblue', alpha=0.3)
plt.fill_between(data['Date'], data['Number of reported results'], where=((data['Date'] > max_reported_date) & (data['Date'] <= pd.Timestamp('2022-07-01'))), color='lightgreen', alpha=0.3)
plt.fill_between(data['Date'], data['Number of reported results'], where=(data['Date'] >= pd.Timestamp('2022-07-01')), color='orange', alpha=0.3)

plt.legend()
plt.show()