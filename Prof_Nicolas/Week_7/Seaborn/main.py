import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd

df = pd.read_csv('mpg_epa.csv')

plt.figure(figsize=(10, 6))

sns.histplot(df['mpg'], kde=True, color='skyblue', edgecolor='black')
plt.title('Distribuição de MPG')
plt.savefig('mpg_epa_seaborn.png')
plt.show()