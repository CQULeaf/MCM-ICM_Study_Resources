import pandas as pd

# 加载上传的数据集
data_path = 'Wimbledon_featured_matches_both_process.csv'
data = pd.read_csv(data_path)

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 定义特征和目标
features = ['ace_diff_cumsum', 'double_diff_cumsum', 'unf_diff_cumsum', 'net_diff_cumsum', 
            'break_won_diff_cumsum', 'break_missed_diff_cumsum']
target = 'swing'

# 处理缺失值
data.dropna(subset=[target], inplace=True)

# 分离特征和目标
X = data[features]
y = data[target]

# 分割数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 缺失值填充
imputer = SimpleImputer(strategy='mean')
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)

# 网格搜索参数优化
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30]
}
grid_search = GridSearchCV(estimator=RandomForestRegressor(random_state=42), param_grid=param_grid, cv=5, scoring='neg_mean_squared_error', verbose=2, n_jobs=-1)
grid_search.fit(X_train_imputed, y_train)

# 可视化网格搜索结果
results = pd.DataFrame(grid_search.cv_results_)

# 创建透视表
pivot_table = results.pivot(index='param_n_estimators', columns='param_max_depth', values='mean_test_score')
pivot_table = -pivot_table  # 转换为正MSE

# 绘制热图
plt.figure(figsize=(10, 6))
sns.heatmap(pivot_table, annot=True, fmt=".3f", cmap="YlGnBu")
plt.title('Grid Search Scores')
plt.xlabel('Max Depth')
plt.ylabel('N Estimators')
plt.show()
