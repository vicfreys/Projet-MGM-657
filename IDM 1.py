# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 10:07:12 2016

@author: Vic
"""

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation


dt = 0.01
Duree  = 200
nPas = int(Duree/dt)
nbVehicule = 10


class vehicule(object):
    
    """
    Classe véhicule :
        X[x, v, a] (position, vitesse, accélération)
    """
    
    def __init__(self, X0 = [0.,10.,0.], alpha = 0, t = 0, longueur = 5., v_lim = 30., dmin = 2., amax = 0., b = 1.5, T_H = 1.5):
        self.X = np.array([X0,]) # X[t][0:1:2] Position (0), Vitesse(1), Accélération (2) au temps t
        self.alpha = alpha # Numéro de véhicule
        self.dmin = dmin # Distance minimale entre 2 véhicules
        self.t = t # Instant t
        self.longueur = longueur # Longueur véhicule
        self.v_lim = v_lim # Vitesse limite
        self.a = a # Accélération maximale
        self.b = b # Décélération maximale
        self.T_H = T_H # Time Headway
        
        
    def getMove(self):
        
        self.X = np.append(self.X, [[0.,0.,0.]], axis = 0) # Correspond à l'état de point à t+1
                
        """
        Accélération
        """
        # Différence de vitesse
        deltaV = self.X[self.t][1] - 0.0 # Par la suite, 0.0 sera remplacé par la vitesse du véhicule de devant (comment faire, classe ...)
        
        # Ecart désiré avec le véhicule de devant
        s_star = self.dmin+ np.max([0.0 , self.X[self.t][1] * self.T_H + (self.X[self.t][1] * deltaV)/(2.0*np.sqrt(self.a*self.b))])
        
        # Ecart actuel
        s_alpha = 0.0 - self.X[self.t][0] - self.longueur # Par la suite, 0.0 sera remplacé par la position du véhicule de devant (comment faire, classe ...)
        
        # Terme "Behavior at high approaching rates"
        gap_term = (s_star / s_alpha)**2;
        
        # Vitesse limite (Terme "Free Road Behavior")
        limit_term = (self.X[self.t][1] / self.v_lim)**4.
        
        # Modifie l'accélération
        self.X[self.t][2]  = self.a * (1. - limit_term - gap_term)
        
        """
        Déplacement
        """
        dep_x = self.X[i][1]*dt + 0.5*self.X[self.t][2]*dt*dt # Déplacement de x (sur une droite)
        self.X[self.t+1][1] =  self.X[self.t][1] + self.X[self.t][2]*dt # Vitesse à t+1
        self.X[self.t+1][0] = self.X[self.t][0] + dep_x # Position à t+1
        
        

V = np.array([]) # Crée une liste de classe véhicule
Xi = np.zeros(nbVehicule*3).reshape(nbVehicule, 3) # Coordonnées initiales pour chaque véhicule
t=0

# Crée les véhicules
for i in range(nbVehicule):
    Xi[i][1] = np.random.random_integers(10, 10) # Permet de définir une vitesse aléatoire pour chaque véhicule
    V = np.append(V, vehicule(X0 = Xi[i], alpha = i+1)) # Attribue le numéro de véhicule (alpha)

"""
for vehicule in V:
    vehicule.getAcc()
    print "acceleration ", vehicule.alpha, " = " , vehicule.acceleration
    vehicule.getSpeed()
    print "vitesse ", vehicule.alpha, " = ", vehicule.X[t][1]

    print "position ", vehicule.alpha, " = ", vehicule.X[t][0]
"""

# Première simulation
i=0
while i < 20000:
        
    V[0].getMove()
    i+=1
    V[0].t = i
