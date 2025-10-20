import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.patches as mpatches

def f(x):
    """Fonction à intégrer : f(x) = 0.1 * x^2"""
    return 0.1 * x**2

def f_periodique(x):
    """Fonction périodique comme dans l'image (approximation)"""
    return 1.5 + 0.6 * np.sin(2 * np.pi * x / 2.5) + 0.3 * np.cos(4 * np.pi * x / 2.5)

def methode_trapezes(f, a, b, m):
    """
    Méthode des trapèzes
    
    Paramètres:
    f: fonction à intégrer
    a, b: bornes de l'intervalle [a, b]
    m: nombre de trapèzes (ou nombre de points de subdivision - 1)
    
    Retourne:
    I_T: approximation de l'intégrale par la méthode des trapèzes
    points: points de subdivision
    valeurs: valeurs de f aux points de subdivision
    """
    # Calcul des points de subdivision (formule de l'image)
    points = np.linspace(a, b, m + 1)
    
    # Calcul des valeurs de f aux points de subdivision
    valeurs = f(points)
    
    # Calcul de la largeur des sous-intervalles
    h = (b - a) / m
    
    # Formule de la méthode des trapèzes (de l'image)
    # I_T = (b-a)/(2m) * (f(y_0) + 2f(y_1) + 2f(y_2) + ... + 2f(y_{m-1}) + f(y_m))
    I_T = h * (valeurs[0] + 2 * np.sum(valeurs[1:-1]) + valeurs[-1]) / 2
    
    return I_T, points, valeurs, h

def integrale_exacte_parabole(f, a, b):
    """
    Calcul de l'intégrale exacte de f(x) = 0.1*x^2
    ∫ 0.1*x^2 dx = 0.1 * x^3/3 = 0.1/3 * x^3
    """
    return 0.1/3 * (b**3 - a**3)

