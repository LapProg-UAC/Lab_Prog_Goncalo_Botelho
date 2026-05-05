import plotly.express as px
import pandas as pd

df = pd.read_csv('pinguins_palmer.csv')

# O argumento 'color' agrupa os dados e cria a legenda automaticamente
fig = px.scatter(
    df, 
    x="massa", 
    y="barbatana", 
    color="especie",
    title="Scatterplot Colorido Automático",
    
)

fig.show()