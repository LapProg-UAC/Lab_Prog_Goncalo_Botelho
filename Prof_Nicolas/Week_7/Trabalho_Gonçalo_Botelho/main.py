import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_pinguins = pd.read_csv('pinguins_palmer.csv')
df_co2 = pd.read_csv('co2_maunaloa.csv')

#Cálculo das barbatanas (180mm em 2010 + 14mm/ano)
df_co2['barbatana_est'] = 180 + (df_co2['ano'] - 2010) * 14

#Relação onde o ganho de massa segue a tendência do CO2 + ruído
np.random.seed(42)
df_co2['ganho_massa'] = (df_co2['ppm'] * 0.45) + np.random.normal(0, 4, len(df_co2))
correlacao = df_co2['ganho_massa'].corr(df_co2['ppm'])

#Estrutura do painel
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6))
fig.patch.set_facecolor('#ffffff')

#Gráfico gerado pelo código com Plotly
especies = df_pinguins['especie'].unique()
cores = ['#636EFA', '#EF553B', '#00CC96']

for i, esp in enumerate(especies):
    sub = df_pinguins[df_pinguins['especie'] == esp]
    ax1.scatter(sub['massa'], sub['barbatana'], label=esp, color=cores[i], s=100, edgecolors='white', alpha=0.8)

ax1.set_title('a) Massa vs Barbatana (Estilo Plotly)', fontsize=13, pad=15)
ax1.set_xlabel('Massa Corporal (g)')
ax1.set_ylabel('Comprimento Barbatana (mm)')
ax1.legend(title="Espécie")
ax1.grid(True, linestyle='--', alpha=0.3)

#Gráfico gerado pelo código com Bokeh
ax2.plot(df_co2['ano'], df_co2['ppm'], linewidth=2, zorder=1)
ax2.scatter(df_co2['ano'], df_co2['ppm'], color='#1F1F7A', s=64, edgecolors='black', zorder=2)

ax2.set_title('b) CO2 Mauna Loa (Estilo Bokeh)', fontsize=13, pad=15)
ax2.set_xlabel('Ano')
ax2.set_ylabel('PPM')
ax2.grid(True, alpha=0.2)

#Gráfico com correlação e estimativa
ax3.scatter(df_co2['ppm'], df_co2['ganho_massa'], color='#228B22', s=120, label='Dados Est.')

m, b = np.polyfit(df_co2['ppm'], df_co2['ganho_massa'], 1)
ax3.plot(df_co2['ppm'], m*df_co2['ppm'] + b, color='red', linestyle='--', alpha=0.5)

ax3.set_title(f'c) Correlação: {correlacao:.2f}', fontsize=13, pad=15)
ax3.set_xlabel('Nível de CO2 (ppm)')
ax3.set_ylabel('Ganho de Massa (g/ano)')

ultimo_ano = df_co2['ano'].max()
ultima_barb = df_co2['barbatana_est'].max()

plt.tight_layout()
plt.savefig('painel_pinguins_co2.jpg', format='jpg', dpi=200)