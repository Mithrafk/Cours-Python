#%%
import random as rd

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

#%%
class plante:
    def __init__(self, pos):
        self.pos = pos
        self.vivant = True

    def mort(self):
        self.vivant = False

#%%
class animale:
    def __init__(self, pos, espece, vitesse, vision, constante):
        self.pos = pos
        self.espece = espece
        self.vitesse = vitesse
        self.vision = vision
        self.constante = constante
        self.age = 1
        self.vivant = True
        self.nourriture = 5 * self.constante

    def deplacement(self, cibles = None):
        for _ in range(self.vitesse):
            x = self.pos[0]
            y = self.pos[1]
            if cibles:                                          # Si on au moins une cible
                nearest = min( [(abs(c.pos[0]-x) + abs(c.pos[1]-y), c) for c in cibles], key=lambda a: a[0] ) # recherche de la cible la plus proche | Distance de Manhattan plutot qu'euclidienne
                
                if nearest[0] <= self.vision:                   # Si la plus proche est <= portée detection
                    dx = nearest[1].pos[0] - x                  # On va se diriger vers elle (en réduisant la plus grande distance x ou y)
                    dy = nearest[1].pos[1] - y
                    if abs(dx) >= abs(dy):
                        x += np.sign(dx)
                    else:
                        y += np.sign(dy)

                    if nearest[0] <= 1:              # On pourait self.pos = (x,y), puis nearest[1].pos == self.pos, mais ca oblige a le remettre plusierus fois en dessous
                        self.manger(nearest[1]) 
                        cibles.remove(nearest[1])               # Actualisation des cibles vivantes
                else:                                           # Sinon mouvement aléatoire
                    if rd.random() > 0.5:
                        x += rd.choice([-1,1])
                    else:
                        y += rd.choice([-1,1])

            else:
                if rd.random() > 0.5:
                    x += rd.choice([-1,1])
                else:
                    y += rd.choice([-1,1])
            
            if x < 0:                                           # Tests pour boucler sur les bords de la map si on en sort
                x = Taille_carte - 1
            elif x >= Taille_carte:
                x = 0
            if y < 0:
                y = Taille_carte - 1
            elif y >= Taille_carte:
                y = 0

            self.nourriture -= 0.35 * self.constante * max(self.age/(5*self.constante), 1) # Les deplacements dependent de l'espece (self.constante) et de l'age
            self.pos = (x,y)

    def manger(self, cible):
        if cible.vivant:
            cible.mort()
            self.nourriture += 5 * self.constante * (1 if self.age < 15*self.constante else self.age/(15*self.constante) )

    def mort(self):
        self.vivant = False

    def repro(self):
        if self.nourriture >= 15 * self.constante:
            self.nourriture -= 15 * self.constante/2
            return type(self)(self.pos, self.espece, self.vitesse, self.vision, self.constante)
        return None

class herbivore(animale):       # classe heritiere de animale
    def __init__(self, pos, espece, vitesse, vision, constante):
        super().__init__(pos, espece, vitesse, vision, constante)   # On donne les argument pour init animale

    def action(self, plante_list):
        if self.nourriture == 0:   # Si affame ou trop vieux = mort
            self.mort()
        
        self.deplacement(plante_list)      # deplacement de n cases visant une plante (s'il y en a a porte)

        self.age += 1    
        return self.repro()

class carnivore(animale):       # classe heritiere de animale
    def __init__(self, pos, espece, vitesse, vision, constante):
        super().__init__(pos, espece, vitesse, vision, constante)   # On donne les argument pour init animale

    def action(self, herbivore_list):
        if self.nourriture == 0:   # Si affame ou trop vieux = mort
            self.mort()
        
        self.deplacement(herbivore_list)      # deplacement de n cases visant une plante (s'il y en a a porte)

        self.age += 1    
        return self.repro()

#%%


#%% Activiter sur la grille
def rand_dep(n):
    if rd.random() > 0.5:
        dx = rd.randint(-1*n, 1*n)
        n =  n - abs(dx)  
        dy = rd.randint(-1*n, 1*n)
    else:
        dy = rd.randint(-1*n, 1*n)
        n =  n - abs(dy)  
        dx = rd.randint(-1*n, 1*n)
    return dx, dy

