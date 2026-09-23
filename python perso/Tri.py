import numpy as np
import matplotlib.pyplot as plt

def sort(L):
    n = len(L)
    if n <= 1:
        return list(L)

    milieu = n // 2
    gauche = sort(L[:milieu])
    droite = sort(L[milieu:])

    return merge(gauche, droite)

def merge(L1, L2):
    i, j = 0, 0
    n, p = len(L1), len(L2)
    L = []
    while i < n and j < p:
        if L1[i] < L2[j]:
            L.append(L1[i])
            i += 1
        else:
            L.append(L2[j])
            j += 1
    if i < n:
        for k in range(n-i):
            L.append(L1[i+k])
    else:
        for k in range(p-j):
            L.append(L2[j+k])
    return L

def tri_avec_etapes(L):
    """Retourne le tableau trie et les etats apres chaque fusion."""
    travail = list(L)
    etapes = []

    def decouper_fusionner(debut, fin, profondeur):
        if fin - debut <= 1:
            return

        milieu = (debut + fin) // 2
        decouper_fusionner(debut, milieu, profondeur + 1)
        decouper_fusionner(milieu, fin, profondeur + 1)

        travail[debut:fin] = merge(travail[debut:milieu], travail[milieu:fin])
        etapes.append((travail.copy(), debut, fin, profondeur))

    decouper_fusionner(0, len(travail), 0)
    return travail, etapes


def afficher_tri(L, pause=0.001):
    """Anime les fusions du tri fusion, des sous-listes aux plus grandes."""
    resultat, etapes = tri_avec_etapes(L)
    x = np.arange(len(L))
    maximum = max(L, default=1)

    plt.ion()
    fig, ax = plt.subplots()

    for numero, (etat, debut, fin, profondeur) in enumerate(etapes, start=1):
        couleurs = np.full(len(etat), "lightgray", dtype=object)
        couleurs[debut:fin] = "royalblue"

        ax.clear()
        ax.bar(x, etat, color=couleurs)
        ax.set_title(
            f"Tri fusion - fusion {numero}/{len(etapes)} "
            f"(indices {debut} a {fin - 1})"
        )
        ax.set_xlabel("Position dans la liste")
        ax.set_ylabel("Valeur")
        ax.set_xlim(-0.5, len(L) - 0.5)
        ax.set_ylim(0, maximum * 1.1)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()
        plt.pause(pause)

    plt.ioff()
    ax.clear()
    ax.bar(x, resultat, color="seagreen")
    ax.set_title("Tri termine")
    ax.set_xlabel("Position dans la liste")
    ax.set_ylabel("Valeur")
    ax.set_xlim(-0.5, len(L) - 0.5)
    ax.set_ylim(0, maximum * 1.1)
    plt.show()
    return resultat

L = list(np.random.random(500) * 50)

if __name__ == "__main__":
    afficher_tri(L)