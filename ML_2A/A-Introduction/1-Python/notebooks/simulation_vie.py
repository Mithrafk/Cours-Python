#%%
import random as rd


class plante():
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.vivant = True


class herbivore():
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.nourriture = 5
        self.age = 1
        self.vivant = True

    def deplacement(self, x, y):
        self.pos = (self.pos[0] + x, self.pos[1] + y)
        self.nourriture -= 0.25

    def manger(self, plante):
        if plante.vivant:
            plante.vivant = False
            self.nourriture += 1.25

    def repro(self):
        self.nourriture -= 5
        return herbivore(self.name + "_enfant", self.pos)


class carnivore():
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.nourriture = 5
        self.age = 1
        self.vivant = True

    def deplacement(self, x, y):
        self.pos = (self.pos[0] + x, self.pos[1] + y)
        self.nourriture -= 0.5

    def manger(self, herbivore):
        if herbivore.vivant:
            herbivore.vivant = False
            self.nourriture += 2.5

    def repro(self):
        if self.nourriture >= 20:
            self.nourriture -= 10
            return carnivore(self.name + "_enfant", self.pos)


#%%
def initialisation(nplante, nherbivore, ncarnivore):
    plante_list =       [plante(f"plante_{i}", (rd.randint(0,100), rd.randint(0,100))) for i in range(nplante)]
    herbivore_list =    [herbivore(f"herbivore_{i}", (rd.randint(0,100), rd.randint(0,100))) for i in range(nherbivore)]
    carnivore_list =    [carnivore(f"carnivore_{i}", (rd.randint(0,100), rd.randint(0,100))) for i in range(ncarnivore)]
    return plante_list, herbivore_list, carnivore_list

def Simulation(plante_list, herbivore_list, carnivore_list, jour):
    for herbivore in herbivore_list: #action des herbivores
        while herbivore.vivant:

            if herbivore.nourriture == 0:
                herbivore.vivant = False
            elif herbivore.nourriture > 0 and herbivore.nourriture < 10:
                herbivore.deplacement(rd.randint(-1,1),rd.randint(-1,1)) # mouvement aléatoire

            for plante in plante_list:
                if plante.pos == herbivore.pos:
                    herbivore.manger(plante.name)

            herbivore.repro()
            
            break

    for carnivore in carnivore_list: #action des carnivores
        while carnivore.vivant:

            if carnivore.nourriture == 0:
                carnivore.vivant = False
            elif carnivore.nourriture > 0 and carnivore.nourriture < 20:
                carnivore.deplacement(rd.randint(-1,1),rd.randint(-1,1)) # mouvement aléatoire

            for herbivore in herbivore_list:
                if herbivore.pos == carnivore.pos:
                    carnivore.manger(herbivore.name)

            carnivore.repro()

            break



def main():
    jour = 0
    plante_list, herbivore_list, carnivore_list = initialisation (100,40,20)
    for k in range(100):
        Simulation(plante_list, herbivore_list, carnivore_list, jour)
        jour += 1