def initialisation(nplante, nherbivore, ncarnivore):
    plante_list =       [plante((rd.randint(0,Taille_carte - 1), rd.randint(0,Taille_carte - 1))) for i in range(nplante)]
    herbivore_list =    [herbivore((rd.randint(0,Taille_carte - 1), rd.randint(0,Taille_carte - 1)), 'lapin', 2, 4, 1) for i in range(nherbivore)]
    carnivore_list =    [carnivore((rd.randint(0,Taille_carte - 1), rd.randint(0,Taille_carte - 1)), 'renard', 3, 5, 2) for i in range(ncarnivore)]
    return plante_list, herbivore_list, carnivore_list


def Simulation(plante_list, herbivore_list, carnivore_list):
    add_herbivore = []
    for herbivore in herbivore_list: #action des herbivores
        if herbivore.vivant:
            xp, yp = get_positions(plante_list)
            enfant = herbivore.action(plante_list)
            if enfant is not None:
                add_herbivore.append(enfant)

    add_carnivore = []
    for carnivore in carnivore_list: #action des carnivores
        if carnivore.vivant:
            xh, yh = get_positions(herbivore_list)
            enfant = carnivore.action(herbivore_list)
            if enfant is not None:
                add_carnivore.append(enfant)

    plante_list[:] = [p for p in plante_list if p.vivant]
    herbivore_list[:] = [h for h in herbivore_list if h.vivant] + add_herbivore 
    carnivore_list[:] = [c for c in carnivore_list if c.vivant] + add_carnivore


#%% Affichage graphique
Taille_carte = 100
NB_FRAMES = 200          # nombre de jours simulés
INTERVALLE_MS = 150      # vitesse d'animation (ms entre 2 frames)


def get_positions(liste_individus):
    """Extrait les positions (x, y) des individus encore vivants."""
    vivants = [ind for ind in liste_individus if ind.vivant]
    if not vivants:
        return [], []
    xs = [ind.pos[0] for ind in vivants]
    ys = [ind.pos[1] for ind in vivants]
    return xs, ys


def creer_animation(plante_list, herbivore_list, carnivore_list):
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(0, Taille_carte)
    ax.set_ylim(0, Taille_carte)
    ax.set_title("Jour 0")
    ax.set_aspect("equal")

    # un scatter plot par classe, pour avoir une couleur/légende distincte
    scat_plantes = ax.scatter([], [], c="forestgreen", s=15, label="Plantes", marker="s")
    scat_herbivores = ax.scatter([], [], c="royalblue", s=30, label="Herbivores")
    scat_carnivores = ax.scatter([], [], c="firebrick", s=40, label="Carnivores")

    ax.legend(loc="upper right")

    jour_compteur = {"jour": 0}
    
    def update(frame):
        # fait avancer la simulation d'un jour
        Simulation(plante_list, herbivore_list, carnivore_list)
        jour_compteur["jour"] += 1

        xp, yp = get_positions(plante_list)
        xh, yh = get_positions(herbivore_list)
        xc, yc = get_positions(carnivore_list)

        # set_offsets attend un tableau de forme (N, 2), même vide
        scat_plantes.set_offsets(np.column_stack((xp, yp)) if xp else np.empty((0, 2)))
        scat_herbivores.set_offsets(np.column_stack((xh, yh)) if xh else np.empty((0, 2)))
        scat_carnivores.set_offsets(np.column_stack((xc, yc)) if xc else np.empty((0, 2)))

        ax.set_title(
            f"Jour {jour_compteur['jour']} — "
            f"{len(xp)} plantes, {len(xh)} herbivores, {len(xc)} carnivores"
        )

        return scat_plantes, scat_herbivores, scat_carnivores

    anim = animation.FuncAnimation(
        fig, update, frames=NB_FRAMES, interval=INTERVALLE_MS, blit=False, repeat=False
    )
    plt.show()
    return anim

#%%
plante_list, herbivore_list, carnivore_list = initialisation(500, 40, 20)
anim = creer_animation(plante_list, herbivore_list, carnivore_list)

# %%
