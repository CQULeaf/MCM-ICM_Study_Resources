import pandas as pd
import numpy as np

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


# 1. 检查 Word 列是否包含五个字母的单词
words_not_five_letters = data[~data['Word'].str.match(r'^[A-Za-z]{5}$')]


# 2. 检查百分比列的总和是否为100
percentage_columns = ['Percent in 1 try', '2 tries', '3 tries', '4 tries', '5 tries', '6 tries', '7 or more tries (X)']
data['Total Percent'] = data[percentage_columns].sum(axis = 1)
rows_not_valid = data[(data['Total Percent'] < 98) | (data['Total Percent'] > 102)]

# 3. 检查单词是否符合规范
print('Words not five letters long:', words_not_five_letters['Word'].unique()) # unique() returns a numpy array
print(words_not_five_letters["Contest number"].unique())
print('Rows not valid', len(rows_not_valid))
print(rows_not_valid["Contest number"].unique())