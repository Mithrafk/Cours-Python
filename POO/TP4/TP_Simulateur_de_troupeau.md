# TP Python --- Simulateur de troupeau

## 1. Contexte

Une exploitation d'élevage souhaite disposer d'un petit simulateur
permettant d'observer l'évolution d'un troupeau de vaches au cours du
temps.

Chaque animal possède un âge, un sexe et un état reproductif. Au cours
de la simulation, les animaux : - vieillissent ; - peuvent devenir aptes
à la reproduction ; - peuvent être gestants ; - peuvent donner naissance
à un veau ; - produisent du lait selon leur âge et leur cycle
reproductif ; - peuvent être réformés puis retirés du troupeau.

L'objectif est de construire un programme orienté objet capable de
simuler l'évolution du troupeau année après année et de visualiser sa
structure démographique.

Au départ, le troupeau est volontairement irrégulier. Après plusieurs
années virtuelles, on souhaite observer une pyramide des âges qui tend
vers une structure relativement stable, autour d'une quinzaine d'années
de simulation.

Le projet permettra de mobiliser naturellement : - la programmation
orientée objet ; - l'héritage ; - la composition ; - les méthodes ; -
les collections Python ; - les fichiers CSV/JSON ; - la validation des
données ; - la simulation à pas de temps discret ; - les statistiques
; - la visualisation ; - l'analyse de complexité.

## 2. Objectifs pédagogiques

À la fin du projet, l'étudiant devra être capable de :

1.  modéliser un problème avec plusieurs classes ;
2.  utiliser l'héritage entre une classe générale et une classe
    spécialisée ;
3.  utiliser la composition entre objets ;
4.  concevoir des méthodes d'évolution d'état ;
5.  gérer un ensemble d'objets évoluant dans le temps ;
6.  manipuler des données provenant d'un fichier ;
7.  détecter et corriger des données incohérentes ;
8.  mettre en œuvre une simulation discrète ;
9.  produire des statistiques à partir d'une simulation ;
10. représenter graphiquement une pyramide des âges ;
11. analyser la complexité des principales opérations ;
12. documenter les hypothèses de modélisation.

## 3. Scénario

Le troupeau est constitué principalement de vaches laitières.

La simulation avance par pas de temps d'un an.

À chaque année, le programme effectue, dans un ordre défini :

1.  vieillissement des animaux ;
2.  mise à jour de l'état reproductif ;
3.  naissance des veaux ;
4.  mise à jour de la production laitière ;
5.  décision éventuelle de réforme ;
6.  ajout des nouveaux animaux au troupeau ;
7.  calcul des statistiques ;
8.  affichage ou enregistrement des résultats.

La simulation pourra être lancée sur : - 1 an - 5 ans - 10 ans - 15
ans - 20 ans - ou davantage.

## 4. Modèle objet

Le projet doit au minimum comporter trois classes :

``` text
Animal
   ↑
   |
Vache
```

``` text
Troupeau
   |
   +--- contient plusieurs Animal / Vache
```

### 4.1 Classe Animal

Animal est la classe générale.

Elle contient les propriétés communes à tous les animaux.

Attributs minimaux :

-   `id`
-   `sexe`
-   `age`

On pourra également ajouter :

-   `annee_naissance`

ou :

-   `vivant`

selon les choix de conception.

Exemple :

``` python
class Animal:

    def __init__(self, identifiant, sexe, age):
        self.id = identifiant
        self.sexe = sexe
        self.age = age
```

## 5. Héritage : classe Vache

La classe Vache hérite de Animal.

Elle possède les caractéristiques supplémentaires nécessaires à la
simulation laitière.

Attributs minimaux proposés :

-   `race`
-   `lactation`
-   `nombre_de_veaux`
-   `gestante`
-   `age_derniere_mise_bas`
-   `jours_depuis_mise_bas`

Exemple :

``` python
class Vache(Animal):

    def __init__(
        self,
        identifiant,
        sexe,
        age,
        race,
        gestante=False
    ):
        super().__init__(
            identifiant,
            sexe,
            age
        )

        self.race = race
        self.gestante = gestante
```

Les étudiants peuvent choisir d'autres attributs, mais ils devront
justifier leurs choix.

## 6. Classe Troupeau

La classe Troupeau représente l'exploitation.

Elle contient les animaux.

