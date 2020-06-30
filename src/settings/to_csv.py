import pandas as pd


read_file = pd.read_table("settings/settings.txt", header = 0, sep = ' ')
read_file = read_file.T
read_file.to_csv('settings/settings.csv', index=None, header = None)