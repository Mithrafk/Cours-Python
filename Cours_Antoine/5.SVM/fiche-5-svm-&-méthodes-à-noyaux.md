# SVM & méthodes à noyaux — Fiche de révision

**Sommaire**

1. [Le cadre : induction supervisée, risques et critères](#1-le-cadre-induction-supervisée-risques-et-critères)
2. [Garanties PAC, dimension VC et SRM](#2-garanties-pac-dimension-vc-et-srm)
3. [Perceptron à marge maximale : dérivation (primal)](#3-perceptron-à-marge-maximale-dérivation-primal)
4. [Forme duale, KKT et vecteurs supports](#4-forme-duale-kkt-et-vecteurs-supports)
5. [Marges douces et perte hinge](#5-marges-douces-et-perte-hinge)
6. [La marge comme mesure de capacité](#6-la-marge-comme-mesure-de-capacité)
7. [Théorème de Cover et changement de représentation](#7-théorème-de-cover-et-changement-de-représentation)
8. [Le kernel trick](#8-le-kernel-trick)
9. [Fonctions noyaux usuelles et construction](#9-fonctions-noyaux-usuelles-et-construction)
10. [Exemple travaillé : noyau polynomial](#10-exemple-travaillé-noyau-polynomial)
11. [En pratique : hyperparamètres et diagnostic](#11-en-pratique-hyperparamètres-et-diagnostic)
12. [SVR, nouveautés, kernelisation](#12-svr-nouveautés-kernelisation)
13. [Noyaux pour données non vectorielles](#13-noyaux-pour-données-non-vectorielles)
14. [Bilan : forces et limites](#14-bilan-forces-et-limites)
15. [Pièges à éviter](#15-pièges-à-éviter)
16. [Quiz d'auto-test](#16-quiz-dauto-test)

---

## 1. Le cadre : induction supervisée, risques et critères

**Apprentissage supervisé** = apprendre une fonction $X \to Y$ à partir d'un ensemble d'apprentissage :

$$\mathcal{S} = \{(\mathbf{x}_i, y_i)\}_{1 \leq i \leq m}$$

- $m$ : nombre d'exemples ; $\mathbf{x}_i \in \mathcal{X}$ : description ; $y_i \in \mathcal{Y}$ : étiquette
- **Régression** : $Y = \mathbb{R}$ (prix, date de panne, structure météo...)
- **Classification** : $Y$ = ensemble fini (molécule active/inactive, microarray cancer/pas cancer, série temporelle normale/anormale)

> 💡 **La question centrale de l'induction** : on vise la **performance en généralisation**, mais on ne mesure que la **performance en apprentissage**. Parmi toutes les hypothèses qui bien se comportent sur $\mathcal{S}$, **laquelle favoriser ?**

Deux grandeurs :

$$\hat{R}(h) = \frac{1}{m} \sum_{i=1}^{m} \ell(h(\mathbf{x}_i), y_i)$$

- $\hat{R}(h)$ : **risque empirique** (mesurable sur $\mathcal{S}$) ; $\ell$ : fonction de perte

$$R(h) = \int_{\mathcal{X} \times \mathcal{Y}} \ell(h(\mathbf{x}), y) \, \mathbf{p}_{\mathcal{X}\mathcal{Y}}(\mathbf{x}, y) \, d\mathbf{x} \, dy$$

- $R(h)$ : **risque réel** = espérance du coût sur la vraie distribution (inconnue)

**Critère inductif** le plus naturel : l'**ERM** (minimisation du risque empirique) : $\mathcal{H} \times \mathcal{S} \to \text{valeur}(h)$, choisir $h$ minimisant $\hat{R}$.

> ⚠️ L'ERM n'est **sain que si l'espace d'hypothèses $\mathcal{H}$ est contraint** (richesse limitée). Sinon, une hypothèse très riche peut avoir $\hat{R}=0$ et une généralisation désastreuse (ex. : mémoriser $\mathcal{S}$). L'analyse de Vapnik formalise ce lien : il faut optimiser un **risque régularisé** dans lequel entre la richesse de $\mathcal{H}$.

📌 Exemple du cours : dans $\mathbb{R}^2$ avec $\mathcal{H}$ = les rectangles, plusieurs rectangles séparent les $+$ des $-$ → lequel choisir ? C'est tout l'objet de la fiche.

---

## 2. Garanties PAC, dimension VC et SRM

### 2.1 Bornes PAC (cas $\mathcal{H}$ fini)

**Hypothèses** : $\mathcal{H}$ fini de cardinal $|\mathcal{H}|$ ; $m$ exemples i.i.d. ; $\delta \in \; ]0,1]$.

| Cas | Garantie |
|---|---|
| **Réalisable** ($\exists h \in \mathcal{H}$ sans erreur) | $\forall h \in \mathcal{H} : P^m\left[ R(h) \leq \hat{R}(h) + \dfrac{\log \mathcal{H}+ \log \frac{1}{\delta}}{m} \right] > 1 - \delta$ |
| **Non réalisable** | $\forall h \in \mathcal{H} : P^m\left[ R(h) \leq \hat{R}(h) + \sqrt{\dfrac{\log \mathcal{H}+ \log \frac{1}{\delta}}{2m}} \right] > 1 - \delta$ |

- $\delta$ : paramètre de **confiance** ; le terme ajouté à $\hat{R}$ diminue quand $m$ croît et augmente avec $\log|\mathcal{H}|$ (richesse)

**Complexité d'échantillon** (combien d'exemples pour une précision $\varepsilon$) :

$$\text{réalisable : } m \geq \frac{\log |\mathcal{H}| + \log \frac{1}{\delta}}{\varepsilon} \qquad \text{non réalisable : } m \geq \frac{\log |\mathcal{H}| + \log \frac{1}{\delta}}{2\varepsilon^2}$$

### 2.2 Cas $\mathcal{H}$ infini : dimension de Vapnik-Chervonenkis

> 💡 **Idée** : ramener l'étude du cas infini à un ensemble fini d'hypothèses → mesurer jusqu'où $\mathcal{H}$ peut **étiqueter arbitrairement** n'importe quel échantillon.

**Définition (via la fonction de croissance $\Pi_{\mathcal{H}}$)** :

$$d_{VC}(\mathcal{H}) = \max\{m : \Pi_{\mathcal{H}}(m) = 2^m\}$$

- $d_{VC}$ : taille du **plus grand ensemble de points** que les hypothèses de $\mathcal{H}$ peuvent étiqueter de **toutes** les manières possibles ($2^m$)
- Mesure **purement combinatoire**, indépendante du nombre d'exemples ; caractérise la **richesse / capacité** de $\mathcal{H}$
- Connue pour certains $\mathcal{H}$ (ex. séparateurs linéaires), seulement **estimée** pour beaucoup d'autres

**Illustration du cours** : $d_{VC}$(séparateurs linéaires en 2D) $= 3$ ; $d_{VC}$(rectangles alignés sur les axes) $= 4$.

> 🔎 **Complément** : en dimension $d$, $d_{VC}$(hyperplans) $= d+1$. C'est la réponse aux questions posées sur la diapo d'illustration.

**Borne sur le risque réel** (si $d = d_{VC}(\mathcal{H})$) :

$$\forall h \in \mathcal{H}, \forall \delta \leq 1 : \quad P^m\left[R(h) \leq \hat{R}(h) + \sqrt{\frac{8 d \log \frac{2 e m}{d} + 8 \log \frac{4}{\delta}}{m}}\right] > 1 - \delta$$

### 2.3 SRM : Structural Risk Minimization

> 💡 **SRM** = stratifier **a priori** (indépendamment des données) les espaces d'hypothèses emboîtés (par ex. par $d_{VC}$ croissante), puis choisir le meilleur compromis risque empirique ↔ capacité. Critère inductif résultant : le **risque empirique régularisé** — (1) satisfaire les contraintes posées par les exemples, (2) choisir la bonne capacité de $\mathcal{H}$.

**La recette pour concevoir un algorithme d'apprentissage** :

$$h_{opt} = \underset{h \in \mathcal{H}}{\text{ArgMin}} \left[ \underbrace{\frac{1}{m} \sum_{i=1}^{m} \ell(h(\mathbf{x}_i), y_i)}_{\text{risque empirique}} + \lambda \underbrace{reg(\mathcal{H})}_{\text{biais sur le monde}} \right]$$

1. Exprimer le coût d'erreur en une **fonction de perte**
2. Définir un **terme de régularisation** (attendus sur les régularités du monde)
3. Si possible, rendre le problème d'optimisation **convexe**
4. Utiliser/développer un algorithme d'optimisation efficace

**Exemple : approximateurs linéaires parcimonieux** — $h(\mathbf{x}) = \mathbf{w} \cdot \mathbf{x}$, a priori « peu de coefficients non nuls » :

$$\mathbf{w}^*_{ridge} = \underset{\mathbf{w}}{\text{Argmin}} \left\{ \sum_{i=1}^{m} (y_i - \mathbf{w}\mathbf{x}_i)^2 + \lambda \|\mathbf{w}\|_2^2 \right\} \qquad \mathbf{w}^*_{lasso} = \underset{\mathbf{w}}{\text{Argmin}} \left\{ \sum_{i=1}^{m} (y_i - \mathbf{w}\mathbf{x}_i)^2 + \lambda \|\mathbf{w}\|_1 \right\}$$

- Ridge : régularisation $\ell_2$ (réduit les coefficients) ; Lasso : $\ell_1$ (met des coefficients exactement à zéro → parcimonie)

> 💡 **Autre retombée de l'analyse de Vapnik** : l'écart risque empirique/risque réel décroît plus vite si $f$ (le vrai concept) $\in \mathcal{H}$. D'où l'idée : **s'arranger pour que $f \in \mathcal{H}$** → le théorème de Cover va jouer ce rôle (§7).

> 📝 **Tes notes** : tu as noté le principe PAC sous la forme $P[R(h) \leq \hat{R}(h) + \Omega(h)] \leq 1-\delta$. ⚠️ **Correction** : c'est l'inverse pour la probabilité — la borne tient **avec probabilité $> 1-\delta$** (c'est le sens de « Probably Approximately Correct ») : $P[\,R(h) \leq \hat{R}(h) + \Omega(h)\,] > 1-\delta$.
>
> 🚩 Tu as noté $d_{vc} = \frac{|H|}{n}$ : **c'est faux**. La dimension VC n'est pas un rapport ; c'est $d_{VC}(\mathcal{H}) = \max\{m : \Pi_{\mathcal{H}}(m) = 2^m\}$ (plus grand nombre de points shatterables). À retenir : elle *caractérise la richesse de $\mathcal{H}$*, connue pour les séparateurs linéaires mais seulement estimée pour beaucoup d'espaces — ça, tes notes le disaient juste.

---

## 3. Perceptron à marge maximale : dérivation (primal)

### 3.1 Rappel perceptron

Hyperplan en dimension $d$ (sous-espace de dimension $d-1$) :

$$\sum_{j=1}^{d} w_j x_j + w_0 = 0 \qquad h(\mathbf{x}) = \sum_{j=1}^{d} w_j x_j + w_0$$

Exemple du cours (plan) : $1 + 2x_1 + 3x_2 = 0$, soit $x_2 = -\frac{2}{3}x_1 - \frac{1}{3}$. Pour un nouveau point $\mathbf{x}^*$ : $h(\mathbf{x}^*) \geq 0 \Rightarrow \mathbf{x}^* \in \mathcal{C}_1$, $\leq 0 \Rightarrow \mathcal{C}_2$, $= 0$ : indéterminé.

> ⚠️ Pour un même ensemble d'apprentissage linéairement séparable, il existe une **infinité de solutions**. Le perceptron classique en trouve **une**, quelconque.

### 3.2 Pourquoi la plus grande marge ?

On choisit le classifieur qui **maximise la distance aux exemples les plus proches des deux classes** (hyperplan « au milieu »).

> 💡 **Intuition** : c'est la solution la plus **robuste aux variations de $\mathcal{S}$** — un nouveau point bruité a moins de chances de changer de côté.
>
> 📝 **Tes notes** : on cherche pas seulement $UNE$ séparatrice, mais $LA$ séparatrice qui passe au milieu — ça **sécurise l'induction** des nouveaux points. ✅ C'est exactement l'argument de robustesse de la diapo.

### 3.3 Dérivation de la marge

**Hypothèses** : classes linéairement séparables ; étiquettes $y_i = +1$ (classe $+$), $y_i = -1$ (classe $-$). Notation : les diapos écrivent indifféremment $u_i$ ou $y_i$ pour les étiquettes.

On fixe le référentiel (on en est libre) : les hyperplans de marge sont définis par

$$\forall \mathbf{x}_i : \quad y_i(\mathbf{w} \cdot \mathbf{x}_i + w_0) \geq 1 \qquad \text{et} \qquad y_i(\mathbf{w} \cdot \mathbf{x} + w_0) = 1 \quad \forall \mathbf{x} \text{ sur la marge}$$

Pour $\mathbf{x}_+$ (point support de classe $+$) : $\mathbf{w} \cdot \mathbf{x}_+ = 1 - w_0$ ; pour $\mathbf{x}_-$ : $\mathbf{w} \cdot \mathbf{x}_- = -1 - w_0$. La **largeur** de la bande de marge est la projection de $(\mathbf{x}_+ - \mathbf{x}_-)$ sur la normale unitaire :

$$\text{width} = (\mathbf{x}_+ - \mathbf{x}_-) \cdot \frac{\mathbf{w}}{\|\mathbf{w}\|} = \frac{2}{\|\mathbf{w}\|}$$

- $\mathbf{w}$ : vecteur de poids (normal à l'hyperplan) ; $w_0$ : biais/seuil ; largeur $\propto 1/\|\mathbf{w}\|$

Maximiser la marge $\iff$ **minimiser** $\|\mathbf{w}\|$, ou de façon équivalente (pour avoir une dérivée simple) $\frac{1}{2}\|\mathbf{w}\|^2$.

### 3.4 Problème primal

$$\left\{ \begin{array}{ll} \text{Minimiser} & \dfrac{1}{2}\|\mathbf{w}\|^2 \\[2mm] \text{sous contraintes} & u_i(\mathbf{w}^\top \mathbf{x}_i + w_0) \geq 1, \quad i = 1, \dots, m \end{array} \right.$$

> 💡 **Problème d'optimisation quadratique** (objectif quadratique **convexe**) **sous contraintes linéaires** → **optimum global unique**, tout un éventail d'algorithmes efficaces existe. (Contrairement à la régression linéaire classique en MSE, pas de solution fermée directe, mais des solveurs QP performants.)

Solution : $\mathbf{w}^*$, $w_0^*$ et la fonction de décision :

$$h(\mathbf{x}) = \text{sign}\{\mathbf{w}^{*\top}\mathbf{x} + w_0^*\}$$

---

## 4. Forme duale, KKT et vecteurs supports

### 4.1 Pourquoi passer au dual ?

Un problème d'optimisation admet une **forme duale** si la fonction à optimiser et les contraintes sont **strictement convexes** ; alors la solution duale est aussi solution du primal. Pour les SVM, le dual s'exprime **uniquement via des produits scalaires** $\langle \mathbf{x}_i, \mathbf{x}_j \rangle$ → clé du kernel trick (§8).

### 4.2 Lagrangien et conditions

On forme le lagrangien (avec $\alpha_i \geq 0$ les multiplicateurs) :

$$L(\mathbf{w}, w_0, \alpha) = \frac{1}{2}\|\mathbf{w}\|^2 - \sum_{i=1}^{m} \alpha_i \left( y_i(\mathbf{w} \cdot \mathbf{x}_i + w_0) - 1 \right)$$

La solution est un **point selle** : $\frac{\partial L}{\partial \mathbf{w}} = 0$, $\frac{\partial L}{\partial w_0} = 0$ :

$$\frac{\partial L}{\partial \mathbf{w}} = \mathbf{w} - \sum_{i=1}^{m} \alpha_i y_i \mathbf{x}_i = 0 \qquad\qquad \frac{\partial L}{\partial w_0} = -\sum_{i=1}^{m} \alpha_i y_i = 0$$

D'où les deux relations clés :

$$\sum_{i=1}^{m} \alpha_i y_i = 0 \qquad \text{et} \qquad \mathbf{w}^* = \sum_{i=1}^{m} \alpha_i y_i \mathbf{x}_i$$

- La seconde est le **théorème du représentant (representer theorem)** : la solution est une **combinaison linéaire des exemples**.

### 4.3 Problème dual

$$\left\{ \begin{array}{l} \underset{\alpha}{\text{Max}} \left[ \displaystyle\sum_{i=1}^{m} \alpha_i - \frac{1}{2} \sum_{i,j=1}^{m} \alpha_i \alpha_j \, u_i u_j \, \langle \mathbf{x}_i, \mathbf{x}_j \rangle \right] \\[4mm] \text{avec } \alpha_i \geq 0, \quad i = 1, \dots, m \qquad \text{et} \qquad \sum_{i=1}^{m} \alpha_i u_i = 0 \end{array} \right.$$

- $u_i = y_i \in \{-1, +1\}$ : étiquette ; $\alpha_i$ : poids (Lagrange) ; $\langle \cdot, \cdot \rangle$ : produit scalaire — **seule quantité impliquant les données** !

### 4.4 KKT et vecteurs supports

**Conditions de Karush-Kuhn-Tucker** : seuls les points **sur la marge** ($\mathbf{w}^{*\top}\mathbf{x}_i + w_0^* = \pm 1$) ont $\alpha_i^* > 0$ → ce sont les **vecteurs supports** ($\mathcal{P}_S$). Tous les autres points ont $\alpha_i = 0$ et **peuvent être supprimés** sans changer la solution.

La solution est donc **parcimonieuse (sparse)** :

$$h^*(\mathbf{x}) = \text{sign}\left\{\sum_{i \in \mathcal{P}_S} \alpha_i^* u_i \, \langle \mathbf{x}_i, \mathbf{x} \rangle + w_0^*\right\}$$

**Calcul du seuil** $w_0$ : à partir de n'importe quel vecteur support $(\mathbf{x}_c, y_c)$ :

$$w_0 = y_c - \mathbf{w}^\top \mathbf{x}_c = y_c - \sum_{i=1}^{m} y_i \alpha_i \, \mathbf{x}_i^\top \mathbf{x}_c$$

ou, mieux (moyenne sur deux vecteurs supports de classes opposées $\mathbf{x}_A$ (classe $+$) et $\mathbf{x}_B$ (classe $-$)) :

$$w_0^* = -\frac{1}{2} \sum_{i=1}^{n} y_i \alpha_i^* (\mathbf{x}_i^\top \mathbf{x}_A + \mathbf{x}_i^\top \mathbf{x}_B)$$

> 📝 **Tes notes** : tu as écrit $h(x) = \text{sign}\{\sum w_i \langle x_i, x\rangle\}$. ⚠️ **Précision à corriger** : les coefficients ne sont pas des $w_i$, ce sont les **multiplicateurs de Lagrange** pondérés par les étiquettes, et il ne faut pas oublier le biais : $h^*(\mathbf{x}) = \text{sign}\{\sum_{i \in \mathcal{P}_S} \alpha_i^* u_i \langle \mathbf{x}_i, \mathbf{x} \rangle + w_0^*\}$. (Ta formule d'hypothèse en tête de notes avec les $\alpha_i^* u_i$ était, elle, correcte.)

### 4.5 Mini-exemple du cours (linéaire)

| $i$ | point $\mathbf{x}$ | étiquette | $\alpha$ |
|---|---|---|---|
| 0 | (1, 2) | +1 | 0.5 |
| 1 | (2, 1) | +1 | 0.5 |
| 2 | (3, 3) | +1 | 0 |
| 3 | (0, 0) | −1 | 1 |
| 4 | (−1, −1) | −1 | 0 |
| 5 | (−3, 1) | −1 | 0 |

Seuls les points avec $\alpha \neq 0$ (marqués $*$ sur la figure) déterminent l'hyperplan : ce sont les **vecteurs supports**.

---

## 5. Marges douces et perte hinge

### 5.1 Problème motivation : bruit et outliers

> ⚠️ Que se passe-t-il s'il y a du **bruit** ou des **outliers** ? Un seul point mal étiqueté peut forcer une marge minuscule (voire l'impossibilité de séparation parfaite). On accepte donc de **violer certaines contraintes**, dans une limite contrôlée par la constante $C$.

> 📝 **Tes notes** : on pourrait séparer parfaitement les 2 nuages en réduisant la marge pour forcer ça ; mais si on veut une grande marge (modèle plus robuste), on accepte un point du mauvais côté, on modifie la séparatrice, et on **pénalise par la distance du point mal placé à la marge** — réglé par un hyperparamètre, souvent $C$. ✅ Bien vu : c'est exactement le compromis $\xi_i$/$C$ ci-dessous.

### 5.2 Perte de substitution (surrogate loss) : la hinge

$$\ell(y, h(\mathbf{x})) = \max(0, 1 - y \cdot h(\mathbf{x})) = (1 - y \cdot h(\mathbf{x}))_+ = \xi$$

- $y \in \{-1, +1\}$, $h(\mathbf{x})$ : score (avant sign)
- $\xi_i$ : **variable ressort (slack)** = pénalité si l'exemple est dans la marge ou du mauvais côté
- **Hinge = « coude »** : pénalité **nulle** si le point est bien classé hors de la marge ($y\,h(\mathbf{x}) \geq 1$), puis croît **linéairement** (jusqu'à $\infty$) dès qu'on entre dans la marge

### 5.3 Le critère inductif du SVM

$$\mathbf{w}^{*} = \underset{\mathbf{w}}{\text{ArgMin}} \left[ \underbrace{\sum_{i=1}^{m} |1 - y_i h(\mathbf{x}_i)|_+}_{\text{risque empirique}} + \underbrace{\frac{1}{2}\mathbf{w}^\top\mathbf{w}}_{\text{marge}} \right]$$

- **Risque empirique** : somme des hinges ; **Marge** : régularisateur $\frac{1}{2}\|\mathbf{w}\|^2$

> 💡 C'est un **risque empirique régularisé** : $h^* = \text{ArgMin}_{h\in\mathcal{H}}[R_{Emp}(h) + \lambda\, reg(h)]$ — exactement la recette du §2.3, avec la hinge comme fonction de perte de substitution et la marge comme régularisation. **C'est la forme de la fonction de coût qui induit la régularisation.**

### 5.4 Forme relaxée (problème primal soft margin)

$$\text{Minimiser } \|\mathbf{w}\|^2 + C\sum_{i=1}^{n}\xi_i \qquad \text{sous contraintes } \forall i : \; (\langle \mathbf{w}, X_i \rangle + b)\, Y_i \geq 1 - \xi_i$$

- $\xi_i \geq 0$ : violation autorisée de la marge pour l'exemple $i$ ; $C$ : coût unitaire de la violation
- La décomposition de $\mathbf{w}$ comme combinaison de vecteurs supports **reste valable** dans ce cadre
- Le dual est le même qu'en §4.3, avec en plus la contrainte de borne $0 \leq \alpha_i \leq C$ (les $\alpha_i$ sont plafonnés par $C$)

### 5.5 Rôle de $C$ : compromis biais-variance

| | $C$ **grand** | $C$ **petit** |
|---|---|---|
| Attitude | les erreurs coûtent cher | on tolère les erreurs |
| Marge exigée | grandes marges voulues | moins exigeant sur la marge |
| Variance | **faible** (moins sensible aux variations de $\mathcal{S}$) | **grande** (sensible aux caractéristiques de $\mathcal{S}$) |
| Biais | **fort** | **faible** |

> 💡 **$C$ contrôle le compromis biais-variance** ; en pratique il est fixé par **validation croisée**.

---

## 6. La marge comme mesure de capacité

### 6.1 La borne VC est inutilisable en grande dimension

Si on borne avec la dimension VC (qui vaut $d+1$ pour un perceptron en dimension $d$) :

$$R(h) \leq \hat{R}(h) + \sqrt{\frac{2(d+1)\log\frac{e\,m}{d+1}}{m}} + \sqrt{\frac{\log\frac{1}{\delta}}{2m}}$$

- $m$ : nb d'exemples ; $d$ : dimension ; $\delta$ : confiance

> ⚠️ **Clairement non-informative quand $d$ est grand devant $m$** : le terme de capacité explose. Or le kernel trick (§8) nous envoie précisément dans des espaces de très grande (voire infinie) dimension → il faut une autre mesure de capacité.

### 6.2 Bornes fondées sur la marge

**Cas $f \in \mathcal{H}$** (le concept cible est dans l'espace des hypothèses) :

$$R(h) \leq \mathcal{O}\left(\frac{\left(\frac{R}{\gamma}\right)^2 \ln^2 m + \ln\left(\frac{1}{\delta}\right)}{m}\right)$$

**Cas $f \notin \mathcal{H}$** :

$$R(h) \leq \hat{R}(h) + \mathcal{O}\left(\sqrt{\frac{\left(\frac{R}{\gamma}\right)^2 \ln^2 m + \ln\left(\frac{1}{\delta}\right)}{m}}\right)$$

- $R$ : rayon de la **plus petite sphère englobant les vecteurs d'apprentissage**
- $\gamma$ : **marge** ; $m$ : nb d'exemples ; $\delta$ : paramètre de confiance
- ⚠️ Noter la **racine carrée** dans le cas $f \notin \mathcal{H}$ (borne moins bonne)

> 💡 **La borne ne dépend plus de la dimension $d$ !** Mesure de capacité indépendante de la dimension, valable même pour des espaces **de dimension infinie** → c'est **central pour les méthodes à noyaux**. Le rapport $R/\gamma$ (rayon/marge) remplace la dimension VC.

### 6.3 Borne en nombre de vecteurs supports

Avec probabilité $1-\delta$, sur $m$ exemples :

$$R(h) \leq \frac{1}{m - \#sv}\left(\#sv \log\frac{e\,m}{\#sv} + \log\frac{m}{\delta}\right)$$

- $\#sv$ : nombre de vecteurs supports → plus il y a de vecteurs supports, plus la borne est mauvaise (cf. heuristiques §11)

### 6.4 Leçons

- La **marge contrôle le taux de convergence** et la **capacité de l'hypothèse**, **automatiquement** : pas de stratification a priori (comme en SRM), mais **après observation des exemples**
- La **hinge loss agit comme un régularisateur**
- La marge permet de **se soustraire à la dimension VC** (donc à la dimension de l'espace)

> 📝 **Tes notes** : tu as noté le « nouveau théorème » sous la forme $R(h) \leq \hat{R}(h) + o(\frac{R^2}{\delta^2 m})$. ⚠️ **À corriger** : (1) le rayon et la marge apparaissent via le **rapport $(R/\gamma)^2$**, pas $R^2/\delta^2$ ; (2) $\delta$ désigne la **confiance**, la marge se note $\gamma$ — ne pas confondre les deux ; (3) il y a un $\ln^2 m$ au numérateur, et une **racine carrée globale seulement si $f \notin \mathcal{H}$** (sinon pas de $\hat{R}$ et pas de racine).
>
> 📝 **Le conflit que tu as noté est juste et important** : Cover demande une dimension **très grande** pour garantir la séparabilité linéaire, mais la borne VC **explose quand la dimension croît** — « les deux se repoussent ». 💡 La résolution du conflit, c'est **la marge** : elle fournit une garantie de généralisation **indépendante de la dimension**, ce qui autorise à travailler implicitement en dimension infinie. D'où le succès des SVM.

---

## 7. Théorème de Cover et changement de représentation

### 7.1 Théorème de Cover

**Énoncé** : soient $m$ points $\mathbf{x}_1, \dots, \mathbf{x}_m \in \mathbb{R}^d$. Le nombre de groupements $\mathcal{O}(m,d)$ que des hyperplans de dimension $(d-1)$ peuvent réaliser pour séparer les $m$ points en deux classes, toutes combinaisons confondues, est :

$$\mathcal{O}(m, d) = 2\sum_{i=0}^{d}\binom{m-1}{i}$$

**Conséquences** :

- Si $m > 2(d+1)$ : la probabilité de séparabilité linéaire devient **petite**
- Si $d$ est grand et $m < 2(d+1)$ : la probabilité qu'**un groupement quelconque** des données en deux classes soit **linéairement séparable tend vers 1**

> 💡 **En pratique** : projeter les points dans un espace de redescription $\Phi(X)$ de dimension suffisamment grande ⇒ il **existe un hyperplan séparateur** (quasi sûr).

### 7.2 Du linéaire au non-linéaire

Idée : **augmenter la dimension** de l'espace d'entrée en générant plein de nouvelles dimensions (combinaisons et fonctions des dimensions initiales), puis chercher un **discriminant linéaire dans cet espace de redescription**.

$$\text{non-linéaire dans } X \;\xrightarrow{\;\Phi\;}\; \text{linéaire dans } \Phi(X), \quad \dim\Phi(X) > \dim(X)$$

Une fois l'hyperplan trouvé dans $\Phi(X)$, on **reprojette** dans l'espace de départ → on obtient une **frontière non linéaire**.

**Exemples du cours** :

- $(x_1, x_2) \to (x_1', x_2') = (x_1^2, x_2^2)$ : un cercle du plan devient une droite
- Cercle idéal : $f(\mathbf{x}) = x_1^2 + x_2^2 - R^2 = \langle \mathbf{w}, \phi(\mathbf{x}) \rangle + b$ avec $\phi(\mathbf{x}) = (x_1^2, x_2^2)^\top$, $\mathbf{w} = (1,1)^\top$, $b = -R^2$
  - ⚠️ La diapo écrit « $b=1$ », c'est une coquille : pour obtenir $x_1^2+x_2^2-R^2$ il faut $b=-R^2$ (ou $R^2=1$).
- $(x_1, x_2) \mapsto (x_1, x_2, x_1^2+x_2^2)$ : ajout d'une 3ᵉ dimension qui « soulève » une classe
- $(x_1, x_2) \mapsto (x_1^2, \sqrt{2}\,x_1 x_2, x_2^2)$ (voir §9.1)

**Traduction des besoins** (diapo) : trouver un espace de redescription $\phi(X)$ de (très) grande dimension, où une fonction de décision linéaire existe et respecte la vraie « similarité » entre points — mais comment trouver $\phi$ avec des **calculs tractables** ? → réponse : le kernel trick.

---

## 8. Le kernel trick

### 8.1 L'astuce

La forme duale (§4.3) et la fonction de décision ne font intervenir les données **que par produits scalaires** $\langle \mathbf{x}_i, \mathbf{x} \rangle$. Donc :

$$\text{remplacer } \langle \mathbf{x}, \mathbf{x}' \rangle \text{ par } K(\mathbf{x}, \mathbf{x}') = \langle \Phi(\mathbf{x}), \Phi(\mathbf{x}') \rangle$$

| Approche naïve | Kernel trick |
|---|---|
| Calculer explicitement $\Phi(\mathbf{x})$ pour chaque donnée, résoudre dans l'espace des features | Écrire l'algorithme **en produits scalaires**, remplacer par $K$ |
| Coût de calcul explicite (dès fois prohibitif, ou infini !) | **Insensible à la dimension** ; on ne connaît même pas $\Phi$ |
| — | Exige que la **matrice de Gram $K$ soit semi-définie positive** |

**Définition (fonction noyau)** :

$$k : \mathcal{X} \times \mathcal{X} \to \mathbb{R}, \qquad \forall \mathbf{x}, \mathbf{z} \in \mathcal{X} : \quad k(\mathbf{x}, \mathbf{z}) = \langle \phi(\mathbf{x}), \phi(\mathbf{z}) \rangle$$

- $\phi : \mathbf{x} \mapsto \phi(\mathbf{x}) \in F$ : application de redescription ; $F$ : espace muni d'un **produit scalaire**

> 📝 **Tes notes** : « le noyau me donne le produit scalaire **comme si** on était dans l'espace de représentation → on n'a plus à projeter réellement ». ✅ Exact. ⚠️ Mais tu as noté $\forall x, z : k(x,z) \leq \langle \Phi(x), \Phi(z) \rangle$ : **c'est une égalité**, pas une inégalité — par définition $k(x,z) = \langle\phi(x), \phi(z)\rangle$.

### 8.2 SVM à noyaux : forme duale kernelisée

$$h^*(\mathbf{x}) = \text{sign}\left\{\sum_{i \in \mathcal{P}_S} \alpha_i^* u_i \, \kappa(\mathbf{x}_i, \mathbf{x}) + w_0^*\right\}$$

$$\left\{ \begin{array}{l} \underset{\alpha}{\text{Max}} \left[ \displaystyle\sum_{i=1}^{m} \alpha_i - \frac{1}{2}\sum_{i,j=1}^{m} \alpha_i \alpha_j \, u_i u_j \, \kappa(\mathbf{x}_i, \mathbf{x}_j) \right] \\[2mm] \alpha_i \geq 0 \quad \text{et} \quad \sum_{i=1}^{m} \alpha_i u_i = 0 \end{array} \right.$$

- Tout ce qui change : $\langle \mathbf{x}_i, \mathbf{x}_j \rangle \to \kappa(\mathbf{x}_i, \mathbf{x}_j)$ ; tout le reste (KKT, vecteurs supports, calcul de $w_0$) est identique
- Avec soft margin : ajouter $0 \leq \alpha_i \leq C$

### 8.3 L'essence des SVM (the gist)

- **Représentation non paramétrique** : l'hypothèse est une fonction des exemples d'apprentissage ; sa complexité dépend de $|\mathcal{S}|$
- **Parcimonieux** : seuls les $m' \leq m$ exemples support interviennent
- Solution la plus robuste (grande marge) ⇒ nécessite **moins de précision** (le moins de bits)
- La complexité ne dépend **pas de $d$**, mais de $m'$

### 8.4 Une autre lecture : un « plus proche voisin » sophistiqué

$$\text{signe}\left(\sum_i \alpha_i u_i \, \kappa(\mathbf{x}, \mathbf{x}_i) + w_0\right)$$

| kNN | SVM |
|---|---|
| tous les voisins comptent | seuls les **points critiques** (vecteurs supports) comptent |
| pondération uniforme / distance | pondérés par les $\alpha_i$ |
| similarité = distance choisie | similarité = noyau (produit scalaire) |
| règle locale | $h(\mathbf{x})$ = **combinaison linéaire** des similarités |

- La solution est **entièrement déterminée par la matrice de Gram** — ses caractéristiques en disent long sur le problème (cf. §11.3)

**Les 4 questions/réponses du cours** :

1. Un ensemble d'apprentissage est-il plus sûrement séparable une fois projeté en grande dimension ? — **Oui** (Cover)
2. Comment choisir les nouvelles dimensions ? — **Automatiquement** (via le noyau)
3. Comment éviter le sur-apprentissage ? — **Simple** (la marge contrôle la capacité)
4. Comment garder des calculs tractables ? — **Pas même un problème** (produits scalaires uniquement)

---

## 9. Fonctions noyaux usuelles et construction

### 9.1 Exemple fondateur : $k(\mathbf{x}, \mathbf{z}) = \langle \mathbf{x}, \mathbf{z} \rangle^2$

Soit $\mathcal{X} \subseteq \mathbb{R}^2$ et $\phi(\mathbf{x}) = (x_1^2, x_2^2, \sqrt{2}\,x_1 x_2) \in \mathbb{R}^3$ :

$$\langle \phi(\mathbf{x}), \phi(\mathbf{z}) \rangle = x_1^2 z_1^2 + x_2^2 z_2^2 + 2 x_1 x_2 z_1 z_2 = (x_1 z_1 + x_2 z_2)^2 = \langle \mathbf{x}, \mathbf{z} \rangle^2$$

- Donc $k(\mathbf{x}, \mathbf{z}) = \langle\mathbf{x},\mathbf{z}\rangle^2$ **est une fonction noyau** : produit scalaire dans l'espace des features sans jamais calculer $\phi$
- L'hypothèse correspondante : $h(\mathbf{x}) = w_{11}x_1^2 + w_{22}x_2^2 + w_{12}\sqrt{2}x_1x_2$

> 🔎 **Remarque du cours** : l'espace $F$ défini par $\Phi$ **n'est pas unique** ! Le même noyau $\langle\mathbf{x},\mathbf{z}\rangle^2$ correspond aussi au produit scalaire dans $\mathbb{R}^4$ avec $\phi(\mathbf{x}) = (x_1^2, x_2^2, x_1x_2, x_2x_1)$. Seul le noyau compte, pas la projection.

### 9.2 Noyaux pour vecteurs

| Noyau | Formule | Propriété / lecture |
|---|---|---|
| Polynomial 1 | $k_{poly1}(\mathbf{x}, \mathbf{z}) = (\mathbf{x}^\top\mathbf{z})^d$ | tous les produits d'**exactement** $d$ variables |
| Polynomial 2 | $k_{poly2}(\mathbf{x}, \mathbf{z}) = (\mathbf{x}^\top\mathbf{z} + c)^d$ | tous les produits d'**au plus** $d$ variables |
| Gaussien (RBF) | $k_G(\mathbf{x}, \mathbf{z}) = \exp\left(-\dfrac{d(\mathbf{x}, \mathbf{z})^2}{2\sigma^2}\right)$ | lié à une **décomposition en série de Fourier** |
| Sigmoid « noyau » | $k(\mathbf{x}, \mathbf{z}) = \tanh(\kappa\, \mathbf{x}^\top\mathbf{z} + \theta)$ | **pas défini positivement** ; proche des fonctions de décision des réseaux de neurones |

- $\mathbf{x}, \mathbf{z}$ : vecteurs d'entrée ; $d$ : degré ; $c$ : constante (offset) ; $\sigma$ : largeur de bande ; $\kappa, \theta$ : pente et biais du tanh

> 📝 **Tes notes** sur le sigmoid : « ça fonctionne même si ça ne valide pas la théorie mathématique des noyaux ». ✅ Exactement : utilisé en pratique pour la ressemblance avec les réseaux de neurones, mais **ce n'est pas un vrai noyau** (pas semi-défini positif en général) — la théorie (existence de $\Phi$, bornes) ne s'applique pas.
>
> 🚩 Dans tes notes, le noyau gaussien est écrit « $-\exp(-\dots)$ » : **le signe moins est une erreur de copie** — le noyau gaussien est **positif** : $k_G = \exp(-d(\mathbf{x},\mathbf{z})^2/2\sigma^2)$. (Un $-\exp$ ne serait pas semi-défini positif.)

### 9.3 Noyau gaussien (RBF) en détail

$$K(\mathbf{x}, \mathbf{x}') = \exp\left(-\gamma\|\mathbf{x} - \mathbf{x}'\|^2\right)$$

- **Pas de forme close pour $\Phi$** ; $\Phi(X)$ est de **dimension infinie**
- Pour $x \in \mathbb{R}$, on peut écrire :

$$\Phi(x) = e^{-\gamma x^2}\left[1, \; \sqrt{\tfrac{2\gamma}{1!}}x, \; \sqrt{\tfrac{(2\gamma)^2}{2!}}x^2, \; \sqrt{\tfrac{(2\gamma)^3}{3!}}x^3, \dots\right]$$

- **Choix de $\gamma$** : intuition — penser à la matrice $H$ avec $H_{i,j} = y_i y_j K(\mathbf{x}_i, \mathbf{x}_j)$ (diagnostic via la matrice de Gram, cf. §11.3)

> 💡 Le RBF illustre la puissance du kernel trick : on travaille **implicitement dans un espace de dimension infinie** tout en ne manipulant que des nombres réels calculables.

### 9.4 Règles de composition (construire des noyaux)

Si $\kappa_1$, $\kappa_2$ sont des noyaux (et $c > 0$, $f$ une fonction, $poly$ un polynôme à coefficients positifs, $\Phi$ une application, $A$ semi-définie positive) :

| | Règle |
|---|---|
| (i) | $\kappa(\mathbf{x}, \mathbf{x}') = c\,\kappa_1(\mathbf{x}, \mathbf{x}')$ |
| (ii) | $\kappa(\mathbf{x}, \mathbf{x}') = f(\mathbf{x})\,\kappa_1(\mathbf{x}, \mathbf{x}')\,f(\mathbf{x}')$ |
| (iii) | $\kappa(\mathbf{x}, \mathbf{x}') = poly(\kappa_1(\mathbf{x}, \mathbf{x}'))$ |
| (iv) | $\kappa(\mathbf{x}, \mathbf{x}') = \exp(\kappa_1(\mathbf{x}, \mathbf{x}'))$ |
| (v) | $\kappa = \kappa_1 + \kappa_2$ (somme) |
| (vi) | $\kappa = \kappa_1 \cdot \kappa_2$ (produit) |
| (vii) | $\kappa(\mathbf{x}, \mathbf{x}') = \kappa_3(\Phi(\mathbf{x}), \Phi(\mathbf{x}'))$ |
| (viii) | $\kappa(\mathbf{x}, \mathbf{x}') = \mathbf{x}^\top A \mathbf{x}'$ |
| (ix) | $\kappa(\mathbf{x}, \mathbf{x}') = \kappa_a(\mathbf{x}_a, \mathbf{x}'_a) + \kappa_b(\mathbf{x}_b, \mathbf{x}'_b)$ (sous-espaces de description) |
| (x) | $\kappa(\mathbf{x}, \mathbf{x}') = \kappa_a(\mathbf{x}_a, \mathbf{x}'_a) \cdot \kappa_b(\mathbf{x}_b, \mathbf{x}'_b)$ |

> 💡 (i)–(x) = boîte à outils : on **combine des noyaux élémentaires** pour construire un noyau adapté à la structure des données (somme sur sous-espaces = description multi-vues ; produit = « ET » combinatoire).

---

## 10. Exemple travaillé : noyau polynomial

**Données** : 5 points sur la droite, étiquetés :

$$(x_1{=}1, u_1{=}{+}1), \ (x_2{=}2, u_2{=}{+}1), \ (x_3{=}4, u_3{=}{-}1), \ (x_4{=}5, u_4{=}{-}1), \ (x_5{=}6, u_5{=}{+}1)$$

**Noyau** : polynomial de degré 2, $k(x_i, x_j) = (x_i x_j + 1)^2$, avec $C = 100$.

**Problème dual** (soft margin, ici les $\alpha_i$ bornés par $C$) :

$$\max_\alpha \sum_{i=1}^{5}\alpha_i - \frac{1}{2}\sum_{i,j=1}^{5}\alpha_i\alpha_j u_i u_j (x_i x_j + 1)^2 \qquad \text{s.c.} \quad \sum_i \alpha_i u_i = 0, \quad 0 \leq \alpha_i \leq 100$$

**Solution** (par un solveur d'optimisation quadratique) :

$$\alpha_1 = 0, \quad \alpha_2 = 2.5, \quad \alpha_3 = 0, \quad \alpha_4 = 7.333, \quad \alpha_5 = 4.833$$

- Vérif de la contrainte : $\sum \alpha_i u_i = 2.5 - 7.333 + 4.833 = 0$ ✓
- **Vecteurs supports** : $\{x_2 = 2, \; x_4 = 5, \; x_5 = 6\}$ (ceux avec $\alpha_i \neq 0$)

**Fonction de décision** :

$$h(x) = (2.5)(+1)(2x+1)^2 + (7.333)(-1)(5x+1)^2 + (4.833)(+1)(6x+1)^2 + b = 0.6667\,x^2 - 5.333\,x + b$$

- ⚠️ La diapo imprime « $(1)$ » devant le terme en $x_4$ : c'est une coquille, le facteur est $u_4 = -1$ (sinon on n'obtient pas le résultat affiché $0.6667x^2 - 5.333x$).
- **Calcul de $b$** : les vecteurs supports sont sur la marge, donc $u_i(w^\top\Phi(x_i) + b) = 1$ ; avec $h(2) = 1$ (ou $h(5) = -1$, ou $h(6) = 1$) on obtient $b = 9$

$$\boxed{h(x) = 0.6667\,x^2 - 5.333\,x + 9}$$

- Frontière = parabole dans l'espace d'origine = hyperplan dans l'espace de redescription
- Vérification : $h(2)=1$, $h(5)=-1$, $h(6)=1$ (les 3 supports sur la marge), $h(1)>1$ et $h(4)<-1$ (bien classés hors marge, $\alpha=0$)

---

## 11. En pratique : hyperparamètres et diagnostic

### 11.1 Ce qu'on doit choisir

- Le **type de noyau** $\kappa$ : sa forme, ses paramètres (degré, $\sigma$/$\gamma$, ...)
- La valeur de la **constante $C$**
- → tout ceci se fait par **validation croisée** (classique)

### 11.2 Sensibilité aux hyperparamètres (illustrations du cours)

**Damier (checkerboard), noyau gaussien** $K(x,x') = e^{-\frac{|x-x'|^2}{2\sigma^2}}$, deux valeurs de $\sigma$ :

- petit $\sigma$ (figure du haut) : **beaucoup plus de vecteurs supports** ; grand $\sigma$ (bas) : moins
- ⚠️ Dans les **deux** cas : $R_{emp} = 0$ ! → le risque empirique seul ne dit **rien** sur la qualité ; c'est le nombre de SV et la marge qui renseignent

**47 exemples (22 $+$, 25 $-$), $C = 10000$** :

| Noyau | Vecteurs supports |
|---|---|
| polynomial degré 5 | 4 $+$ et 3 $-$ |
| polynomial degrés 2 / 5 / 8 | SV de plus en plus nombreux quand le degré s'éloigne de l'optimum |
| gaussien $\sigma = 2$ / $5$ / $10$ | $(4{-},5{+})$ → $(8{-},6{+})$ → $(10{-},11{+})$ : petits $\sigma$ ⇒ plus de SV |

**Ajout de quelques points** : 47 + 8 exemples (noyau polynomial degré 5, $C=10000$) → les vecteurs supports changent (5 $+$, 8 $-$) : la solution s'adapte localement, seuls les points critiques comptent.

**Contrôle de $C$** (noyau radial, $\gamma = 1$) : $C = 2$ vs $C = 10000$ :

- petit $C$ : frontière régulière, proche de la frontière de Bayes optimale
- grand $C$ : **sur-apprentissage** — la frontière épouse le bruit, l'erreur en test explose
- 💡 Illustration de la nécessité de la **régularisation** ; la validation croisée sert à ça

### 11.3 Estimer la généralisation

**Empiriquement** : validation croisée.

**Heuristiques (mais fondées théoriquement)** :

1. **Nombre de vecteurs supports** : moins il y en a, mieux c'est (cf. borne §6.3)
2. **Caractéristiques de la matrice de Gram** $G$ avec $G_{ij} = \langle v_i, v_j \rangle$ :

$$|G(v_1, \dots, v_n)| = \begin{vmatrix} \langle v_1, v_1 \rangle & \cdots & \langle v_1, v_n \rangle \\ \vdots & \ddots & \vdots \\ \langle v_n, v_1 \rangle & \cdots & \langle v_n, v_n \rangle \end{vmatrix}$$

- **Pas de structure dans $G$** → aucune régularité exploitable dans les données
- Termes **hors-diagonale très petits** → **sur-apprentissage** (chaque point ne ressemble à aucun autre)
- Matrice **uniforme** → **sous-apprentissage** (tous les points se ressemblent, tout finit dans la même classe)

> 📝 **Tes notes** (à retenir comme règles pratiques) :
> - « Plus on a de points supports, plus on est en train de faire du sur-apprentissage ; moins on en a, meilleure sera la généralisation » ✅ (cohérent avec la borne en $\#sv$) — « toutefois le vrai critère est la marge » ✅
> - **Règle heuristique perso : max ~25 % des points en vecteurs supports, sinon gros problème** (en réalité souvent moins). 🔎 C'est cohérent avec la borne du §6.3 : beaucoup de SV ⇒ $R(h)$ mal borné.

---

## 12. SVR, nouveautés, kernelisation

### 12.1 SVR : Support Vector Regression

**Fonction de perte $\varepsilon$-insensible** :

$$|y - f(\mathbf{x})|_\varepsilon = \max\{0, \; |y - f(\mathbf{x})| - \varepsilon\}$$

- $\varepsilon$ : demi-largeur du « tube » de tolérance autour de $f$ — aucune pénalité tant que l'erreur reste dans le tube

**Régression linéaire** $f(\mathbf{x}) = \mathbf{w}\cdot\mathbf{x} + w_0$, à minimiser :

$$\frac{1}{2}\|\mathbf{w}\|^2 + C\sum_{i=1}^{m}|y_i - f(\mathbf{x}_i)|_\varepsilon$$

**Solution généralisée** :

$$f(\mathbf{x}) = \sum_{i=1}^{m}(\alpha_i^{*} - \alpha_i)\,K(\mathbf{x}_i, \mathbf{x}) + w_0$$

- $(\alpha_i^* - \alpha_i)$ : deux multiplicateurs par exemple (un par côté du tube) ; seuls les points **hors du tube** ont un coefficient non nul → ici aussi, parcimonie via vecteurs supports
- Kernelisable à l'identique (remplacer les produits scalaires par $K$)

### 12.2 Détection de nouveautés (non supervisé)

- On cherche à **séparer au maximum le nuage de points de l'origine** : la frontière apprise délimite « le normal » ; les points au-dehors sont des nouveautés/anomalies. (Même machinerie : marge maximale + noyaux.)

### 12.3 Kernelisation d'une méthode linéaire

> 📝 **Tes notes (Aller plus loin)** : « dès qu'on a un produit scalaire, on peut transformer une méthode linéaire (comme l'ACP) en méthode non linéaire en passant par les espaces de redescription = **kernelisation d'une méthode linéaire** ». ✅ C'est le message du cours : le noyau n'est pas réservé aux SVM.

Applications listées : classification multi-classes, régression, détection de nouveautés, **ACP non linéaire** (kernel-PCA).

> 🔎 **Complément** : le principe général est la **modularité** : découplage entre l'**algorithme** (linéaire, exprimé en produits scalaires) et la **description des données** (le noyau). Toute méthode linéaire qui n'utilise les données que via des produits scalaires (ACP, k-means, régression ridge, analyse discriminante...) est kernelisable.

---

## 13. Noyaux pour données non vectorielles

Les noyaux existent pour des espaces **non vectoriels** : génômes, textes, images, vidéos, graphes sociaux...

### 13.1 String kernels (textes)

$\Phi$ : projection sur $\mathbb{R}^D$ avec $D = |\Sigma|^n$ (tous les $n$-grammes possibles sur l'alphabet $\Sigma$).

Exemple du cours (poids $\varepsilon^{n}$ par $n$-gramme commun, selon sa longueur) :

| | CH | CA | CT | AT |
|---|---|---|---|---|
| CHAT | $\varepsilon^2$ | $\varepsilon^3$ | $\varepsilon^4$ | $\varepsilon^2$ |
| CARTON | 0 | $\varepsilon^2$ | $\varepsilon^4$ | $\varepsilon^3$ |

$$K(CHAT, CARTON) = 2\varepsilon^5 + \varepsilon^8$$

- On préfère la version **normalisée** :

$$\kappa(s, s') = \frac{K(s, s')}{\sqrt{K(s, s)\,K(s', s')}}$$

### 13.2 Graph kernels

- Fonctions noyau sur des **parcours (walks)** dans les graphes ; parcours vs chemin
- Les noyaux **nth-order, random et geometric walk** se calculent efficacement en **temps polynomial**

### 13.3 Applications

- **Document mining** : le pré-traitement compte énormément (**stop-words, stemming**), aspects multi-langues, classification de documents, recherche d'information
- **Bio-informatique** : pré-traitement important, classification (structures secondaires de protéines)
- Catégorisation de textes, reconnaissance de caractères manuscrits, détection de visages/piétons, diagnostic médical (ex. cancer du sein), classification de protéines, prévision de consommation électrique, indexation de vidéos par mots-clés...

---

## 14. Bilan : forces et limites

### Forces

- Recherche un séparateur linéaire : problème **convexe quadratique** → **optimum global** (pas de minimum local)
- **Adaptatif** : changement automatique d'espace de description (embedding space)
- Séparateur défini **par un ensemble d'exemples** — mais seulement ceux sur la marge (contrairement à un kNN)
- **Combine les avantages** des méthodes **non paramétriques** (s'ajuste automatiquement aux données) et **paramétriques** (résiste bien au sur-apprentissage)
- Conceptuellement : introduit **la marge comme mesure de capacité** ; le kernel trick ouvre les problèmes non linéaires aux méthodes linéaires **bien contrôlées** grâce aux redescriptions virtuelles

### Limites

- **Boîte (relativement) noire** : très difficile d'interpréter ce qui a été appris (vecteurs supports et poids dans un espace de features inconnu)
- Les connaissances a priori ne s'expriment **que par le choix du noyau**
- Mal adapté aux problèmes à **dépendances à longue distance**
- **Un seul niveau de non-linéarité** (vs « deep belief networks »)
- Axes de recherche : **apprendre des noyaux**, **combiner des noyaux**

---

## 15. Pièges à éviter

> 🚩 **Notations** : ne pas confondre $y_i$ (étiquette $\pm 1$), $\alpha_i$ (multiplicateur), $w_i$ (poids), $w_0/b$ (biais). Ne pas écrire la solution avec des « $w_i$ » : c'est $\sum \alpha_i^* u_i \kappa(\mathbf{x}_i, \mathbf{x}) + w_0^*$.

> 🚩 **Marge** : largeur totale $= 2/\|\mathbf{w}\|$ ; distance hyperplan→bord de marge $= 1/\|\mathbf{w}\|$. Maximiser la marge $=$ minimiser $\frac{1}{2}\|\mathbf{w}\|^2$ (le $\frac{1}{2}$ est là pour dériver proprement, ça ne change pas l'optimum).

> 🚩 **Primal vs dual** : le primal **minimise** $\frac{1}{2}\|\mathbf{w}\|^2$ ; le dual **maximise** en $\alpha$. Contraintes du dual : $\alpha_i \geq 0$ (hard) ou $0 \leq \alpha_i \leq C$ (soft), et toujours $\sum \alpha_i u_i = 0$.

> 🚩 **Vecteurs supports** : points avec $\alpha_i \neq 0$, c.-à-d. **sur la marge** ($y_i(\mathbf{w}\cdot\mathbf{x}_i + w_0) = 1$) — pas « les plus proches de la frontière » en général, et pas les points d'une classe seulement.

> 🚩 **PAC** : la garantie tient **avec probabilité $> 1-\delta$** (et non $\leq 1-\delta$). $\delta$ = confiance ; $\gamma$ = marge ; ne pas mélanger.

> 🚩 **Dimension VC** : $d_{VC} = \max\{m : \Pi_\mathcal{H}(m) = 2^m\}$, pas un rapport $|H|/n$. $d_{VC}$(hyperplans en dim $d$) $= d+1$.

> 🚩 **Bornes de généralisation** : version VC → dépend de $d$, inexploitable en grande dimension ; version marge → dépend de $(R/\gamma)$, **pas de $d$** ; racine carrée uniquement si $f \notin \mathcal{H}$.

> 🚩 **Noyau** : $k(\mathbf{x},\mathbf{z}) = \langle\phi(\mathbf{x}),\phi(\mathbf{z})\rangle$ (**égalité**). Condition de validité : **semi-défini positif** (matrice de Gram). Le « sigmoid kernel » n'en est pas vraiment un.

> 🚩 **Gaussien** : $k_G = \exp(-\|\mathbf{x}-\mathbf{z}\|^2/2\sigma^2)$ — **positif**, le signe moins est dans l'exposant. Petit $\sigma$ ⇒ plus de vecteurs supports ⇒ risque de sur-apprentissage.

> 🚩 **$C$** : grand $C$ = les erreurs coûtent cher = marge exigée grande mais risque de **sur-apprentissage** (moins de régularisation) ; petit $C$ = tolérant = plus régulier mais risque de sous-apprentissage. Toujours choisi par validation croisée.

> 🚩 **$R_{emp} = 0$ ne prouve rien** : sur le damier, les deux valeurs de $\sigma$ donnent $R_{emp}=0$ avec des qualités très différentes. Se méfier aussi : un SVM qui sépare parfaitement avec 90 % de vecteurs supports est en sur-apprentissage (règle perso : $\leq$ 25 % de SV).

> 🚩 **Cover** : c'est $m < 2(d+1)$ avec $d$ **grand** qui rend la séparabilité probable — pas « n'importe quelle projection » : c'est l'**augmentation de dimension** qui aide (à nombre de points fixé).

---

## 16. Quiz d'auto-test

Réponds d'abord de tête, puis clique sur la question pour afficher la réponse. Pondération indicative entre crochets (plus de points = plus important).

<details>
<summary><b>Question 1 [3 pts] :</b> Écrire le problème primal du SVM linéaire (marge dure) et la fonction de décision qui en découle. <i>(Cliquez ici pour la réponse)</i></summary>
<br>

Minimiser $\frac{1}{2}\|\mathbf{w}\|^2$ sous contraintes $u_i(\mathbf{w}^\top\mathbf{x}_i + w_0) \geq 1$, $i = 1, \dots, m$ ; puis $h(\mathbf{x}) = \text{sign}\{\mathbf{w}^{*\top}\mathbf{x} + w_0^*\}$.

- $\mathbf{w}$ : vecteur de poids ; $w_0$ : biais ; $u_i = y_i \in \{-1,+1\}$ ; $m$ : nb d'exemples
- Problème quadratique convexe sous contraintes linéaires → optimum global, algorithmes efficaces
</details>

<details>
<summary><b>Question 2 [2 pts] :</b> Quelle est la largeur de la marge ? Pourquoi minimise-t-on $\frac{1}{2}\|\mathbf{w}\|^2$ plutôt que $2/\|\mathbf{w}\|$ ? <i>(Cliquez ici pour la réponse)</i></summary>
<br>

Largeur $= 2/\|\mathbf{w}\|$ (distance hyperplan→bord de marge : $1/\|\mathbf{w}\|$), obtenue par $(\mathbf{x}_+ - \mathbf{x}_-) \cdot \frac{\mathbf{w}}{\|\mathbf{w}\|}$.

- Maximiser $2/\|\mathbf{w}\|$ $\iff$ minimiser $\|\mathbf{w}\|$ ; le $\frac{1}{2}\|\mathbf{w}\|^2$ équivalent est différentiable et strictement convexe (dérivée $= \mathbf{w}$) — même optimum.
</details>

<details>
<summary><b>Question 3 [3 pts] :</b> Écrire le problème dual (objectif + contraintes). Que donne l'annulation de $\partial L/\partial \mathbf{w}$ ? <i>(Cliquez ici pour la réponse)</i></summary>
<br>

$$\underset{\alpha}{\text{Max}}\left[\sum_{i=1}^{m}\alpha_i - \frac{1}{2}\sum_{i,j=1}^{m}\alpha_i\alpha_j\, u_i u_j\, \langle\mathbf{x}_i, \mathbf{x}_j\rangle\right] \quad \text{avec} \quad \alpha_i \geq 0, \quad \sum_{i=1}^{m}\alpha_i u_i = 0$$

- $\partial L/\partial\mathbf{w} = \mathbf{w} - \sum_i \alpha_i y_i \mathbf{x}_i = 0$ donne $\mathbf{w}^* = \sum_i \alpha_i y_i \mathbf{x}_i$ (**representer theorem**) ; $\partial L/\partial w_0 = 0$ donne $\sum_i \alpha_i y_i = 0$
- Les données n'interviennent **que par produits scalaires** → clé du kernel trick
</details>

<details>
<summary><b>Question 4 [2 pts] :</b> Que disent les conditions de KKT sur les $\alpha_i$ ? Qu'est-ce qu'un vecteur support ? <i>(Cliquez ici pour la réponse)</i></summary>
<br>

KKT : $\alpha_i > 0$ seulement pour les points sur la marge ($y_i(\mathbf{w}\cdot\mathbf{x}_i + w_0) = \pm 1$) ; tous les autres ont $\alpha_i = 0$. Un **vecteur support** est un point avec $\alpha_i \neq 0$ — eux seuls définissent l'hyperplan, la solution est **parcimonieuse (sparse)**.
</details>

<details>
<summary><b>Question 5 [2 pts] :</b> Comment calcule-t-on $w_0$ une fois les $\alpha_i$ trouvés ? <i>(Cliquez ici pour la réponse)</i></summary>
<br>

Via un vecteur support $(\mathbf{x}_c, y_c)$ : $w_0 = y_c - \mathbf{w}^\top\mathbf{x}_c = y_c - \sum_i y_i\alpha_i\, \mathbf{x}_i^\top\mathbf{x}_c$ ; mieux : moyenne sur deux vecteurs supports de classes opposées $\mathbf{x}_A$ ($+$) et $\mathbf{x}_B$ ($-$) :

$$w_0^* = -\frac{1}{2}\sum_{i=1}^{n} y_i\alpha_i^*(\mathbf{x}_i^\top\mathbf{x}_A + \mathbf{x}_i^\top\mathbf{x}_B)$$
</details>

<details>
<summary><b>Question 6 [3 pts] :</b> Donner la perte hinge, expliquer son nom et son comportement (où est-elle nulle ? comment croît-elle ?). <i>(Cliquez ici pour la réponse)</i></summary>
<br>

$$\ell(y, h(\mathbf{x})) = \max(0, 1 - y\,h(\mathbf{x})) = (1 - y\,h(\mathbf{x}))_+ = \xi$$

- « Hinge = coude » : **nulle** si $y\,h(\mathbf{x}) \geq 1$ (bien classé hors marge), puis croît **linéairement** dès qu'on entre dans la marge (jusqu'à $\infty$)
- $\xi$ : variable ressort (slack) ; c'est la **fonction de perte de substitution (surrogate)** du SVM, avec de bonnes justifications théoriques
</details>

<details>
<summary><b>Question 7 [3 pts] :</b> Écrire le problème soft-margin (avec les $\xi_i$). Rôle de $C$ ? Effet d'un $C$ grand vs petit (biais, variance) ? <i>(Cliquez ici pour la réponse)</i></summary>
<br>

Minimiser $\|\mathbf{w}\|^2 + C\sum_{i=1}^{n}\xi_i$ sous contraintes $(\langle\mathbf{w}, X_i\rangle + b)Y_i \geq 1 - \xi_i$.

- $C$ grand : les erreurs coûtent cher → marge exigée grande, **biais fort / variance faible**, risque de sur-apprentissage ; $C$ petit : tolérant → **biais faible / variance grande**, risque de sous-apprentissage
- $C$ contrôle le compromis biais-variance, choisi par **validation croisée**. Le développement de $\mathbf{w}$ sur les vecteurs supports reste valide ; au dual s'ajoute $0 \leq \alpha_i \leq C$
</details>

<details>
<summary><b>Question 8 [2 pts] :</b> Écrire le critère $w^* = \text{ArgMin}[\dots]$ qui combine risque empirique et marge, et identifier chaque terme. <i>(Cliquez ici pour la réponse)</i></summary>
<br>

$$\mathbf{w}^{*} = \underset{\mathbf{w}}{\text{ArgMin}} \left[ \underbrace{\sum_{i=1}^{m}|1 - y_i h(\mathbf{x}_i)|_+}_{\text{risque empirique}} + \underbrace{\frac{1}{2}\mathbf{w}^\top\mathbf{w}}_{\text{marge}} \right]$$

- C'est un **risque empirique régularisé** $h^* = \text{ArgMin}_{h\in\mathcal{H}}[R_{Emp}(h) + \lambda\,reg(h)]$ : la forme de la fonction de coût induit la régularisation ; la hinge agit comme régularisateur
</details>

<details>
<summary><b>Question 9 [3 pts] :</b> Donner la borne de généralisation via la dimension VC pour un perceptron, puis la borne via la marge ($f \in \mathcal{H}$, puis $f \notin \mathcal{H}$). Pourquoi la seconde délivre-t-elle les SVM en grande dimension ? <i>(Cliquez ici pour la réponse)</i></summary>
<br>

VC ($d_{VC} = d+1$) : $R(h) \leq \hat{R}(h) + \sqrt{\frac{2(d+1)\log\frac{em}{d+1}}{m}} + \sqrt{\frac{\log\frac{1}{\delta}}{2m}}$ — **non-informative quand $d$ est grand devant $m$**.

Marge, si $f \in \mathcal{H}$ : $R(h) \leq \mathcal{O}\left(\frac{(\frac{R}{\gamma})^2\ln^2 m + \ln\frac{1}{\delta}}{m}\right)$ ; si $f \notin \mathcal{H}$ (avec racine carrée et $\hat{R}$) : $R(h) \leq \hat{R}(h) + \mathcal{O}\left(\sqrt{\frac{(\frac{R}{\gamma})^2\ln^2 m + \ln\frac{1}{\delta}}{m}}\right)$.

- $R$ : rayon de la plus petite sphère englobant les exemples ; $\gamma$ : marge ; $\delta$ : confiance ; $m$ : nb d'exemples
- La capacité dépend du rapport $R/\gamma$, **pas de $d$** → valable même en dimension infinie, ce qui rend possibles les méthodes à noyaux
</details>

<details>
<summary><b>Question 10 [2 pts] :</b> Donner la borne de généralisation en fonction du nombre de vecteurs supports. Que peut-on en conclure comme diagnostic ? <i>(Cliquez ici pour la réponse)</i></summary>
<br>

Avec probabilité $1-\delta$ sur $m$ exemples :

$$R(h) \leq \frac{1}{m - \#sv}\left(\#sv \log\frac{e\,m}{\#sv} + \log\frac{m}{\delta}\right)$$

- Moins de SV ⇒ meilleure borne ⇒ meilleure généralisation ; beaucoup de SV ⇒ sur-apprentissage probable (règle perso : $\leq$ 25 % des points en SV)
</details>

<details>
<summary><b>Question 11 [2 pts] :</b> Énoncer le théorème de Cover ($\mathcal{O}(m,d)$) et ses deux conséquences sur $m$ vs $2(d+1)$. <i>(Cliquez ici pour la réponse)</i></summary>
<br>

$\mathcal{O}(m,d) = 2\sum_{i=0}^{d}\binom{m-1}{i}$ = nombre de groupements de $m$ points de $\mathbb{R}^d$ séparables par des hyperplans de dimension $(d-1)$, toutes combinaisons confondues.

- Si $m > 2(d+1)$ : la probabilité de séparabilité linéaire devient **petite**
- Si $d$ est grand et $m < 2(d+1)$ : la probabilité qu'**un groupement quelconque** en deux classes soit linéairement séparable **tend vers 1**
</details>

<details>
<summary><b>Question 12 [3 pts] :</b> Définition d'une fonction noyau. Quelle condition doit satisfaire la matrice de Gram pour que le kernel trick soit valide ? <i>(Cliquez ici pour la réponse)</i></summary>
<br>

$$k : \mathcal{X} \times \mathcal{X} \to \mathbb{R}, \qquad \forall \mathbf{x}, \mathbf{z} \in \mathcal{X} : \quad k(\mathbf{x}, \mathbf{z}) = \langle\phi(\mathbf{x}), \phi(\mathbf{z})\rangle$$

- $\phi : \mathbf{x} \mapsto \phi(\mathbf{x}) \in F$ : application de redescription ; $F$ : espace muni d'un produit scalaire
- Validité : la matrice de Gram $K$ doit être **semi-définie positive**
</details>

<details>
<summary><b>Question 13 [2 pts] :</b> Écrire la fonction de décision du SVM à noyau. Pourquoi la méthode est-elle « insensible à la dimension » ? <i>(Cliquez ici pour la réponse)</i></summary>
<br>

$$h^*(\mathbf{x}) = \text{sign}\left\{\sum_{i \in \mathcal{P}_S}\alpha_i^* u_i\, \kappa(\mathbf{x}_i, \mathbf{x}) + w_0^*\right\}$$

- On ne manipule que des valeurs de noyau (produits scalaires implicites), jamais $\phi$ ni la dimension de $F$ — même infinie (RBF) ; les calculs restent de dimension restreinte alors qu'on passe implicitement en très grande dimension
</details>

<details>
<summary><b>Question 14 [2 pts] :</b> Donner l'espace de redescription $\phi$ associé à $k(\mathbf{x},\mathbf{z}) = \langle\mathbf{x},\mathbf{z}\rangle^2$ et vérifier l'égalité. L'espace $F$ est-il unique ? <i>(Cliquez ici pour la réponse)</i></summary>
<br>

$\phi(\mathbf{x}) = (x_1^2, x_2^2, \sqrt{2}\,x_1x_2) \in \mathbb{R}^3$ :

$$\langle\phi(\mathbf{x}), \phi(\mathbf{z})\rangle = x_1^2z_1^2 + x_2^2z_2^2 + 2x_1x_2z_1z_2 = (x_1z_1 + x_2z_2)^2 = \langle\mathbf{x},\mathbf{z}\rangle^2$$

- $F$ **n'est pas unique** : le même noyau correspond aussi à $\phi(\mathbf{x}) = (x_1^2, x_2^2, x_1x_2, x_2x_1) \in \mathbb{R}^4$ — seul le noyau compte
</details>

<details>
<summary><b>Question 15 [3 pts] :</b> Citer les 3 familles de noyaux pour vecteurs du cours avec leurs formules. Quelle est la particularité du sigmoid ? du noyau gaussien ? <i>(Cliquez ici pour la réponse)</i></summary>
<br>

- Polynomiaux : $k_{poly1}(\mathbf{x},\mathbf{z}) = (\mathbf{x}^\top\mathbf{z})^d$ (produits d'exactement $d$ variables) et $k_{poly2}(\mathbf{x},\mathbf{z}) = (\mathbf{x}^\top\mathbf{z} + c)^d$ (au plus $d$)
- Gaussien : $k_G(\mathbf{x},\mathbf{z}) = \exp(-d(\mathbf{x},\mathbf{z})^2/2\sigma^2)$ — lié à une **décomposition en série de Fourier** ; **pas de forme close pour $\Phi$**, espace de **dimension infinie**
- Sigmoid : $\tanh(\kappa\,\mathbf{x}^\top\mathbf{z} + \theta)$ — **pas définie positive** (pas un vrai noyau), mais proche des fonctions de décision des réseaux de neurones (fonctionne en pratique sans valider la théorie)
</details>

<details>
<summary><b>Question 16 [2 pts] :</b> Donner les règles de diagnostic liées (a) au nombre de vecteurs supports, (b) à la matrice de Gram (hors-diagonale petites, matrice uniforme). <i>(Cliquez ici pour la réponse)</i></summary>
<br>

(a) Moins de SV = mieux (généralisation, régularité de la séparatrice) — règle perso : $\leq$ 25 % des points, sinon gros problème (souvent moins en réalité) ; toutefois le vrai critère est la marge.

(b) Pas de structure dans $G$ → aucune régularité exploitable ; termes hors-diagonale très petits → **sur-apprentissage** ; matrice uniforme → **sous-apprentissage** (tout dans la même classe).
</details>

<details>
<summary><b>Question 17 [2 pts] :</b> SVR : fonction de perte, problème à minimiser, forme de la solution. <i>(Cliquez ici pour la réponse)</i></summary>
<br>

Perte $\varepsilon$-insensible : $|y - f(\mathbf{x})|_\varepsilon = \max\{0, |y - f(\mathbf{x})| - \varepsilon\}$ ; avec $f(\mathbf{x}) = \mathbf{w}\cdot\mathbf{x} + w_0$, minimiser :

$$\frac{1}{2}\|\mathbf{w}\|^2 + C\sum_{i=1}^{m}|y_i - f(\mathbf{x}_i)|_\varepsilon$$

Solution généralisée : $f(\mathbf{x}) = \sum_{i=1}^{m}(\alpha_i^{*} - \alpha_i)K(\mathbf{x}_i, \mathbf{x}) + w_0$ — deux multiplicateurs par exemple (un par côté du tube), seuls les points hors du tube comptent.
</details>

<details>
<summary><b>Question 18 [2 pts] :</b> Quelles sont les limites des SVM (au moins 3) ? <i>(Cliquez ici pour la réponse)</i></summary>
<br>

- **Boîte noire** : très difficile d'interpréter ce qui a été appris (vecteurs supports et poids dans un espace de features inconnu)
- Les connaissances a priori ne s'expriment **que par le choix du noyau**
- Mal adapté aux **dépendances à longue distance** ; **un seul niveau de non-linéarité** (vs « deep belief networks »)
- Axes de recherche : apprendre des noyaux, combiner des noyaux
</details>

<details>
<summary><b>Question 19 [2 pts] :</b> Donner l'exemple du noyau sur les chaînes de caractères : que représente $K(CHAT, CARTON) = 2\varepsilon^5 + \varepsilon^8$ ? Quelle version préférer ? <i>(Cliquez ici pour la réponse)</i></summary>
<br>

$\Phi$ projette sur $\mathbb{R}^D$ avec $D = |\Sigma|^n$ (tous les $n$-grammes) ; chaque $n$-gramme commun contribue pour le produit des poids : $CA$ : $\varepsilon^3\cdot\varepsilon^2 = \varepsilon^5$ ; $AT$ : $\varepsilon^2\cdot\varepsilon^3 = \varepsilon^5$ ; $CT$ : $\varepsilon^4\cdot\varepsilon^4 = \varepsilon^8$ ($CH$ absent de CARTON) — d'où $2\varepsilon^5 + \varepsilon^8$.

On préfère la version **normalisée** : $\kappa(s,s') = \frac{K(s,s')}{\sqrt{K(s,s)K(s',s')}}$.
</details>

<details>
<summary><b>Question 20 [1 pt] :</b> Citer deux tâches (hors classification binaire) auxquelles s'étendent les méthodes à noyaux. <i>(Cliquez ici pour la réponse)</i></summary>
<br>

Régression (SVR), détection de nouveautés (séparer le nuage de l'origine), classification multi-classes, **ACP non linéaire** — c'est la **kernelisation d'une méthode linéaire** : toute méthode n'utilisant les données que via des produits scalaires (découplage algorithme / description des données).
</details>