Il s'agit d'un exemple de composition :

``` text
Troupeau
   |
   +--- Vache
   +--- Vache
   +--- Vache
   +--- ...
```

Le troupeau peut contenir une liste :

``` python
class Troupeau:

    def __init__(self):
        self.animaux = []
```

La classe Troupeau devra gérer notamment :

-   `ajouter_animal()`
-   `supprimer_animal()`
-   `vieillir()`
-   `reproduire()`
-   `mettre_a_jour_lactation()`
-   `reformer()`
-   `statistiques()`
-   `pyramide_ages()`

## 7. Règles de simulation

Les règles suivantes constituent le modèle simplifié du projet.

Elles ne cherchent pas à représenter fidèlement l'élevage réel : elles
servent à construire une simulation pédagogique.

### 7.1 Vieillissement

À chaque pas de temps :

`âge ← âge + 1`

Ainsi :

-   veau de 1 an → 2 ans
-   vache de 5 ans → 6 ans

## 8. Catégories d'âge

Pour les analyses démographiques, utiliser les classes d'âge suivantes :

-   0--1 an
-   2--3 ans
-   4--5 ans
-   6--7 ans
-   8--9 ans
-   10--11 ans
-   12--13 ans
-   14 ans et plus

La pyramide des âges utilisera ces classes.

## 9. Reproduction

Afin de garder le modèle simple, une vache peut devenir reproductrice à
partir de :

**2 ans**

Une vache adulte peut être gestante si elle n'est pas déjà gestante.

On utilisera une probabilité simplifiée de reproduction.

Par exemple :

**probabilité annuelle de gestation : 0,80**

Une vache gestante donne naissance après une période de gestation.

Pour simplifier le modèle discret, on considérera :

**gestation = 1 an**

Ainsi, si une vache devient gestante pendant l'année t, le veau naît au
début de l'année t+1.

## 10. Naissances

Lorsqu'une vache arrive au terme de sa gestation :

-   un veau est créé ;
-   le veau reçoit un identifiant unique ;
-   son âge est initialisé à 0 ;
-   son sexe est choisi aléatoirement.

On prendra par exemple :

-   50 % femelle
-   50 % mâle

Les veaux femelles pourront entrer dans le troupeau reproducteur
lorsqu'elles atteindront l'âge prévu.

## 11. Production laitière

La quantité de lait produite est simplifiée.

On pourra utiliser une production annuelle dépendant de l'âge et de
l'état reproductif.

Exemple de règle :

  Âge                Production annuelle indicative
  ---------------- --------------------------------
  moins de 2 ans                                0 L
  2--3 ans                                  4 500 L
  4--5 ans                                  6 000 L
  6--7 ans                                  6 500 L
  8--9 ans                                  6 000 L
  10--11 ans                                5 000 L
  12--13 ans                                3 500 L
  14 ans et plus                        0 à 2 000 L

Ces valeurs sont volontairement simplifiées.

La méthode :

`produire_lait()`

devra retourner la quantité produite pendant l'année.

### Variante

La production peut être multipliée par un coefficient aléatoire compris
entre :

**0,90 et 1,10**

afin de représenter la variabilité individuelle.

## 12. Réforme

Une vache doit pouvoir être retirée du troupeau.

Pour simplifier, la réforme pourra dépendre de plusieurs règles.

Exemple :

**âge ≥ 12 ans**

ou :

**production \< seuil minimal**

ou, éventuellement :

**probabilité annuelle de réforme**

Par exemple :

**à partir de 10 ans :**

**5 % de réforme par an**

et :

**à partir de 12 ans :**

**réforme obligatoire**

### À vous de jouer

Implémenter une méthode :

`doit_etre_reformee()`

qui retourne :

`True`

ou :

`False`

## 13. Jeu de données volontairement dégradé

Le fichier de départ est fourni sous la forme :

`troupeau_initial.csv`

Il contient volontairement des données imparfaites.

Créer le fichier suivant :

