# Paramètres généraux:
from random import *
from tkinter import *
import csv
from tkinter import ttk

Base = 'U:/theo.bessadet/info/projet/Base données Questions.csv'
#Base = 'C:/Users/theob/Desktop/info/Base donnée.csv'

BRon, QWv, OL = False, False, False
LearnOK, ListLearn = [], []

## Action sur la base de donnée de questions:
# Lire les questions:
def ListQuestion(nom):
    h = open(nom, 'r', encoding='utf-8')
    r = h.readlines()                        # On copie notre fichier csv dans une liste
    h.close()
    n = len(r)
    b = []
    for k in range(1, n):
        line = r[k]
        line = line.rstrip()
        b.append(line)                      # On supprime la 1ère ligne (et le dernier
                                                #caractère ajouté par le format du fichier csv)
    return b                                # On rend notre liste de questions nettoyées

# Formater les questions pour entrer dans BioQuizz:
def ChoixQuestion(nom, Theme):
    global Question, Carre, Correct
    ListLearn = []
    B = ListQuestion(nom)                    # On lis notre base de donnée
    n = len(B)

    if Theme == None:                        # Aucun Choix de Thème:
        q = uniform(0,n-1)
        Q = int(q)
        Choix = B[Q]                             # On choisit une question au hasard parmis la base de donnée
        Affiche = Choix.split(',')               # On isole les 6 parties de notre ligne dans une liste
        R4 = []
        for k in range(4):                       # On isole les 4 réponses: Carré
            R4.append(Affiche[2+k])
        Carre = sample(R4, 4)                    # On mélange les réponses: ne pas avoir la bonne réponse toujours à la même place
        Correct = Affiche[2]
        Question = Affiche[1]
    else:                                   # Récuperer toutes les questions d'un thème donné
        for k in range(n):                       # On regarde toutes les questions à la suite:
            Choix = B[k]
            Affiche = Choix.split(',')
            if Affiche[0] == Theme:              # Si le thème de la question correspond à celui choisi, on l'ajoute à la liste
                ListLearn.append(Affiche)
    return ListLearn

# Editer la liste des thèmes :
def listTheme(nom):                              # Fonction qui rend tous les thèmes présents dans notre base de donnée
    listTheme = []
    B = ListQuestion(nom)
    n = len(B)
    for k in range(n):                           # On regarde les questions une par une:
        Choix = B[k]
        Affiche = Choix.split(',')
        m = len(listTheme)
        j = 0
        Pres = False
        while j < m and Pres == False:               # On balaye la liste contenant les thèmes "connus"
            if Affiche[0] == listTheme[j]:              # Si le thème de la question k est déjà présent dans la liste
                Pres = True                             # On fixe "Pres" à "True", et donc le thème ne sera pas ajouté dans la liste
            j = j + 1
        if Pres == False:                     # Si on rencontre un nouveau thème (c'est-à-dire Pres = False), on l'ajoute dans la liste
            listTheme.append(Affiche[0])
    return listTheme

## Programme entrée de Question :
def RenitThem():
    global wT1, wT2
    wT1.set('')
    wT2.set('')

