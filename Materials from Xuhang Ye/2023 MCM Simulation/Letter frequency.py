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

# data = data[::-1]

# 检查Word列的Letter Frequence并输出
# Letter to Scrabble score mapping
scrabble_scores = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1,
    'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8,
    'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1,
    'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1,
    'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
} # scrabble_scores越大，字母越少

# Function to calculate Scrabble score of a word
def calculate_scrabble_score(word):
    return sum(scrabble_scores[letter] for letter in word.lower())

# Apply the function to the 'Word' column
data['Scrabble Score'] = data['Word'].apply(calculate_scrabble_score)


# 对于这七列，我希望从Percent in 1 try - 6 tries 这七列分别加权系数为1-6，然后加权求和
Weight = [1, 2, 3, 4, 5, 6]
data['Score'] = (data['Percent in 1 try'] * Weight[0] + data['2 tries'] * Weight[1] + data['3 tries'] * Weight[2] + data['4 tries'] * Weight[3] + data['5 tries'] * Weight[4] + data['6 tries'] * Weight[5]) / 100

# 研究加权后的相应权重百分比数据与Word列的情感分数的关系,将x,y轴变长
plt.figure(figsize = (10, 6))
plt.xlabel('Scrabble scores', fontsize = 18)
plt.ylabel('Score', fontsize = 18)
plt.xticks(range(0, 26),fontsize=14)
plt.yticks(fontsize=14)
plt.xlim(0, 25)  # 设置x轴范围
plt.ylim(1, 6)   # 设置y轴范围
plt.scatter(data['Scrabble Score'], data['Score'], color='lightseagreen', alpha=0.5)
plt.show()