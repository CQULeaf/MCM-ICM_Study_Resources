# 重新导入必要的库和重新定义变量，因为代码执行状态被重置
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, confusion_matrix, roc_curve
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
import matplotlib as mpl

# 设置全局字体为Palatino Linotype
mpl.rcParams['font.family'] = 'Palatino Linotype'

# 重新加载数据
file_path = '2023-wimbledon-both-process.csv'
data = pd.read_csv(file_path)

# 定义特征和目标变量
features_columns = ['ace_diff_cumsum', 'double_diff_cumsum', 'unf_diff_cumsum', 'net_diff_cumsum', 
                    'break_won_diff_cumsum', 'break_missed_diff_cumsum']

# 筛选出测试集和重新定义的训练集
test_match_ids = ['2023-wimbledon-2503', '2023-wimbledon-2701']
selected_train_match_ids = ['2023-wimbledon-2504',  '2023-wimbledon-2602', '2023-wimbledon-2601'
                            ]
test_set = data[data['match_id'].isin(test_match_ids)]
new_train_set = data[data['match_id'].isin(selected_train_match_ids)]

# 准备数据
X_train = new_train_set[features_columns]
y_train = new_train_set['swing']
X_test = test_set[features_columns]
y_test = test_set['swing']

# 处理目标变量的缺失值
imputer = SimpleImputer(strategy='most_frequent')
y_train_imputed = imputer.fit_transform(y_train.values.reshape(-1, 1)).ravel()
y_test_imputed = imputer.transform(y_test.values.reshape(-1, 1)).ravel()

# 重新训练随机森林模型
rf_classifier_new = RandomForestClassifier(random_state=42, n_estimators=100, max_depth=10, min_samples_split=2, min_samples_leaf=1)
rf_classifier_new.fit(X_train, y_train_imputed)

# 计算AUC值
auc_score = roc_auc_score(y_test_imputed, rf_classifier_new.predict_proba(X_test)[:, 1])

# 生成ROC曲线数据
fpr, tpr, thresholds = roc_curve(y_test_imputed, rf_classifier_new.predict_proba(X_test)[:, 1])

# 绘制ROC曲线
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'ROC curve (area = {auc_score:.2f})')
plt.plot([0, 1], [0, 1], 'k--')  # 随机概率线
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate', fontsize=20)
plt.ylabel('True Positive Rate', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend(loc="lower right", fontsize=16)
plt.show()

# 生成混淆矩阵
conf_matrix = confusion_matrix(y_test_imputed, rf_classifier_new.predict(X_test))

print(conf_matrix, auc_score)
