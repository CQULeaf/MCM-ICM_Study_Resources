# import pandas as pd
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt
# import matplotlib as mpl

# # 设置全局字体为Palatino Linotype
# mpl.rcParams['font.family'] = 'Palatino Linotype'

# data = pd.read_csv('Alcaraz_vs_Djokovic_combined1.csv')

# # Calculate Pearson correlation coefficient again
# correlation_coefficient = data['momentum_value_diff_cumsum'].corr(data['performance_diff'])

# # Plotting scatter plot with regression line for the two columns
# plt.figure(figsize=(10, 6))
# sns.regplot(x='momentum_value_diff_cumsum', y='performance_diff', data=data, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
# plt.xlabel('Momentum Value Difference', fontsize=18)
# plt.ylabel('Performance Value Difference', fontsize=18)
# plt.xticks(fontsize=18)
# plt.yticks(fontsize=18)

# # Correctly placing the Pearson correlation coefficient text after plotting
# plt.text(x=data['momentum_value_diff_cumsum'].quantile(0.1), y=data['performance_diff'].max() - 1, 
#          s=f'Pearson r: {correlation_coefficient:.3f}', 
#          fontsize=16, 
#          backgroundcolor='white')
# plt.show()

# import pandas as pd
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt
# import matplotlib as mpl

# # 设置全局字体为Palatino Linotype
# mpl.rcParams['font.family'] = 'Palatino Linotype'

# data = pd.read_csv('Alcaraz_vs_Djokovic_combined1.csv')

# # Calculate Pearson correlation coefficient
# correlation_coefficient = data['momentum_value_diff_cumsum'].corr(data['performance_diff'])

# # Plotting scatter plot manually
# plt.figure(figsize=(10, 6))
# plt.scatter(data['momentum_value_diff_cumsum'], data['performance_diff'], alpha=0.5, label='Data Points')
# plt.xlabel('Momentum Value Difference', fontsize=18)
# plt.ylabel('Performance Value Difference', fontsize=18)
# plt.xticks(fontsize=18)
# plt.yticks(fontsize=18)

# # Fit and plot regression line
# coef = np.polyfit(data['momentum_value_diff_cumsum'], data['performance_diff'], 1)
# poly1d_fn = np.poly1d(coef)
# plt.plot(data['momentum_value_diff_cumsum'], poly1d_fn(data['momentum_value_diff_cumsum']), color='red', label='Regression Line', fill_between=True)

# # Adding the Pearson correlation coefficient text
# plt.text(x=data['momentum_value_diff_cumsum'].quantile(0.1), y=data['performance_diff'].max() - 1, 
#          s=f'Pearson r: {correlation_coefficient:.3f}', 
#          fontsize=16, 
#          backgroundcolor='white')

# # Display the legend
# plt.legend(fontsize=16)
# plt.show()

# import pandas as pd
# import numpy as np

# data = pd.read_csv('Wimbledon_featured_matches_full_processed.csv')

# # 计算每场比赛的momentum_value_diff_cumsum与performance_diff之间的皮尔逊相关系数

# # 按match_id分组，对每组计算相关系数
# correlation_by_match = data.groupby('match_id').apply(lambda x: x['momentum_value_diff_cumsum'].corr(x['performance_diff_cumsum']))

# # 将结果转换为DataFrame
# correlation_df = correlation_by_match.reset_index()
# correlation_df.columns = ['Match ID', 'Pearson Correlation Coefficient']

# # # 查看汇总的相关系数
# # print(correlation_df.head(40))

# from scipy.stats import pearsonr

# # 定义一个函数来计算皮尔逊相关系数和p-value
# def calculate_pearson_and_pvalue(x):
#     correlation, p_value = pearsonr(x['momentum_value_diff_cumsum'], x['performance_diff_cumsum'])
#     return pd.Series({'Pearson Correlation Coefficient': correlation, 'p-value': p_value})

# # 按match_id分组，对每组应用函数
# results = data.groupby('match_id').apply(calculate_pearson_and_pvalue)

# # 查看前20场比赛的相关性结果和p-value
# print(results.head(40))

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy.stats as stats

mpl.rcParams['font.family'] = 'Palatino Linotype'

data = pd.read_csv('Alcaraz_vs_Djokovic_combined1.csv')

# Calculate Pearson correlation coefficient
correlation_coefficient = data['momentum_value_diff_cumsum'].corr(data['performance_diff'])

plt.figure(figsize=(10, 6))
plt.scatter(data['momentum_value_diff_cumsum'], data['performance_diff'], alpha=0.5, label='Data Points')
plt.xlabel('Momentum Value Difference', fontsize=18)
plt.ylabel('Performance Value Difference', fontsize=18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

# Fit and plot regression line
coef = np.polyfit(data['momentum_value_diff_cumsum'], data['performance_diff'], 1)
poly1d_fn = np.poly1d(coef)
# 预测值
y_pred = poly1d_fn(data['momentum_value_diff_cumsum'])

# 绘制回归线
plt.plot(data['momentum_value_diff_cumsum'], y_pred, color='red', label='Regression Line')

# 计算并绘制置信区间
# 计算预测值的标准误差
yerr = y_pred - data['performance_diff']
mean_x = np.mean(data['momentum_value_diff_cumsum'])
n = len(data)
t = stats.t.ppf(0.975, n-2)
s_err = np.sum(np.power(yerr, 2))
conf = t * np.sqrt((s_err/(n-2))*(1.0/n + (np.power((data['momentum_value_diff_cumsum']-mean_x),2)/((np.sum(np.power(data['momentum_value_diff_cumsum'],2)))-n*(np.power(mean_x,2))))))
lower = y_pred - conf
upper = y_pred + conf

plt.fill_between(data['momentum_value_diff_cumsum'], lower, upper, color='grey', label='Confidence Interval', alpha=0.3)

# 添加Pearson相关系数文本
plt.text(x=data['momentum_value_diff_cumsum'].quantile(0.1), y=data['performance_diff'].max() - 1, 
         s=f'Pearson r: {correlation_coefficient:.3f}', 
         fontsize=16, 
         backgroundcolor='white')

plt.legend(fontsize=14)
plt.show()