``` csv
id,sexe,age,race,gestante
V001,F,4,Prim'Holstein,false
V002,F,7,Prim'Holstein,true
V003,f,3,Montbéliarde,False
V004,F,12,Prim'Holstein,false
V005,F,2,Montbéliarde,false
V006,M,1,Prim'Holstein,false
V007,F,6,Montbeliarde,true
V008,F,8,Prim'Holstein,
V009,F,-1,Prim'Holstein,false
V010,X,5,Prim'Holstein,false
V011,F,15,Prim'Holstein,false
V012,F,4,,false
V013,F,9,Montbéliarde,true
V014,F,2,Prim'Holstein,TRUE
V015,F,6,Prim'Holstein,false
V015,F,6,Prim'Holstein,false
V016,M,0,Prim'Holstein,false
V017,F,11,Montbéliarde,false
V018,F,3,Montbéliarde,oui
V019,F,5,PRIM'HOLSTEIN,false
V020,F,13,Prim'Holstein,false
```

## 14. Problèmes volontairement introduits

Le fichier contient plusieurs anomalies.

Les étudiants doivent les identifier.

### Problème 1 --- Casse du sexe

``` text
F
f
M
X
```

Toutes les valeurs ne sont pas valides.

### Problème 2 --- Âge négatif

``` text
V009,-1
```

Un âge négatif est impossible.

### Problème 3 --- Race absente

``` text
V012
```

La race est manquante.

### Problème 4 --- Valeur manquante

``` text
V008
```

La valeur de gestante est absente.

### Problème 5 --- Synonymes / variantes

On trouve :

-   Montbéliarde
-   Montbeliarde

et :

-   Prim'Holstein
-   PRIM'HOLSTEIN

Une normalisation est nécessaire.

### Problème 6 --- Valeur booléenne incorrecte

``` text
oui
```

doit être interprété ou rejeté selon la stratégie choisie.

### Problème 7 --- Identifiant en double

``` text
V015
V015
```

Deux animaux ne doivent pas posséder le même identifiant.

### Problème 8 --- Sexe invalide

``` text
V010,X
```

L'étudiant doit définir les valeurs autorisées.

## 15. Validation des données

Écrire une fonction :

`valider_animal(donnees)`

qui vérifie :

-   présence de l'identifiant ;
-   unicité de l'identifiant ;
-   sexe valide ;
-   âge valide ;
-   race renseignée ;
-   valeur de gestante interprétable.

La fonction pourra renvoyer :

-   valide / invalide

ou un rapport plus détaillé.

Exemple :

``` text
V009
Erreur : âge négatif

V010
Erreur : sexe invalide

V012
Erreur : race absente

V015
Erreur : identifiant déjà utilisé
```

## 16. Nettoyage des données

Créer une fonction :

`nettoyer_animal(donnees)`

Elle devra notamment :

-   normaliser les chaînes ;
-   convertir correctement les booléens ;
-   corriger les variantes de race ;
-   éliminer ou signaler les lignes invalides ;
-   détecter les doublons.

Le programme devra produire un rapport indiquant :

``` text
20 lignes lues

16 animaux valides
4 lignes rejetées
1 doublon détecté
3 corrections automatiques
```

Les nombres ci-dessus sont un exemple : le résultat réel dépendra des
règles retenues.

## 17. Chargement du troupeau

Écrire :

`charger_csv(nom_fichier)`

qui :

1.  lit le fichier CSV ;
2.  valide les données ;
3.  nettoie les données ;
4.  crée les objets Vache appropriés ;
5.  les ajoute au Troupeau.

## 18. Simulation

Le cœur du projet est la méthode :

`simuler(annees)`

Chaque année doit suivre un ordre clairement documenté.

Une proposition :

Pour chaque année :

``` text
1. vieillir les animaux
2. faire évoluer les gestations
3. créer les naissances
4. calculer la production de lait
5. calculer les réformes
6. supprimer les animaux réformés
7. ajouter les nouveau-nés
8. calculer les statistiques
```

L'ordre exact peut être modifié, mais il devra être justifié.

## 19. Méthodes attendues

La classe Vache devra comporter au minimum des méthodes de ce type :

-   `vieillir()`
-   `peut_se_reproduire()`
-   `devient_gestante()`
-   `naissance()`
-   `produire_lait()`
-   `doit_etre_reformee()`

La classe Troupeau devra comporter notamment :

-   `ajouter_animal()`
-   `supprimer_animal()`
-   `faire_vieillir()`
-   `gerer_reproduction()`
-   `gerer_naissances()`
-   `calculer_production_laitiere()`
-   `gerer_reformes()`
-   `statistiques()`
-   `pyramide_ages()`
-   `simuler()`

