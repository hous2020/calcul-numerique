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

## Algorithmes et Formules

### 1. Méthode des Rectangles (Riemann)

#### Algorithme général :
1. Diviser l'intervalle [a,b] en m sous-intervalles de largeur h = (b-a)/m
2. Calculer les points de subdivision : y_i = a + i*h pour i = 0,1,...,m
3. Approximer f sur chaque intervalle [y_i, y_{i+1}] par une constante
4. Calculer l'aire de chaque rectangle et sommer

#### Formules :
- **Rectangles à gauche** : `I_R = h * Σ[i=0 à m-1] f(y_i)`
- **Rectangles à droite** : `I_R = h * Σ[i=1 à m] f(y_i)`
- **Rectangles au milieu** : `I_R = h * Σ[i=0 à m-1] f((y_i + y_{i+1})/2)`

où h = (b-a)/m et y_i = a + i*h

#### Précision : O(h)

---

### 2. Méthode des Trapèzes

#### Algorithme général :
1. Diviser l'intervalle [a,b] en m sous-intervalles de largeur h = (b-a)/m
2. Calculer les points de subdivision : y_i = a + i*h pour i = 0,1,...,m
3. Sur chaque intervalle [y_i, y_{i+1}], approximer f par une droite passant par (y_i, f(y_i)) et (y_{i+1}, f(y_{i+1}))
4. Calculer l'aire de chaque trapèze et sommer

#### Formule :
```
I_T = h/2 * [f(y_0) + 2f(y_1) + 2f(y_2) + ... + 2f(y_{m-1}) + f(y_m)]
```

où h = (b-a)/m et y_i = a + i*h

#### Précision : O(h²)

---

### 3. Méthode de Simpson

#### Algorithme général :
1. Diviser l'intervalle [a,b] en 2n sous-intervalles de largeur h = (b-a)/(2n)
2. Calculer les points de subdivision : z_i = a + i*h pour i = 0,1,...,2n
3. Grouper les points par triplets : [z_{2i}, z_{2i+1}, z_{2i+2}] pour i = 0,1,...,n-1
4. Sur chaque intervalle [z_{2i}, z_{2i+2}], approximer f par une parabole passant par les 3 points
5. Utiliser l'interpolation de Lagrange pour construire la parabole
6. Calculer l'aire sous chaque parabole et sommer

#### Formule :
```
I_S = h/3 * [f(z_0) + 4f(z_1) + 2f(z_2) + 4f(z_3) + ... + 4f(z_{2n-1}) + f(z_{2n})]
```

où h = (b-a)/(2n) et z_i = a + i*h

#### Interpolation de Lagrange (pour la parabole) :
```
g_i(t) = f(z_{2i}) * L_0(t) + f(z_{2i+1}) * L_1(t) + f(z_{2i+2}) * L_2(t)
```

où :
- L_0(t) = (t - z_{2i+1})(t - z_{2i+2}) / [(z_{2i} - z_{2i+1})(z_{2i} - z_{2i+2})]
- L_1(t) = (t - z_{2i})(t - z_{2i+2}) / [(z_{2i+1} - z_{2i})(z_{2i+1} - z_{2i+2})]
- L_2(t) = (t - z_{2i})(t - z_{2i+1}) / [(z_{2i+2} - z_{2i})(z_{2i+2} - z_{2i+1})]

#### Précision : O(h⁴)

## Précision et convergence

- **Rectangles** : Convergence en O(h)
- **Trapèzes** : Convergence en O(h²)  
- **Simpson** : Convergence en O(h⁴)

La méthode de Simpson est généralement la plus précise et est exacte pour les polynômes de degré ≤ 3.

## Avantages et Inconvénients

### Méthode des Rectangles
**Avantages :**
- Simple à implémenter
- Calculs rapides
- Facile à comprendre

**Inconvénients :**
- Précision limitée (O(h))
- Peut sous-estimer ou surestimer selon la méthode choisie
- Nécessite beaucoup de points pour une bonne précision

### Méthode des Trapèzes
**Avantages :**
- Bon compromis simplicité/précision
- Convergence quadratique (O(h²))
- Plus précise que les rectangles
- Facile à implémenter

**Inconvénients :**
- Moins précise que Simpson
- Peut avoir des erreurs importantes sur des fonctions très oscillantes

### Méthode de Simpson
**Avantages :**
- Très précise (O(h⁴))
- Exacte pour les polynômes de degré ≤ 3
- Convergence rapide
- Excellente pour la plupart des fonctions lisses

**Inconvénients :**
- Plus complexe à implémenter
- Nécessite un nombre pair de sous-intervalles
- Peut être instable sur des fonctions très oscillantes
- Calculs plus coûteux

## Cas d'usage recommandés

### Utilisez la méthode des rectangles quand :
- Vous avez besoin d'une approximation rapide et simple
- La précision n'est pas critique
- Vous voulez comprendre le concept d'intégration numérique
- Vous travaillez avec des fonctions monotones

### Utilisez la méthode des trapèzes quand :
- Vous voulez un bon compromis entre simplicité et précision
- Vous avez des contraintes de temps de calcul modérées
- La fonction est relativement lisse
- Vous voulez une méthode robuste et fiable

### Utilisez la méthode de Simpson quand :
- La précision est importante
- Vous travaillez avec des fonctions lisses
- Vous avez des polynômes de degré ≤ 3 (exactitude garantie)
- Vous pouvez vous permettre des calculs plus coûteux
- Vous voulez la meilleure précision possible

## Exemples d'application

### Calcul d'aires
```python
# Calculer l'aire sous f(x) = x² de 0 à 2
def f(x): return x**2
aire = methode_simpson(f, 0, 2, 10)  # Très précis
```

### Calcul de volumes de révolution
```python
# Volume d'un cône (f(x) = x de 0 à h)
def f(x): return x
volume = methode_trapezes(f, 0, 5, 50) * np.pi  # Approximation du volume
```

### Calcul de probabilités
```python
# Probabilité P(0 ≤ X ≤ 2) pour une distribution normale
def f(x): return np.exp(-x**2/2) / np.sqrt(2*np.pi)
probabilite = methode_simpson(f, 0, 2, 20)
```

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
