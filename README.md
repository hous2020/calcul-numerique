# Analyse Numérique : Outil d'Interpolation Unifié

Ce projet est une application de bureau interactive qui combine plusieurs méthodes d'interpolation et d'approximation de fonctions. Il permet de visualiser et de comparer l'interpolation de Lagrange et l'approximation par spline quadratique pour une fonction donnée par l'utilisateur.

## Fonctionnalités

- **Interface Graphique Unifiée** : Une seule fenêtre construite avec Tkinter pour accéder à toutes les analyses.
- **Modes d'Analyse Multiples** : L'utilisateur peut choisir entre trois modes via des boutons radio :
  1.  **Comparer Erreurs** : Affiche les courbes d'erreur de Lagrange et de la spline sur un même graphique pour une comparaison directe.
  2.  **Lagrange** : Affiche l'approximation par le polynôme de Lagrange et sa courbe d'erreur.
  3.  **Spline Quadratique** : Affiche l'approximation par spline quadratique et sa courbe d'erreur.
- **Entrée de Fonction Dynamique** : Un champ de texte permet à l'utilisateur de saisir n'importe quelle fonction de `x`.
- **Calcul Symbolique** : Utilise `sympy` pour interpréter la fonction et calculer sa dérivée, assurant une grande précision pour la condition initiale de la spline.

## Structure du Projet

Ce projet a été développé de manière incrémentale. Voici une description de chaque fichier clé et de son rôle dans l'évolution du projet :

-   `analyse_numerique_gui.py`: **Application Finale et Unifiée.** C'est le script principal à utiliser. Il lance une interface graphique complète qui intègre toutes les fonctionnalités : l'analyse par interpolation de Lagrange, l'approximation par spline quadratique, et la comparaison de leurs erreurs respectives.

-   `spline_quadratique.py`: **Première Étape.** Initialement, ce script implémentait l'approximation par spline quadratique. Il a d'abord été un script en ligne de commande, puis a été doté de sa propre interface graphique (Tkinter). Sa logique est maintenant intégrée dans l'application principale.

-   `lagrange.py`: **Deuxième Étape.** Ce script a été développé pour implémenter l'interpolation de Lagrange. Comme pour la spline, il a évolué d'un script en ligne de commande vers une application avec sa propre interface graphique. Sa fonctionnalité est également incluse dans l'application unifiée.

-   `comparaison_interpolation.py`: **Étape de Comparaison.** Ce script a été créé pour comparer directement les erreurs des deux méthodes (Lagrange et spline) via la ligne de commande. Cette fonctionnalité est maintenant une option dans l'interface graphique principale.

-   `requirements.txt`: La liste des dépendances Python (`numpy`, `matplotlib`, `sympy`) nécessaires pour exécuter le projet.

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

Pour lancer l'application, exécutez le script `analyse_numerique_gui.py` :

```bash
python analyse_numerique_gui.py
```

Une fenêtre s'ouvrira. Pour l'utiliser :
1.  **Entrez une fonction** dans le champ de texte (ex: `x**3 - cos(x)`).
2.  **Sélectionnez un mode d'analyse** (Comparer Erreurs, Lagrange, ou Spline Quadratique).
3.  **Cliquez sur "Générer le graphique"** pour afficher les résultats.

## Licence

Ce projet est destiné à un usage éducatif dans le cadre d'un cours d'analyse numérique.