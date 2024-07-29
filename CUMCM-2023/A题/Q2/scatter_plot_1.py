import pandas as pd 
import matplotlib.pyplot as plt

df = pd.read_csv(r'C:\Users\Administrator\Desktop\2023国赛\A题\Q1\mirror_loc.csv')
df.columns=['x','y']
plt.scatter(df['x'],df['y'])
plt.show()