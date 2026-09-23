# Diagramme UML de la simulation

```mermaid
classDiagram
    direction TB

    class plante {
        +NOURRITURE: int = 12
        +pos: tuple
        +nourriture: float
        +vivant: bool
        +__init__(pos)
        +mort()
    }

    class animale {
        <<classe de base>>
        +COUT_DEP: float
        +AGE_MATURE: int
        +AGE_VIEU: int
        +ESPERANCE: int
        +SENES_K: float
        +SENES_P: float
        +COUT_JEUNE: float
        +REPRO_AGE: int
        +REPRO_SEUIL: float
        +REPRO_GARDE: float
        +REPRO_PART: float
        +REPRO_PAUSE: int
        +SUCCES_CHASSE: float
        +PART_CORPS: float
        +pos: tuple
        +espece: str
        +vitesse: int
        +vision: int
        +rmax: float
        +nourriture: float
        +trepro: int
        +age: int
        +vivant: bool
        +__init__(pos, espece, vitesse, vision, rmax, nourriture)
        +facteur_age() float
        +deplacement(cibles)
        +manger(cible)
        +mort()
        +repro() animale
    }

    class herbivore {
        <<sous-classe>>
        +NOURRITURE_INIT: float = 0.4
        +__init__(pos, espece, vitesse, vision, rmax, nourriture)
        +action(plante_list) animale
    }

    class carnivore {
        <<sous-classe>>
        +NOURRITURE_INIT: float = 0.8
        +__init__(pos, espece, vitesse, vision, rmax, nourriture)
        +action(herbivore_list) animale
    }

    class FonctionsSimulation {
        <<fonctions globales>>
        +initialisation(nplante, nherbivore, ncarnivore)
        +Simulation(plante_list, herbivore_list, carnivore_list)
        +run_simulation(...)
        +repousse_plantes(plante_list, plante_max, taux_repousse)
        +dep_age(...)
        +proportion_reserve_proie(r_proie, r)
    }

    class Dashboard {
        <<interface graphique>>
        +lancer_dashboard(history)
        +maj_affichage(jour)
        +toggle_play(event)
        +step_prev(event)
        +step_next(event)
        +on_slide(val)
    }

    animale <|-- herbivore : herite
    animale <|-- carnivore : herite

    FonctionsSimulation ..> plante : cree / filtre
    FonctionsSimulation ..> herbivore : cree / simule
    FonctionsSimulation ..> carnivore : cree / simule
    FonctionsSimulation ..> animale : utilise les comportements

    herbivore ..> plante : chasse / mange
    carnivore ..> herbivore : chasse / mange
    animale ..> plante : cible possible
    animale ..> animale : se reproduit

    Dashboard ..> FonctionsSimulation : affiche history
    Dashboard ..> plante : affiche positions
    Dashboard ..> herbivore : affiche positions, ages, reserves
    Dashboard ..> carnivore : affiche positions, ages, reserves
```

## Relations principales

- `herbivore` et `carnivore` heritent de `animale`.
- Un `herbivore` se deplace vers des `plante` et peut les manger.
- Un `carnivore` se deplace vers des `herbivore` et peut les manger.
- `animale.repro()` cree un nouvel objet du meme type que le parent.
- Les fonctions globales gerent l'initialisation, un jour de simulation, la repousse des plantes et l'historique.
- `Dashboard` lit l'historique produit par `run_simulation()` pour afficher la simulation.
