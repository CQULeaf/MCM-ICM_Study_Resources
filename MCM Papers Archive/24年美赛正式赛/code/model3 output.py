import pandas as pd
import numpy as np

data = pd.read_csv('2023-wimbledon-women_both_process1.csv')

# Correctly set the first row of 'swing' to NaN to avoid the warning
data.loc[0, 'swing'] = None

# Create the 'swing' column based on the comparison of adjacent 'game_victor' values
data['swing'] = (data['game_victor'].diff() != 0).astype(int)
data['swing'].iloc[0] = None  # Set the first row of 'swing' to None (NaN)

# Save the result to a new CSV file
data.to_csv('2023-wimbledon-both-process.csv', index=False)