L'étudiant peut proposer une organisation différente si elle est
cohérente.

## 20. Identifiants des nouveau-nés

Chaque nouveau-né doit recevoir un identifiant unique.

Exemple :

``` text
V021
V022
V023
...
```

L'identifiant ne doit jamais être réutilisé, même si l'animal
correspondant est réformé.

### Question

**Quelle structure de données peut permettre de vérifier efficacement
qu'un identifiant n'existe pas déjà ?**

## 21. Statistiques annuelles

À chaque année, calculer au minimum :

-   nombre total d'animaux ;
-   nombre de femelles ;
-   nombre de mâles ;
-   nombre de vaches reproductrices ;
-   nombre de gestantes ;
-   nombre de naissances ;
-   nombre de réformes ;
-   production totale de lait ;
-   âge moyen du troupeau.

Exemple :

``` text
Année 5

Effectif :              42
Femelles :              37
Mâles :                  5
Gestantes :             24
Naissances :             8
Réformes :               3
Production :       198 430 L
Âge moyen :           5.7 ans
```

## 22. Historique de la simulation

Le programme devra conserver les statistiques de chaque année.

Exemple :

``` python
historique = [
    {
        "annee": 0,
        "effectif": 20,
        "naissances": 0,
        "reformes": 0,
        "lait": 95000
    },
    ...
]
```

Cet historique servira à produire les graphiques.

## 23. Pyramide des âges

La pyramide des âges doit représenter la répartition des animaux par
classe d'âge.

Par exemple :

``` text
0-1       ████████████
2-3       █████████████████
4-5       ███████████████████
6-7       ███████████████
8-9       ██████████
10-11     ██████
12-13     ███
14+       █
```

On pourra utiliser matplotlib.

La méthode :

`troupeau.pyramide_ages()`

devra produire un graphique lisible.

## 24. Évolution de la pyramide des âges

Produire au minimum quatre pyramides :

-   Année 0
-   Année 5
-   Année 10
-   Année 15

### Travail d'analyse

Comparer les quatre graphiques et répondre :

1.  Comment évolue la structure du troupeau ?
2.  L'effectif augmente-t-il, diminue-t-il ou oscille-t-il ?
3.  Les classes d'âge deviennent-elles plus régulières ?
4.  Après une quinzaine d'années, observe-t-on une structure
    relativement stable ?

## 25. Étude de stabilisation

L'objectif principal est d'observer le comportement du système à long
terme.

Lancer une simulation sur :

**30 années**

Puis tracer :

### Graphique 1

**Année → Effectif total**

### Graphique 2

**Année → Production totale de lait**

### Graphique 3

**Année → Âge moyen**

### Graphique 4

**Année → Nombre de naissances**

### Question

**Que signifie ici « stabilisation » ?**

Les étudiants doivent proposer une définition opérationnelle, par
exemple :

la répartition des classes d'âge et l'effectif oscillent autour de
valeurs relativement constantes pendant plusieurs années.

## 26. Analyse de sensibilité

Modifier un paramètre à la fois.

Tester par exemple :

**probabilité de reproduction :**

-   0,60
-   0,70
-   0,80
-   0,90

Puis :

**âge maximal :**

-   10
-   12
-   14
-   16 ans

Puis :

**probabilité de réforme :**

-   0,02
-   0,05
-   0,10

### Travail demandé

Comparer l'effet de ces paramètres sur :

-   l'effectif ;
-   la production de lait ;
-   l'âge moyen ;
-   la structure de la pyramide des âges.

## 27. Diagramme de classes

Produire un diagramme présentant au minimum :

``` text
                 Animal
                   ▲
                   │
                 Vache
```

``` text
                 Troupeau
                   │
                   │ composition
                   ▼
            plusieurs Vache
```

Le diagramme doit faire apparaître :

-   héritage ;
-   composition ;
-   principaux attributs ;
-   principales méthodes.

## 28. Questions de programmation orientée objet

Répondre dans le rapport.

### Question 1

Pourquoi Vache hérite-t-elle de Animal ?

### Question 2

Quels attributs sont communs à tous les animaux ?

### Question 3

Quels attributs sont spécifiques à une vache laitière ?

### Question 4

Pourquoi Troupeau est-il un exemple de composition ?

### Question 5

Pourquoi serait-il mauvais de placer toute la logique de simulation dans
main() ?