# Fenêtre Entrer:
def OpenEntrer():
    global Fn, Fene, QW, wList, QWv, wT1, wT2
    if QWv == False :
        Fn.withdraw()
    else:
        QW.destroy()
        QWv = False

    # Paramètres:
    Fene = Toplevel(Fn)
    Fene.title("BioQuizz")
    Fene.geometry("475x275")
    Fene.focus_set()
    GridSize(Fene,3,6)
    ListTheme = listTheme(Base)

    # Entrée des demandes:
    wT1 = StringVar()
    theme = ttk.Combobox(Fene, values = ListTheme, textvariable = wT1)
    wT2 = StringVar()
    EntreT = Entry(Fene, textvariable = wT2)
    wQ = StringVar()
    EntreQ = Entry(Fene, textvariable = wQ, width = 50)
    wRC = StringVar()
    EntreRC = Entry(Fene, textvariable = wRC, fg = 'green')
    wR1 = StringVar()
    EntreR1 = Entry(Fene, textvariable = wR1, fg = 'brown')
    wR2 = StringVar()
    EntreR2 = Entry(Fene, textvariable = wR2, fg = 'brown')
    wR3 = StringVar()
    EntreR3 = Entry(Fene, textvariable = wR3, fg = 'brown')

    wList = [wT1, wT2, wQ, wRC, wR1, wR2, wR3]

    # Texte:
    tQ = Label(Fene, text = 'Votre Question :')
    tT = Label(Fene, text = 'Choix du thème :                      Thème déjà existant  ---- OU --- Nouveau Thème')
    tR1 = Label(Fene, text = 'Entrer la bonne réponse,', fg = 'green')
    tR2 = Label(Fene, text = 'puis 3 autres réponses', fg = 'brown')

    # Boutons:
    BoutonAcc = Button(Fene, text = "Accueil", command = MainMenu)
    BoutonVal = Button(Fene, text = "Valider l'entrée", command = QWriterVerif)
    BoutonRenitThem = Button(Fene, text = 'rénitialiser le thème', command = RenitThem)

    # Grids:
    BoutonAcc.grid(column = 1, row = 5)
    BoutonVal.grid(column = 2, row = 5)
    BoutonRenitThem.grid(row = 2)

    tQ.grid(row = 0)
    tT.grid(row = 1, columnspan = 3)
    tR1.grid(row = 3)
    tR2.grid(row = 4)


    EntreQ.grid(column = 1, columnspan = 2, row = 0)
    EntreT.grid(column = 2, row = 2)
    theme.grid(column = 1, row = 2)
    EntreRC.grid(column = 1, row = 3)
    EntreR1.grid(column = 2, row = 3)
    EntreR2.grid(column = 1, row = 4)
    EntreR3.grid(column = 2, row = 4)

# Vérifier qu'il n'existe pas de cases non remplies, puis écrire une liste avec tous les éléments récupérés:
def QWriterVerif():
    global wList, NewQ
    c = 0                                   # c: compteur de cases vides
    NewQ = []
    for k in range(7):
        NewQ.append(wList[k].get())         # Convertir les éléments récupéré en chaîne de caractère
    for k in range(7):
        if NewQ[k] == '':                   # Si un élément de la liste est vide, augmenter c de un
            c = c + 1
    if NewQ[0] != '' and NewQ[1] != '':     # Si 2 thèmes sont renseignés, demander d'en supprimer un
        Manque = Label(Fene, text = 'Sélectionner 1 seul theme')
        Manque.grid(row = 6, columnspan = 4)
    elif c == 1:
        QWriter()                           # S'il n'y a aucune erreure, on enregistre la question
    else:
        Manque = Label(Fene, text = "il reste " + str(c-1) + " cases à remplir !")
        Manque.grid(row = 6, columnspan = 4)


# Entrer une nouvelle question:
def QWriter():
    global wList, NewQ, Fene, QW ,QWv
    Fene.destroy()
    QWv = True

    if NewQ[0] == '':
        NewQ.pop(0)
    else:
        NewQ.pop(1)

    # Ecrire la nouvelle question dans le fichier:
    with open(Base, 'a', newline = '', encoding = 'utf-8') as csv_file:  # Ouvrir le fichier csv en mode ajout
        writer = csv.writer(csv_file)
        writer.writerow(NewQ)                                            # Ajouter la nouvelle question au fichier

    # Paramètres:
    QW = Toplevel(Fn)
    QW.title("BioQuizz")
    QW.geometry("350x225")
    QW.focus_set()
    GridSize(QW,5,5)

    # Boutons:
    BoutonAcc = Button(QW, text = "Accueil", command = MainMenu)
    BoutonEntrer = Button(QW, text = "Entrer une nouvelle question", command = OpenEntrer)

    # Grids:
    BoutonAcc.grid()
    BoutonEntrer.grid(column = 3)


## Programme Quizz

