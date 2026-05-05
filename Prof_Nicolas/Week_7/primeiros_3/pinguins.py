import pandas as pd
import matplotlib.pyplot as plt 

df = pd.read_csv('pinguins_palmer.csv')

especies = df['especies'].unique()
cores = [
    (200/255, 0/255, 50/255),
    (10/255, 20/255, 100/255),
    (150/255, 200/255, 0/255)
]

plt.figure(figsize=(10, 6))

for i, especie in enumerate(especies):
    subset = df[df['especie'] == especie]
    