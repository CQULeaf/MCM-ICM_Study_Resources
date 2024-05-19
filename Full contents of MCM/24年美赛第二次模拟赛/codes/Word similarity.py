import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib as mpl
import warnings

warnings.filterwarnings('ignore')

# 设置全局字体为Palatino Linotype
mpl.rcParams['font.family'] = 'Palatino Linotype'

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

data = data[::-1]

# 找出Word列中后缀为ch,er,ly的单词并将其值设为1，其余设为0
# Function to check if the word ends with 'ch', 'er', or 'ly'
def check_suffix(word):
    return word.endswith(('ch','ly','ll', 'ge'))

# Apply the function to the 'Word' column and store the result in a new column
data['Suffix_ch_er_ly'] = data['Word'].apply(lambda x: 1 if check_suffix(x) else 0)


# 对于这七列，我希望从Percent in 1 try - 6 tries 这七列分别加权系数为1-6，然后加权求和，再排名
Weight = [1, 2, 3, 4, 5, 6]
data['Score'] = (data['Percent in 1 try'] * Weight[0] + data['2 tries'] * Weight[1] + data['3 tries'] * Weight[2] + data['4 tries'] * Weight[3] + data['5 tries'] * Weight[4] + data['6 tries'] * Weight[5]) / 100

# 研究加权后的相应权重百分比数据与Word列的情感分数的关系
plt.figure(figsize = (10, 6))
plt.xlabel('Word similarity', fontsize = 18)
plt.ylabel('Score', fontsize = 18)
plt.xticks(range(0, 2), fontsize=14)
plt.yticks(fontsize=14)
plt.ylim(2, 5)   # 设置y轴范围
plt.scatter(data['Suffix_ch_er_ly'], data['Score'], color='lightseagreen', alpha=0.5)
plt.show()