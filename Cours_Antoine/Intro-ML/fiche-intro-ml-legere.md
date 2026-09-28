# 📘 Introduction au Machine Learning

*Cours d'Antoine Cornuéjols — AgroParisTech, IODAA*

Résumé théorique uniquement : pas d'historique/dates, pas de mini-simulateurs. Format pensé pour la relecture rapide avant examen.

---

## Sommaire

- [1. Pourquoi le machine learning ?](#1-pourquoi-le-machine-learning-)
- [2. Trois grandes catégories de tâches](#2-trois-grandes-catégories-de-tâches)
- [3. Les grands types d'apprentissage](#3-les-grands-types-dapprentissage)
- [4. Vocabulaire des données](#4-vocabulaire-des-données)
- [5. Le problème de l'induction](#5-le-problème-de-linduction)
- [6. Le biais : pourquoi, et quels types](#6-le-biais--pourquoi-et-quels-types)
- [7. Le théorème No Free Lunch](#7-le-théorème-no-free-lunch)
- [8. Les trois ingrédients de l'apprentissage](#8-les-trois-ingrédients-de-lapprentissage)
- [9. Sous-apprentissage et sur-apprentissage](#9-sous-apprentissage-et-sur-apprentissage)
- [10. Le critère inductif : perte, risque, ERM](#10-le-critère-inductif--perte-risque-erm)
- [11. PAC learning : justifier l'ERM](#11-pac-learning--justifier-lerm)
- [12. Généraliser / spécialiser une hypothèse](#12-généraliser--spécialiser-une-hypothèse)
- [13. L'espace des versions (S-set, G-set)](#13-lespace-des-versions-s-set-g-set)
- [🚩 Pièges à éviter](#-pièges-à-éviter)

---

## 1. Pourquoi le machine learning ?

Certains problèmes ont une solution simple par un modèle explicite : prédire la météo de demain par « il fera comme aujourd'hui » est déjà un très bon modèle, sans aucun apprentissage. Mais pour reconnaître un objet dans une image ou un mot dans un signal audio, on ne sait pas écrire directement la règle : nos propres critères seraient biaisés par notre façon de percevoir, qui ne correspond pas à celle d'une machine.

> 💡 **Idée clé.** Au lieu de coder la règle, on donne à la machine des paires **(entrée, sortie)** et on lui demande de trouver seule le calcul qui va de l'une à l'autre. Cela demande beaucoup de données et de calcul, et soulève une nouvelle question : *comment évaluer ce qu'elle a vraiment appris ?*

## 2. Trois grandes catégories de tâches

| Catégorie | Principe | Exemples |
|---|---|---|
| **Reconnaissance / prédiction** | Associer une étiquette ou une valeur à une donnée | Reconnaître un objet (base des CAPTCHA) · molécules bio-actives contre le cancer · prédiction de séries temporelles |
| **IA générative** | Produire de nouveaux objets | **AlphaFold** (structure 3D d'une protéine à partir de sa séquence) · **ITHACA** (compléter des textes anciens lacunaires) |
| **IA agentique** | Agents partiellement autonomes, agissant sur leur environnement | Aide au code / débogage · découverte scientifique · enjeu actuel : apprendre à *raisonner* |

### Limites : robustesse et exemples adverses

Un modèle n'apprend que ce que ses données lui montrent — rien de plus.

- **Apprentissage adverse.** On peut fabriquer des perturbations invisibles pour un humain (texte invisible, quelques pixels modifiés) qui font dérailler complètement la prédiction d'un modèle.
- **Situations jamais rencontrées.** Un modèle entraîné à reconnaître des sportifs sautant en parachute n'a jamais vu de personne âgée le faire ; face à ce cas, il peut conclure à tort à un « jeune athlète », faute d'avoir observé cette variabilité.
- **Illustration (renforcement à deux agents).** Un « tireur » et un « gardien » s'entraînent l'un contre l'autre et deviennent très bons ensemble. Si on retire ensuite le gardien entraîné pour un gardien immobile (une situation bien plus simple), le tireur devient incompétent : il n'a jamais rencontré ce cas et ne sait plus s'adapter, alors que marquer est devenu plus facile. L'IA n'a pas « compris » la tâche au sens large — elle a calé son comportement sur celui, précis, de son adversaire d'entraînement.

> 🚩 Il n'existe pas de méthode uniformément parfaite : tout modèle porte un biais (§6).

## 3. Les grands types d'apprentissage

Objectifs génériques : mieux **comprendre**, **prédire**, **prescrire** (agir).

### Descriptif (non supervisé)
Identifier des régularités sans étiquettes : **clustering** (grouper des échantillons) ou **motifs fréquents** (ex. : lait + œufs ⇒ farine, souvent achetée ensuite).

> ⚠️ **Le vrai problème : l'évaluation.** Le résultat dépend de ce qu'on *cherche*, pas de la réalité — demander 4 clusters en renvoie 4, même sans raison. Un expert peut juger, mais il a tendance à *inventer* une explication a posteriori, et il n'y a pas de vérité connue à comparer en exploration pure.

### Prédictif (supervisé)
Un échantillon de couples $(x, y)$ ⇒ trouver la fonction qui prédit $y$ à partir de $x$. Discrimination sur cas discrets (classification) ou continus (régression). Problème central : comment filtrer les données pour repérer les plus informatives ?

### Prescriptif (pour intervenir)
Notion clé : la **causalité**.

> **Corrélation ne donne pas causalité.** Le beau temps et un baromètre haut sont corrélés, mais c'est la pression atmosphérique qui influence les deux — ni l'un ni l'autre ne « cause » l'autre.

Problème pratique : il faut souvent agir sans connaître (ni pouvoir connaître) les vraies relations causales.

### Par renforcement
Boucle **perception → action → récompense**, objectif : maximiser le gain cumulé.

- **Attribution du crédit** : une récompense ponctuelle ne dit pas quelle action passée, dans une longue séquence, en est responsable.
- Deux agents dont les actions s'influencent mutuellement peuvent s'entraîner en auto-jeu (voir l'exemple tireur/gardien du §2, qui montre aussi la limite de robustesse de cette approche).

## 4. Vocabulaire des données

| Terme | Synonymes | Rôle |
|---|---|---|
| **Exemple** | Échantillon, instance | Une ligne du jeu de données |
| **Descripteur** | Attribut, *feature* | Une colonne d'entrée — les $X$ |
| **Étiquette** | Classe, cible, *label* | La colonne à prédire — les $Y$ |

## 5. Le problème de l'induction

En supervisé, l'objectif est de tester le modèle sur un individu **jamais observé** — c'est la mesure de sa robustesse.

**Difficulté fondamentale.** La grande majorité des fonctions reliant $X$ à $Y$ ne sont pas compressibles en une règle courte : les décrire exactement demanderait d'être exhaustif sur *tous* les exemples possibles.

> 💡 **Solution (nécessairement incomplète) : restreindre l'espace des hypothèses.** Si l'on sait qu'un gène ne dépasse jamais $x$ paires de bases, ou que la couleur des yeux ne dépend que des chromosomes 2, 7 et 9, on peut chercher dans un espace bien plus petit.

Se mettre ainsi des œillères est nécessaire pour apprendre avec un temps et une quantité de données raisonnables — **mais** ce biais doit être **aligné avec la vérité** : si l'on suppose 150 paires de bases alors que le gène en fait réellement 200, on ne le trouvera jamais, quelle que soit la quantité de données.

## 6. Le biais : pourquoi, et quels types

> **Un biais** est ce qui restreint l'univers des hypothèses envisagées, c'est-à-dire ce qui fait préférer certaines hypothèses à d'autres. Un biais est **nécessaire** : sans lui, aucune généralisation n'est possible (§7, No Free Lunch).

| Type | Nature | Description |
|---|---|---|
| **De représentation** (déclaratif) | Restreint l'espace $\mathcal H$ | On choisit un sous-ensemble de l'univers des hypothèses, en admettant que les hypothèses exclues sont impossibles ou très improbables |
| **De recherche** (procédural) | Restreint l'*exploration* de $\mathcal H$ | On cherche (ex. par une méthode de type gradient) une hypothèse de performance optimale dans l'espace autorisé — sans garantie d'unicité de la solution trouvée |
| **De cursus** | Restreint l'*ordre* de présentation | Biais dû à l'ordre dans lequel les exemples sont vus. Analogie scolaire : apprendre d'abord l'addition puis la soustraction façonne durablement notre façon de penser les mathématiques ensuite |

## 7. Le théorème No Free Lunch

> **Aucune méthode d'induction n'est supérieure à une autre — même une prédiction au hasard — en moyenne sur l'ensemble de *tous* les problèmes possibles.**

Ce résultat tient précisément parce qu'on mélange tous les types de problèmes, sans aucun biais qui privilégierait une catégorie.

- Sur **une catégorie de problèmes**, avec un biais adapté, certains modèles deviennent effectivement meilleurs — mais ce résultat n'est **pas généralisable** ailleurs.
- Il faut donc toujours préciser sur quel type de problème un algorithme fonctionne, et sur quel type il ne fonctionne pas.
- Corollaire : on **ne peut pas apprendre le biais lui-même** de façon universelle — il doit venir du concepteur, pas des seules données.

## 8. Les trois ingrédients de l'apprentissage

1. **L'espace des hypothèses $\mathcal H$** — quelle famille de fonctions est admise ?
2. **Le critère inductif** — comment évaluer chaque $h$ à partir de l'échantillon $S$ ? (§10)
3. **La méthode d'exploration de $\mathcal H$** — comment trouver une bonne hypothèse ?

## 9. Sous-apprentissage et sur-apprentissage

Directement liés au choix du biais et à la richesse de $\mathcal H$ par rapport aux données disponibles.

| | Symptôme | Cause |
|---|---|---|
| **Sur-apprentissage** | Le modèle colle trop aux données d'apprentissage ; il change beaucoup si l'on modifie légèrement ces données | $\mathcal H$ trop riche par rapport aux données |
| **Sous-apprentissage** | Le modèle ne capture pas assez les variations réelles (ex. : modèle linéaire pour une relation quadratique) | $\mathcal H$ trop pauvre |

## 10. Le critère inductif : perte, risque, ERM

**Fonction de perte**, pour une hypothèse $h$ et un exemple $(x, y)$ :

$$
l\big(h(x),\, y\big)
$$

Choix courants : l'erreur quadratique, ou l'indicatrice (1 si mal classé, 0 sinon).

> ⚠️ La perte n'est pas forcément symétrique : en médecine, on préfère souvent un faux positif à un faux négatif (une fausse alerte plutôt qu'un diagnostic manqué).

**Risque réel** (espérance du coût si l'on choisit $h$) :

$$
R(h) = \iint l\big(h(x), y\big)\; P(x,y)\; dx\,dy
$$

L'hypothèse théoriquement optimale serait $h^{*} = \arg\min_{h \in \mathcal H} R(h)$ — mais $R(h)$ **n'est pas calculable** : la distribution jointe $P(x,y)$ est inconnue.

**Risque empirique**, calculé sur l'échantillon d'apprentissage de taille $m$ :

$$
\hat R(h) = \frac{1}{m} \sum_{i=1}^{m} l\big(h(x_i),\, y_i\big)
$$

**Principe ERM** (*Empirical Risk Minimization*) — on retient l'hypothèse qui minimise le risque empirique :

$$
\hat h = \arg\min_{h \in \mathcal H} \hat R(h)
$$

> 💡 **La question centrale du principe inductif.** Ce principe est-il « sain » ? On ne peut pas vérifier directement ces deux questions (on ne connaît pas $R$, seulement $\hat R$) :
> - $\hat h$ est-elle bonne relativement au risque réel ? (a-t-on $\hat R(\hat h) \approx R(\hat h)$ ?)
> - Aurait-on pu faire beaucoup mieux ? (a-t-on $R(h^{*}) \approx R(\hat h)$ ?)
>
> C'est à ces deux questions que répond l'analyse PAC (§11).

## 11. PAC learning : justifier l'ERM

Le résultat central du cadre **PAC** (*Probablement Approximativement Correct*) borne l'écart entre risque réel et risque empirique :

$$
\forall\, h \in \mathcal H,\ \forall\, \delta \le 1 :\qquad
\mathbb P^{m}\Big[\, R_{\text{réel}}(h) \;\le\; R_{\text{emp}}(h) + \varepsilon \,\Big] \;>\; 1-\delta
$$

$$
\varepsilon = \frac{\log|\mathcal H| + \log\dfrac{1}{\delta}}{m}
$$

- $m$ : nombre d'exemples d'apprentissage.
- $|\mathcal H|$ : taille (cardinal) de l'espace des hypothèses.
- $\delta$ : le risque d'erreur toléré sur la garantie elle-même (« probablement » : avec probabilité $> 1-\delta$).
- $\varepsilon$ : l'écart maximal toléré entre risque réel et risque empirique (« approximativement » correct, à $\varepsilon$ près).

> 🔑 **Conclusion du cours.** *Le principe de minimisation du risque empirique n'est justifié que s'il existe des contraintes sur l'espace des hypothèses $\mathcal H$.* Plus $|\mathcal H|$ est grand, plus $\varepsilon$ doit être grand (à $m$ et $\delta$ fixés) pour garder la même confiance : un espace trop riche dégrade la garantie théorique — cela rejoint directement la nécessité d'un biais (§6) et le risque de sur-apprentissage (§9).

## 12. Généraliser / spécialiser une hypothèse

Pour prédire face à un problème d'induction, une solution simple est la méthode des **plus proches voisins** (nécessite une notion de distance). Une autre approche fait évoluer une hypothèse par petites étapes :

- **Augmenter la couverture = généraliser** (réduire le nombre de contraintes) → plus d'exemples valident l'hypothèse.
- **Réduire la couverture = spécialiser** (ajouter des contraintes) → moins d'exemples valident l'hypothèse.

> 💡 Différence fondamentale avec l'apprentissage par gradient (réseaux de neurones) : ici, pas de descente continue dans un espace de paramètres — on applique des **opérateurs discrets** dans l'espace des hypothèses, en restreignant la recherche aux exemples effectivement rencontrés (explorer tout $\mathcal H$ n'est pas efficace).

**Opérateurs de généralisation** (la spécialisation applique l'inverse) :

| Opérateur | Exemple |
|---|---|
| Supprimer une conjonction | `A ∧ B → C`  devient  `A → C` |
| Ajouter une alternative | `A → C`  devient  `A ∨ B → C` |
| Étendre le domaine d'un descripteur | `rouge`  devient  `rouge ∨ bleu` |
| Monter dans une hiérarchie de descripteurs | `chlore, brome`  deviennent  `halogène` |

## 13. L'espace des versions (S-set, G-set)

Structure compacte représentant **toutes** les hypothèses cohérentes avec les exemples vus, sans avoir à les énumérer.

| Élément | Définition |
|---|---|
| **S-set** | Hypothèses cohérentes **maximalement spécifiques** — les plus restrictives sans exclure de positif (borne inférieure du treillis) |
| **G-set** | Hypothèses cohérentes **maximalement générales** — les plus larges sans couvrir de négatif (borne supérieure du treillis) |
| **Espace des versions** | Toutes les $h \in \mathcal H$ « entre » S et G, i.e. de risque empirique nul |

L'algorithme met à jour S et G à chaque nouvel exemple (opérateurs du §12), jusqu'à convergence idéale vers une hypothèse unique.

> 🚩 **Fragile au bruit** : un seul exemple mal étiqueté peut faire disparaître la bonne hypothèse de l'espace des versions.

### Exercice travaillé en cours (golf)

Six descripteurs pour décrire une journée (« vais-je jouer au golf ? ») : Ciel (3 valeurs), Température, Humidité, Vent, Eau, Prévision (2 valeurs chacun).

- Exemples possibles : $3 \times 2^{5} = 96$.
- Fonctions possibles (classes $+/-$) : $2^{96}$.
- Hypothèses admises (conjonctions, `?` = indifférent, + l'hypothèse vide) : $4 \times 3^{5} + 1 = 972$.

| # | Exemple ⟨ciel, temp., humid., vent, eau, prév.⟩ | Classe | S (spécifique) | G (générale) |
|---|---|:---:|---|---|
| 1 | soleil, chaud, normale, fort, chaude, égale | **+** | { ⟨soleil,chaud,normale,fort,chaude,égale⟩ } | { ⟨?,?,?,?,?,?⟩ } |
| 2 | soleil, chaud, élevée, fort, chaude, égale | **+** | { ⟨soleil,chaud,**?**,fort,chaude,égale⟩ } | inchangé |
| 3 | pluie, froid, élevée, fort, chaude, change | **−** | inchangé | { ⟨soleil,?,?,?,?,?⟩, ⟨?,chaud,?,?,?,?⟩, ⟨?,?,?,?,?,égale⟩ } |
| 4 | soleil, chaud, élevée, fort, fraîche, change | **+** | { ⟨soleil,chaud,**?**,fort,**?**,**?**⟩ } | { ⟨soleil,?,?,?,?,?⟩, ⟨?,chaud,?,?,?,?⟩ } *(⟨?,?,?,?,?,égale⟩ éliminée : ne couvre plus l'ex. 4)* |

Lecture des mises à jour :
- Un exemple **positif** généralise S au minimum nécessaire pour le couvrir, et élimine de G tout ce qui ne le couvre pas.
- Un exemple **négatif** spécialise G au minimum nécessaire pour l'exclure, et élimine de S tout ce qui le couvre encore.

---

## 🚩 Pièges à éviter

- **Non supervisé ≠ pas de biais** : le nombre de clusters demandé influence directement le résultat, indépendamment de toute « vérité ».
- **Corrélation ≠ causalité** : ne jamais confondre les deux dans un cadre prescriptif.
- **No Free Lunch** : un algorithme meilleur sur *ta* catégorie de problèmes ne l'est pas nécessairement ailleurs — ce n'est pas une contradiction du théorème.
- $R(h)$ **n'est jamais calculable directement** : on travaille toujours avec $\hat R(h)$ ; PAC learning quantifie l'écart entre les deux.
- Ne pas confondre **risque empirique nul** (aucune erreur sur les exemples vus) et **bonne généralisation** — tout l'enjeu du sur-apprentissage et de l'analyse PAC.
- Dans l'espace des versions : **S = borne spécifique / G = borne générale**, pas l'inverse.
- L'algorithme de l'espace des versions est **fragile au bruit** : un seul exemple mal étiqueté peut effondrer S et G.
- Un exemple **positif** touche **G** (on retire ce qui ne le couvre pas) et **généralise S** ; un exemple **négatif** touche **S** (on retire ce qui le couvre) et **spécialise G** — le sens inverse est une erreur fréquente.
