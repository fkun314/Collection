import pandas as pd
import matplotlib.pyplot as plt

df_csv = pd.read_csv('Kitano_to_Takahata.csv')

'''
data format
RecordTimestamp, speed
1705646576	0
1705646586	0.1920298817
1705646591	1.927531478
1705646593	3.974967838
1705646595	6.854875588
...
'''

df_csv_2 = pd.read_csv("speed_and_position.csv")

df_csv.columns = ['RecordTimestamp', 'Speed']

base_time = df_csv['RecordTimestamp'].iloc[0]
df_csv['Elapsed Time'] = df_csv['RecordTimestamp'] - base_time

plt.figure(figsize=(10, 6))
plt.plot(df_csv['Elapsed Time'], df_csv['Speed']*3.6, marker='o')
plt.title('Kitano to Takahata[km/h]')
plt.xlabel('Elapsed Time (seconds)')
plt.ylabel('Speed[km/h]')
plt.grid(True)
# plt.show()

plt.savefig('Kitano_to_Takahata.png')