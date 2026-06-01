import os
import yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


caminho_yaml = os.path.join(CURRENT_DIR, 'config.yaml')
with open(caminho_yaml, 'r') as ficheiro:
    config = yaml.safe_load(ficheiro)

penguins_name = config['files']['penguins_input']
co2_name = config['files']['co2_input']
resolution = config['graphics']['resolution_dpi']
image_name = config['files']['image_output']

BASE_DIR = os.path.dirname(CURRENT_DIR)
INPUT_DIR = os.path.join(BASE_DIR, "InputFiles")
OUTPUT_DIR = os.path.join(BASE_DIR, "OutputFiles")
PENGUINS_FILE = os.path.join(INPUT_DIR, penguins_name)
CO2_FILE = os.path.join(INPUT_DIR, co2_name)
IMAGE_PATH = os.path.join(OUTPUT_DIR, image_name)

def main():
    '''
    Generates and saves a visualization panel with three charts analyzing penguin data and CO2 levels.

    The function executes the following main steps:
    1. Loads data from local CSV files.
    2. Performs estimation calculations (flipper size based on year) and generates synthetic 
       variables with noise (mass gain) to demonstrate correlations.
    3. Builds a figure with a 1x3 grid of subplots:
       - Chart a: Body Mass vs Flipper Length scatter plot by penguin species.
       - Chart b: Evolution of CO2 levels in Mauna Loa over the years.
       - Chart c: Scatter plot with a linear regression line showing the correlation 
         between CO2 level and estimated mass gain.
    4. Saves the final panel as a JPG image with 200 dpi resolution.

    Requirements:
    - The CSV files defined in data.env must exist in the 'InputFiles' directory.
    '''

    df_penguins = pd.read_csv(PENGUINS_FILE)
    df_co2 = pd.read_csv(CO2_FILE)

    df_co2['flipper_est'] = 180 + (df_co2['ano'] - 2010) * 14

    np.random.seed(42)
    df_co2['mass_gain'] = (df_co2['ppm'] * 0.45) + np.random.normal(0, 4, len(df_co2))
    correlation = df_co2['mass_gain'].corr(df_co2['ppm'])

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6))
    fig.patch.set_facecolor('#ffffff')

    species_list = df_penguins['especie'].unique()
    colors = ['#636EFA', '#EF553B', '#00CC96']

    for i, species in enumerate(species_list):
        sub = df_penguins[df_penguins['especie'] == species]
        ax1.scatter(sub['massa'], sub['barbatana'], label=species, color=colors[i], s=100, edgecolors='white', alpha=0.8)

    ax1.set_title('a) Mass vs Flipper Length (Plotly Style)', fontsize=13, pad=15)
    ax1.set_xlabel('Body Mass (g)')
    ax1.set_ylabel('Flipper Length (mm)')
    ax1.legend(title="Species")
    ax1.grid(True, linestyle='--', alpha=0.3)

    ax2.plot(df_co2['ano'], df_co2['ppm'], linewidth=2, zorder=1)
    ax2.scatter(df_co2['ano'], df_co2['ppm'], color='#1F1F7A', s=64, edgecolors='black', zorder=2)

    ax2.set_title('b) Mauna Loa CO2 (Bokeh Style)', fontsize=13, pad=15)
    ax2.set_xlabel('Year')
    ax2.set_ylabel('PPM')
    ax2.grid(True, alpha=0.2)

    ax3.scatter(df_co2['ppm'], df_co2['mass_gain'], color='#228B22', s=120, label='Est. Data')

    m, b = np.polyfit(df_co2['ppm'], df_co2['mass_gain'], 1)
    ax3.plot(df_co2['ppm'], m*df_co2['ppm'] + b, color='red', linestyle='--', alpha=0.5)

    ax3.set_title(f'c) Correlation: {correlation:.2f}', fontsize=13, pad=15)
    ax3.set_xlabel('CO2 Level (ppm)')
    ax3.set_ylabel('Mass Gain (g/year)')

    plt.tight_layout()
    plt.savefig(IMAGE_PATH, format='jpg', dpi = resolution)
    print(f"\nPanel saved at: {IMAGE_PATH}\n")

if __name__ == "__main__":
    main()