# Fenêtre Quizz:
def OpenQuizz():
    global Fn, Fene, BR, BRon
    Fn.withdraw()
    if BRon == True:
        BR.destroy()
        BRon = False
    ChoixQuestion(Base, None)

    # Paramètres:
    Fene = Toplevel(Fn)
    Fene.title("BioQuizz")
    Fene.geometry("350x225")
    Fene.focus_set()
    GridSize(Fene,3,5)

    # Boutons:
    BoutonAcc = Button(Fene, text = "Accueil", command = MainMenu)
    Reponse_0 = Button(Fene, text = Carre[0], command = VerifR0)
    Reponse_1 = Button(Fene, text = Carre[1], command = VerifR1)
    Reponse_2 = Button(Fene, text = Carre[2], command = VerifR2)
    Reponse_3 = Button(Fene, text = Carre[3], command = VerifR3)

    # Texte:
    Titre = Label(Fene, text = "Question :")
    Ennonce = Label(Fene, text = Question)

    # Grids:
    Titre.grid(column = 0, row = 0, columnspan = 2)
    BoutonAcc.grid(column = 2, row = 4)
    Ennonce.grid(column = 0, row = 1, columnspan = 2)
    Reponse_0.grid(column = 0, row = 2)
    Reponse_1.grid(column = 0, row = 3)
    Reponse_2.grid(column = 1, row = 2)
    Reponse_3.grid(column = 1, row = 3)


# Vérification de la réponse au Quizz:
def VerifR0():
    global Carre, Correct, txt
    if Carre[0] == Correct:
        txt = "Bravo, vous avez trouvé la bonne réponse."
        AfficheReponse()
    else:
        txt = "Vous vous êtes trompé de réponse."
        AfficheReponse()

def VerifR1():
    global Carre, Correct, txt
    if Carre[1] == Correct:
        txt = "Bravo, vous avez trouvé la bonne réponse."
        AfficheReponse()
    else:
        txt = "Vous vous êtes trompé de réponse."
        AfficheReponse()

def VerifR2():
    global Carre, Correct, txt
    if Carre[2] == Correct:
        txt = "Bravo, vous avez trouvé la bonne réponse."
        AfficheReponse()
    else:
        txt = "Vous vous êtes trompé de réponse."
        AfficheReponse()

def VerifR3():
    global Carre, Correct, txt
    if Carre[3] == Correct:
        txt = "Bravo, vous avez trouvé la bonne réponse."
        AfficheReponse()
    else:
        txt = "Vous vous êtes trompé de réponse."
        AfficheReponse()

# Afficher le résultat de la question:
def AfficheReponse():
    global Fene, BRon, BR, txt
    BRon = True
    Fene.destroy()
    C = []

    # Définir la couleur en fonction de la bonne réponse:

    for k in range(4):
        if Carre[k] == Correct:
            C.append("green")
        else:
            C.append("red")

    # Paramètres:
    BR = Toplevel(Fn)
    BR.title("BioQuizz")
    BR.geometry("350x225")
    BR.focus_set()
    GridSize(BR,4,4)

    # Boutons:
    BoutonAcc = Button(BR, text = "Accueil", command = MainMenu)
    NQuest = Button(BR, text = "Question suivante", command = OpenQuizz)

    # Texte:
    Reponse = Label(BR, text = txt)
    Reponse_0 = Label(BR, text = Carre[0], bg = C[0])
    Reponse_1 = Label(BR, text = Carre[1], bg = C[1])
    Reponse_2 = Label(BR, text = Carre[2], bg = C[2])
    Reponse_3 = Label(BR, text = Carre[3], bg = C[3])

    # Grids:
    Reponse.grid(column = 0, columnspan = 2, row = 0)
    Reponse_0.grid(column = 0, row = 1)
    Reponse_1.grid(column = 0, row = 2)
    Reponse_2.grid(column = 1, row = 1)
    Reponse_3.grid(column = 1, row = 2)
    BoutonAcc.grid(column = 2, row = 3)
    NQuest.grid(column = 2, row = 2)


## Programme Apprentissage:

# 1er Affichage:
def OpenLearn_1():
    global theme, Fene, ComptQuest, New, OL, ListTheme
    Fn.withdraw()
    if OL == True:
        Fene.destroy()
        OL = False

    # Paramètres:
    Fene = Toplevel(Fn)
    Fene.title("BioQuizz")
    Fene.geometry("350x250")
    Fene.focus_set()
    ComptQuest, New = 0, True
    ListTheme = listTheme(Base)
    GridSize(Fene,2,3)

    # 1er Affichage:
    theme = StringVar()
    themeAsk = ttk.Combobox(Fene, textvariable = theme, values = ListTheme)
    themeAsk.grid(row = 1)

    # Boutons:
    ValidTheme = Button(Fene, text = 'Valider le choix du thème', command = OpenLearnTest)
    ValidTheme.grid(row = 0)

    BoutonAcc = Button(Fene, text = "Accueil", command = MainMenu)
    BoutonAcc.grid(column = 1, row = 1)

def OpenLearnTest():
    global theme, ListTheme
    T = theme.get()
    if T in ListTheme:
        OpenLearn_2()
    elif T != '':
        Manque = Label(Fene, text = 'Choisissez un Theme de la liste')
        Manque.grid(columnspan = 2, row = 2)
    else:
        Manque = Label(Fene, text = 'Choisissez un Theme')
        Manque.grid(columnspan = 2, row = 2)

# Fenêtre Apprentissage:
def OpenLearn_2():
    global Fn, Fene, theme, ComptQuest, ListLearn, New, BoutonValid
    Fene.destroy()

    # Paramètres:
    Fene = Toplevel(Fn)
    Fene.title("BioQuizz")
    Fene.geometry("350x225")
    Fene.focus_set()
    GridSize(Fene,5,5)

    # Choisir les questions qui sont dans le thème:
    Theme = theme.get()
    if New == True:                                 # Si on arrive dans une nouvelle boucle d'apprentissage, on copie l'ensemble des
        ListLearn = ChoixQuestion(Base, Theme)          # questions qui ont le thème qui nous intéresse
        New = False

    # Sélectionner la question:
    Question = ListLearn[ComptQuest][1]

    # Boutons:
    BoutonAcc = Button(Fene, text = "Accueil", command = MainMenu)
    BoutonValid = Button(Fene, text = 'Valider la réponse', command = ValidRep)

    # Texte:
    LearnQ = Label(Fene, text = Question)
    TEntreR = Label(Fene, text = "entrer votre réponse :")

    # Entrée:
    rQ = StringVar()
    EntreR = Entry(Fene, textvariable = rQ)

    # Grids:
    BoutonAcc.grid(column = 2, row = 4)
    EntreR.grid(column = 1 , columnspan = 2, row = 2)
    TEntreR.grid(column = 0, row =2)
    LearnQ.grid(column = 0, columnspan = 3, row = 1)
    BoutonValid.grid(column = 2, row = 3)

# Valider réponse apprentissage:
def ValidRep():
    global Fene, ListLearn, BoutonValid

    # Texte:
    QReponse = Label(Fene, text = 'La réponse était : ' + ListLearn[ComptQuest][2] )

    # Boutons:
    ValidB_1 = Button(Fene, text = 'Réponse Correcte', command = TRep)
    ValidB_2 = Button(Fene, text = 'Réponse Fausse', command = FRep)

    # Grids:
    ValidB_1.grid(column = 0, row = 4)
    ValidB_2.grid(column = 1, row = 4)
    QReponse.grid(column = 0, columnspan = 2, row = 3)
    BoutonValid['state']= DISABLED

    # Réponse correcte:
def TRep():                             # Si la réponse est correcte :
    global Fene, ComptQuest, ListLearn
    Fene.destroy()
    ListLearn.pop(ComptQuest)           # On supprime cette question du cylce de question
    if ComptQuest >= len(ListLearn):    # Si on vient de répondre à la derniere question
        ComptQuest = 0                             # on revient au début du cycle de question
    if len(ListLearn) > 0:              # S'il reste des questions dans le cycle, on continue de les poser
        OpenLearn_2()
    if len(ListLearn) == 0:             # Sinon on termine la séssion d'apprentissage
        OpenLearn_3()

    # Réponse fausse:
def FRep():                             # Si la réponse est fausse :
    global Fene, ComptQuest, ListLearn
    Fene.destroy()
    ComptQuest = ComptQuest + 1         # On passe à la question suivante
    if ComptQuest >= len(ListLearn):    # Si on vient de répondre à la derniere question
        ComptQuest = 0                             # on revient au début du cycle de question
    OpenLearn_2()

# Fin D'apprentissage: Félicitation !!!
def OpenLearn_3():
    global Fn, Fene, theme, OL
    Fene.destroy()
    OL = True

    # Paramètres:
    Fene = Toplevel(Fn)
    Fene.title("BioQuizz")
    Fene.geometry("350x225")
    Fene.focus_set()
    GridSize(Fene,5,5)

    # Texte:
    Text = Label(Fene, text = "Bravo, vous avez terminé la série de question.")

    # Boutons:
    BoutonAcc = Button(Fene, text = "Accueil", command = MainMenu)
    BoutonApprentissage = Button(Fene, text = "Apprentissage", command = OpenLearn_1)

    # Grille:
    BoutonAcc.grid(column = 2, row = 2)
    BoutonApprentissage.grid(row = 2, column = 0)
    Text.grid(columnspan = 3, row = 0, column = 0)

#Lancer Questions du Thème:
def ValidT():
    BoutonValid = Button(Fene, text = 'Valider la réponse :', command = ValidRep)

    # Texte:
    LearnQ = Label(Fene, text = Question)
    rQ = StringVar()
    EntreR = Entry(Fene, textvariable = rQ)

    # Grids:
    EntreR.grid(column = 0, columnspan = 2, row = 2)
    LearnQ.grid(column = 0, columnspan = 3, row = 1)
    BoutonValid.grid(column = 2, row = 2)


## Programme Principal:

# Commande Retour Menu Principal:
def MainMenu():                  # Fonction permettant de fermer la fenêtre actuelle et de retourner à l'écran d'accueil
    global Fn, Fene, BRon, BR, QW, QWv
    if QWv == True:              # On teste les differentes fenêtres potentiellement ouvertes, si elles le sont, on les ferme
        QW.destroy()
        QWv = False
    elif BRon == True:
        BR.destroy()
        BRon = False
    else:
        Fene.destroy()
    Fn.update()
    Fn.deiconify()               # Puis on réouvre la fenêtre principale

# Taille de la grille prédéfinie:
def GridSize(Fn,n,p):
    for k in range(n):
        Fn.columnconfigure(k ,weight = 1)
    for k in range(p):
        Fn.rowconfigure(k ,weight = 1)

# Fenêtre principale:
def Fn_1():
    global Fn, Button

    # Paramètres:
    Fn = Tk()                           # On ouvre une fenêtre, avec son nom et sa taille
    Fn.title("BioQuizz")
    Fn.geometry("370x250")
    GridSize(Fn,5,5)

    # Boutons: on donne les commandes et les noms des différents boutons
    BoutonQuizz = Button(Fn, text = "Quizz", command = OpenQuizz)
    BoutonApprentissage = Button(Fn, text = "Apprentissage", command = OpenLearn_1)
    BoutonEntrer = Button(Fn, text = "Entrer une question", command = OpenEntrer)

    # Texte: on inscrit les différents textes à afficher
    Titre = Label(text = "BioQuizz")
    Mode = Label(text = "Sélectionner le Mode :")
    Description = Label( text =" BioQuizz est un logiciel de Quizz ")

    # Placement widgets: on définit la disposition et l'agencement de tous nos widgets
    BoutonQuizz.grid(column=1, row = 2, sticky = W, ipadx = 37, pady = 5, padx = 4)
    BoutonApprentissage.grid(column=1, row=3, sticky = W, ipadx = 14, pady = 5, padx = 4)
    BoutonEntrer.grid(column=1, row=4, sticky = W, pady = 5, padx = 4)
    Titre.grid(column = 0, columnspan = 3, row = 0)
    Mode.grid(column = 0, row = 2)
    Description.grid(column = 0, row = 1, columnspan = 3, sticky = 'ew')

    Fn.mainloop()


Fn_1()      # Ligne de code initialisant le lancement de notre fenêtre principale