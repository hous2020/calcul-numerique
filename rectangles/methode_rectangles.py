import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

def f(x):
    """Fonction à intégrer : f(x) = 0.1 * x^2"""
    return 0.1 * x**2

def methode_rectangles_gauche(f, a, b, m):
    """
    Méthode des rectangles (somme de Riemann à gauche)
    
    Paramètres:
    f: fonction à intégrer
    a, b: bornes de l'intervalle [a, b]
    m: nombre de rectangles
    
    Retourne:
    I_R: approximation de l'intégrale
    points: points de subdivision
    hauteurs: hauteurs des rectangles
    """
    # Calcul des points de subdivision
    points = np.linspace(a, b, m + 1)
    
    # Calcul des hauteurs (valeurs de f aux points gauches)
    hauteurs = f(points[:-1])  # Tous sauf le dernier point
    
    # Calcul de la largeur des rectangles
    largeur = (b - a) / m
    
    # Calcul de l'approximation (formule de l'image)
    I_R = largeur * np.sum(hauteurs)
    
    return I_R, points, hauteurs, largeur

def methode_rectangles_droite(f, a, b, m):
    """
    Méthode des rectangles (somme de Riemann à droite)
    """
    points = np.linspace(a, b, m + 1)
    hauteurs = f(points[1:])  # Tous sauf le premier point
    largeur = (b - a) / m
    I_R = largeur * np.sum(hauteurs)
    return I_R, points, hauteurs, largeur

def methode_rectangles_milieu(f, a, b, m):
    """
    Méthode des rectangles (somme de Riemann au milieu)
    """
    points = np.linspace(a, b, m + 1)
    milieux = (points[:-1] + points[1:]) / 2
    hauteurs = f(milieux)
    largeur = (b - a) / m
    I_R = largeur * np.sum(hauteurs)
    return I_R, points, hauteurs, largeur

def integrale_exacte(f, a, b):
    """
    Calcul de l'intégrale exacte de f(x) = 0.1*x^2
    ∫ 0.1*x^2 dx = 0.1 * x^3/3 = 0.1/3 * x^3
    """
    return 0.1/3 * (b**3 - a**3)

def visualiser_rectangles(f, a, b, m, methode='gauche'):
    """
    Visualisation de la méthode des rectangles
    """
    # Calcul de l'approximation
    if methode == 'gauche':
        I_R, points, hauteurs, largeur = methode_rectangles_gauche(f, a, b, m)
    elif methode == 'droite':
        I_R, points, hauteurs, largeur = methode_rectangles_droite(f, a, b, m)
    else:  # milieu
        I_R, points, hauteurs, largeur = methode_rectangles_milieu(f, a, b, m)
    
    # Création de la figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Points pour tracer la courbe
    x_curve = np.linspace(a, b, 1000)
    y_curve = f(x_curve)
    
    # Tracé de la courbe
    ax.plot(x_curve, y_curve, 'r-', linewidth=2, label=f'f(x) = 0.1x²')
    
    # Tracé des rectangles
    for i in range(m):
        if methode == 'gauche':
            x_rect = points[i]
        elif methode == 'droite':
            x_rect = points[i+1]
        else:  # milieu
            x_rect = (points[i] + points[i+1]) / 2
        
        # Création du rectangle
        rect = Rectangle((points[i], 0), largeur, hauteurs[i], 
                        linewidth=1.5, edgecolor='blue', 
                        facecolor='lightblue', alpha=0.7)
        ax.add_patch(rect)
        
        # Ligne verticale droite du rectangle (comme dans l'image)
        ax.plot([points[i+1], points[i+1]], [0, hauteurs[i]], 
                'k--', linewidth=1)
    
    # Configuration du graphique
    ax.set_xlim(a-0.5, b+0.5)
    ax.set_ylim(-0.2, max(y_curve) + 0.5)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    ax.set_title(f'Méthode des rectangles ({methode}) - m = {m}', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Calcul de l'intégrale exacte
    I_exacte = integrale_exacte(f, a, b)
    erreur = abs(I_R - I_exacte)
    
    # Affichage des résultats
    ax.text(0.02, 0.98, f'Approximation: I_R = {I_R:.4f}\n'
                        f'Valeur exacte: I = {I_exacte:.4f}\n'
                        f'Erreur: {erreur:.4f}', 
            transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    return fig, I_R, I_exacte, erreur

def comparer_methodes(f, a, b, m_values):
    """
    Comparaison des différentes méthodes de rectangles
    """
    print("Comparaison des méthodes des rectangles")
    print("=" * 50)
    print(f"Fonction: f(x) = 0.1x² sur [{a}, {b}]")
    print(f"Intégrale exacte: {integrale_exacte(f, a, b):.6f}")
    print()
    
    for m in m_values:
        print(f"Nombre de rectangles: {m}")
        print("-" * 30)
        
        # Méthode gauche
        I_gauche, _, _, _ = methode_rectangles_gauche(f, a, b, m)
        erreur_gauche = abs(I_gauche - integrale_exacte(f, a, b))
        
        # Méthode droite
        I_droite, _, _, _ = methode_rectangles_droite(f, a, b, m)
        erreur_droite = abs(I_droite - integrale_exacte(f, a, b))
        
        # Méthode milieu
        I_milieu, _, _, _ = methode_rectangles_milieu(f, a, b, m)
        erreur_milieu = abs(I_milieu - integrale_exacte(f, a, b))
        
        print(f"Gauche:  I_R = {I_gauche:.6f}, erreur = {erreur_gauche:.6f}")
        print(f"Droite:  I_R = {I_droite:.6f}, erreur = {erreur_droite:.6f}")
        print(f"Milieu:  I_R = {I_milieu:.6f}, erreur = {erreur_milieu:.6f}")
        print()

def main():
    """
    Fonction principale pour démonstration
    """
    # Paramètres de l'exemple
    a, b = 0, 5  # Intervalle [0, 5]
    m = 5        # Nombre de rectangles
    
    print("Méthode des rectangles - Implémentation Python")
    print("=" * 50)
    
    # Visualisation de la méthode des rectangles à gauche (comme dans l'image)
    fig, I_R, I_exacte, erreur = visualiser_rectangles(f, a, b, m, 'gauche')
    plt.show()
    
    # Comparaison des méthodes
    m_values = [5, 10, 20, 50]
    comparer_methodes(f, a, b, m_values)

if __name__ == "__main__":
    main()
