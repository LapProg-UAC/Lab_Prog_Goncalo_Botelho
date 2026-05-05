import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

def animate(frame):
    ax.clear()
    # Efeito de onda da gota
    Z1 = np.sin(R - frame * 0.3) * np.exp(-R * 0.2)
    ax.plot_surface(X, Y, Z1, cmap=cm.plasma, alpha=0.9)
    ax.set_zlim(-1, 1)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title(f'Gota caindo - Frame {frame}')

anim = FuncAnimation(fig, animate, frames=100, interval=50)
plt.show()