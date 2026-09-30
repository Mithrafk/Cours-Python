# Fiche de Révision : Évaluation et Comparaison d'Algorithmes

## Sommaire
1. [Principes Généraux de l'Évaluation](#1-principes-généraux-de-lévaluation)
2. [Gestion des Données et Méthodes d'Échantillonnage](#2-gestion-des-données-et-méthodes-déchantillonnage)
3. [Mesurer la Performance : Matrice et Métriques](#3-mesurer-la-performance--matrice-et-métriques)
4. [La Courbe ROC](#4-la-courbe-roc)
5. [Intervalles de Confiance (Un Algorithme)](#5-intervalles-de-confiance-un-algorithme)
6. [Tests Statistiques : Comparaison d'Algorithmes](#6-tests-statistiques--comparaison-dalgorithmes)
7. [Pièges à Éviter](#7-pièges-à-éviter)
8. [Quizz d'Auto-Évaluation](#8-quizz-dauto-évaluation)

---

## 1. Principes Généraux de l'Évaluation

Évaluer un modèle d'apprentissage est indispensable car l'induction est faillible. Il n'existe pas de "meilleur" algorithme dans l'absolu (théorème du *No Free Lunch*).

> 💡 **Le but de l'évaluation**
> - Estimer la performance d'un système sur une tâche.
> - Comparer deux systèmes entre eux.
> - Régler les hyperparamètres (paramètres contrôlables).

> 🔎 **Complément : La critique des "Benchmarks"**
> L'évaluation moderne en IA (comme les LLMs) repose trop sur les benchmarks. Bien qu'efficaces pour filtrer l'état de l'art, ils restreignent la vision globale (on cherche "sous le lampadaire" ce qui est facile à mesurer). Ils peinent notamment à évaluer la créativité ou l'amélioration continue des représentations internes (contrairement au cerveau humain).

L'évaluation doit composer avec des **facteurs contrôlables** (choix de l'algorithme, hyperparamètres) et des **facteurs incontrôlables** (bruit, tirage aléatoire des données, initialisation aléatoire).

On distingue deux types d'erreurs :
*   **L'erreur d'apprentissage (Risque empirique) $\hat{e}_S$ :** Mesurée sur les données de test.
*   **L'erreur vraie (Risque réel) $e_D$ :** La véritable erreur sur toute la distribution des données (inaccessible en pratique).

---

## 2. Gestion des Données et Méthodes d'Échantillonnage

Pour éviter le **sur-apprentissage** (overfitting : l'erreur d'entraînement diminue mais l'erreur de test remonte), il faut scinder les données intelligemment.

### 2.1. Le découpage classique (Hold-out)

Si l'on possède beaucoup de données, on divise le jeu en trois :

> 📝 **Tes notes (validées et précisées)**
> - **Apprentissage (Train) :** pour fiter (entraîner) le modèle.
> - **Validation :** pour la recherche des bons hyperparamètres et décider quand arrêter l'apprentissage.
> - **Test :** pour calculer la performance finale (le plus important, sinon on a une fuite de données / *data leakage*).

### 2.2. Méthodes pour "Peu de données"

Quand les données sont limitées, un simple découpage 50/50 ou 80/20 est trop soumis au hasard du tirage (haute variance).

#### La Validation Croisée à $k$ plis ($k$-fold CV)
On divise les données en $k$ sous-ensembles (plis). On entraîne sur $k-1$ plis et on teste sur le pli restant. On répète $k$ fois et on moyenne les erreurs.
> 📝 **Tes notes**
> Estimateur non biaisé car on teste sur des plis non recouverts.

> 🔎 **Complément : Que faire après une CV ?**
> 📝 **Tes notes mentionnent :** "Soit on fait voter les modèles, soit on refait un modèle sur toutes les données... Risqué car l'algo peut partir sur un min local."
> **Précision :** En pratique, ré-entraîner sur *toutes* les données avec les hyperparamètres trouvés est la norme. Le vrai risque souligné par la théorie est que l'on ne possède plus de jeu de test indépendant pour évaluer *ce* modèle final, on doit supposer que sa performance est au moins égale à la moyenne de la CV.

#### Le Leave-One-Out (LOO)
C'est une validation croisée où $k = m$ (le nombre total de données).
*   **Avantage :** Faible biais.
*   **Inconvénients :** Très coûteux en calcul, variance très haute.
> 📝 **Tes notes**
> Tend à sous-estimer l'erreur si les données ne sont pas vraiment i.i.d (indépendantes et identiquement distribuées).

#### Le Bootstrap
On crée $k$ ensembles d'apprentissage de taille $m$ par tirage *avec remise* dans les données initiales.
> 📝 **Tes notes (corrigées)**
> "Ici biaisé. Estimation de erreur = m-e sur k ens. de test + m-e sur ensemble total"
> 🔎 **Pourquoi est-ce biaisé ?** Étant donné le tirage avec remise, un ensemble d'apprentissage Bootstrap ne contient en moyenne que $\approx 63.2\%$ des données uniques originales. Le modèle est donc entraîné sur moins de diversité réelle, ce qui biaise l'estimation de l'erreur à la hausse. Pour corriger cela, on utilise souvent l'estimateur $.632$ Bootstrap.

---

## 3. Mesurer la Performance : Matrice et Métriques

### 3.1. Matrice de confusion (pour 2 classes)

| | Prédiction : Positif (+) | Prédiction : Négatif (-) |
| :--- | :--- | :--- |
| **Réalité : Positif (+)** | **VP** (Vrai Positif / TP) | **FN** (Faux Négatif) |
| **Réalité : Négatif (-)** | **FP** (Faux Positif) | **VN** (Vrai Négatif / TN) |

### 3.2. Métriques issues de la matrice

> 📝 **Tes notes (Mises en forme)**

*   **Accuracy (Taux de bonne prédiction / Exactitude)** :
    $$Accuracy = \frac{VP + VN}{VP + VN + FP + FN} = 1 - \text{Taux d'erreur}$$
    *   $VP, VN, FP, FN$ : Éléments de la matrice de confusion.

*   **Rappel (Recall / Sensibilité / TPR - True Positive Rate)** :
    $$TPR = \frac{VP}{VP + FN}$$
    *   $VP$ : Vrais positifs (Alertes bien détectées).
    *   $FN$ : Faux négatifs (Alertes ratées).

*   **Précision (Taux d'alerte à raison)** :
    $$Precision = \frac{VP}{VP + FP}$$

*   **FPR (False Positive Rate / Fausse alerte)** :
    $$FPR = \frac{FP}{FP + VN}$$

*   **F-Measure (ou F1-score, moyenne harmonique)** :
    $$F_1 = \frac{2 \times Precision \times Rappel}{Precision + Rappel} = \frac{2 VP}{2 VP + FP + FN}$$

> ⚠️ **Attention**
> La performance doit se lire selon l'objectif. Un modèle peut avoir 99% d'Accuracy s'il prédit toujours "Sain" pour une maladie rare (1% de cas). Dans ce cas, le modèle est inutile. Il faut regarder la Précision et le Rappel.

---

## 4. La Courbe ROC

La courbe ROC (Receiver Operating Characteristic) évalue un classifieur dont la sortie est un score (ou une probabilité) en faisant varier le **seuil de décision** de 0 à 1.

*   **Axe Y :** $TPR$ (Rappel / Sensibilité)
*   **Axe X :** $FPR$ (Taux de faux positifs = 1 - Spécificité)

> 💡 **Principe**
> Arbitrer entre les erreurs de Type I (Faux Positifs, $\alpha$) et de Type II (Faux Négatifs, $\beta$). Un seuil "laxiste" augmente le TPR mais aussi le FPR. Un seuil "sévère" diminue le FPR mais fait chuter le TPR.

> 📝 **Tes notes**
> - **Courbe en escalier :** Si on trie les exemples par score décroissant, chaque nouvel exemple met à jour la courbe. Si c'est un vrai positif, on monte d'un cran (en haut). Si c'est un faux positif, on va à droite.
> - **Meilleur modèle :** Forme de "rectangle", passe par le point $(0,1)$ parfait.
> - **Pire modèle :** Diagonale $y=x$ (ligne de hasard, pertinence = 0.5).
> - **AUC (Area Under the Curve) :** L'intégrale de la courbe. Donne la performance globale du modèle (indépendante du seuil) en un seul chiffre entre 0.5 et 1.

---

## 5. Intervalles de Confiance (Un Algorithme)

Pour estimer la vraie erreur $e_D$ à partir de l'erreur de test $\hat{e}_S$ mesurée sur un échantillon de taille $m$, on utilise des intervalles de confiance.

**Hypothèses :**
- Les erreurs suivent une loi Binomiale.
- Si $m \times \hat{e}_S \times (1 - \hat{e}_S) \ge 5$, on peut estimer la loi binomiale par une loi Normale de moyenne $\mu = \hat{e}_S$ et d'écart-type $\sigma = \sqrt{\frac{\hat{e}_S(1-\hat{e}_S)}{m}}$.

**Formule de l'intervalle de confiance :**
Pour une probabilité de confiance $N\%$, la vraie erreur $e_D$ se trouve dans l'intervalle :
$$ e_D \in \left[ \hat{e}_S - Z_N \sqrt{\frac{\hat{e}_S(1-\hat{e}_S)}{m}} \ ; \ \hat{e}_S + Z_N \sqrt{\frac{\hat{e}_S(1-\hat{e}_S)}{m}} \right] $$

*   $\hat{e}_S$ : Erreur empirique mesurée sur le test.
*   $m$ : Nombre d'exemples dans l'ensemble de test (nécessite $m \ge 30$).
*   $Z_N$ : Coefficient lié à la loi normale (ex: **$Z_{95\%} = 1.96$**).

---

## 6. Tests Statistiques : Comparaison d'Algorithmes

Comment savoir si l'algorithme A est *vraiment* meilleur que B, et non par simple hasard ? On pose l'hypothèse nulle $H_0$ : "Il n'y a pas de différence de performance", et on cherche à la rejeter (via une p-value < $\alpha$, souvent $\alpha = 0.05$).

### 6.1. Comparaison de 2 algorithmes sur UN MÊME jeu de données

#### A. Le Two-Matched-Sample t-test (T-test couplé)
Utilisé avec une validation croisée à $k$ plis. On calcule la différence des erreurs $\Delta_i = e_i^A - e_i^B$ sur chaque pli $i$.

**Hypothèse :** La distribution des différences de moyenne tend vers une loi Normale.
**Formule de la statistique $\tau_t$ :**
$$ \tau_t = \frac{\sqrt{k} \cdot \mu}{\sigma} $$
*   $k$ : nombre de plis de la validation croisée.
*   $\mu$ : moyenne des différences $\Delta_i$.
*   $\sigma$ : écart-type des différences $\Delta_i$.

Si $\tau_t \notin [-t_{\alpha/2, k-1}, t_{\alpha/2, k-1}]$, on rejette $H_0$. A et B sont significativement différents.
> 🚩 **Piège fréquent :** Les $\Delta_i$ d'une 10-CV classique ne sont pas i.i.d. (les données d'entraînement se chevauchent). Dietterich (1998) recommande plutôt une **$5 \times 2$ CV couplée** pour respecter les hypothèses du t-test.

#### B. Le Test de McNemar
Compare directement les classifications croisées de A et B, en ne regardant que les exemples où les modèles *sont en désaccord*.
$$ \tau_{\chi^2} = \frac{(|e_{01} - e_{10}| - 1)^2}{e_{01} + e_{10}} $$
*   $e_{01}$ : nombre d'exemples où A a faux et B a bon.
*   $e_{10}$ : nombre d'exemples où A a bon et B a faux.
*   Suit une loi du $\chi^2$. Si $\tau_{\chi^2} > \chi^2_\alpha$, on rejette $H_0$.

### 6.2. Comparaison de 2 algorithmes sur PLUSIEURS jeux de données

> ⚠️ **Attention**
> Sur plusieurs jeux de données, les taux d'erreur ne suivent plus une loi Normale. Il faut utiliser des **tests non-paramétriques**.

#### Le test de rang signé de Wilcoxon
Basé sur le *rang* des différences de performance (au lieu de la valeur absolue).
1. On calcule $d_i = \text{Perf}(A) - \text{Perf}(B)$ sur chaque jeu $i$.
2. On trie les valeurs absolues $|d_i|$ et on leur attribue un rang.
3. On somme les rangs où $d_i > 0$ ($W_{s1}$) et ceux où $d_i < 0$ ($W_{s2}$).
4. $T_{wilcox} = \min(W_{s1}, W_{s2})$. On compare $T_{wilcox}$ à une table critique (ou par approximation Normale si $n \ge 25$).

### 6.3. Comparaison de N algorithmes sur PLUSIEURS jeux de données

Comparer les algos 2 à 2 fausse les probabilités (problème des tests multiples). On utilise un test "Post Hoc".

#### Le test de Nemenyi
Il cherche quels algorithmes sont effectivement différents après qu'un test global ait détecté une différence.
1. On calcule le rang moyen de chaque algo sur tous les jeux de données : $\overline{R}_{\cdot j}$.
2. On calcule la statistique $q$ pour comparer deux algos :
$$ q = \frac{\overline{R}_{\cdot j_1} - \overline{R}_{\cdot j_2}}{\sqrt{\frac{k(k+1)}{6n}}} $$
*   $k$ : nombre d'algorithmes.
*   $n$ : nombre de jeux de données.
3. On rejette $H_0$ si $q > q_\alpha$. 
*On définit souvent une **Différence Critique (CD)** : si l'écart de rang moyen entre deux algos est supérieur à CD, ils sont statistiquement différents (souvent visualisé avec des barres horizontales liant les algos équivalents).*

---

## 7. Pièges à Éviter

*   🚩 **Mélanger Validation et Test :** Régler ses hyperparamètres sur le jeu de test est la pire erreur (fuite de données). Le jeu de test ne doit être vu qu'une seule fois, à la toute fin.
*   🚩 **Oublier les intervalles de confiance :** Une différence de 1% d'Accuracy entre deux modèles n'a aucun sens si l'intervalle de confiance est de $\pm 5\%$.
*   🚩 **Se fier au rang moyen seul (Nemenyi) :** Le rang moyen ne donne aucune information sur l'écart de performance absolue. Un modèle classé 2ème peut être à 0.001% de performance du 1er !
*   🚩 **Mal choisir sa métrique :** Utiliser l'Accuracy sur un jeu de données fortement déséquilibré (ex: 99% classe A, 1% classe B). Le modèle prédisant toujours A aura 99% d'Accuracy mais sera totalement inutile.

---

## 8. Quizz d'Auto-Évaluation

<details>
<summary><b>Question 1 :</b> Quelle est la différence fondamentale entre l'ensemble de Validation et l'ensemble de Test ? <i>(Cliquez ici pour la réponse)</i></</summary>
<br>
L'ensemble de validation sert à <b>choisir</b> les meilleurs hyperparamètres et éviter le sur-apprentissage pendant la phase de développement. L'ensemble de test sert <b>uniquement à la fin</b> pour estimer la performance finale du modèle de façon non biaisée. L'algorithme ne doit prendre aucune décision d'optimisation sur le test.
</details>

<details>
<summary><b>Question 2 :</b> Pourquoi est-il déconseillé d'utiliser le T-test couplé classique pour comparer deux modèles sur une validation croisée à 10 plis (10-CV) ? <i>(Cliquez ici pour la réponse)</i></summary>
<br>
Parce que le t-test suppose que les observations sont indépendantes (i.i.d). Or, dans une 10-CV, les 10 ensembles d'entraînement se chevauchent fortement (90% de données communes à chaque fois), les modèles et leurs erreurs ne sont donc pas statistiquement indépendants. On recommande la méthode 5x2 CV.
</details>

<details>
<summary><b>Question 3 :</b> Quel test statistique utiliser pour comparer 2 algorithmes sur 15 jeux de données différents ? <i>(Cliquez ici pour la réponse)</i></summary>
<br>
Le <b>Test de rang signé de Wilcoxon</b>. On ne peut pas utiliser le t-test car les performances sur des jeux de données de natures différentes ne suivent pas une loi Normale. Le test de Wilcoxon est un test non paramétrique basé sur les rangs.
</details>

<details>
<summary><b>Question 4 :</b> Dans une matrice de confusion, si je veux limiter au maximum les "Fausses Alertes" (FPR), quelle métrique vais-je chercher à maximiser ? <i>(Cliquez ici pour la réponse)</i></summary>
<br>
La <b>Précision</b>. La Précision ($VP / (VP + FP)$) mesure la proportion de prédictions positives qui étaient correctes. Si je la maximise, je réduis drastiquement les Faux Positifs (FP), c'est-à-dire les fausses alertes.
</details>

<details>
<summary><b>Question 5 :</b> Sur une courbe ROC, que représente le point situé aux coordonnées (0, 1) ? <i>(Cliquez ici pour la réponse)</i></summary>
<br>
C'est le <b>classifieur parfait</b>. Un TPR (Taux de Vrais Positifs) de 1 (100% de détection) pour un FPR (Taux de Faux Positifs) de 0 (0 fausse alerte).
</details>