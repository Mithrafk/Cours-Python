#%%
import numpy as np
import pandas as pd

#%% Definir une matrice en numpy
A = np.array([[1,2,3,4], [1,3,4,5], [1,4,2,12]])

print(A)

#%% min, max, mean ... en numpy np.min(A) == A.min()

print(np.max(A, axis = 1)) # l'axe 1 disparait, ici en 2D on garde le 0

#%% M.Reshape()
maxA = np.max(A,1).reshape(3,1) # == reshape.(-1,1)

print(maxA)

# %% Il donne l'argmax de la matrice, mais en remettant tout en ligne
print(np.argmax(A))
print(np.argmax(A,0)) #l'indice du max de chaque colonne : 0 = garde la dim 0 == "ligne"


# %% matrice de 0-1 dim 4,6
# rand =  
# randn loi normale centrée réduite +/-inf avec 99% entre +/- 3
B = np.random.rand(4,6)
print(B)

# %% trouver les valeurs > 0.5 dans B
[I,J] = np.where(B > 0.5)      #position de chaque valeur
print([I,J])

for i, j in zip(I, J):          # rendre les valeurs
    print(B[i,j])

# %% Prendre les lignes ou le max > 0.7
i = np.where(B.max(1) > 0.7)
B2 = B[i,:]

print(B2)

# %% Concatener des mat
print(np.shape(A), np.shape(B))
np.concatenate( (B,B2), axis = 1)

# %%
