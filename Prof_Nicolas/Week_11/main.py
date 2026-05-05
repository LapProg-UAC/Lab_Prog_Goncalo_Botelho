import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)
Z1 = np.sin(R)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Superfície com cor (objeto central)
ax.plot_surface(X, Y, Z1, cmap=cm.plasma, alpha=0.8, linewidth=5)

# Adicionar contornos na base (Z=0) - linhas de nível
ax.contour(X, Y, Z1, levels = 50, offset=0, cmap=cm.plasma, alpha=0.8, linewidths=1.5)

ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('3D Surface com Ondas (Círculos em Z=0)')
plt.savefig('3D_Surface_com_Ondas.jpg', format='jpg', dpi=300) 
plt.show()