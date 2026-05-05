import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('mpg_epa.csv')

plt.figure(figsize=(10, 6))

plt.hist(df['mpg'], bins=6, color= '#1f77b4', edgecolor='black', alpha=0.5)

plt.title('MPG')
plt.xlabel('milhas')
plt.ylabel('frequência')

plt.grid(axis='y', linestyle='-', alpha=0.5)

plt.tight_layout()
plt.savefig('histograma.png')
plt.show()