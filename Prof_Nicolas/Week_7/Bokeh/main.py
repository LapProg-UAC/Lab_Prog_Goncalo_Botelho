from bokeh.plotting import figure, show
import pandas as pd 

df = pd.read_csv('co2_maunaloa.csv')

p = figure(title='CO2', x_axis_label='Ano', y_axis_label='PPM')

p.line(df['ano'], df['ppm'], line_width=2)
p.circle(df['ano'], df['ppm'], size=8)

show(p)