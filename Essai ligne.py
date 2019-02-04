# -*- coding: utf-8 -*-
"""
Simulateur de traffic

"""
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation

# Méthode RK4 résolutin ODE
def RK4(func, y0, t):
  dt = t[1] - t[0]
  nt = len(t)
  Y  = np.zeros([nt, len(y0)])
  Y[0] = y0
  for i in xrange(nt-1):
    k1 = func(Y[i], t[i])
    k2 = func(Y[i] + dt/2. * k1, t[i] + dt/2.)
    k3 = func(Y[i] + dt/2. * k2, t[i] + dt/2.)
    k4 = func(Y[i] + dt    * k3, t[i] + dt)
    Y[i+1] = Y[i] + dt / 6. * (k1 + 2. * k2 + 2. * k3 + k4)
  return Y


gammas = np.linspace(2,4,5) # Gamma = [2., 4.]
nGamma = len(gammas)


# Variables

AMAX = 0.6 #Accélération maximale des véhicules (a)
DMAX = 1.5 #Distance maximale avant freinage (b)
VMAX = 30 #Vitesse maximales des véhicules sur route libre (V0)

MIN_DIST  = 2.0 #Distance minimale entre deux véhicules (S0)
TIME_HEAD = 1.5 #Time Head = temps de sécurité (T)
CAR_SIZE  = 5.0 #Taille de la voiture

DELTA = 4.0 #Delta

# Partie Dynamique

dt = 0.01 #Pas de temps (temps d'échantillonna)
T = 200.0 #Durée d'échantillonnage
nSteps = int(T/dt) #Nombre d'échantillons

t_t = np.linspace(0., T, nSteps)

x = np.zeros((nGamma, nSteps+1))
v = np.zeros((nGamma, nSteps+1))
a = np.zeros((nGamma, nSteps))

def getAcceleration(x,v, gamma):
    
    """
    Fonction accélération IDM (Intelligent Driver Model)
    """
    
    # Différence de vitesse
    deltaV = v - 0.0

    # Ecart désiré avec le véhicule de devant
    s_star = MIN_DIST + np.max([0.0 , v * TIME_HEAD + (v * deltaV)/(2.0*np.sqrt(AMAX*DMAX))])

    # Ecart actuel
    s_alpha = 0.0 - x - CAR_SIZE
    
    # Terme Behavior at high approaching rates
    gap_term = (s_star / s_alpha)**gamma;

    # Vitesse limite (Terme Free Road Behavior)
    limit_term = (v / VMAX)**DELTA
    
    # Accélération
    a = AMAX * (1. - limit_term - gap_term)
    
    return a
    
for i, gamma in enumerate(gammas):
    
    v0 = 11.0 #Vitesse initiale
    x0 = 0.0 #
    t = 0.0
    
    #Condition initiales pour chaque véhicules
    x[i,0] = x0;
    v[i,0] = v0;
    
    for j in range(nSteps):
        a[i,j] = getAcceleration(x[i,j],v[i,j],gamma) # L'accélération du véhicle i
        
        dep_x = v[i,j] * dt + 0.5*a[i,j]*dt*dt 

        v[i,j+1] = v[i,j] + a[i,j] * dt
        x[i,j+1] = x[i,j] + dep_x
        
fig = plt.figure(0)
ax = plt.subplot(111, autoscale_on=False, xlim=(x0, x0 + 1000), ylim=(-1, nGamma)) #Définit les limites du cadre
yLoc = np.arange(-1, nGamma-1, 1) + 1 #Permet de tracer autant de ligne que de véhicules

line, = ax.plot(x[:,0],yLoc, 'o', lw=2)
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
t = 0


fig = plt.figure(1)
plt.subplot(ylim=(-1, 1))
plt.plot(t_t, a[0,:], '-r')
plt.plot(t_t, a[1,:], '-b')

def init():
    """initialize animation"""
    line.set_data([],[])
    time_text.set_text('')
    return line, time_text
    
def animate(i):
    """perform animation step"""
    global x, dt, t
    line.set_data(x[:,i],yLoc)
    time_text.set_text('time = %.1f' %t)
    t+=dt
    return line, time_text
    
ani = animation.FuncAnimation(fig, animate, frames=nSteps,
                              interval=0.1, blit=True, init_func=init)

plt.show()