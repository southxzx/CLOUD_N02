import pandas as pd
from scipy import stats
df = pd.read_csv('users9.csv',header=0)
df['Humid'].fillna(df['Humid'].mean(), inplace=True)
df['Time'].fillna(df['Time'].mean(), inplace=True)
df.plot.scatter(x='Humid',y='Time',c='Red')
size_train=int(len(df)*0.8)
df_train=df[:size_train]
df_test=df[size_train:]
print(df_train)
print(df_test)

stats.linregress(df_train['Humid'],df_train['Time'])