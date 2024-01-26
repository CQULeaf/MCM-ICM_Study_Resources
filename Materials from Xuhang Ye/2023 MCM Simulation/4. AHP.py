import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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

# 选取相关列
columns_of_interest = ['Percent in 1 try', '2 tries', '3 tries', '4 tries', '5 tries', '6 tries', '7 or more tries (X)']
relevant_data = data[columns_of_interest]

# 归一化相关数据
normalized_data = (relevant_data - relevant_data.min()) / (relevant_data.max() - relevant_data.min())


judgment_matrix = np.array([
    [1, 3, 5, 7, 7, 3, 1],
    [1/3, 1, 3, 5, 5, 1, 1/3],
    [1/5, 1/3, 1, 3, 3, 1/3, 1/5],
    [1/7, 1/5, 1/3, 1, 1, 1/5, 1/7],
    [1/7, 1/5, 1/3, 1, 1, 1/5, 1/7],
    [1/3, 1, 3, 5, 5, 1, 1/3],
    [1, 3, 5, 7, 7, 3, 1]
])

# 将判断矩阵归一化（每个元素除以所在列的和）
judgment_matrix = judgment_matrix / judgment_matrix.sum(axis = 0)

# 将归一化的各列相加（即为按行求和）
judgment_matrix = judgment_matrix.sum(axis = 1)

# 将列向量归一化
judgment_matrix = judgment_matrix / judgment_matrix.sum()

# # 求判断矩阵的最大特征值
# max_eigenvalue = np.max(np.linalg.eig(judgment_matrix)[0])
# print(max_eigenvalue)

# # 计算一致性指标
# consistency_index = (max_eigenvalue - judgment_matrix.shape[0]) / (judgment_matrix.shape[0] - 1)
# print(consistency_index)


# 归一化后的列向量，取前四个为负值，后三个为正值，返回一个列表
judgment_matrix = np.append(-judgment_matrix[0 : 4], judgment_matrix[4 : ])
print(judgment_matrix)

# 计算加权得分
weighted_scores = normalized_data.dot(judgment_matrix) # 矩阵乘法
data['Score'] = weighted_scores  # 将得分添加到原始数据中

# 对数据按照得分进行排序
sorted_data = data.sort_values(by='Score', ascending=False)

# # # 打印前20和后20的单词及其得分
# # print("Top 20 Words and Scores:")
# # print(sorted_data[['Word', 'Score']].head(20))

# # print("\nBottom 20 Words and Scores:")
# # print(sorted_data[['Word', 'Score']].tail(20))

# 然后，选择包含 'Word' 列的部分创建一个新的 DataFrame

# 最后，将这个 DataFrame 保存为 Excel 文件
output_file_path = 'Words_Sorted_By_Score1.xlsx'
sorted_data['Score'].to_excel(output_file_path, index=False)

print(f"Words sorted by score have been saved to '{output_file_path}'.")