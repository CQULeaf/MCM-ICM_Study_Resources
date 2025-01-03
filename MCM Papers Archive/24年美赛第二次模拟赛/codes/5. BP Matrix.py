import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib as mpl
from wordfreq import zipf_frequency
from afinn import Afinn
import warnings

warnings.filterwarnings('ignore')

file_path = 'Words_Sorted_By_Score.xlsx'
data = pd.read_excel(file_path)

scrabble_scores = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1,
    'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8,
    'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1,
    'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1,
    'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# Function to check if the word ends with 'ch', 'er', 'ly', or 'ge'
def check_suffix(word):
    return word.endswith(('ch', 'er', 'ly', 'ge'))

# Placeholder function for word analysis
def analyze_word(word):
    
    # 每个单词的sentiment_polarity
    afinn = Afinn()
    sentiment_polarity = afinn.score(word)
    # 每个单词重复字母的最大个数
    repeat_letters = max(word.count(char) for char in set(word))
    # 每个单词的letter_frequency
    letter_frequency = sum(scrabble_scores[letter] for letter in word)
    # Check if the word ends with specific suffixes
    suffix = 1 if check_suffix(word) else 0
    return sentiment_polarity, repeat_letters, letter_frequency, suffix

# Apply the function to each word
metrics = data['Word'].apply(analyze_word)

# Convert the results to a DataFrame
metrics_df = pd.DataFrame(metrics.tolist(), columns=['sentiment_polarity', 'repeat_letters', 'letter_frequency', 'suffix'])

# Concatenate with the original DataFrame
final_df = pd.concat([data, metrics_df], axis=1)

# Determine the number of words in each category
total_words = len(final_df)
hard_limit = 180

# Categorize the words
final_df['Category'] = ['Hard' if i < hard_limit else 'Easy' for i in range(total_words)]

# 将四个属性的值归一化
final_df['sentiment_polarity'] = (final_df['sentiment_polarity'] - final_df['sentiment_polarity'].min()) / (final_df['sentiment_polarity'].max() - final_df['sentiment_polarity'].min())
final_df['repeat_letters'] = (final_df['repeat_letters'] - final_df['repeat_letters'].min()) / (final_df['repeat_letters'].max() - final_df['repeat_letters'].min())
final_df['letter_frequency'] = (final_df['letter_frequency'] - final_df['letter_frequency'].min()) / (final_df['letter_frequency'].max() - final_df['letter_frequency'].min())
final_df['suffix'] = (final_df['suffix'] - final_df['suffix'].min()) / (final_df['suffix'].max() - final_df['suffix'].min())

# 在final_df中加入一个新的单词
eerie = analyze_word('eerie')
eerie_df = pd.DataFrame([eerie], columns=['sentiment_polarity', 'repeat_letters', 'letter_frequency', 'suffix'])
eerie_df['Word'] = 'eerie'
final_df = pd.concat([final_df, eerie_df], axis=0, ignore_index=True)

# 给定一个新的单词的四个属性，求与之最相似的2个单词，使用欧氏距离
def find_similar_word(word, df):
    # 从df中取出四个属性的值
    sentiment_polarity = df['sentiment_polarity'].values
    repeat_letters = df['repeat_letters'].values
    letter_frequency = df['letter_frequency'].values
    suffix = df['suffix'].values
    # 计算欧氏距离
    dist = np.sqrt((sentiment_polarity - word[0]) ** 2 + (repeat_letters - word[1]) ** 2 + (letter_frequency - word[2]) ** 2 + (suffix - word[3]) ** 2)
    # 返回这两个单词以及其对应的dist
    return df['Word'][dist.argsort()[:3]], dist[dist.argsort()[:3]]

# 找出与eerie最相似的两个单词，除了eerie本身
similar_words, dist = find_similar_word(eerie, final_df[final_df['Word'] != 'eerie'])
print(similar_words)

