# -*- coding: utf-8 -*-
"""
Simulation traffic
@author: Vicor Freyssint, Bertrand Gaut,Yoan Darmedru et Robin Corruble

Reste à faire :
    - Afficher la simulation pour chaque véhicule
    - OK (semble fonctionner pour certaines valeurs, à voir par la suite) 
    - --> Régir le comportement de chaque véhicule selon le véhicule de devant (problème de classe...)
    - Afficher l'ordre de placement des véhicules
    - Faire apparaître les véhicules à des positions différentes et respectant la distance minimale dmin
    - Adapter le problème à une route circulaire
    - Eventuel probleme lié au premier véhicule...
    - Problèmes avec certaines valeurs (ex T_H = 2. et a = 2.) 
      et des vitesses (si un véhicule à une vitesse bien supérieur à celui de devant à t =0, "nan")
    - OK --> URGENT :   probème lié au tableau des positions des voitures, 
                        il faudrait le mettre à jour pour chaque position
"""

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation

dt = 0.01 # Pas de temps
Duree  = 10 # Durée
nPas = int(Duree/dt) # Nombre de pas pour la simulation
nbVehicule = 10 # Nombre de véhicules désirés pour la simulation
vmax = 30

class vehicule(object):
    
    """
    Classe véhicule
         
    """
    
    def __init__(self, X0 = [0.,10.,0.], alpha = 0, t = 0, longueur = 5., v_lim = vmax, dmin = 2., a = 1.5, b = 1.5, T_H = 1., next_alpha =0):
        self.X = np.array([X0,]) # X[t][0:1:2] Position (0), Vitesse(1), Accélération (2) au temps t
        self.alpha = alpha # Numéro de véhicule, correspondra à l'indice dans le tableau des 
        self.dmin = dmin # Distance minimale entre 2 véhicules
        self.t = t # Instant t
        self.longueur = longueur # Longueur véhicule (5. pour voiture, 12. pour les camions)
        self.v_lim = v_lim # Vitesse limite
        self.a = a # Accélération maximale
        self.b = b # Décélération confortable maximale (Comfortable braking deceleration)
        self.T_H = T_H # Time Headway
        self.next_alpha = next_alpha
        
        
        
    def getMove(self):
        
        self.X = np.append(self.X, [[0.,0.,0.]], axis = 0) # Correspond à l'état de point à t+1
                
        """
        Accélération
        """

        # Différence de vitesse
        deltaV = self.X[self.t][1]  - vitVehicule[self.t][self.next_alpha]
        
        # Ecart désiré avec le véhicule de devant
        s_star = self.dmin+ np.max([0.0 , self.X[self.t][1] * self.T_H + (self.X[self.t][1] * deltaV)/(2.0*np.sqrt(self.a*self.b))])
        
        # Ecart actuel
        s_alpha = posVehicule[self.t][self.next_alpha] - self.X[self.t][0] - self.longueur
        
        # Terme "Behavior at high approaching rates"
        gap_term = (s_star / s_alpha)**2
        
        # Vitesse limite (Terme "Free Road Behavior")
        limit_term = (self.X[self.t][1] / self.v_lim)**4.
        
        # Modifie l'accélération
        self.X[self.t][2]  = self.a * (1. - limit_term - gap_term)
        
        
        """
        Déplacement (position et vitesse)
        """
        dep_x = self.X[i][1]*dt + 0.5*self.X[self.t][2]*dt*dt # Déplacement de x (sur une droite)
        
        # Mise à jour des positions du véhicule
        self.X[self.t+1][1] = self.X[self.t][1] + self.X[self.t][2]*dt # Vitesse à t+1
        self.X[self.t+1][0] = self.X[self.t][0] + dep_x # Position à t+1
    
    #Cherche les voitures devant chacune
    def voitureSuivante(self):
        
        dist_alpha = posVehicule[self.t][...,self.alpha] # Donne la position de la voiture alpha (celle à qui l'on veut déterminer la voiture suivante alpha-1)
        pos_prime1 = posVehicule[self.t] - dist_alpha # On soustrait la valeur de la distance à la liste, 
                                      # afin de trouver la plus petite valeur positive, qui correspond à la voiture la plus proche
        
        # On parcourt l'ensemble des valeurs de la liste
        for i in range(len(pos_prime1)):
            if pos_prime1[i] <= 0: # Si une valeur est négative ou nulle = voiture située derrière ou au même niveau
                pos_prime1[i] = np.nan # On affecte la valeur "nan", différenciable du zéro pour la recherche du minimum
    
        alpha_1 = np.nanmin(pos_prime1) # Valeur minimale (ignore les "nan", d'où ce qui a été fait précédemment)
       
       
        alpha_suiv = self.alpha # Par défaut, la voiture suivante est la voiture alpha elle même
        
        # On recherche l'indice de la valeur correspondante dans la liste
        for j in range(len(pos_prime1)):
            if pos_prime1[j] == alpha_1:
                alpha_suiv = j # alpha_suiv correspond à l'index de la liste
        
        return alpha_suiv # Retourn l'alpha du véhicule
    
    # Permet de trouver la voiture leader pour le véhicule alpha en question
    def getNextcar(self):
        self.next_alpha = self.voitureSuivante()
        return self.next_alpha
        
        
