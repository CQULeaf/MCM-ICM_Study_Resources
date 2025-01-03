import pandas as pd
import numpy as np

# 读取数据
# data = pd.read_csv('Wimbledon_featured_matches_critic.csv')
data = pd.read_excel('2023-wimbledon-women.xlsx')

columns_1 = ['p1_ace', 'p1_double_fault', 'p1_unf_err', 'p1_net_pt_won', 'p1_break_pt_won', 'p1_break_pt_missed']
columns_2 = ['p2_ace', 'p2_double_fault', 'p2_unf_err', 'p2_net_pt_won', 'p2_break_pt_won', 'p2_break_pt_missed']

# 修改的函数，计算列之间的差值并形成新的对应列
def calculate_difference_and_add(data, columns_1, columns_2):
    diff_columns = []
    for col1, col2 in zip(columns_1, columns_2):
        if 'break_pt_won' in col1 or 'break_pt_missed' in col1:
            # 对于破发点赢和失，分别处理
            base_name = col1.split('_')[1] + '_' + col1.split('_')[3]  # 区分break_pt_won和break_pt_missed
        else:
            base_name = col1.split('_')[1]  # 对于其他情况，使用原逻辑
        new_col_name = base_name + '_diff'  # 构造新列名
        data[new_col_name] = data[col1] - data[col2]
        diff_columns.append(new_col_name)
    return data, diff_columns

# 使用修改后的函数处理数据，形成新列并添加到原数据中
data, diff_columns = calculate_difference_and_add(data, columns_1, columns_2)

# 定义一个新的函数来计算每个set内的diff累积和，并在新的一盘开始时重置
def calculate_cumsum_and_reset_at_new_set(df, diff_columns):
    for col in diff_columns:
        cumsum_col_name = col + '_cumsum'  # 构造累积和列名
        df[cumsum_col_name] = df[col].cumsum()
        # 设置重置逻辑
        df[cumsum_col_name] = df.groupby(['match_id', 'set_no'])[cumsum_col_name].transform(lambda x: x - x.iloc[0] + df[col].iloc[0])
    return df

# 按 match_id 和 set_no 分组，然后应用新的函数
data = data.groupby(['match_id', 'set_no'], as_index=False).apply(calculate_cumsum_and_reset_at_new_set, diff_columns)

# 保存结果
data.to_csv('2023-wimbledon-women_input_process.csv', index=False)