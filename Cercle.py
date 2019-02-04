# -*- coding: utf-8 -*-
"""
Essai cercle afin d'adapter le programme "Essai ligne"
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

v0 = 10.
a0 = 0.
dt = 0.01
T = 200.
nPas = int(T/dt)
t = np.linspace(-T,T,nPas)

R = 5.

theta = np.linspace(0., 2*np.pi, 360.)

x = R**0.3/(2*np.pi)*np.cos(2*np.pi*theta/R)
y = R**0.3/(2*np.pi)*np.sin(2*np.pi*theta/R)

#x = road_length/(2*np.pi)*np.cos(2*np.pi*xx[i,:]/road_length)
#y = road_length/(2*np.pi)*np.sin(2*np.pi*xx[i,:]/road_length)


fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

plt.axes(xlim=(-2, 2), ylim=(-2, 2))


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
                               frames=360*int(R), 
                               interval=dt,
                               blit=True)

plt.show()

"""
y = np.linspace(-R, R, 100)
X, Y = np.meshgrid(x,y)
F = X**2 + Y**2 - R
plt.contour(X,Y,F, [0])
plt.show()
"""
