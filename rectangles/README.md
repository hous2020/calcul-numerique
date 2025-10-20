# Méthodes d'Intégration Numérique

Ce dossier contient des implémentations complètes des principales méthodes d'intégration numérique en Python, basées sur les formules mathématiques des images fournies.

## Fichiers disponibles

### 1. `methode_rectangles.py`
Implémentation de la **méthode des rectangles** (somme de Riemann) avec :
- Rectangles à gauche
- Rectangles à droite  
- Rectangles au milieu
- Visualisation graphique
- Comparaison avec l'intégrale exacte

### 2. `methode_trapezes.py`
Implémentation de la **méthode des trapèzes** avec :
- Formule de la méthode des trapèzes
- Visualisation graphique
- Comparaison des performances

### 3. `methode_simpson.py`
Implémentation de la **méthode de Simpson** avec :
- Interpolation de Lagrange pour les paraboles
- Formule de Simpson complète
- Visualisation des paraboles interpolantes
- Comparaison avec les autres méthodes

### 4. `comparaison_methodes.py`
Fichier principal pour :
- Comparaison complète de toutes les méthodes
- Étude de convergence
- Visualisations comparatives
- Tests sur différentes fonctions

## Utilisation

### Exécution simple
```bash
# Méthode des rectangles
python methode_rectangles.py

# Méthode des trapèzes  
python methode_trapezes.py

# Méthode de Simpson
python methode_simpson.py

# Comparaison complète
python comparaison_methodes.py
```

### Utilisation en tant que module
```python
from methode_rectangles import methode_rectangles_gauche
from methode_trapezes import methode_trapezes
from methode_simpson import methode_simpson

# Exemple d'utilisation
def f(x):
    return 0.1 * x**2

# Méthode des rectangles (gauche)
I_rect, points, hauteurs, largeur = methode_rectangles_gauche(f, 0, 5, 10)

# Méthode des trapèzes
I_trap, points, valeurs, h = methode_trapezes(f, 0, 5, 10)

# Méthode de Simpson
I_simpson, points, valeurs, h = methode_simpson(f, 0, 5, 5)  # n=5 paraboles
```

## Fonctions de test incluses

- **f(x) = 0.1x²** : Fonction parabolique (intégrale exacte disponible)
- **f(x) = x³ - 2x² + x + 1** : Fonction cubique (Simpson exact)
- **f(x) = 1.5 + 0.6sin(2πx/2.5) + 0.3cos(4πx/2.5)** : Fonction périodique
- **f(x) = e^(-x/2)** : Fonction exponentielle

## Formules implémentées

### Méthode des rectangles
```
I_R = (b-a)/m * Σ[i=0 à m-1] f(y_i)
```
où y_i = a + i*(b-a)/m

### Méthode des trapèzes
```
I_T = (b-a)/(2m) * [f(y_0) + 2f(y_1) + 2f(y_2) + ... + 2f(y_{m-1}) + f(y_m)]
```

### Méthode de Simpson
```
I_S = (b-a)/(6n) * [f(z_0) + 4f(z_1) + 2f(z_2) + 4f(z_3) + ... + 4f(z_{2n-1}) + f(z_{2n})]
```
où z_i = a + i*(b-a)/(2n)

## Précision et convergence

- **Rectangles** : Convergence en O(h)
- **Trapèzes** : Convergence en O(h²)  
- **Simpson** : Convergence en O(h⁴)

La méthode de Simpson est généralement la plus précise et est exacte pour les polynômes de degré ≤ 3.

## Dépendances

- numpy
- matplotlib
- scipy (pour certaines intégrales exactes)

## Visualisations

Chaque méthode inclut des visualisations graphiques montrant :
- La fonction originale
- L'approximation par la méthode choisie
- Les erreurs d'approximation
- Les comparaisons entre méthodes
