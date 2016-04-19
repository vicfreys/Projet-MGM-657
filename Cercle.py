# -*- coding: utf-8 -*-
"""
Essai cercle afin d'adapter le programme "Essai ligne"
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation


theta = np.linspace(0., 2*np.pi, 360.)

#W Coordonnées du point
x = np.cos(theta)
y = np.sin(theta)


fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

plt.axes(xlim=(-1, 1), ylim=(-1, 1))

#plt.plot(x, y , '-')

point, = plt.plot([],[], 'o')

def init():
    point.set_data([], [])
    return point,

def animate(i):
    point.set_data(x[i],y[i])
   
    return point,
    
anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=360, 
                               interval=20,
                               blit=True)

plt.show()