# -*- coding: utf-8 -*-
"""
@author: Vicor Freyssinet, Bertrand Haut, Yoan Darmedru, Robin Corruble
Simulation de traffic selon l'"Inteligent Driver Model"


Problèmes, bugs :
    - OK --> URGENT :   probème lié au tableau des positions des voitures, 
                        il faudrait le mettre à jour pour chaque position
                        et des vitesses (si un véhicule a une vitesse bien supérieure à celui de devant à t =0, "nan")
Reste à faire : 
    - Stocker les fichiers dans un fichier texte afin de rendre plus rapide l'éxécution du programme
    - Afficher les vitesses de chaque véhicule sur le graphique
    - Adapter le problème à une route circulaire
       
- IDEES d'amélioration : 
    - Impact sur la consommation de carburants
    - Nombre d'accidents produits selon les différents paramètres
    - Créer plusieurs types de comportements : normal, agressif, sportif, lent...
                            - 
"""

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
plt.rcParams['animation.ffmpeg_path'] ='H:\\MGM 657\\Projet\\ffmpeg-20160512-git-cd244fa-win32-static\\bin\\ffmpeg.exe'
FFwriter = animation.FFMpegWriter()

#   ------------------------
#   Définition des variables
#   ------------------------
dt = 0.01 # Pas de temps
Duree  = 100 # Durée
nPas = int(Duree/dt) # Nombre de pas pour la simulation
nbVehicule = 5 # Nombre de véhicules désirés pour la simulation
vmax = 60 # Vitesse maximale
# Pour avoir a listes de N termes : np.zeros(a*N).reshape(N, a)
Xi = np.zeros(nbVehicule*3).reshape(nbVehicule, 3) # Coordonnées initiales (à t = 0) pour chaque véhicule
V = np.array([]) # Crée une liste de classe véhicule
posVehicule = np.zeros(nbVehicule) # Position des véhicules
vitVehicule = np.zeros(nbVehicule) # Position
Pos = np.zeros(nbVehicule*nPas).reshape(nPas,nbVehicule) # Array pour enregistrer les positions des véhicules pour tous les instants t
Vit = np.zeros(nbVehicule*nPas).reshape(nPas,nbVehicule) # Array pour enregistrer les vitesses des véhicules pour tous les instants t

i = 0
j = 0
class vehicule(object):
    
    """
    Classe véhicule       
    """
    
    def __init__(self, X0 = [0.,10.,0.], alpha = 0, longueur = 5., v_lim = vmax, dmin = 2., a =1., b = 1.5, T_H = 2., next_alpha = 0):
        self.X = np.array(X0) # X[0:1:2] Position [0], Vitesse[1], Accélération [2] au temps t
        self.alpha = alpha # Numéro de véhicule, correspondra à l'indice dans le tableau des véhicules
        self.dmin = dmin # Distance minimale entre 2 véhicules ()
        self.longueur = longueur # Longueur véhicule (l)
        self.v_lim = v_lim # Vitesse limite (v0)
        self.a = a # Accélération maximale (a)
        self.b = b # Décélération confortable maximale (b, Comfortable braking deceleration)
        self.T_H = T_H # Time Headway (T)
        self.next_alpha = next_alpha # Alpha du véicule de devant (alpha-1)
        
    def getMove(self, dt,i):
        
        #self.X = np.append(self.X, [[0.,0.,0.]], axis = 0) # Correspond à l'état de point à t+1
             
        """
        Calcul de l'accélération
        """
        # Si le véhicule est seul (le véhicule de devant par exemple)
        if self.alpha == 0:
            
            # On ne calcule que le free road behavior (limit_term)
            limit_term = (self.X[1] / self.v_lim)**4.
            self.X[2]  = self.a * (1. - limit_term )
            """
            # Ralentissements
            if (100 < i < 2000) or (4000 < i < 7000):
                
                vlim=0
                
                # Vitesse limite (Terme "Free Road Behavior")
                limit_term = (self.X[1] / vlim)**4.
                
                # Modifie l'accélération
                self.X[2]  = self.a * (1. - limit_term)
            """ 
        else:
            # Ecart de vitesse avec le véhicule de devant
            deltaV = self.X[1] - vitVehicule[self.next_alpha]
        
            # Ecart désiré avec le véhicule de devant
            s_star = self.dmin+ np.max([0.0 , self.X[1] * self.T_H + (self.X[1] * deltaV)/(2.0*np.sqrt(self.a*self.b))])
            
            # Ecart actuel
            s_alpha = posVehicule[self.next_alpha] - self.X[0] - self.longueur
            
            # Terme "Behavior at high approaching rates"
            gap_term = (s_star / s_alpha)**2.
            
            # Vitesse limite (Terme "Free Road Behavior")
            limit_term = (self.X[1] / self.v_lim)**4.
            
            # Modifie l'accélération
            self.X[2]  = self.a * (1. - limit_term - gap_term)
            """
            # Ralentissement
            if 1000 < i < 4000:

                vlim=30
                
                # Vitesse limite (Terme "Free Road Behavior")
                limit_term = (self.X[1] / vlim)**4.
                
                # Modifie l'accélération
                self.X[2]  = self.a * (1. - limit_term)
            """
    
        """
        Déplacement (position et vitesse)
        """
        dep_x = self.X[1]*dt + 0.5*self.X[2]*dt*dt # Déplacement de x (sur une droite)
        
        # Mise à jour des positions du véhicule
        self.X[1] = self.X[1] + self.X[2]*dt # Vitesse à t+1
        self.X[0] = self.X[0] + dep_x # Position à t+1
    
    # Cherche les voitures suivantes
    def voitureSuivante(self):
        
        dist_alpha = posVehicule[...,self.alpha] # Donne la position de la voiture alpha (celle à qui l'on veut déterminer la voiture suivante alpha-1)
        pos_prime1 = posVehicule - dist_alpha # On soustrait la valeur de la distance à la liste, 
                                                      # afin de trouver la plus petite valeur positive, qui correspond à la voiture la plus proche
        
        # On parcourt l'ensemble des valeurs de la liste
        for i in range(len(pos_prime1)):
            if pos_prime1[i] <= 0: # Si une valeur est négative ou nulle = voiture située derrière ou au même niveau
                pos_prime1[i] = np.nan # On affecte la valeur "nan", différenciable du zéro pour la recherche du minimum
    
        alpha_1 = np.nanmin(pos_prime1) # Valeur minimale (ignore les "nan", d'où ce qui a été fait précédemment)
       
       
        alpha_suiv = self.alpha # Par défaut, la voiture suivante est la voiture alpha elle même
        
        # On recherche l'indice de la valeur correspondante dans la liste
        for k in range(len(pos_prime1)):
            if pos_prime1[k] == alpha_1:
                alpha_suiv = k # alpha_suiv correspond à l'index de la liste
        
        return alpha_suiv # Retourn l'alpha du véhicule suivant
    
    # Permet de trouver la voiture leader pour le véhicule alpha
    def getNextcar(self):
        
        self.next_alpha = self.voitureSuivante()
        #return self.next_alpha
        