def visualiser_trapezes(f, a, b, m, titre="Méthode des trapèzes"):
    """
    Visualisation de la méthode des trapèzes
    """
    # Calcul de l'approximation
    I_T, points, valeurs, h = methode_trapezes(f, a, b, m)
    
    # Création de la figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Points pour tracer la courbe
    x_curve = np.linspace(a, b, 1000)
    y_curve = f(x_curve)
    
    # Tracé de la courbe
    ax.plot(x_curve, y_curve, 'r-', linewidth=2, label=f'f(x)')
    
    # Tracé des trapèzes
    for i in range(m):
        # Points du trapèze
        x_trap = [points[i], points[i+1], points[i+1], points[i]]
        y_trap = [0, 0, valeurs[i+1], valeurs[i]]
        
        # Création du trapèze
        trap = Polygon(list(zip(x_trap, y_trap)), 
                      linewidth=1.5, edgecolor='blue', 
                      facecolor='lightblue', alpha=0.7)
        ax.add_patch(trap)
        
        # Lignes verticales aux points de subdivision
        ax.plot([points[i+1], points[i+1]], [0, valeurs[i+1]], 
                'k--', linewidth=1)
    
    # Configuration du graphique
    ax.set_xlim(a-0.5, b+0.5)
    ax.set_ylim(-0.2, max(y_curve) + 0.5)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    ax.set_title(f'{titre} - m = {m}', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Calcul de l'intégrale exacte (si disponible)
    try:
        I_exacte = integrale_exacte_parabole(f, a, b)
        erreur = abs(I_T - I_exacte)
        
        # Affichage des résultats
        ax.text(0.02, 0.98, f'Approximation: I_T = {I_T:.4f}\n'
                            f'Valeur exacte: I = {I_exacte:.4f}\n'
                            f'Erreur: {erreur:.4f}', 
                transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    except:
        ax.text(0.02, 0.98, f'Approximation: I_T = {I_T:.4f}', 
                transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    return fig, I_T

def comparer_methodes_integration(f, a, b, m_values):
    """
    Comparaison des méthodes d'intégration
    """
    print("Comparaison des méthodes d'intégration")
    print("=" * 50)
    print(f"Fonction: f(x) sur [{a}, {b}]")
    
    try:
        I_exacte = integrale_exacte_parabole(f, a, b)
        print(f"Intégrale exacte: {I_exacte:.6f}")
    except:
        print("Intégrale exacte: Non disponible")
    print()
    
    for m in m_values:
        print(f"Nombre de trapèzes: {m}")
        print("-" * 30)
        
        # Méthode des trapèzes
        I_trap, _, _, _ = methode_trapezes(f, a, b, m)
        
        try:
            erreur_trap = abs(I_trap - I_exacte)
            print(f"Trapèzes: I_T = {I_trap:.6f}, erreur = {erreur_trap:.6f}")
        except:
            print(f"Trapèzes: I_T = {I_trap:.6f}")
        print()

def demonstration_formule():
    """
    Démonstration de la dérivation de la formule des trapèzes
    """
    print("DÉRIVATION DE LA FORMULE DES TRAPÈZES")
    print("=" * 50)
    print()
    print("1. Sur chaque intervalle [y_i, y_{i+1}], on approxime f par une fonction affine g_i")
    print("   telle que g_i(y_i) = f(y_i) et g_i(y_{i+1}) = f(y_{i+1})")
    print()
    print("2. La fonction affine g_i est donnée par:")
    print("   g_i(t) = f(y_i) + (t - y_i)/(y_{i+1} - y_i) * (f(y_{i+1}) - f(y_i))")
    print()
    print("3. L'intégrale de g_i sur [y_i, y_{i+1}] est:")
    print("   ∫[y_i à y_{i+1}] g_i(t) dt = (y_{i+1} - y_i)/2 * (f(y_{i+1}) + f(y_i))")
    print()
    print("4. Avec y_i = a + i*(b-a)/m et h = (b-a)/m, on obtient:")
    print("   ∫[y_i à y_{i+1}] g_i(t) dt = h/2 * (f(y_{i+1}) + f(y_i))")
    print()
    print("5. L'approximation totale est:")
    print("   I_T = h/2 * [f(y_0) + 2f(y_1) + 2f(y_2) + ... + 2f(y_{m-1}) + f(y_m)]")
    print("   I_T = (b-a)/(2m) * [f(y_0) + 2f(y_1) + 2f(y_2) + ... + 2f(y_{m-1}) + f(y_m)]")
    print()

def main():
    """
    Fonction principale pour démonstration
    """
    print("Méthode des trapèzes - Implémentation Python")
    print("=" * 50)
    
    # Démonstration de la formule
    demonstration_formule()
    
    # Exemple 1: Fonction parabolique f(x) = 0.1*x^2
    print("\nEXEMPLE 1: Fonction parabolique f(x) = 0.1*x^2")
    print("-" * 50)
    a1, b1 = 0, 5
    m1 = 5
    
    fig1, I_T1 = visualiser_trapezes(f, a1, b1, m1, "Méthode des trapèzes - f(x) = 0.1x²")
    plt.show()
    
    # Comparaison pour la fonction parabolique
    m_values = [5, 10, 20, 50]
    comparer_methodes_integration(f, a1, b1, m_values)
    
    # Exemple 2: Fonction périodique (comme dans l'image)
    print("\nEXEMPLE 2: Fonction périodique")
    print("-" * 50)
    a2, b2 = 0, 5
    m2 = 5
    
    fig2, I_T2 = visualiser_trapezes(f_periodique, a2, b2, m2, "Méthode des trapèzes - Fonction périodique")
    plt.show()
    
    # Comparaison pour la fonction périodique
    comparer_methodes_integration(f_periodique, a2, b2, m_values)
    
    # Visualisation comparative
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Fonction parabolique
    for i, m in enumerate([5, 10]):
        ax = axes[0, i]
        I_T, points, valeurs, h = methode_trapezes(f, a1, b1, m)
        
        # Tracé de la courbe
        x_curve = np.linspace(a1, b1, 1000)
        y_curve = f(x_curve)
        ax.plot(x_curve, y_curve, 'r-', linewidth=2, label=f'f(x) = 0.1x²')
        
        # Tracé des trapèzes
        for j in range(m):
            x_trap = [points[j], points[j+1], points[j+1], points[j]]
            y_trap = [0, 0, valeurs[j+1], valeurs[j]]
            trap = Polygon(list(zip(x_trap, y_trap)), 
                          linewidth=1, edgecolor='blue', 
                          facecolor='lightblue', alpha=0.7)
            ax.add_patch(trap)
        
        ax.set_title(f'f(x) = 0.1x² (m={m})', fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        I_exacte = integrale_exacte_parabole(f, a1, b1)
        erreur = abs(I_T - I_exacte)
        ax.text(0.02, 0.98, f'I_T = {I_T:.4f}\nErreur = {erreur:.4f}', 
                transform=ax.transAxes, fontsize=9,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Fonction périodique
    for i, m in enumerate([5, 10]):
        ax = axes[1, i]
        I_T, points, valeurs, h = methode_trapezes(f_periodique, a2, b2, m)
        
        # Tracé de la courbe
        x_curve = np.linspace(a2, b2, 1000)
        y_curve = f_periodique(x_curve)
        ax.plot(x_curve, y_curve, 'r-', linewidth=2, label='f(x) périodique')
        
        # Tracé des trapèzes
        for j in range(m):
            x_trap = [points[j], points[j+1], points[j+1], points[j]]
            y_trap = [0, 0, valeurs[j+1], valeurs[j]]
            trap = Polygon(list(zip(x_trap, y_trap)), 
                          linewidth=1, edgecolor='blue', 
                          facecolor='lightblue', alpha=0.7)
            ax.add_patch(trap)
        
        ax.set_title(f'Fonction périodique (m={m})', fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        ax.text(0.02, 0.98, f'I_T = {I_T:.4f}', 
                transform=ax.transAxes, fontsize=9,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
