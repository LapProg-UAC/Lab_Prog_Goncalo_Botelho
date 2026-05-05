import pandas as pd
import matplotlib.pyplot as plt

# 1. Carregar o ficheiro
df = pd.read_csv('co2_maunaloa.csv')

# 2. Criar o gráfico
# Definir o tamanho da figura
plt.figure(figsize=(10, 6))

# Criar a linha
plt.plot(df['ano'], df['ppm'], marker='o', color='darkblue', label='Concentração de CO2')

# Preencher a área por baixo da linha
plt.fill_between(df['ano'], df['ppm'], color='skyblue', alpha=0.4)

# 3. Personalizar o gráfico
plt.title('Evolução do CO2 no Observatório de Mauna Loa (NOAA)', fontsize=14)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('CO2 (ppm)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# 4. Mostrar e guardar o gráfico
plt.tight_layout()
plt.savefig('co2_evolution.png')
# plt.show() # Descomente para ver localmente