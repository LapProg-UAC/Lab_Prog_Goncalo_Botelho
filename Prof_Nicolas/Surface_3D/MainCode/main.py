import os
import yaml
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# Get current directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the YAML configuration file
yaml_path = os.path.join(CURRENT_DIR, 'config.yaml')
with open(yaml_path, 'r') as file:
    config = yaml.safe_load(file)

BASE_DIR = os.path.dirname(CURRENT_DIR)
OUTPUT_DIR = os.path.join(BASE_DIR, "OutputFiles")

multi_surface_name = config['output_files']['multi_surface']
surface_contour_name = config['output_files']['surface_contour']

MULTI_SURFACE_PATH = os.path.join(OUTPUT_DIR, multi_surface_name)
SURFACE_CONTOUR_PATH = os.path.join(OUTPUT_DIR, surface_contour_name)

def multi_surface_plot(X, Y, Z1, Z2, Z3):
    '''
    Generates a 3D surface plot with three overlapping surfaces.

    Parameters:
    - X, Y: 2D arrays representing the grid coordinates.
    - Z1, Z2, Z3: 2D arrays representing the Z values for each surface.

    The function creates a figure with three surfaces plotted using different colormaps and saves it as a JPG image.
    '''
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot_surface(X, Y, Z1, cmap=cm.autumn, alpha=0.6, linewidth=0, antialiased=True, shade=True)
    ax.plot_surface(X, Y, Z2, cmap=cm.winter, alpha=0.6, linewidth=0, antialiased=True, shade=True)
    ax.plot_surface(X, Y, Z3, cmap=cm.cool, alpha=0.6, linewidth=0, antialiased=True, shade=True)

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title('3D Surface Plot of Overlapping Waves')
    
    plt.savefig(MULTI_SURFACE_PATH, format='jpg', dpi=300) 
    plt.close(fig)
    print(f"Multi-surface plot saved at: {MULTI_SURFACE_PATH}")

def surface_with_contours(X, Y, Z): 
    '''
    Generates a 3D surface plot with contour lines at the base.

    Parameters:
    - X, Y: 2D arrays representing the grid coordinates.
    - Z: 2D array representing the Z values for the surface.

    The function creates a figure with a single surface and contour lines plotted at Z=0, then saves it as a JPG image.
    '''
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(X, Y, Z, cmap=cm.plasma, alpha=0.8, linewidth=5)
    
    ax.contour(X, Y, Z, levels=50, offset=0, cmap=cm.plasma, alpha=0.8, linewidths=1.5)

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title('3D Surface with Base Contour Waves (Z=0)')
    
    plt.savefig(SURFACE_CONTOUR_PATH, format='jpg', dpi=300) 
    plt.close(fig)
    print(f"Surface with contours saved at: {SURFACE_CONTOUR_PATH}\n")

def main():
    '''
    Generates and saves two 3D surface plots based on mathematical functions.

    The function performs the following steps:
    1. Reads grid parameters from a 'config.yaml' file.
    2. Calculates a 3D meshgrid and the corresponding Z values using sine and cosine functions.
    3. Generates Figure 1: Three overlapping 3D surfaces with different colormaps.
    4. Generates Figure 2: A single 3D surface with level contour lines plotted at Z=0.
    5. Saves both figures as high-resolution JPG images in the 'OutputFiles' directory.
    '''

    val_start = config['grid_parameters']['start']
    val_end = config['grid_parameters']['end']
    n_points = config['grid_parameters']['num_points']

    x = np.linspace(val_start, val_end, n_points)
    y = np.linspace(val_start, val_end, n_points)
    X, Y = np.meshgrid(x, y)
    
    R = np.sqrt(X**2 + Y**2)
    
    Z1 = np.sin(R)
    Z2 = np.cos(R)
    Z3 = np.sin(R + np.pi/4)

    multi_surface_plot(X, Y, Z1, Z2, Z3)
    surface_with_contours(X, Y, Z1)

if __name__ == "__main__":
    main()