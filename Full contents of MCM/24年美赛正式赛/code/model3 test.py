from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer

import pandas as pd

# 加载数据
file_path = 'Wimbledon_featured_matches_both_process.csv'
data = pd.read_csv(file_path)

# 筛选出特定 match_id 的行作为测试集
test_match_ids = ['2023-wimbledon-1301', '2023-wimbledon-1701', '2023-wimbledon-1308']
test_set = data[data['match_id'].isin(test_match_ids)]

# 使用剩余的数据作为训练集
train_set = data[~data['match_id'].isin(test_match_ids)]

# 验证分割结果
train_set_shape = train_set.shape
test_set_shape = test_set.shape


# 准备特征和目标变量
features_columns = ['ace_diff_cumsum', 'double_diff_cumsum', 'unf_diff_cumsum', 'net_diff_cumsum', 
                    'break_won_diff_cumsum', 'break_missed_diff_cumsum']
X_train = train_set[features_columns]
y_train = train_set['swing']
X_test = test_set[features_columns]
y_test = test_set['swing']

# 处理目标变量的缺失值
imputer = SimpleImputer(strategy='most_frequent')
y_train_imputed = imputer.fit_transform(y_train.values.reshape(-1, 1)).ravel()
y_test_imputed = imputer.transform(y_test.values.reshape(-1, 1)).ravel()

# 训练随机森林模型
rf_classifier = RandomForestClassifier(random_state=42)
rf_classifier.fit(X_train, y_train_imputed)

# 预测测试集结果
y_pred = rf_classifier.predict(X_test)

# 计算准确率
accuracy = accuracy_score(y_test_imputed, y_pred)

accuracy