"""
Programme
"""     


Xi = np.zeros(nbVehicule*3).reshape(nbVehicule, 3) # Coordonnées initiales pour chaque véhicule
V = np.array([]) # Crée une liste de classe véhicule
posVehicule = np.zeros(nbVehicule*nPas).reshape(nPas,nbVehicule) # Position des véhicules pour tous les instants t
vitVehicule = np.zeros(nbVehicule*nPas).reshape(nPas,nbVehicule) # # Position des véhicules pour tous les instants t

# Crée les véhicules
for i in range(nbVehicule):
    Xi[i][1] = np.random.random_integers(0, vmax) # Permet de définir une vitesse aléatoire pour chaque véhicule
    Xi[i][0] = i*7 #np.random.random_integers(0, 100) # Permet de définir une position aléatoire pour chaque véhicule

    V = np.append(V, vehicule(X0 = Xi[i], alpha = i)) # Attribue le numéro de véhicule (alpha) et ainsi que ses conditions initiales


# Affiche les condition initiales (t=0) de chaque véhicule
for v in V:
    print "Position " , v.alpha, " : ", v.X[0][0]
for v in V:
    print "Vitesse " , v.alpha, " : ", v.X[0][1]

# Première simulation

i=0    # Initialisation du compteur 
while i < nPas: # Pour chaque instant t...
    for j in range(len(V)): # ... on met à jour chaque véhicule
        V[j].t = i # Mise à jour de l'instant t des véhicule (à améliorer)
        V[j].getNextcar() # Recherche du véhicule leader
        V[j].getMove() # Déplacement du véhicule
        posVehicule[i][j] = np.array(V[j].X[i][0]) # Les positions de tous les véhicules à t = i
        vitVehicule[i][j] = np.array(V[j].X[i][1]) # Les vitesses de tous les véhicules à t = i
    i+=1 # On incrémente le pas


ti = nPas
# Affiche les positions à l'instant ti
for v in V:
    print "Position " , v.alpha, " à t = ", ti, " : ", v.X[ti][0]
for v in V:
    print "Vitesse " , v.alpha, " à t = ", ti, " : ", v.X[ti][1]

print "Fini"


"""
Partie animation
"""

t=0
fig = plt.figure(0)
ax = plt.subplot(111, autoscale_on=False, xlim=(0, 1000), ylim=(-5, 5)) #Définit les limites du cadre

point, = ax.plot([],[], 'o', lw=2)

temps = ax.text(0.02, 0.95, '', transform=ax.transAxes)

def init():
    
    point.set_data([],[])
    temps.set_text('')

    return point, temps
    
def animate(i):

    global dt, t
    point.set_data(V[0].X[i][0],0)
    temps.set_text('time = %.1f' %t)
    t += dt
    return point, temps
    
ani = animation.FuncAnimation(fig, animate, frames=nPas,
                              interval = 0.1, blit=True, init_func=init)

plt.show()