#   ----------------
#   PROGRAMME FINAL
#   ----------------    

#   ----------------------------------------
#   Création et initialisation des véhicules
#   ----------------------------------------
for i in range(nbVehicule):
    # Attribution des Conditions Initiales pour chaque véhicule
    Xi[i][1] = vmax - i*(vmax/nbVehicule) #np.random.random_integers(10, 10) # Permet de définir une vitesse aléatoire pour chaque véhicule
    Xi[i][0] = 50.*(nbVehicule-1)-i*50. #np.random.random_integers(0, 100) # Permet de définir une position aléatoire pour chaque véhicule
    Xi[i][2] = 10
    # Remplit la liste des véhicules avec leur vitesse initiale et leur alpha
    V = np.append(V, vehicule(X0 = Xi[i], alpha = i)) # Attribue le numéro de véhicule (alpha) et ainsi que ses conditions initiales
    

# Affiche les condition initiales (t=0) de chaque véhicule
for v in V:
    print "Position " , v.alpha, " : ", v.X[0]
for v in V:
    print "Vitesse " , v.alpha, " : ", v.X[1]

#   -------------------------
#   Simulation sans animation
#   -------------------------
"""
i = 0    # Initialisation du compteur

while i < nPas: # Pour chaque instant t...
   
    for j in range(len(V)): # ... on met à jour les différents paramètres de chaque véhicule 
        #V[j].getNextcar() # Recherche du véhicule leader
        #print "Next alpha " , j, " est ", V[j].next_alpha
        #V[j].getMove() # Déplacement du véhicule selon le véhicule de devant (leader)
        posVehicule[j] = np.array(V[j].X[0]) # Les positions de tous les véhicules à t = i
        vitVehicule[j] = np.array(V[j].X[1]) # Les vitesses de tous les véhicules à t = i
        Pos[i][j] = V[j].X[0]
        Vit[i][j] = V[j].X[1]

        V[j].getNextcar() # Recherche du véhicule leader
        #print V[j].getNextcar()
        V[j].getMove(dt) # Déplacement du véhicule selon le véhicule de devant (leader)

    i+=1 # On incrémente le pas

# Affiche les positions à l'instant ti
ti = nPas # Temps final
for v in V:
    print "Position " , v.alpha, " à t = ", ti, " : ", v.X[0]
for v in V:
    print "Vitesse " , v.alpha, " à t = ", ti, " : ", v.X[1]

print "Fini"


#   ----------
#   Graphiques
#   ----------

temps = np.linspace(0, Duree, nPas)
fig = plt.figure(0)
plt.clf()
plt.plot(Pos, Vit)
plt.grid()
plt.legend()
plt.xlabel("Position, $p$")
plt.ylabel("Vitesse, $v$")

# Affiche la position de tous les véhicules
fig = plt.figure(2)
plt.clf()
plt.plot(temps, Vit)
plt.grid()
plt.legend()
plt.xlabel("Temps, $t$")
plt.ylabel("Position, $x(t)$")

"""
#   -------------------------
#   Simulation avec animation
#   -------------------------

i=0
fig = plt.figure(4)
ax = plt.subplot(111, autoscale_on=False, xlim=(0, 8000), ylim=(-5, 5)) # Définit les limites du cadre
t=0
voitures = [ax.plot([],[], 'o', lw=2)[0] for _ in range(nbVehicule)]

def init():
    for voiture in voitures:
        voiture.set_data([],[])
    return voitures
    
def animate(i):
    
    for k, voiture in enumerate(voitures):
        
        voiture.set_data(V[k].X[0],0)
        posVehicule[k] = np.array(V[k].X[0]) # Les positions de tous les véhicules à t = i
        vitVehicule[k] = np.array(V[k].X[1]) # Les vitesses de tous les véhicules à t = i

        V[k].getNextcar() # Recherche du véhicule leader
       
        V[k].getMove(dt,i) # Met en mouvement les véhicules
        #print V[0].X[1]
    
    return voitures
    
ani = animation.FuncAnimation(fig, animate, frames=nPas,
                              interval = dt, blit=True, init_func=init)
#ani.save('02_no_info.mp4', writer=FFwriter, fps=30)
plt.show()
