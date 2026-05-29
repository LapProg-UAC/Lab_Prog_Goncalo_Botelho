import os
import yaml
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Get current directory (MainCode)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the YAML configuration file
yaml_path = os.path.join(CURRENT_DIR, 'config.yaml')
with open(yaml_path, 'r') as file:
    config = yaml.safe_load(file)

BASE_DIR = os.path.dirname(CURRENT_DIR)
OUTPUT_DIR = os.path.join(BASE_DIR, "OutputFiles")


def generate_3d_face_gif(emotion, output_dir, anim_params):
    '''
    Generates a 3D animated GIF of a face displaying a specific emotion.
    
    Parameters:
    - emotion (str): The target emotion ('happy', 'sad', 'surprise', 'fear', 'disgust', 'neutral').
    - output_dir (str): The folder path where the GIF will be saved.
    - anim_params (dict): Dictionary containing animation settings (fps, interval, face_color, etc.).
    '''
    
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.axis('off')
    
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_zlim(-1.2, 1.2)
    
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x_head = np.outer(np.cos(u), np.sin(v))
    y_head = np.outer(np.sin(u), np.sin(v))
    z_head = np.outer(np.ones(np.size(u)), np.cos(v))
    
    face_color = anim_params.get('face_color', '#FFD700')
    ax.plot_surface(x_head, y_head, z_head, color=face_color, 
                    linewidth=0, antialiased=False, zorder=1)

    eye_size = 500
    x_eyes_base = np.array([-0.35, 0.35])
    z_eyes_base = np.array([0.3, 0.3])
    x_mouth_base = np.linspace(-0.35, 0.35, 100)
    
    if emotion == "happy":
        z_mouth_base = 1.5 * (x_mouth_base**2) - 0.4
        
    elif emotion == "sad":
        z_mouth_base = -1.5 * (x_mouth_base**2) - 0.15
        
    elif emotion == "surprise":
        eye_size = 1000
        t = np.linspace(0, 2 * np.pi, 100)
        x_mouth_base = 0.15 * np.cos(t)
        z_mouth_base = 0.15 * np.sin(t) - 0.3

    elif emotion == "fear":
        eye_size = 900
        x_mouth_base = np.linspace(-0.4, 0.4, 100) 
        z_mouth_base = -2.5 * (x_mouth_base**2) - 0.05
        
    elif emotion == "disgust":
        eye_size = 150 
        z_mouth_base = 0.05 * np.sin(15 * x_mouth_base) + (0.4 * x_mouth_base) - 0.3

    else: 
        z_mouth_base = np.full_like(x_mouth_base, -0.3)

    y_eyes_base = -np.sqrt(1.0 - x_eyes_base**2 - z_eyes_base**2)
    
    ax.scatter(x_eyes_base * 1.02, y_eyes_base * 1.02, z_eyes_base * 1.02, 
               color='black', s=eye_size, depthshade=False, zorder=10)

    y_mouth_base = -np.sqrt(1.0 - x_mouth_base**2 - z_mouth_base**2)
    
    x_mouth = x_mouth_base * 1.02
    y_mouth = y_mouth_base * 1.02
    z_mouth = z_mouth_base * 1.02
    
    ax.plot(x_mouth, y_mouth, z_mouth, color='black', linewidth=6, zorder=10)

    ax.set_box_aspect([1, 1, 1])

    filename = f"face_{emotion}_3d.gif"
    filepath = os.path.join(output_dir, filename)
    print(f"Generating GIF: '{filename}'... (please wait)")

    def update(frame):
        ax.view_init(elev=10, azim=frame)
        return fig,

    step = anim_params.get('rotation_step', 4)
    frames = np.arange(-90, 270, step) 
    
    interval = anim_params.get('interval', 50)
    animation = FuncAnimation(fig, update, frames=frames, interval=interval)
    
    fps = anim_params.get('fps', 20)
    animation.save(filepath, writer='pillow', fps=fps)
    
    plt.close(fig) 
    print(f"Success! Saved at: {filepath}\n")


def main():
    '''
    Main execution pipeline.
    Reads configuration, extracts target emotions, and generates GIFs sequentially.
    '''

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    anim_params = config['animation_parameters']
    emotions_list = config['emotions_to_generate']
    
    print(f"Starting generation for {len(emotions_list)} emotions...\n")
    
    for emotion in emotions_list:
        generate_3d_face_gif(emotion, OUTPUT_DIR, anim_params)
        
    print("All animations generated successfully!")

if __name__ == "__main__":
    main()