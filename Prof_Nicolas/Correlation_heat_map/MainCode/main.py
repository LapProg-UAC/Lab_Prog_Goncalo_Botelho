import os
import yaml
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

import plotly.graph_objects as go
from bokeh.plotting import figure, output_file, save

# Get current directory (MainCode)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the YAML configuration file
yaml_path = os.path.join(CURRENT_DIR, 'config.yaml')
with open(yaml_path, 'r') as file:
    config = yaml.safe_load(file)

# Go back one level to access the OutputFiles folder
BASE_DIR = os.path.dirname(CURRENT_DIR)
OUTPUT_DIR = os.path.join(BASE_DIR, "OutputFiles")

# Extract output filenames from config and build full paths
heatmap_name = config['output_files']['correlation_heatmap']
plotly_name = config['output_files']['plotly_plot']
bokeh_name = config['output_files']['bokeh_plot']

HEATMAP_PATH = os.path.join(OUTPUT_DIR, heatmap_name)
PLOTLY_PATH = os.path.join(OUTPUT_DIR, plotly_name)
BOKEH_PATH = os.path.join(OUTPUT_DIR, bokeh_name)

def main():
    '''
    Generates synthetic sine and cosine signals, calculates their correlation,
    and exports three different visualizations.

    The function performs the following steps:
    1. Reads simulation parameters (time array limits) from a 'config.yaml' file.
    2. Generates two mathematical signals: y1 = sin(t) and y2 = cos(t).
    3. Calculates and prints the correlation matrix between the two signals.
    4. Creates and saves three types of plots to the 'OutputFiles' directory:
       - A Seaborn correlation heatmap (saved as a JPG image).
       - An interactive Plotly line chart (saved as an HTML file).
       - An interactive Bokeh line chart (saved as an HTML file).
    '''

    t_start = config['signal_parameters']['start']
    t_end = config['signal_parameters']['end']
    t_points = config['signal_parameters']['num_points']

    t = np.linspace(t_start, t_end, t_points)
    y1 = np.sin(t)
    y2 = np.cos(t)

    df = pd.DataFrame({
        "y1": y1,
        "y2": y2
    })

    corr = df.corr()
    
    plt.figure()
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("Correlation Matrix")
    
    plt.savefig(HEATMAP_PATH, format='jpg', dpi=200)
    plt.close() 
    print(f"Heatmap saved at: {HEATMAP_PATH}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=y1, mode='lines', name='sin(t)'))
    fig.add_trace(go.Scatter(x=t, y=y2, mode='lines', name='cos(t)'))

    fig.update_layout(title="Signals (Plotly)",
                      xaxis_title="t",
                      yaxis_title="Amplitude")
    
    fig.write_html(PLOTLY_PATH)
    print(f"Plotly graph saved at: {PLOTLY_PATH}")

    output_file(BOKEH_PATH)
    
    p = figure(title="Signals (Bokeh)",
               x_axis_label='t',
               y_axis_label='Amplitude')

    p.line(t, y1, legend_label="sin(t)")
    p.line(t, y2, legend_label="cos(t)")
    
    save(p)
    print(f"Bokeh graph saved at: {BOKEH_PATH}\n")


if __name__ == "__main__":
    main()