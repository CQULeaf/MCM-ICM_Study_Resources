import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib as mpl
from datetime import datetime
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

# 将日期与Number of reported results列抽出，以便于后续的处理
data = data[['Date', 'Number of reported results']]
data = data.set_index('Date') # 将Date列设置为索引
# print(data.head())

# 由于日期是从后往前排列的，即最近的日期在前最远的日期在后，需要将其反转
data = data[::-1]
# print(data.head())

# 设置全局字体为Palatino Linotype
mpl.rcParams['font.family'] = 'Palatino Linotype'

# plt.figure(figsize = (10, 6)) 
# plt.xlabel('Date', fontsize = 18)  # 增大xlabel字体大小
# plt.ylabel('Number', fontsize = 18)  # 增大ylabel字体大小
# # 增大坐标轴上的数据字体大小
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)
# plt.plot(data)
# plt.show()

# 将前80%的数据作为训练集，后20%的数据作为测试集
train_size = int(len(data) * 0.8)
train = data[:train_size]
test = data[train_size:]
# future = data['Number of reported results'][train_size:].index + pd.DateOffset(months=3)

# # ADF检验
# adf_test = adfuller(train['Number of reported results'])
# print('ADF Statistic:', adf_test[0])
# print('p-value:', adf_test[1])
# print('Critical Values:')
# for key, value in adf_test[4].items():
#     print(f'   {key}: {value}')

# # 根据p-value判断平稳性
# if adf_test[1] < 0.05:
#     print("数据平稳")
# else:
#     print("数据不平稳，可能需要进一步的差分")

# 使用训练集的数据进行差分
diff_data = train.diff().dropna()  # 进行一次差分并去除缺失值

# # ADF检验
# adf_test = adfuller(diff_data)
# print('ADF Statistic:', adf_test[0])
# print('p-value:', adf_test[1])
# print('Critical Values:')
# for key, value in adf_test[4].items():
#     print(f'   {key}: {value}')

# # 根据p-value判断平稳性
# if adf_test[1] < 0.05:
#     print("数据平稳")
# else:
#     print("数据不平稳，可能需要进一步的差分")

# # 一阶差分后的时序图
# plt.figure(figsize = (10, 6))
# plt.xlabel('Date', fontsize = 18)
# plt.ylabel('Number', fontsize = 18)
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)
# plt.plot(diff_data)
# plt.show()

# # 残差分析,acf图和pacf图,标题字体放大
# from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# # 设置标题和坐标轴标签的字体大小
# title_fontsize = 16
# axis_label_fontsize = 14

# # 绘制自相关图（ACF）
# fig, ax = plt.subplots()
# plot_acf(results.resid, lags=40, ax=ax)
# ax.set_title('Autocorrelation', fontsize=title_fontsize)
# ax.tick_params(axis='both', labelsize=axis_label_fontsize)

# # 绘制偏自相关图（PACF）
# fig, ax = plt.subplots()
# plot_pacf(results.resid, lags=40, ax=ax)
# ax.set_title('Partial Autocorrelation', fontsize=title_fontsize)
# ax.tick_params(axis='both', labelsize=axis_label_fontsize)

# plt.show()

# BIC

# # 设置模型的参数范围
# p = range(0, 10)  # 比如0到5
# d = 1             # 已经确定差分两次
# q = range(0, 10)  # 比如0到5

# # 存储每个模型的AIC和BIC
# aic_values = []
# bic_values = []
# parameters = []

# # 遍历所有的参数组合
# for p_value in p:
#     for q_value in q:
#         try:
#             model = ARIMA(diff_data, order=(p_value, d, q_value))
#             model_fit = model.fit()
#             aic_values.append(model_fit.aic)
#             bic_values.append(model_fit.bic)
#             parameters.append((p_value, d, q_value))
#         except:
#             continue

# # 将结果转换为DataFrame
# results_df = pd.DataFrame({
#     'AIC': aic_values,
#     'BIC': bic_values,
#     'Parameters': parameters
# })

# # 找到最小的AIC和BIC
# min_aic_row = results_df[results_df['AIC'] == results_df['AIC'].min()]
# min_bic_row = results_df[results_df['BIC'] == results_df['BIC'].min()]

# print("Best ARIMA model (by AIC):")
# print(min_aic_row)
# print("\nBest ARIMA model (by BIC):")
# print(min_bic_row)

# # 绘制BIC矩阵

# p_range = range(0, 10)  # 请根据您的参数范围进行调整
# q_range = range(0, 10)  # 请根据您的参数范围进行调整
# bic_matrix = np.array(results_df['BIC']).reshape(len(p_range), len(q_range))

# plt.figure(figsize=(10, 6))
# plt.xlabel('q', fontsize=18)
# plt.ylabel('p', fontsize=18)
# plt.xticks(range(len(q_range)), q_range, fontsize=14)
# plt.yticks(range(len(p_range)), p_range, fontsize=14)

# # 使用更好的颜色映射
# cmap = plt.get_cmap('coolwarm')
# plt.imshow(bic_matrix, cmap=cmap, interpolation='none')

# # 添加颜色条
# plt.colorbar()

# for i in range(len(p_range)):
#     for j in range(len(q_range)):
#         # 检查是否是特殊数据点
#         if i == min_bic_row['Parameters'].values[0][0] and j == min_bic_row['Parameters'].values[0][2]:
#             text_color = 'black'  # 特殊数据标红
#         else:
#             text_color = 'white'  # 其他数据使用白色字体

#         plt.text(j, i, round(bic_matrix[i, j], 2), ha='center', va='center', color=text_color, fontsize=9)

# plt.show()

# 为时间序列添加日频率信息
data = data.asfreq('D')

# 再次分割数据集，分为训练集，测试集
train = data['Number of reported results'][:train_size]
test = data['Number of reported results'][train_size:]
# 计算额外预测天数之后的日期
from pandas.tseries.offsets import DateOffset
future_date = test.index[-1] + DateOffset(days=75)

# 拟合ARIMA模型
model = ARIMA(train, order=(2, 1, 6))
results = model.fit()

# 预测
pred = results.predict(start=test.index[0], end=future_date, typ='levels')

# 绘图
plt.figure(figsize = (10, 6))
plt.xlabel('Date', fontsize = 18)
plt.ylabel('Number', fontsize = 18)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.plot(train, label='Training', color='green')
plt.plot(test, label='Test', color='blue')
plt.plot(pred, label='Prediction', color='red')
plt.legend(fontsize=14)
plt.show()