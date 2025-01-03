import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import matplotlib as mpl

# 设置全局字体为Palatino Linotype
mpl.rcParams['font.family'] = 'Palatino Linotype'

# Reload the data
file_path = 'Wimbledon_featured_matches_both_process.csv'
data = pd.read_csv(file_path)

# Selecting features and target
features = ['ace_diff_cumsum', 'double_diff_cumsum', 'unf_diff_cumsum', 'net_diff_cumsum', 
            'break_won_diff_cumsum', 'break_missed_diff_cumsum']
target = 'swing'

# Preparing the data
data.dropna(subset=[target], inplace=True)  # Dropping rows where target is NaN
X = data[features]
y = data[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
imputer = SimpleImputer(strategy='mean')
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)

# Training the Random Forest model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_imputed, y_train)

# Get feature importances
feature_importances = model.feature_importances_

# Creating a DataFrame to hold the feature importances
importances_df = pd.DataFrame({'Feature': features, 'Importance': feature_importances})

# 新的指标名称，这里只更改前五个
new_feature_names = ['aceDiff', 'doubleDiff', 'unfDiff', 'netWonDiff', 'breakWonDiff', 'breakMissedDiff']

# 确保数据框有足够的指标来更改
if len(importances_df) >= len(new_feature_names):
    importances_df.loc[:len(new_feature_names)-1, 'Feature'] = new_feature_names

# 指定颜色，这里为前五个指标指定不同颜色
# colors = ['#6f94cd', '#aed0ee', '#5976ba', '#12264f', '#2e59a7', '#88abda']
colors = ['#aed0ee', '#88abda', '#6f94cd', '#5976ba', '#2e59a7', '#1e3b7a']


# Sorting the DataFrame by importance
importances_df = importances_df.sort_values(by='Importance', ascending=False)

# Plotting
plt.figure(figsize=(20, 8))
plt.barh(importances_df['Feature'], importances_df['Importance'], color=colors[::-1])
plt.xlabel('Importance', fontsize=24)
plt.ylabel('Features', fontsize=24)
plt.xticks(fontsize=24)
plt.yticks(fontsize=15)
plt.gca().invert_yaxis()  # To display the most important feature on top
plt.show()