### Question 6

Quelle différence entre :

``` python
animal.vieillir()
```

et :

``` python
troupeau.faire_vieillir()
```

## 29. Analyse de complexité

On note :

`n = nombre d’animaux dans le troupeau`

Si l'on parcourt tous les animaux chaque année pour effectuer les mises
à jour :

**O(n)**

pour une étape de vieillissement.

Si chaque année comporte un nombre constant de parcours du troupeau, une
année de simulation reste de l'ordre de :

**O(n)**

dans le modèle simple.

Pour A années :

**O(A × n)**

hors coût éventuel de structures supplémentaires.

### Question

Pourquoi une mauvaise implémentation pourrait-elle devenir beaucoup plus
coûteuse ?

Exemple :

-   rechercher systématiquement un animal dans une liste ;
-   effectuer des comparaisons inutiles entre tous les couples d'animaux
    ;
-   recalculer plusieurs fois les mêmes statistiques.

## 30. Robustesse

Le programme doit rester fonctionnel en présence :

-   d'un fichier absent ;
-   d'un CSV mal formé ;
-   de données incomplètes ;
-   d'un identifiant déjà utilisé ;
-   d'une valeur d'âge invalide ;
-   d'un choix utilisateur incorrect ;
-   d'un nombre d'années négatif.

Utiliser des exceptions spécifiques lorsque cela est pertinent :

``` python
try:
    ...
except FileNotFoundError:
    ...
```

## 31. Interface minimale

Le programme devra proposer un menu proche de :

``` text
=====================================
       SIMULATEUR DE TROUPEAU
=====================================

1. Charger un troupeau
2. Afficher le troupeau
3. Afficher les statistiques
4. Simuler 1 année
5. Simuler plusieurs années
6. Afficher la pyramide des âges
7. Afficher l'historique
8. Modifier les paramètres
0. Quitter
```

## 32. Paramètres configurables

Les paramètres de simulation ne doivent pas être écrits partout dans le
programme.

Créer par exemple une structure :

``` python
PARAMETRES = {
    "age_reproduction": 2,
    "probabilite_gestation": 0.80,
    "duree_gestation": 1,
    "age_reforme": 12,
    "probabilite_reforme": 0.05
}
```

Cela permettra de tester facilement plusieurs scénarios.

## 33. Tests obligatoires

Le projet doit contenir des tests pour au moins les situations suivantes
:

  Test                           Résultat attendu
  ------------------------------ ---------------------------
  Création d'un animal valide    Objet créé
  Âge négatif                    Erreur
  Sexe invalide                  Erreur
  Identifiant en double          Détection
  Vieillissement                 âge + 1
  Vache trop jeune               pas de reproduction
  Vache gestante                 pas de nouvelle gestation
  Fin de gestation               naissance
  Réforme                        retrait du troupeau
  Nouveau-né                     âge 0
  Production d'une jeune vache   cohérente avec le modèle
  Chargement CSV                 objets créés
  Fichier absent                 message d'erreur
  Simulation                     statistiques mises à jour

## 34. Livrables

Les étudiants devront rendre :

### 1. Code source

Par exemple :

``` text
projet_troupeau/
│
├── animal.py
├── vache.py
├── troupeau.py
├── simulation.py
├── statistiques.py
├── main.py
├── tests.py
└── troupeau_initial.csv
```

Une organisation différente est acceptée si elle est cohérente.

### 2. Jeu de données nettoyé

`troupeau_nettoye.csv`

### 3. Rapport

Entre 4 et 6 pages, comprenant :

-   présentation du modèle ;
-   diagramme de classes ;
-   choix de conception ;
-   stratégie de nettoyage ;
-   description des règles de simulation ;
-   graphiques ;
-   analyse de la stabilisation ;
-   analyse de complexité ;
-   tests ;
-   limites du modèle.

### 4. Résultats graphiques

Au minimum :

-   pyramide initiale ;
-   pyramide à 5 ans ;
-   pyramide à 10 ans ;
-   pyramide à 15 ans ;
-   évolution de l'effectif ;
-   évolution de la production laitière.

