# 📘 Fiche de révision — Conformal prediction

> Cours d'Antoine Cornuéjols (AgroParisTech – INRAE, MIA Paris-Saclay) · 24 diapos · complété par tes notes (`4_conf.txt`)
>
> **Légende des encadrés** : 💡 idée clé · ⚠️ attention · 🚩 piège fréquent · 🔎 complément (absent du cours) · 📝 Tes notes

---

## Sommaire

1. [Le problème de la confiance](#1-le-problème-de-la-confiance)
2. [Les ensembles profonds](#2-les-ensembles-profonds)
3. [Objectif et garantie de couverture](#3-objectif-et-garantie-de-couverture)
4. [Idée générale et jeu de calibration](#4-idée-générale-et-jeu-de-calibration)
5. [Algorithme et formules](#5-algorithme-et-formules)
6. [Exemples travaillés](#6-exemples-travaillés)
7. [Implémentation Python](#7-implémentation-python)
8. [Conditions et message à retenir](#8-conditions-et-message-à-retenir)
9. [Pièges à éviter](#9-pièges-à-éviter)
10. [Quiz auto-test](#10-quiz-auto-test)
11. [Corrigé du quiz](#11-corrigé-du-quiz)

---

## 1. Le problème de la confiance

### 1.1 Question centrale (diapo 2)

> **Comment évaluer la confiance dans _une_ prédiction faite par un modèle ?**

### 1.2 Tâche supervisée typique (diapo 3)

| Élément | Contenu |
|---|---|
| Entrée $x$ | images IRM |
| Sortie $y$ | $\{\text{normal}, \text{cancer}\}$ |
| Approche usuelle | 1) obtenir un **jeu d'entraînement** d'IRM annotées ; 2) **apprendre** un classifieur (ex. réseau de neurones) ; 3) **évaluer l'accuracy** sur le jeu de test (ex. 90 %) |

### 1.3 Pourquoi 90 % d'accuracy ne suffit pas (diapo 4)

> 💡 L'accuracy est une **moyenne sur le jeu de test**. Elle ne dit **rien** sur la **fiabilité / confiance** pour l'entrée **courante** (pas encore vue). Le décideur (le médecin) a besoin de connaître la vraisemblance des issues alternatives, ou de pouvoir écarter les issues improbables : une prédiction ponctuelle ne suffit pas.

### 1.4 La sortie softmax comme « confiance » (diapo 5)

Habituellement, la sortie du classifieur (ex. softmax d'un réseau de neurones) est prise pour la **confiance** de la prédiction.

Hypothèse : $\mathbf z \in \mathbb R^K$ (vecteur de scores bruts) ; $K$ classes.

$$\sigma(\mathbf z)_j \;=\; \frac{e^{z_j}}{\sum_{k=1}^{K} e^{z_k}} \qquad \forall j \in \{1,\dots,K\}$$

- $\sigma(\mathbf z)_j$ : « vraisemblance » prédite pour la classe $j$ (dans $]0,1[$, somme égale à 1) ;
- $z_j$ : score brut (logit) de la classe $j$ — 🔎 terme non défini sur la diapo ;
- $K$ : nombre de classes ; $k$ : indice de sommation.

**Mais ça échoue souvent lamentablement** : les vraisemblances softmax sont en général **mal calibrées** : elles ne reflètent pas la **vraie probabilité** de classification correcte pour l'entrée donnée.

| Image | Prédiction | Confiance affichée |
|---|---|---|
| photo de panda | « panda » | 57,7 % |
| panda $+\,0{,}007 \times$ bruit (imperceptible) | « gibbon » | **99,3 %** |

(exemple d'exemples adverses, Goodfellow et al.)

> ⚠️ Le bruit est quasi invisible, pourtant la prédiction change de classe **avec une confiance quasi maximale**. Une softmax élevée peut donc être **élevée et fausse**.

> 🔎 **Complément — calibration.** Un modèle est **bien calibré** si, parmi les prédictions faites avec une confiance $p$, une proportion $p$ est correcte :
> $$\mathbb P\big(Y = \hat y \;\big|\; \hat p = p\big) = p \qquad \forall p \in [0,1]$$
> - $\hat y$ : classe prédite ; $\hat p$ : confiance associée à cette prédiction ; $Y$ : vraie classe.
> Les réseaux profonds sont souvent **sur-confiants** (confiance > précision réelle).

### 1.5 📝 Tes notes (exemple médecine)

> 📝 **Tes notes** — Pour utiliser l'IA en médecine, il ne faut pas dire « pas cancer » alors que c'est un cancer. Idée : sortir des probabilités ; si 100 % « pas cancer » → ok, si < 90 % → un expert regarde. Mais un modèle peut se tromper avec une certitude de 95 % → on ne peut pas l'utiliser tel quel. Solution : plusieurs modèles différents (pour éviter les erreurs typiques de chaque modèle) et consensus, mais très cher et toujours pas de garantie de réponse correcte. **Question : quel type de garantie, et comment l'obtenir ?**

**Lien avec les diapos :**

| Tes notes | Diapo | Commentaire |
|---|---|---|
| « sorties en proba » | 5 | = softmax pris comme confiance |
| « certitude de 95 % mais faux » | 5 | exemple panda → gibbon (99,3 %) |
| « plusieurs modèles, consensus » | 6 | = **deep ensembles** |
| « très cher, pas de garantie » | 6 | encadré : *no correctness guarantees* + *computationally expensive* |
| « quel type de garantie ? » | 7–24 | réponse du cours : **garantie de couverture** $\mathbb P(y \in C(x)) \ge 1-\alpha$ (section 3) |

> ⚠️ **Corrections / précisions sur tes notes**
> - « Si 100 % pas cancer, ok » est **trop optimiste** : même une sortie à 100 % n'est pas une probabilité calibrée (cf. gibbon à 99,3 %). Un modèle peut afficher 100 % et avoir tort.
> - Le seuil « < 90 % → expert » est une **règle ad hoc sur la softmax** : il ne garantit **aucun taux d'erreur chiffré**. C'est justement ce que la conformal prediction apporte (seuil *calibré* sur des données).
> - « Modèles différents » : dans la diapo 6, ce sont des réseaux entraînés sur des **sous-ensembles aléatoires** des données, ou sur les mêmes données avec des **poids initiaux aléatoires différents** (pas forcément des architectures différentes). L'idée de diversité est la même.
> - 🔎 « Dire pas cancer alors que si » = un **faux négatif** : l'erreur la plus coûteuse en médecine. Le cadre conformal permet de contrôler la probabilité que **la vraie classe soit dans l'ensemble proposé** (donc de limiter ce type d'erreur en moyenne).

---

## 2. Les ensembles profonds

**Deep ensembles** (diapo 6) — tentative de **quantification d'incertitude** :

1. **Entraîner plusieurs réseaux** sur des sous-ensembles aléatoires des données (ou sur les mêmes données en partant de poids initiaux aléatoires différents) ;
2. Utiliser la **distribution prédictive** sur l'entrée induite par ces réseaux (ex. leur consensus ou leur désaccord).

| Avantage | Limites (encadré de la diapo) |
|---|---|
| Donne une idée de l'incertitude (désaccord entre réseaux) | **Aucune garantie de correction** ; **coûteux en calcul** (il faut entraîner et exécuter plusieurs réseaux) |

> 🔎 Tous les réseaux peuvent se tromper **de la même façon** (même biais de données) : consensus ≠ vérité. D'où le besoin d'une méthode avec **garantie**.

---

## 3. Objectif et garantie de couverture

### 3.1 Ce que l'on voudrait (diapo 7)

Au lieu d'une seule classe, produire un **ensemble de prédiction** $\mathcal C(x_{\text{test}})$ (ensemble d'étiquettes possibles) tel que :

Hypothèses : $Z \cup \{(x_{\text{test}}, y_{\text{test}})\}$ échangeable ; $\alpha \in [0,1]$ fixé par l'utilisateur.

$$\mathbb P\big(y_{\text{test}} \in \mathcal C(x_{\text{test}})\big) \;\ge\; 1-\alpha$$

- $\mathcal C(x_{\text{test}})$ : ensemble de prédiction (sous-ensemble des classes) pour l'entrée $x_{\text{test}}$ ;
- $y_{\text{test}}$ : vraie étiquette (inconnue au moment de la prédiction) ;
- $\alpha$ : **taux d'erreur** choisi par l'utilisateur (ex. 0,1) ; $1-\alpha$ : **couverture visée** (ex. 90 %) ;
- $\mathbb P$ : probabilité prise sur l'aléa du **jeu de calibration ET du point de test** (c'est ce qu'on appelle **couverture marginale**).

> 💡 **Idée clé** : on ne donne plus « une réponse + une confiance douteuse », mais **un ensemble dont la probabilité de contenir la bonne réponse est garantie**. **La taille de l'ensemble mesure l'incertitude** : petit = sûr ; grand = incertain.

### 3.2 Exemple ImageNet — classe « fox squirrel » (diapo 7)

Trois images de la classe *fox squirrel*, de plus en plus difficiles ; ensembles générés par la conformal prediction (scores softmax entre parenthèses) :

| Difficulté | Ensemble $\mathcal C(x_{\text{test}})$ |
|---|---|
| Facile | {fox squirrel (0,99)} → ensemble **singleton** |
| Moyenne | {fox squirrel (0,82), gray fox (0,03), bucket (0,02), rain barrel (0,02)} |
| Difficile | {marmot (0,30), fox squirrel (0,22), mink (0,18), weasel (0,16), beaver (0,03), polecat (0,01)} → la vraie classe n'est **plus la plus probable**, mais elle est **dans l'ensemble** |

> 💡 Plus l'image est ambiguë, plus l'ensemble grandit : l'ensemble **s'adapte à la difficulté de l'entrée courante**.

### 3.3 Définition générale (texte de la diapo 7, article de Angelopoulos & Bates)

La **conformal prediction** (aussi appelée *conformal inference*) est une façon simple de générer des **ensembles de prédiction pour n'importe quel modèle**. On part d'un modèle déjà entraîné $\hat f$ (ex. classifieur neuronal), puis on construit les ensembles à l'aide d'une **petite quantité de données de calibration supplémentaires** : c'est l'**étape de calibration**.

---

## 4. Idée générale et jeu de calibration

### 4.1 Comment faire ? (diapo 8)

> 💡 Utiliser la **confiance** qu'avait le système (l'hypothèse apprise) dans les classifications **passées** pour aider à évaluer la **confiance** dans la prédiction pour l'**entrée courante**.

### 4.2 Le jeu de calibration (diapo 9)

1. **Définir une fonction de confiance** $c(\mathbf x, y)$.
   Exemple en classification : soit $h_y(\mathbf x)$ la **vraisemblance prédite** pour la classe $y$ sachant $\mathbf x$ (ex. $\text{Softmax}(\mathbf x, y)$). On prend alors $c(\mathbf x, y) = h_y(\mathbf x)$.
2. **Tirer au hasard $n$ exemples étiquetés** : le jeu de calibration

$$Z = \big\{(\mathbf x_1, y_1), \dots, (\mathbf x_n, y_n)\big\}$$

- $\mathbf x_i$ : entrée du $i$-ème exemple de calibration ; $y_i$ : sa **vraie classe** ;
- $n$ : taille du jeu de calibration.

3. **Calculer les niveaux de confiance de calibration** $c(\mathbf x_1, y_1), \dots, c(\mathbf x_n, y_n)$ (confiance accordée à la **vraie classe**) puis **leurs quantiles** (histogramme de la diapo 10 : axe horizontal « niveau de confiance » de 1 à 0, axe vertical « taille »).

> 🔎 Le jeu de calibration est un jeu **mis de côté (holdout)** : il n'a servi ni à entraîner le modèle, ni à choisir ses hyperparamètres. C'est ce qui rend les scores de calibration représentatifs de ceux d'un futur point de test.

---

## 5. Algorithme et formules

### 5.1 Version « confiance » (diapos 10 à 21)

Idée : on regarde **à quel point le modèle est confiant sur la vraie classe**, en calibration. Pour garantir la couverture $1-\alpha$, on garde dans l'ensemble toutes les classes dont la confiance dépasse un **seuil** $Q_\alpha$ qui est atteint (ou dépassé) par une fraction $\ge 1-\alpha$ des confiances de calibration.

Hypothèses : $c_{(1)} \ge c_{(2)} \ge \dots \ge c_{(n)}$ sont les confiances de calibration $c(\mathbf x_i, y_i)$ triées par ordre **décroissant** ; $\alpha \in\, ]0,1[$ ; $k \le n$.

$$k \;=\; \big\lceil (1-\alpha)\,(n+1) \big\rceil \qquad\qquad Q_\alpha \;=\; c_{(k)} \qquad\qquad \mathcal C(\mathbf x) \;=\; \big\{\, y \;:\; h_y(\mathbf x) \;\ge\; Q_\alpha \,\big\}$$

- $k$ : **rang** retenu (le $k$-ième plus grand score de confiance) ;
- $\lceil\cdot\rceil$ : partie entière supérieure (arrondi **vers le haut**) ;
- $n+1$ : correction de **taille finie** (on compte le point de test en plus des $n$ points) ;
- $Q_\alpha$ : **seuil de confiance** (noté $Q_{0.1}$, $Q_{0.5}$… dans les diapos) ;
- $h_y(\mathbf x)$ : confiance prédite pour la classe $y$ sur la **nouvelle** entrée $\mathbf x$.

**Procédure en pratique :**

1. Calculer la confiance de la **vraie classe** pour chaque exemple de calibration ;
2. Trier par ordre décroissant ;
3. Calculer $k = \lceil (1-\alpha)(n+1)\rceil$ et lire $Q_\alpha$ = $k$-ième valeur ;
4. Pour la nouvelle entrée, **garder toute classe $y$ telle que $h_y(\mathbf x) \ge Q_\alpha$**.

> ⚠️ **Notation des diapos (incohérente)** : sur la diapo 10, $\hat q_\alpha = \dfrac{\lceil (1-\alpha)(n+1) \rceil}{n}$ est un **niveau de quantile** (une fraction entre 0 et 1). Sur les diapos 11 à 21, $\hat q$ désigne le **rang entier** $\lceil (1-\alpha)(n+1) \rceil$ (sans division par $n$), et l'indice de $\hat q$ vaut tantôt $\alpha$, tantôt $1-\alpha$ (ex. diapo 14 : $\alpha = 0{,}9$ mais « $\hat q_{0.1}$ »). Dans cette fiche : **$k$ = rang, $Q_\alpha$ = seuil**.

### 5.2 Version « score de conformité » (diapo 22, article de Angelopoulos & Bates)

Même algorithme, écrit avec un **score d'erreur** $s_i$ (grand = modèle mauvais) :

**Étape 1 — scores de conformité** (sur les données de calibration) :

$$s_i \;=\; 1 - \hat f(X_i)_{Y_i}, \qquad i = 1,\dots,n$$

- $\hat f(X_i)_{Y_i}$ : sortie softmax du modèle pour la **vraie classe** $Y_i$ ; donc $s_i = 1-c_i$ ;
- $s_i$ **élevé** quand la softmax de la vraie classe est **faible**, c'est-à-dire quand le modèle se trompe fortement.

**Étape 2 — quantile ajusté** :

$$\hat q \;=\; \text{quantile de niveau } \frac{\lceil (n+1)(1-\alpha) \rceil}{n} \text{ des scores } s_1,\dots,s_n$$

- $\hat q$ : seuil sur les scores (c'est « presque » le quantile $1-\alpha$, avec la **correction** $(n+1)/n$ de taille finie).

**Étape 3 — ensemble de prédiction** pour un nouveau point ($X_{\text{test}}$ connu, $Y_{\text{test}}$ inconnu) :

$$\mathcal C(X_{\text{test}}) \;=\; \big\{\, y \;:\; \hat f(X_{\text{test}})_y \;\ge\; 1-\hat q \,\big\}$$

- Toutes les classes dont la softmax est **assez élevée** ($\ge 1-\hat q$) entrent dans l'ensemble.

> 💡 **Équivalence 5.1 ↔ 5.2** : $Q_\alpha = 1-\hat q$. Garder $y$ si $h_y(\mathbf x) \ge Q_\alpha$ revient à garder $y$ si son score $1-h_y(\mathbf x) \le \hat q$.

**Garantie** (diapo 7 et article) : **quel que soit le modèle** (même mauvais) et **quelle que soit la distribution inconnue** des données,

$$\mathbb P\big(Y_{\text{test}} \in \mathcal C(X_{\text{test}})\big) \;\ge\; 1-\alpha .$$

> 🔎 **Borne supérieure** (article de référence, si les scores sont presque sûrement distincts) :
> $$1-\alpha \;\le\; \mathbb P\big(Y_{\text{test}} \in \mathcal C(X_{\text{test}})\big) \;\le\; 1-\alpha+\frac{1}{n+1}$$
> La couverture est donc « presque exactement » $1-\alpha$ : pas trop conservatrice si $n$ est grand.

> 🔎 **Pourquoi ça marche (intuition).** Si les $n$ scores de calibration et le score du point de test (celui de sa vraie classe) sont **échangeables**, ce dernier a la **même probabilité d'occuper chacun des $n+1$ rangs**. La probabilité qu'il soit parmi les $k$ plus petits vaut donc $k/(n+1)$ :
> $$\mathbb P\big(s_{\text{test}} \le \hat q\big) \;\ge\; \frac{\lceil (n+1)(1-\alpha)\rceil}{n+1} \;\ge\; 1-\alpha$$
> - $s_{\text{test}} = 1-\hat f(X_{\text{test}})_{Y_{\text{test}}}$ : score de la vraie classe du test ;
> - l'événement $\{s_{\text{test}} \le \hat q\}$ est exactement $\{Y_{\text{test}} \in \mathcal C(X_{\text{test}})\}$ ;
> - le « $+1$ » et le $\lceil\cdot\rceil$ servent à compter le point de test dans le classement.

> 🔎 **Cas des petits $n$.** Si $\lceil (n+1)(1-\alpha)\rceil > n$ (c'est-à-dire $\alpha < \tfrac{1}{n+1}$), aucun score de calibration n'est assez grand : il faut renvoyer **toutes les classes**. Exemple : $n=10$, $\alpha = 0{,}05$ → $\lceil 10{,}45\rceil = 11 > 10$.

> 🔎 **Régression** (le cours dit que la méthode marche aussi en régression, sans détailler). Avec le score $s_i = |y_i - \hat f(x_i)|$ et $\hat q$ défini comme ci-dessus, l'ensemble de prédiction est l'**intervalle** $\big[\hat f(x) - \hat q,\; \hat f(x) + \hat q\big]$.

### 5.3 Effet de $\alpha$

| $\alpha$ | Couverture visée | Seuil $Q_\alpha$ | Ensemble |
|---|---|---|---|
| **petit** (ex. 0,1) | élevée (90 %) | **bas** (rang $k$ grand) | **grand** (parfois toutes les classes) |
| **grand** (ex. 0,9) | faible (10 %) | **haut** (rang $k$ petit) | **petit** (parfois **vide**) |

> 💡 **Compromis** : plus on exige de couverture, plus l'ensemble est gros. Toujours **plus de garantie ⇒ moins de précision de l'ensemble**.

---

## 6. Exemples travaillés

**Cadre commun (diapos 11 à 21)** : classes $\{\text{dog}, \text{tiger}, \text{cat}\}$ ; $n = 10$ exemples de calibration ; on prédit sur une nouvelle entrée avec

$$h(\mathbf x) = (h_{\text{dog}}, h_{\text{tiger}}, h_{\text{cat}}) = (0{,}05;\ 0{,}60;\ 0{,}35)$$

Dans chaque tableau de calibration des diapos, les cases **encadrées en vert** donnent la confiance de la **vraie classe** de chaque image ; la ligne du bas les recopie, triées par ordre décroissant.

> ⚠️ Sur les diapos 11 à 14, certaines vignettes d'images ne semblent pas correspondre à la classe encadrée : se fier aux **encadrés verts** (les vignettes sont illustratives). Quelques colonnes ne somment pas exactement à 1 (ex. diapo 11 colonne 5, diapo 17 colonne 1) : imprécisions sans conséquence sur le raisonnement.

### 6.1 Tableau récapitulatif

| Jeu | Confiance de la vraie classe (décroissante) | $\alpha$ | $k$ | $Q_\alpha$ | $\mathcal C(\mathbf x)$ | Couverture garantie |
|---|---|---|---|---|---|---|
| A (diapos 11–14) | 0,95 · 0,90 · 0,40 · 0,35 · 0,30 · 0,25 · 0,20 · 0,15 · 0,10 · 0,05 | 0,1 | 10 | 0,05 | {dog, tiger, cat} | $\ge 0{,}9$ |
| A | idem | 0,5 | 6 | **0,25** (diapo : 0,30 ⚠️) | {tiger, cat} | $\ge 0{,}5$ |
| A | idem | 0,9 | 2 | 0,90 | ∅ | $\ge 0{,}1$ |
| B (diapos 15–16) | 0,52 · 0,50 · 0,45 · 0,42 · 0,40 · 0,39 · 0,38 · 0,37 · 0,36 · 0,35 | 0,8 | 3 | 0,45 | {tiger} | $\ge 0{,}2$ |
| C (diapo 17) | 0,92 · 0,90 · 0,88 · 0,87 · 0,86 · 0,84 · 0,82 · 0,80 · 0,78 · 0,75 | 0,1 | 10 | 0,75 | ∅ | $\ge 0{,}9$ |
| D (diapos 18–20) | 0,95 · 0,90 · 0,85 · 0,60 · 0,55 · 0,50 · 0,45 · 0,45 · 0,40 · 0,35 | 0,1 | 10 | 0,35 | {tiger, cat} | $\ge 0{,}9$ |
| D | idem | 0,5 | 6 | **0,50** (diapo : 0,55 ⚠️) | {tiger} | $\ge 0{,}5$ |
| E (diapo 21) | 0,95 · 0,90 · 0,85 · 0,85 · 0,80 · 0,75 · 0,70 · 0,65 · 0,60 · 0,55 | 0,1 | 10 | 0,55 | {tiger} | $\ge 0{,}9$ |

> ⚠️ **Deux écarts avec les diapos** (diapos 13 et 20, $\alpha = 0{,}5$) : avec $k=6$, le 6ᵉ plus grand score est **0,25** (jeu A) et **0,50** (jeu D) ; les diapos affichent 0,30 et 0,55 (le 5ᵉ). **L'ensemble final est le même** dans les deux cas, donc l'erreur est sans conséquence ici, mais retiens la règle : **$k$-ième valeur**, $k = \lceil (1-\alpha)(n+1)\rceil$.

Vecteurs de probabilités du jeu A (diapo 11) pour référence — chaque colonne = une image ; **gras** = vraie classe :

| | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $\hat p_{\text{dog}}$ | **0,95** | 0,05 | 0,10 | 0,25 | 0,45 | **0,25** | 0,35 | 0,55 | **0,10** | 0,40 |
| $\hat p_{\text{tiger}}$ | 0,02 | **0,90** | 0,50 | 0,40 | **0,30** | 0,65 | 0,45 | **0,15** | 0,85 | **0,05** |
| $\hat p_{\text{cat}}$ | 0,03 | 0,05 | **0,40** | **0,35** | 0,35 | 0,10 | **0,20** | 0,30 | 0,05 | 0,55 |

### 6.2 Jeu A — modèle moyen (diapos 11 à 14)

- **$\alpha = 0{,}1$** (diapo 12) : $k = \lceil 0{,}9 \times 11 \rceil = \lceil 9{,}9\rceil = 10$ → $Q = $ 10ᵉ valeur $= 0{,}05$. Les trois classes ont $h_y \ge 0{,}05$ → $\mathcal C = \{\text{dog}, \text{tiger}, \text{cat}\}$, couverture $\ge 0{,}9$.
  *Lecture : pour être sûr à 90 %, il faut tout garder, car une image de calibration a donné seulement 0,05 à sa vraie classe.*
- **$\alpha = 0{,}5$** (diapo 13) : $k = \lceil 5{,}5 \rceil = 6$ → $Q = 0{,}25$ → dog (0,05) exclu ; tiger (0,60) et cat (0,35) gardés → $\{\text{tiger}, \text{cat}\}$, couverture $\ge 0{,}5$.
- **$\alpha = 0{,}9$** (diapo 14) : $k = \lceil 1{,}1 \rceil = 2$ → $Q = 0{,}90$ → aucune classe n'atteint 0,90 (max = 0,60) → $\mathcal C = \varnothing$, couverture $\ge 0{,}1$.

### 6.3 Jeu B — modèle hésitant (diapos 15–16)

Confiances de la vraie classe toutes entre 0,35 et 0,52 (le modèle n'est jamais très sûr, même quand il a raison).

- **$\alpha = 0{,}8$** : $k = \lceil 0{,}2 \times 11 \rceil = \lceil 2{,}2 \rceil = 3$ → $Q = 0{,}45$ (3ᵉ valeur) → seul tiger (0,60) passe → $\mathcal C = \{\text{tiger}\}$, couverture $\ge 0{,}2$.

### 6.4 Jeu C — modèle très confiant (diapo 17)

Confiances de la vraie classe entre 0,75 et 0,92.

- **$\alpha = 0{,}1$** : $k = 10$ → $Q = 0{,}75$ ; la meilleure classe de $\mathbf x$ n'a que 0,60 $< 0{,}75$ → $\mathcal C = \varnothing$, couverture $\ge 0{,}9$.

> 💡 **Ensemble vide = signal d'alarme.** Le modèle est bien moins confiant sur $\mathbf x$ que sur les exemples de calibration typiques : $\mathbf x$ est **atypique** (ou le modèle est incertain). En pratique : s'abstenir / passer la main à un expert.

> ⚠️ Un ensemble vide ne contredit pas « couverture $\ge 0{,}9$ » : la garantie est une **moyenne sur les points de test**. Ici $\mathbf x$ fait partie des ≤ 10 % de cas « autorisés à être ratés ».

### 6.5 Jeu D — modèle mixte, calibration triée par classe (diapos 18 à 20)

Les 10 images sont **groupées par vraie classe** : dog (0,95 · 0,90 · 0,85), tiger (0,60 · 0,55 · 0,50 · 0,45), cat (0,45 · 0,40 · 0,35). Le calcul est identique ; seul l'affichage change.

- **$\alpha = 0{,}1$** (diapo 19) : $k = 10$ → $Q = 0{,}35$ → tiger (0,60) et cat (0,35, **inclus car $\ge$**) → $\{\text{tiger}, \text{cat}\}$, couverture $\ge 0{,}9$.
- **$\alpha = 0{,}5$** (diapo 20) : $k = 6$ → $Q = 0{,}50$ → tiger seul → $\{\text{tiger}\}$, couverture $\ge 0{,}5$.

### 6.6 Jeu E — bon modèle (diapo 21)

dog (0,95 · 0,90 · 0,85), tiger (0,85 · 0,80 · 0,75 · 0,70), cat (0,65 · 0,60 · 0,55).

- **$\alpha = 0{,}1$** : $k = 10$ → $Q = 0{,}55$ → cat (0,35) exclu → $\{\text{tiger}\}$, couverture $\ge 0{,}9$.

### 6.7 Ce qu'on retient des exemples

> 💡 1. **Même sortie $h(\mathbf x)$, ensembles différents** : l'ensemble dépend de la **qualité du modèle sur la calibration** (jeux C, D, E à $\alpha=0{,}1$ : $\varnothing$, $\{\text{tiger},\text{cat}\}$, $\{\text{tiger}\}$).
> 2. **Meilleur modèle ⇒ seuil plus haut ⇒ ensemble plus petit** (donc plus informatif), à **garantie identique** ($\ge 0{,}9$).
> 3. **Plus $\alpha$ grand ⇒ ensemble plus petit** (jeu A : 3 classes → 2 → 0).
> 4. La **validité** (couverture) ne dépend pas du modèle ; son **efficacité** (taille de l'ensemble) si.

### 6.8 Histogramme des scores de calibration (diapos 10 et 23)

Diapo 23 : même histogramme que la diapo 10, avec les pourcentages (population par intervalle de confiance, de 1 à 0) et le titre « **Possible ?** » (non expliqué sur la diapo).

| Intervalle de confiance | 1–0,9 | 0,9–0,8 | 0,8–0,7 | 0,7–0,6 | 0,6–0,5 | 0,5–0,4 | 0,4–0,3 | 0,3–0,2 | 0,2–0,1 | 0,1–0 |
|---|---|---|---|---|---|---|---|---|---|---|
| Part des exemples | 11 % | 19 % | 17 % | 11 % | 12 % | 7 % | 6 % | 9 % | 5 % | 3 % |

> 🔎 **Lecture d'un seuil sur l'histogramme.** Pour $\alpha = 0{,}1$, le seuil $Q_\alpha$ est le point sous lequel se trouvent environ 10 % des confiances. En cumulant depuis la gauche (côté 0) : 3 % sous 0,1 ; 8 % sous 0,2 ; 17 % sous 0,3 → le seuil est **entre 0,2 et 0,3**.

---

## 7. Implémentation Python

Code correspondant à l'algorithme 5.2 (diapo 22) ; `calib_X`, `cal_labels` = jeu de calibration, `val_X` = nouveaux points, `alpha` = taux d'erreur :

```python
import numpy as np

# Étape 1 : scores de conformité sur le jeu de calibration
n = len(cal_labels)
cal_probs = model(calib_X).softmax(dim=1).numpy()
cal_scores = 1 - cal_probs[np.arange(n), cal_labels]   # s_i = 1 - proba de la vraie classe

# Étape 2 : quantile ajusté
q_level = np.ceil((n + 1) * (1 - alpha)) / n
qhat = np.quantile(cal_scores, q_level, method="higher")

# Étape 3 : ensembles de prédiction sur de nouveaux points
val_probs = model(val_X).softmax(dim=1).numpy()
prediction_sets = val_probs >= (1 - qhat)               # tableau booléen (points × classes)
```

| Ligne | Rôle |
|---|---|
| `cal_probs[np.arange(n), cal_labels]` | sélectionne, pour chaque exemple, la proba de **sa vraie classe** |
| `q_level` | niveau de quantile **ajusté** $\lceil (n+1)(1-\alpha)\rceil / n$ |
| `method="higher"` | prend une vraie valeur d'échantillon **au-dessus** (choix **conservateur**, sans interpolation) |
| `val_probs >= 1 - qhat` | garde les classes dont la proba dépasse le seuil $1-\hat q$ |

> 🔎 `np.quantile` exige un niveau $\le 1$ : si $\alpha < \tfrac{1}{n+1}$, `q_level > 1` et le code plante ; il faut alors renvoyer toutes les classes (cf. section 5.2).

---

## 8. Conditions et message à retenir

### 8.1 Take-home message (diapo 24)

- Fournit une **mesure d'incertitude pour l'entrée courante** ;
- Fonctionne **avec n'importe quelle distribution** ;
- Fonctionne **avec n'importe quelle taille $n$** du jeu de calibration ;
- Fonctionne **avec n'importe quel modèle prédictif** (classification **ou** régression) qui fournit une **confiance estimée** dans la prédiction ;
- **Sous l'hypothèse** que $Z \cup \{(\mathbf x_{\text{test}}, y_{\text{test}})\}$ est **échangeable**.

> 🔎 **Échangeabilité** : la loi jointe de la suite ne change pas quand on permute les éléments. Pour toute permutation $\pi$ :
> $$\mathbb P\big(Z_{\pi(1)}, \dots, Z_{\pi(n+1)}\big) = \mathbb P\big(Z_1, \dots, Z_{n+1}\big)$$
> - $Z_i = (\mathbf x_i, y_i)$ ; les $n$ points de calibration et le point de test sont traités comme les $n+1$ éléments.
> Des données **i.i.d. sont échangeables**. L'hypothèse est **violée** en cas de dérive de distribution (test ≠ calibration) ou de séries temporelles : la garantie n'est alors plus assurée.

### 8.2 Comparaison des approches

| | Softmax brute | Ensembles profonds | Conformal prediction |
|---|---|---|---|
| Sortie | une classe + un score | une distribution prédictive | un **ensemble** de classes |
| Garantie de correction | **aucune** (mal calibrée) | **aucune** | **oui** : $\mathbb P(y \in \mathcal C(x)) \ge 1-\alpha$ |
| Coût | faible | **élevé** (plusieurs réseaux) | faible (un modèle + un petit jeu de calibration) |
| Dépend du modèle ? | oui | oui | **non** (validité valable pour tout modèle) |
| Hypothèse | — | — | échangeabilité |

---

## 9. Pièges à éviter

> 🚩 **1. Prendre la softmax pour une vraie probabilité.** Elle est mal calibrée : panda → gibbon à 99,3 %.

> 🚩 **2. Confondre accuracy globale et fiabilité de la prédiction courante.** 90 % en test ne dit rien sur *cette* entrée.

> 🚩 **3. Croire que les ensembles de modèles donnent une garantie.** Consensus ≠ garantie, et c'est coûteux.

> 🚩 **4. Lire « $\mathbb P(y \in \mathcal C(x)) \ge 1-\alpha$ » comme vrai pour chaque $x$.** C'est une **couverture marginale** (moyenne sur calibration et test), pas une garantie pour une entrée ou une classe précise.

> 🚩 **5. Oublier le « $+1$ » et le $\lceil\cdot\rceil$.** Utiliser le quantile brut de niveau $1-\alpha$ donne une couverture un peu **trop basse** à $n$ petit.

> 🚩 **6. Inverser les inégalités.** En version confiance : on garde $y$ si $h_y(\mathbf x) \ge Q_\alpha$. En version score ($s = 1-h$) : on garde $y$ si $s \le \hat q$. Ne pas mélanger.

> 🚩 **7. Confondre $\alpha$ et $1-\alpha$.** $\alpha$ = taux d'erreur toléré (0,1) ; $1-\alpha$ = couverture (0,9). Et attention à la notation $\hat q$ des diapos (niveau vs rang, indice $\alpha$ vs $1-\alpha$).

> 🚩 **8. Calibrer sur des données déjà utilisées pour entraîner ou choisir le modèle.** On perd l'échangeabilité, donc la garantie.

> 🚩 **9. Trouver un ensemble vide « bizarre ».** C'est un **signal d'incertitude** (entrée atypique), compatible avec la garantie moyenne.

> 🚩 **10. Penser qu'un modèle faible invalide la méthode.** La couverture reste valable ; seuls les ensembles deviennent **grands** (efficacité dégradée).

> 🚩 **11. Oublier l'hypothèse d'échangeabilité** : si les données de test ne suivent pas la distribution de calibration (dérive), la garantie tombe.

---

## 10. Quiz auto-test

> Réponds **dans ta tête (ou sur papier)** avant de descendre au corrigé. Barème : **40 points** ; ⭐ = question centrale du cours.

**Q1 (1 pt)** — Pourquoi une accuracy de 90 % ne suffit-elle pas pour le médecin ?

**Q2 (2 pts)** — Écris la formule de la softmax. Pourquoi ne peut-on pas la prendre telle quelle comme niveau de confiance ? Quel exemple de la diapo 5 l'illustre ?

**Q3 (1 pt)** — Que signifie « mal calibré » ?

**Q4 (2 pts)** — Principe des ensembles profonds et deux limites.

**Q5 ⭐ (3 pts)** — Écris la garantie visée par la conformal prediction et explique chaque symbole.

**Q6 (2 pts)** — Que contient $\mathcal C(x_{\text{test}})$ ? Que révèle sa taille (exemple *fox squirrel*) ?

**Q7 (2 pts)** — Quelle est l'idée générale (diapo 8) ? Comment le « passé » est-il utilisé ?

**Q8 (2 pts)** — Définis le jeu de calibration $Z$ et la fonction de confiance $c(\mathbf x, y)$ en classification.

**Q9 ⭐ (3 pts)** — Donne la formule du rang $k$ (ou niveau de quantile $\hat q_\alpha$) et explique le « $+1$ » et le $\lceil\cdot\rceil$.

**Q10 ⭐ (3 pts)** — Écris les trois étapes de l'algorithme avec les formules de $s_i$ et de $\mathcal C(X_{\text{test}})$.

**Q11 ⭐ (3 pts)** — Jeu de calibration (confiances de la vraie classe) : 0,95 · 0,90 · 0,40 · 0,35 · 0,30 · 0,25 · 0,20 · 0,15 · 0,10 · 0,05. Avec $h(\mathbf x) = (0{,}05;\,0{,}60;\,0{,}35)$ sur (dog, tiger, cat) et $\alpha = 0{,}5$ : calcule $k$, le seuil et l'ensemble.

**Q12 (2 pts)** — Même jeu et même $\mathbf x$, avec $\alpha = 0{,}9$ : quel ensemble et pourquoi ?

**Q13 (2 pts)** — Avec $\alpha = 0{,}1$ : jeu D (confiances entre 0,35 et 0,95) donne $\{\text{tiger}, \text{cat}\}$ et jeu E (entre 0,55 et 0,95) donne $\{\text{tiger}\}$. Pourquoi ?

**Q14 (2 pts)** — Jeu C ($\alpha = 0{,}1$, confiances entre 0,75 et 0,92) : on obtient $\varnothing$. Comment l'interpréter ? Est-ce contradictoire avec la garantie ?

**Q15 (2 pts)** — Quel est l'effet d'une diminution de $\alpha$ sur le seuil et sur la taille de l'ensemble ?

**Q16 ⭐ (2 pts)** — Que veut dire « couverture marginale » ? La garantie vaut-elle pour chaque entrée $x$ ?

**Q17 ⭐ (3 pts)** — Cite les trois « avec n'importe quel… » du take-home message et l'hypothèse nécessaire. Définis l'échangeabilité.

**Q18 (1 pt)** — Dans le code, que font `method="higher"` et `val_probs >= 1 - qhat` ?

**Q19 (2 pts)** — (Tes notes) Pourquoi un modèle « sûr à 95 % » reste inutilisable tel quel en médecine, et quel type de garantie cherche-t-on ?

---

<br><br><br><br>

⬇️ ⬇️ ⬇️ **Ne descends pas avant d'avoir répondu !** ⬇️ ⬇️ ⬇️

<br><br><br><br><br><br>

---

## 11. Corrigé du quiz

**R1 (1 pt)** — C'est une moyenne sur le jeu de test : elle ne dit rien sur la fiabilité/confiance pour l'entrée **courante** non vue.

**R2 (2 pts)** — $\sigma(\mathbf z)_j = \dfrac{e^{z_j}}{\sum_{k=1}^K e^{z_k}}$ (1 pt). Elle est **mal calibrée** : elle ne reflète pas la vraie probabilité de classification correcte (0,5 pt). Exemple : panda (57,7 %) $+ 0{,}007\times$ bruit → « gibbon » à 99,3 % (0,5 pt).

**R3 (1 pt)** — La confiance affichée ne correspond pas à la fréquence réelle de bonnes réponses (une prédiction à 90 % devrait être juste 90 % du temps).

**R4 (2 pts)** — Entraîner **plusieurs réseaux** (sous-ensembles aléatoires ou poids initiaux différents) et utiliser la **distribution prédictive** induite (1 pt). Limites : **aucune garantie de correction** et **coût de calcul élevé** (1 pt).

**R5 (3 pts)** — $\mathbb P\big(y_{\text{test}} \in \mathcal C(x_{\text{test}})\big) \ge 1-\alpha$ (1 pt). $\mathcal C$ = ensemble de prédiction ; $\alpha$ = taux d'erreur choisi ; $1-\alpha$ = couverture visée (1 pt). La probabilité porte sur l'aléa du jeu de calibration et du point de test, sous échangeabilité (1 pt).

**R6 (2 pts)** — L'ensemble des étiquettes plausibles (1 pt). Sa taille mesure l'incertitude : singleton {fox squirrel (0,99)} si facile ; 4 classes si moyen ; 6 classes, la vraie classe n'étant plus la plus probable, si difficile (1 pt).

**R7 (2 pts)** — Utiliser la confiance des classifications **passées** de l'hypothèse apprise pour évaluer la confiance de la prédiction sur l'entrée courante (1 pt) : on calcule la confiance de la vraie classe sur des exemples de calibration et on en tire un seuil (quantile) (1 pt).

**R8 (2 pts)** — $Z = \{(\mathbf x_1,y_1),\dots,(\mathbf x_n,y_n)\}$ : $n$ exemples étiquetés tirés au hasard, $y_i$ = vraie classe (1 pt). $c(\mathbf x, y) = h_y(\mathbf x)$ : vraisemblance prédite pour la classe $y$ sachant $\mathbf x$ (ex. softmax) (1 pt).

**R9 (3 pts)** — $k = \lceil (1-\alpha)(n+1)\rceil$ (rang) ou $\hat q_\alpha = \lceil (1-\alpha)(n+1)\rceil / n$ (niveau de quantile) (1 pt). Le « $+1$ » compte le point de test avec les $n$ points de calibration (correction de taille finie) (1 pt). Le $\lceil\cdot\rceil$ arrondit **vers le haut** pour rester conservateur et garantir $\ge 1-\alpha$ (1 pt).

**R10 (3 pts)** — (1) $s_i = 1-\hat f(X_i)_{Y_i}$ sur les données de calibration ; (2) $\hat q$ = quantile de niveau $\lceil (n+1)(1-\alpha)\rceil/n$ des $s_i$ ; (3) $\mathcal C(X_{\text{test}}) = \{y : \hat f(X_{\text{test}})_y \ge 1-\hat q\}$ (1 pt par étape).

**R11 (3 pts)** — $k = \lceil 0{,}5 \times 11\rceil = \lceil 5{,}5\rceil = 6$ (1 pt) ; 6ᵉ plus grande confiance $= 0{,}25$ (la diapo affiche 0,30, même résultat) (1 pt) ; dog (0,05) exclu, tiger (0,60) et cat (0,35) gardés → $\mathcal C = \{\text{tiger}, \text{cat}\}$ (1 pt).

**R12 (2 pts)** — $k = \lceil 0{,}1 \times 11\rceil = 2$ → seuil $= 0{,}90$ (1 pt). Aucune classe n'a $h_y \ge 0{,}90$ (max 0,60) → $\mathcal C = \varnothing$, couverture visée seulement $\ge 0{,}1$ (1 pt).

**R13 (2 pts)** — À $\alpha = 0{,}1$, $k = 10$ : le seuil est la **plus petite** confiance de calibration, soit 0,35 (jeu D) et 0,55 (jeu E) (1 pt). Cat (0,35) passe 0,35 mais pas 0,55 : un modèle plus confiant sur ses vraies classes donne un seuil plus haut et un ensemble plus petit, à garantie identique $\ge 0{,}9$ (1 pt).

**R14 (2 pts)** — $\mathbf x$ est atypique : le modèle est beaucoup moins confiant sur $\mathbf x$ (max 0,60) que sur les exemples de calibration (≥ 0,75) → signal d'incertitude / abstention (1 pt). Pas contradictoire : la garantie est une moyenne sur les points de test ; jusqu'à 10 % des cas peuvent être « ratés » (1 pt).

**R15 (2 pts)** — $\alpha$ plus petit → couverture visée plus haute → rang $k$ plus grand → seuil plus **bas** (1 pt) → ensemble plus **grand**, jusqu'à toutes les classes (1 pt).

**R16 (2 pts)** — Probabilité **moyennée** sur l'aléa du jeu de calibration et du point de test (1 pt). **Non** : pas de garantie pour un $x$ ou une classe particuliers (1 pt).

**R17 (3 pts)** — Avec n'importe quelle **distribution**, n'importe quelle **taille $n$**, n'importe quel **modèle** (classification ou régression) fournissant une confiance estimée (1,5 pt). Hypothèse : $Z \cup \{(\mathbf x_{\text{test}}, y_{\text{test}})\}$ **échangeable** (0,5 pt) ; la loi jointe est invariante par permutation des éléments, les données i.i.d. le sont (1 pt).

**R18 (1 pt)** — `method="higher"` : prend une valeur d'échantillon au-dessus (conservateur) ; `val_probs >= 1 - qhat` : garde les classes dont la softmax dépasse le seuil $1-\hat q$ (renvoie un tableau booléen).

**R19 (2 pts)** — Un modèle peut se tromper avec 95 % de certitude (softmax mal calibrée) ; un faux « pas cancer » est trop coûteux (1 pt). On cherche une **garantie de couverture** $\mathbb P(y \in \mathcal C(x)) \ge 1-\alpha$, obtenue par la **calibration conformale** sur un jeu mis de côté (1 pt).

---

**Auto-évaluation** : **≥ 34/40** → maîtrisé · **26–33** → relire sections 5, 6 et 9 · **< 26** → reprendre les sections 3 à 6.
