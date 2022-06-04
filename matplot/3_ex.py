from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

a, b, c = 3, 2, 1

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

X = np.arange(-2, 2, 0.5)
Y = np.arange(-2, 2, 0.5)
X, Y = np.meshgrid(X, Y)

Z = np.sqrt(c**2 * (X**2/a**2 + Y**2/b**2 + 1))

ax.plot_surface(X, Y, Z)

plt.show()
