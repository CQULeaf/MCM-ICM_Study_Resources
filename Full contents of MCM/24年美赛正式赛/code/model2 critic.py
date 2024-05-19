import pandas as pd
import numpy as np

def calculate_momentum_value(data):
    # 归一化数据
    normalized_data = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))
    
    # 进行正向化处理（1-归一化值），其他列保持不变
    normalized_data.iloc[:, [1, 2, 5]] = 1 - normalized_data.iloc[:, [1, 2, 5]]
    
    # 计算方差
    variance = normalized_data.var(axis=0)
    
    # 计算标准间的冲突
    conflict = np.zeros((normalized_data.shape[1], normalized_data.shape[1]))
    for i in range(normalized_data.shape[1]):
        for j in range(normalized_data.shape[1]):
            if i != j:
                # 计算第i个和第j个标准之间的差异性
                conflict[i, j] = np.sum(np.abs(normalized_data.iloc[:, i] - normalized_data.iloc[:, j]))
    
    # 计算信息量
    information = 1 / (variance + np.max(conflict, axis=1) - np.sum(conflict, axis=1))
    
    # 计算权重
    weights = information / np.sum(information)
    
    # 计算最终得分
    normalized_data['Momentum Value'] = np.sum(normalized_data.multiply(weights, axis=1), axis=1)
    
    return normalized_data['Momentum Value'], weights

# 读取数据
data = pd.read_csv('Wimbledon_featured_matches_critic.csv')

columns_1 = ['p1_ace', 'p1_double_fault', 'p1_unf_err', 'p1_net_pt_won', 'p1_break_pt_won', 'p1_break_pt_missed']
columns_2 = ['p2_ace', 'p2_double_fault', 'p2_unf_err', 'p2_net_pt_won', 'p2_break_pt_won', 'p2_break_pt_missed']

# 使用函数处理数据
momentum_value_p1, weights_p1 = calculate_momentum_value(data[columns_1])
momentum_value_p2, weights_p2 = calculate_momentum_value(data[columns_2])

momentum_value_diff = momentum_value_p1 - momentum_value_p2

print(momentum_value_diff)

# 将momentum_value_diff添加到Wimbledon_featured_matches.csv中
data = pd.read_csv('Wimbledon_featured_matches.csv')
data['momentum_value_diff'] = momentum_value_diff

# 定义一个函数来计算每个set内的momentum_value_diff的累积和，并在新的一盘开始时重置
def calculate_cumsum_reset_at_new_set(df):
    df['momentum_value_diff_cumsum'] = df['momentum_value_diff'].cumsum()
    return df

# 定义一个函数来计算每个set内的momentum_value_diff的累积和，并在新的一盘开始时重置
def calculate_cumsum_reset_at_new_set(df):
    df['momentum_value_diff_cumsum'] = df['momentum_value_diff'].cumsum()
    return df

# 按 match_id 和 set_no 分组，然后应用 calculate_cumsum_reset_at_new_set 函数
data = data.groupby(['match_id', 'set_no'], as_index=False).apply(calculate_cumsum_reset_at_new_set)

# 为了确保在每个新的一盘开始时重置累积和，我们需要检测set_no的变化
# 这可以通过检查每个set的第一行，并将对应的momentum_value_diff_cumsum设置为momentum_value_diff的值来实现
data['reset_indicator'] = data.groupby(['match_id', 'set_no'])['momentum_value_diff'].transform('first')
data.loc[data.groupby(['match_id', 'set_no']).head(1).index, 'momentum_value_diff_cumsum'] = data['reset_indicator']

# 现在，我们可以去除临时添加的列（如果需要的话）
data.drop(columns=['reset_indicator'], inplace=True)

# 导出数据
data.to_csv('Wimbledon_featured_matches_momentum.csv', index=False)