## 35. Grille d'évaluation --- 20 points

  Critère                                                       Points
  ------------------------------------------------------- ------------
  Modélisation objet : Animal, Vache, Troupeau                   3 pts
  Héritage et composition correctement utilisés                  2 pts
  Chargement, validation et nettoyage des données                2 pts
  Gestion du vieillissement, reproduction et naissances          3 pts
  Production laitière et réforme                                 2 pts
  Simulation multi-années et historique                          2 pts
  Pyramide des âges et visualisations                            2 pts
  Robustesse, gestion des erreurs et tests                      1,5 pt
  Analyse de complexité et qualité du code                      1,5 pt
  Rapport et interprétation des résultats                         1 pt
  **Total**                                                 **20 pts**

## 36. Critères qualitatifs

### Excellent

Le programme :

-   respecte clairement les principes de POO ;
-   sépare correctement responsabilités et données ;
-   gère les anomalies sans planter ;
-   permet de modifier facilement les paramètres ;
-   produit des graphiques cohérents ;
-   montre une stabilisation démographique interprétable ;
-   possède des tests pertinents ;
-   présente une bonne analyse algorithmique.

### Satisfaisant

Le programme fonctionne globalement mais présente :

-   quelques duplications de code ;
-   une architecture perfectible ;
-   des contrôles incomplets ;
-   une analyse limitée.

### Insuffisant

Le programme :

-   ne respecte pas réellement l'héritage demandé ;
-   gère mal le cycle de simulation ;
-   plante sur les données dégradées ;
-   ne produit pas de statistiques fiables ;
-   ne permet pas d'observer l'évolution du troupeau.

## 37. Extension --- Plusieurs espèces

Pour aller plus loin, ajouter :

``` text
Animal
 ├── Vache
 ├── Mouton
 └── Chèvre
```

Chaque espèce pourrait avoir :

-   une durée de gestation différente ;
-   une production différente ;
-   un âge de réforme différent ;
-   une probabilité de reproduction différente.

Le Troupeau pourrait alors gérer plusieurs types d'animaux.

## 38. Extension --- Héritage des comportements

Créer une méthode générique :

`produire()`

dans Animal, puis la redéfinir dans :

-   Vache
-   Mouton
-   Chèvre

Cela permettrait d'introduire naturellement la redéfinition de méthode
et le polymorphisme.

## 39. Extension --- Représentation graphique dynamique

Créer une animation montrant l'évolution de la pyramide des âges année
après année.

Objectif :

``` text
Année 0
    ↓
Année 1
    ↓
Année 2
    ↓
...
Année 15
```

Cette extension est facultative mais particulièrement intéressante pour
illustrer la notion de simulation.

## 40. Question de synthèse finale

Dans le rapport, expliquer comment les notions suivantes apparaissent
dans le projet :

-   Classe
-   Objet
-   Attribut
-   Méthode
-   Héritage
-   Composition
-   Encapsulation
-   Collection
-   Simulation
-   État
-   Événement
-   Complexité

Pour chacune, donner un exemple concret extrait du programme.

## 41. Résultat attendu

À la fin du projet, l'utilisateur doit pouvoir lancer :

``` bash
python main.py
```

puis charger le fichier initial et obtenir une simulation telle que :

``` text
Année 0
Effectif : 19
Âge moyen : 6.1 ans
Production : ...
```

``` text
Année 5
Effectif : ...
Âge moyen : ...
Production : ...
```

``` text
Année 10
Effectif : ...
Âge moyen : ...
Production : ...
```

``` text
Année 15
Effectif : ...
Âge moyen : ...
Production : ...
```

Les valeurs numériques exactes peuvent varier puisque la reproduction,
les réformes et éventuellement la production utilisent des paramètres
probabilistes.

L'objectif n'est donc pas d'obtenir une valeur unique, mais de
construire un modèle cohérent et d'observer que, pour un jeu de
paramètres raisonnable, la structure démographique du troupeau tend vers
un régime relativement stable après plusieurs années de simulation.

## 42. Point d'attention scientifique

Ce projet est un modèle informatique simplifié et non un modèle
zootechnique validé.

Les paramètres relatifs à la reproduction, à la lactation, à la réforme
et à la mortalité sont volontairement simplifiés pour mettre l'accent
sur les concepts de programmation.

Les étudiants doivent distinguer :

-   ce qui est imposé par l'énoncé ;
-   ce qui est une hypothèse de modélisation ;
-   ce qui serait nécessaire dans un modèle d'élevage réaliste.

Cette distinction fait partie de l'évaluation.
