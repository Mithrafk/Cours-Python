#%%
"""
Interface graphique matplotlib pour visualiser la simulation.

Hypothèses sur le code de simulation (à adapter si besoin) :
- plante_list, herbivore_list, carnivore_list sont des listes d'objets
  ayant chacun un attribut .pos = (x, y) et .vivant (bool)
- Simulation(plante_list, herbivore_list, carnivore_list) fait
  avancer la simulation d'UN pas (un jour), pas une boucle interne
  jusqu'à la mort de chaque individu.
- initialisation(nplante, nherbivore, ncarnivore) renvoie les 3 listes
  de départ.

Adapte les imports ci-dessous si ton fichier de simulation a un autre nom.
"""
# %%
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random as rd

#%%

from simulation_vie import initialisation, Simulation

#%%
TAILLE_CARTE = 100
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
    ax.set_xlim(0, TAILLE_CARTE)
    ax.set_ylim(0, TAILLE_CARTE)
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


if __name__ == "__main__":
    plante_list, herbivore_list, carnivore_list = initialisation(100, 40, 20)
    anim = creer_animation(plante_list, herbivore_list, carnivore_list)

# %%
