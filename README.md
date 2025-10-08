# Analyse Numérique - Splines Quadratiques

Ce projet implémente l'approximation de fonctions par splines quadratiques en Python, avec une documentation théorique complète.

## Contenu du projet

### Fichiers principaux

1. **: Documentation théorique sur l'approximation polynomiale
2. **[spline_quadratique.py] : Implémentation Python des splines quadratiques
3. **README.md** : Ce fichier

## Théorie

Le projet implémente l'approximation par splines quadratiques, une méthode d'approximation polynomiale par morceaux. 

### Principe

Une spline quadratique S(x) est une fonction définie par morceaux qui vérifie :
- Chaque segment sᵢ(x) est un polynôme de degré 2
- S(x) est continue
- S'(x) est continue
- S(xᵢ) = f(xᵢ) (conditions d'interpolation)

Pour fixer une solution unique, on impose la condition S'(x₀) = 0.

### Formulation mathématique

Chaque segment est exprimé comme :
`sᵢ(x) = aᵢ(x - xᵢ)² + bᵢ(x - xᵢ) + cᵢ`

Avec :
- cᵢ = yᵢ
- bᵢ = zᵢ
- aᵢ = (zᵢ₊₁ - zᵢ) / (2(xᵢ₊₁ - xᵢ))

Les valeurs zᵢ sont calculées récursivement :
- z₀ = 0
- zᵢ₊₁ = 2(yᵢ₊₁ - yᵢ)/(xᵢ₊₁ - xᵢ) - zᵢ

## Implémentation Python

### Fonctions principales

1. **calcul_coefficients_spline_quadratique(x, y)**
   - Calcule les coefficients a, b, c pour chaque segment de la spline quadratique
   - Paramètres : 
     - x : tableau numpy des points xᵢ (doit être trié par ordre croissant)
     - y : tableau numpy des valeurs f(xᵢ) aux points xᵢ
   - Variables internes :
     - n : nombre d'intervalles (n = len(x) - 1)
     - z : tableau des dérivées zᵢ = S'(xᵢ) avec z₀ = 0
   - Processus :
     1. Initialise les tableaux a, b, c de taille n avec des zéros
     2. Initialise le tableau z de taille n+1 avec z₀ = 0
     3. Calcule récursivement tous les zᵢ selon la formule :
        zᵢ₊₁ = 2(yᵢ₊₁ - yᵢ)/(xᵢ₊₁ - xᵢ) - zᵢ
     4. Pour chaque intervalle i, calcule les coefficients :
        - cᵢ = yᵢ
        - bᵢ = zᵢ
        - aᵢ = (zᵢ₊₁ - zᵢ) / (2(xᵢ₊₁ - xᵢ))
   - Retourne : (a, b, c) tableaux numpy de coefficients

2. **evaluer_spline(x_eval, x, a, b, c)**
   - Évalue la spline quadratique en un point donné x_eval
   - Paramètres :
     - x_eval : valeur scalaire où évaluer la spline
     - x : tableau numpy des points xᵢ (doit être le même que pour le calcul des coefficients)
     - a, b, c : tableaux numpy des coefficients obtenus avec calcul_coefficients_spline_quadratique
   - Processus :
     1. Trouve l'intervalle [xᵢ, xᵢ₊₁] contenant x_eval
     2. Gère le cas où x_eval est en dehors de l'intervalle [x₀, xₙ] en utilisant le dernier segment
     3. Évalue le polynôme sᵢ(x) = aᵢ(x - xᵢ)² + bᵢ(x - xᵢ) + cᵢ
   - Retourne : valeur scalaire de la spline en x_eval

3. **test_spline_quadratique()**
   - Teste l'implémentation sur la fonction sinus avec visualisation
   - Processus :
     1. Définit la fonction test f(x) = sin(x)
     2. Crée 7 points équidistants dans [0, 2π]
     3. Calcule les coefficients de la spline pour ces points
     4. Évalue la spline sur 200 points pour le tracé
     5. Trace la fonction originale et l'approximation par spline
     6. Calcule et affiche les erreurs maximale et moyenne
   - Affichage :
     - Graphique comparant sin(x) et la spline quadratique
     - Points d'interpolation en noir
     - Erreurs maximale et moyenne dans la console

### Exemple d'utilisation

```python
import numpy as np
from spline_quadratique import calcul_coefficients_spline_quadratique, evaluer_spline

# Définir les points d'interpolation
x = np.array([0, 1, 2, 3, 4])
y = np.array([0, 1, 4, 9, 16])  # y = x²

# Calculer les coefficients
a, b, c = calcul_coefficients_spline_quadratique(x, y)

# Évaluer la spline en un nouveau point
x_new = 2.5
y_new = evaluer_spline(x_new, x, a, b, c)
print(f"S({x_new}) = {y_new}")
```

## Dépendances

- Python 3.x
- NumPy
- Matplotlib

## Exécution

Pour exécuter le test inclus :

```bash
python spline_quadratique.py
```

Cela générera un graphique comparant la fonction sinus et son approximation par spline quadratique, ainsi que les erreurs d'approximation.

## Résultats typiques

Le test avec la fonction sinus sur 7 points équidistants dans [0, 2π] donne :
- Erreur maximale < 0.2
- Erreur moyenne < 0.05

## Licence

Ce projet est destiné à un usage éducatif dans le cadre d'un cours d'analyse numérique.