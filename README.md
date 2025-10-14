# Analyse Numérique : Outils de Résolution de Systèmes Linéaires

Ce projet est une application de bureau interactive qui implémente et compare les méthodes de résolution de systèmes linéaires. Il permet de visualiser et de comparer les algorithmes de Jacobi et Gauss-Seidel avec des graphiques de convergence en temps réel.

## Fonctionnalités

- **Interface Graphique Optimisée** : Interface focalisée sur la visualisation des courbes de convergence.
- **Algorithmes Implémentés** : 
  1. **Méthode de Jacobi** : Algorithme itératif classique pour résoudre Ax = b
  2. **Méthode de Gauss-Seidel** : Amélioration de Jacobi utilisant les valeurs déjà calculées
  3. **Méthode de Newton** : Résolution de systèmes non-linéaires f(x) = 0
- **Visualisation Interactive** : 2 graphiques principaux - convergence des erreurs et comparaison des solutions
- **Systèmes Prédéfinis** : 4 systèmes de test de différentes tailles (2x2 à 5x5)
- **Contrôles Clavier** : Navigation rapide avec les touches N (système suivant) et R (recalculer)

## Structure du Projet

### Dossier Principal
-   `analyse_numerique_gui.py`: **Application d'Interpolation** - Interface graphique pour l'interpolation de Lagrange et les splines quadratiques.

### Dossier Jacobi/
-   `gauss-jacobi.py`: **Application Principale** - Interface graphique complète pour la comparaison des méthodes de Jacobi et Gauss-Seidel. C'est le script principal à utiliser pour l'analyse des systèmes linéaires.

-   `jacobi_newton.py`: **Méthode de Newton** - Implémentation de la méthode de Newton en dimension n > 1 utilisant l'algorithme de Jacobi pour résoudre les systèmes linéaires.

-   `algorithms.py`: **Algorithmes de Base** - Implémentation des méthodes de Jacobi, Gauss-Seidel et SOR avec historique pour les graphiques.

-   `jacobi_gui.py`: **Interface Alternative** - Interface graphique complète avec saisie manuelle des données.

-   `test_algorithms.py`: **Tests Complets** - Script de test pour valider les algorithmes et comparer les performances.

-   `main.py`: **Point d'Entrée** - Script de lancement pour l'interface graphique des algorithmes.

### Fichiers d'Interpolation
-   `spline_quadratique.py`: **Splines Quadratiques** - Implémentation de l'approximation par spline quadratique.
-   `lagrange.py`: **Interpolation de Lagrange** - Implémentation de l'interpolation polynomiale de Lagrange.
-   `comparaison_interpolation.py`: **Comparaison** - Script de comparaison des méthodes d'interpolation.

-   `requirements.txt`: La liste des dépendances Python (`numpy`, `matplotlib`, `sympy`, `tkinter`) nécessaires pour exécuter le projet.

## Installation

1.  **Clonez le dépôt** ou téléchargez les fichiers.

2.  **Créez un environnement virtuel** (recommandé) :
    ```bash
    python -m venv env
    source env/bin/activate  # Sur Windows: env\Scripts\activate
    ```

3.  **Installez les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```

## Dépendances

-   `numpy`
-   `matplotlib`
-   `sympy`
-   `tkinter` (inclus dans la bibliothèque standard de Python)

## Utilisation

### Application Principale - Algorithmes de Jacobi et Gauss-Seidel

Pour lancer l'application principale de comparaison des méthodes de résolution :

```bash
python Jacobi/gauss-jacobi.py
```

**Contrôles :**
- **N** : Changer de système (4 systèmes prédéfinis)
- **R** : Recalculer les courbes
- **Barre d'outils** : Zoom, pan, sauvegarde, etc.

**Graphiques affichés :**
1. **Convergence des Erreurs** : Évolution de l'erreur ||x|| au cours des itérations
2. **Comparaison des Solutions** : Solutions trouvées par Jacobi, Gauss-Seidel et solution exacte

### Application d'Interpolation

Pour lancer l'application d'interpolation :

```bash
python analyse_numerique_gui.py
```

**Utilisation :**
1. **Entrez une fonction** dans le champ de texte (ex: `x**3 - cos(x)`)
2. **Sélectionnez un mode d'analyse** (Comparer Erreurs, Lagrange, ou Spline Quadratique)
3. **Cliquez sur "Générer le graphique"** pour afficher les résultats

### Autres Applications

```bash
# Méthode de Newton
python Jacobi/jacobi_newton.py

# Tests des algorithmes
python Jacobi/test_algorithms.py

# Interface alternative avec saisie manuelle
python Jacobi/main.py
```

## Algorithmes Implémentés

### Méthode de Jacobi
Algorithme itératif classique pour résoudre le système linéaire **Ax = b** :
```
x_i^(k+1) = (b_i - Σ(j≠i) a_ij * x_j^(k)) / a_ii
```

### Méthode de Gauss-Seidel
Amélioration de Jacobi utilisant les valeurs déjà calculées dans la même itération :
```
x_i^(k+1) = (b_i - Σ(j<i) a_ij * x_j^(k+1) - Σ(j>i) a_ij * x_j^(k)) / a_ii
```

### Méthode de Newton
Résolution de systèmes non-linéaires **f(x) = 0** en dimension n > 1 :
1. Calcul de la Jacobienne ∇f(x)
2. Résolution du système linéaire ∇f(x) * y = -f(x) par Jacobi
3. Mise à jour x ← x - y

## Systèmes de Test

Le projet inclut 4 systèmes prédéfinis :
1. **Système 4x4** : Matrice à diagonale dominante classique
2. **Système 3x3** : Système tridiagonal
3. **Système 5x5** : Système plus grand
4. **Système 2x2** : Système simple pour tests rapides

## Caractéristiques Techniques

- **Convergence** : Toutes les méthodes incluent des critères de convergence
- **Visualisation** : Graphiques interactifs avec matplotlib
- **Performance** : Comparaison automatique des temps de convergence
- **Robustesse** : Gestion d'erreurs et validation des données

## Licence

Ce projet est destiné à un usage éducatif dans le cadre d'un cours d'analyse numérique.