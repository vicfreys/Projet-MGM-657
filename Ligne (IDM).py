"""
Simulateur de traffic sur ligne droit, avec la méthode de l'IDM

"""
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation

# Méthode RK4 résolutin pour l'IDM, mais on ne sait pas quel paramètre intervient ...
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

# Variables

AMAX = 0.6 # Accélération maximale des véhicules (a)
DMAX = 1.5 # Distance maximale avant freinage (b)
VMAX = 30 # Vitesse maximales des véhicules sur route libre (V0)

MIN_DIST  = 2.0 # Distance minimale entre deux véhicules (S0)
TIME_HEAD = 1.5 # Time Head = temps de sécurité (T)
CAR_SIZE  = 5.0 # Taille de la voiture

DELTA = 4.0 # Delta
GAMMA = 2.0 # Gamma (terme au carré)

# Partie Dynamique

dt = 0.01 # Pas de temps (temps d'échantillonna)
T = 200.0 # Durée de l'expérience
nSteps = int(T/dt) # Nombre de pas

x = np.zeros(nSteps+1)
v = np.zeros(nSteps+1)
a = np.zeros(nSteps)
yLoc = np.zeros(nSteps+1)

def getAcceleration(x,v):
    
    """
    Fonction accélération IDM (Intelligent Driver Model) pour un seul véhicule, ou pour le véhicule leader
    x   : Position du véhicule
    v   : Vitesse du véhicule
    """
    
    # Différence de vitesse
    deltaV = v - 0.0 # Par la suite, 0.0 sera remplacé par la vitesse du véhicule de devant (comment faire, classe ...)

    # Ecart désiré avec le véhicule de devant
    s_star = MIN_DIST + np.max([0.0 , v * TIME_HEAD + (v * deltaV)/(2.0*np.sqrt(AMAX*DMAX))])

    # Ecart actuel
    s_alpha = 0.0 - x - CAR_SIZE # Par la suite, 0.0 sera remplacé par la position du véhicule de devant (comment faire, classe ...)
    
    # Terme "Behavior at high approaching rates"
    gap_term = (s_star / s_alpha)**GAMMA;

    # Vitesse limite (Terme "Free Road Behavior")
    limit_term = (v / VMAX)**DELTA
    
    # Accélération
    a = AMAX * (1. - limit_term - gap_term)
    
    return a
    

v0 = 10.0 #Vitesse initiale
x0 = 0.0 # Position initiale
t = 0.0
    
#Condition initiales pour chaque véhicules
x[0] = x0;
v[0] = v0;
    
for i in range(nSteps):
    a[i] = getAcceleration(x[i],v[i]) # L'accélération du véhicle 
    
    dep_x = v[i] * dt + 0.5*a[i]*dt*dt # Le déplacement après intégration

    v[i+1] = v[i] + a[i] * dt
    x[i+1] = x[i] + dep_x


fig = plt.figure(0)
ax = plt.subplot(111, autoscale_on=False, xlim=(x0-1, 1000), ylim=(-1, 1)) #Définit les limites du cadre


point, = ax.plot([],[], 'o', lw=2)
temps = ax.text(0.02, 0.95, '', transform=ax.transAxes)
t = 0


def init():
    
    point.set_data([],[])
    temps.set_text('')
    return point, temps
    
def animate(i):

    global x, dt, t
    point.set_data(x[i],0)
    temps.set_text('time = %.1f' %t)
    t += dt
    return point, temps
    
ani = animation.FuncAnimation(fig, animate, frames=nSteps,
                              interval=0.1, blit=True, init_func=init)

plt.show()
