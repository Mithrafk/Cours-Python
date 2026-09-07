#%% Initialisation
import numpy as np
import pandas as pd

X_init = np.array(['A', 'C', 'C', 'G', 'A', 'C', 'T', 'T', 'A', 'G', 'A', 'C', 'A', 'G', 'G', 'T'], dtype=str)
Y_init = np.array(['T', 'T', 'A', 'C', 'C', 'G', 'A', 'C', 'G', 'T', 'A', 'T', 'A', 'C', 'A', 'G', 'C', 'G', 'T', 'A'],dtype=str)

X_test = np.copy(X_init)
Y_test = np.copy(Y_init)

#%% Fonction
def scoring(a,b):
    ## score de a par rapport à b
    if a == '-' or b == '-':
        return -4 # -4 si contient une deletion
    elif a == b:
        return 2  # +2 si identique
    else:
        return -2 # -2 si différent

def gap(A,i,n):
    # Fonction permettant d'inserrer n tiret à la pos i
    M = np.copy(A)
    for _ in range(n):
        M = np.insert(M,i,'-')
    return M

def Sim(A,B,i,j):
    # Obtenir le score des de comparaison entra A[i:j] et B[i:j]
    score = 0

    if len(A) < j:
        A = gap(A, len(A), j-len(A))
    if len(B) < j:
        B = gap(B, len(B), j-len(B))

    for k in range(i,j):
        score += scoring(A[k],B[k])

    return score

def alignement(A,B):
    # recherche du chemin optimum
    n1 = len(A)
    n2 = len(B)


def mat_sim(A,B):
    # construire la matrice
    n = len(A)
    p = len(B)

    M = np.zeros((n+1,p+1))

    return M
#%% Run
#print(Sim(X_test, Y_test, 15,20))

print(mat_sim(X_test,Y_test))

# %%
