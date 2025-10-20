import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.patches as mpatches
from scipy.interpolate import lagrange

def f(x):
    """Fonction à intégrer : f(x) = 0.1 * x^2"""
    return 0.1 * x**2

def f_periodique(x):
    """Fonction périodique comme dans l'image (approximation)"""
    return 1.5 + 0.6 * np.sin(2 * np.pi * x / 2.5) + 0.3 * np.cos(4 * np.pi * x / 2.5)

def f_cubique(x):
    """Fonction cubique pour tester la précision de Simpson"""
    return x**3 - 2*x**2 + x + 1

def methode_simpson(f, a, b, n):
    """
    Méthode de Simpson
    
    Paramètres:
    f: fonction à intégrer
    a, b: bornes de l'intervalle [a, b]
    n: nombre de paraboles (nombre de paires d'intervalles)
    
    Retourne:
    I_S: approximation de l'intégrale par la méthode de Simpson
    points: points de subdivision (2n+1 points)
    valeurs: valeurs de f aux points de subdivision
    """
    # Calcul des points de subdivision (formule de l'image)
    # z_i = a + i * (b-a)/(2n) pour i = 0, ..., 2n
    points = np.linspace(a, b, 2*n + 1)
    
    # Calcul des valeurs de f aux points de subdivision
    valeurs = f(points)
    
    # Calcul du pas
    h = (b - a) / (2 * n)
    
    # Formule de Simpson (de l'image)
    # I_S = (b-a)/(6n) * [f(z_0) + 4f(z_1) + 2f(z_2) + 4f(z_3) + ... + 4f(z_{2n-1}) + f(z_{2n})]
    coefficients = np.ones(2*n + 1)
    coefficients[1::2] = 4  # Coefficients 4 pour les points impairs
    coefficients[2:-1:2] = 2  # Coefficients 2 pour les points pairs (sauf le premier et dernier)
    
    I_S = (b - a) / (6 * n) * np.sum(coefficients * valeurs)
    
    return I_S, points, valeurs, h

def lagrange_interpolation(x_points, y_points):
    """
    Interpolation de Lagrange pour 3 points (parabole)
    """
    def poly(t):
        result = 0
        n = len(x_points)
        for i in range(n):
            term = y_points[i]
            for j in range(n):
                if i != j:
                    term *= (t - x_points[j]) / (x_points[i] - x_points[j])
            result += term
        return result
    return poly

def integrale_exacte_parabole(f, a, b):
    """
    Calcul de l'intégrale exacte de f(x) = 0.1*x^2
    ∫ 0.1*x^2 dx = 0.1 * x^3/3 = 0.1/3 * x^3
    """
    return 0.1/3 * (b**3 - a**3)

def integrale_exacte_cubique(f, a, b):
    """
    Calcul de l'intégrale exacte de f(x) = x^3 - 2x^2 + x + 1
    ∫ (x^3 - 2x^2 + x + 1) dx = x^4/4 - 2x^3/3 + x^2/2 + x
    """
    return (b**4/4 - 2*b**3/3 + b**2/2 + b) - (a**4/4 - 2*a**3/3 + a**2/2 + a)

def visualiser_simpson(f, a, b, n, titre="Méthode de Simpson"):
    """
    Visualisation de la méthode de Simpson
    """
    # Calcul de l'approximation
    I_S, points, valeurs, h = methode_simpson(f, a, b, n)
    
    # Création de la figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Points pour tracer la courbe
    x_curve = np.linspace(a, b, 1000)
    y_curve = f(x_curve)
    
    # Tracé de la courbe
    ax.plot(x_curve, y_curve, 'r-', linewidth=2, label=f'f(x)')
    
    # Tracé des paraboles de Simpson
    for i in range(n):
        # Points pour la parabole i
        x_parabole = points[2*i:2*i+3]  # 3 points consécutifs
        y_parabole = valeurs[2*i:2*i+3]
        
        # Interpolation de Lagrange pour la parabole
        poly = lagrange_interpolation(x_parabole, y_parabole)
        
        # Points pour tracer la parabole
        x_parabole_curve = np.linspace(x_parabole[0], x_parabole[2], 100)
        y_parabole_curve = poly(x_parabole_curve)
        
        # Tracé de la parabole
        ax.plot(x_parabole_curve, y_parabole_curve, 'b--', linewidth=1.5, alpha=0.8)
        
        # Remplissage sous la parabole
        x_fill = np.concatenate([x_parabole_curve, x_parabole_curve[::-1]])
        y_fill = np.concatenate([y_parabole_curve, np.zeros_like(x_parabole_curve)])
        
        ax.fill(x_fill, y_fill, color='lightblue', alpha=0.3)
        
        # Points de contrôle
        ax.plot(x_parabole, y_parabole, 'bo', markersize=6)
        
        # Lignes verticales aux points de subdivision
        for x_point in x_parabole:
            ax.plot([x_point, x_point], [0, f(x_point)], 'k--', linewidth=1, alpha=0.5)
    
    # Configuration du graphique
    ax.set_xlim(a-0.5, b+0.5)
    ax.set_ylim(-0.2, max(y_curve) + 0.5)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    ax.set_title(f'{titre} - n = {n} (2n+1 = {2*n+1} points)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Calcul de l'intégrale exacte (si disponible)
    try:
        if f == f_cubique:
            I_exacte = integrale_exacte_cubique(f, a, b)
        else:
            I_exacte = integrale_exacte_parabole(f, a, b)
        erreur = abs(I_S - I_exacte)
        
        # Affichage des résultats
        ax.text(0.02, 0.98, f'Approximation: I_S = {I_S:.6f}\n'
                            f'Valeur exacte: I = {I_exacte:.6f}\n'
                            f'Erreur: {erreur:.6f}', 
                transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    except:
        ax.text(0.02, 0.98, f'Approximation: I_S = {I_S:.6f}', 
                transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    return fig, I_S

def comparer_methodes_integration(f, a, b, n_values):
    """
    Comparaison des méthodes d'intégration
    """
    print("Comparaison des méthodes d'intégration")
    print("=" * 60)
    print(f"Fonction: f(x) sur [{a}, {b}]")
    
    try:
        if f == f_cubique:
            I_exacte = integrale_exacte_cubique(f, a, b)
        else:
            I_exacte = integrale_exacte_parabole(f, a, b)
        print(f"Intégrale exacte: {I_exacte:.8f}")
    except:
        print("Intégrale exacte: Non disponible")
    print()
    
    for n in n_values:
        print(f"Nombre de paraboles (n): {n} (2n+1 = {2*n+1} points)")
        print("-" * 50)
        
        # Méthode de Simpson
        I_simpson, _, _, _ = methode_simpson(f, a, b, n)
        
        try:
            erreur_simpson = abs(I_simpson - I_exacte)
            print(f"Simpson:     I_S = {I_simpson:.8f}, erreur = {erreur_simpson:.8f}")
        except:
            print(f"Simpson:     I_S = {I_simpson:.8f}")
        print()

def demonstration_formule_simpson():
    """
    Démonstration de la formule de Simpson
    """
    print("FORMULE DE LA MÉTHODE DE SIMPSON")
    print("=" * 50)
    print()
    print("1. On considère 2n+1 points z_i = a + i*(b-a)/(2n) pour i = 0, ..., 2n")
    print()
    print("2. Sur chaque intervalle [z_{2i}, z_{2i+2}], on approxime f par une parabole g_i")
    print("   passant par les points (z_{2i}, f(z_{2i})), (z_{2i+1}, f(z_{2i+1})), (z_{2i+2}, f(z_{2i+2}))")
    print()
    print("3. La parabole g_i est donnée par l'interpolation de Lagrange:")
    print("   g_i(t) = f(z_{2i}) * L_0(t) + f(z_{2i+1}) * L_1(t) + f(z_{2i+2}) * L_2(t)")
    print("   où L_0, L_1, L_2 sont les polynômes de Lagrange de degré 2")
    print()
    print("4. L'intégrale de g_i sur [z_{2i}, z_{2i+2}] est:")
    print("   ∫[z_{2i} à z_{2i+2}] g_i(t) dt = (b-a)/(6n) * (f(z_{2i}) + 4f(z_{2i+1}) + f(z_{2i+2}))")
    print()
    print("5. L'approximation totale est:")
    print("   I_S = (b-a)/(6n) * [f(z_0) + 4f(z_1) + 2f(z_2) + 4f(z_3) + ... + 4f(z_{2n-1}) + f(z_{2n})]")
    print()

def comparer_toutes_methodes(f, a, b, n):
    """
    Comparaison de toutes les méthodes d'intégration
    """
    print(f"COMPARAISON DES MÉTHODES D'INTÉGRATION")
    print(f"Fonction: f(x) sur [{a}, {b}]")
    print("=" * 60)
    
    # Méthode de Simpson
    I_simpson, _, _, _ = methode_simpson(f, a, b, n)
    
    # Méthode des trapèzes (équivalent à Simpson avec 2n points)
    from methode_trapezes import methode_trapezes
    I_trap, _, _, _ = methode_trapezes(f, a, b, 2*n)
    
    # Méthode des rectangles (gauche, droite, milieu)
    from methode_rectangles import methode_rectangles_gauche, methode_rectangles_droite, methode_rectangles_milieu
    I_rect_g, _, _, _ = methode_rectangles_gauche(f, a, b, 2*n)
    I_rect_d, _, _, _ = methode_rectangles_droite(f, a, b, 2*n)
    I_rect_m, _, _, _ = methode_rectangles_milieu(f, a, b, 2*n)
    
    # Intégrale exacte
    try:
        if f == f_cubique:
            I_exacte = integrale_exacte_cubique(f, a, b)
        else:
            I_exacte = integrale_exacte_parabole(f, a, b)
        
        print(f"Intégrale exacte:     I = {I_exacte:.8f}")
        print()
        print(f"Simpson (n={n}):      I_S = {I_simpson:.8f}, erreur = {abs(I_simpson - I_exacte):.8f}")
        print(f"Trapèzes (2n={2*n}):  I_T = {I_trap:.8f}, erreur = {abs(I_trap - I_exacte):.8f}")
        print(f"Rectangles gauche:    I_R = {I_rect_g:.8f}, erreur = {abs(I_rect_g - I_exacte):.8f}")
        print(f"Rectangles droite:    I_R = {I_rect_d:.8f}, erreur = {abs(I_rect_d - I_exacte):.8f}")
        print(f"Rectangles milieu:    I_R = {I_rect_m:.8f}, erreur = {abs(I_rect_m - I_exacte):.8f}")
    except:
        print(f"Simpson (n={n}):      I_S = {I_simpson:.8f}")
        print(f"Trapèzes (2n={2*n}):  I_T = {I_trap:.8f}")
        print(f"Rectangles gauche:    I_R = {I_rect_g:.8f}")
        print(f"Rectangles droite:    I_R = {I_rect_d:.8f}")
        print(f"Rectangles milieu:    I_R = {I_rect_m:.8f}")
    
    print()

def main():
    """
    Fonction principale pour démonstration
    """
    print("Méthode de Simpson - Implémentation Python")
    print("=" * 50)
    
    # Démonstration de la formule
    demonstration_formule_simpson()
    
    # Exemple 1: Fonction parabolique f(x) = 0.1*x^2
    print("\nEXEMPLE 1: Fonction parabolique f(x) = 0.1*x^2")
    print("-" * 50)
    a1, b1 = 0, 5
    n1 = 2  # 2 paraboles = 5 points
    
    fig1, I_S1 = visualiser_simpson(f, a1, b1, n1, "Méthode de Simpson - f(x) = 0.1x²")
    plt.show()
    
    # Comparaison pour la fonction parabolique
    n_values = [1, 2, 5, 10]
    comparer_methodes_integration(f, a1, b1, n_values)
    
    # Exemple 2: Fonction cubique (Simpson est exact pour les polynômes de degré ≤ 3)
    print("\nEXEMPLE 2: Fonction cubique f(x) = x³ - 2x² + x + 1")
    print("-" * 50)
    a2, b2 = 0, 3
    n2 = 2
    
    fig2, I_S2 = visualiser_simpson(f_cubique, a2, b2, n2, "Méthode de Simpson - Fonction cubique")
    plt.show()
    
    # Comparaison pour la fonction cubique
    comparer_methodes_integration(f_cubique, a2, b2, n_values)
    
    # Comparaison de toutes les méthodes
    print("\nCOMPARAISON DE TOUTES LES MÉTHODES")
    print("=" * 50)
    comparer_toutes_methodes(f, a1, b1, 2)
    comparer_toutes_methodes(f_cubique, a2, b2, 2)
    
    # Visualisation comparative
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Fonction parabolique
    for i, n in enumerate([1, 2]):
        ax = axes[0, i]
        I_S, points, valeurs, h = methode_simpson(f, a1, b1, n)
        
        # Tracé de la courbe
        x_curve = np.linspace(a1, b1, 1000)
        y_curve = f(x_curve)
        ax.plot(x_curve, y_curve, 'r-', linewidth=2, label=f'f(x) = 0.1x²')
        
        # Tracé des paraboles
        for j in range(n):
            x_parabole = points[2*j:2*j+3]
            y_parabole = valeurs[2*j:2*j+3]
            poly = lagrange_interpolation(x_parabole, y_parabole)
            x_parabole_curve = np.linspace(x_parabole[0], x_parabole[2], 100)
            y_parabole_curve = poly(x_parabole_curve)
            ax.plot(x_parabole_curve, y_parabole_curve, 'b--', linewidth=1.5, alpha=0.8)
            ax.fill_between(x_parabole_curve, 0, y_parabole_curve, alpha=0.3, color='lightblue')
            ax.plot(x_parabole, y_parabole, 'bo', markersize=4)
        
        ax.set_title(f'f(x) = 0.1x² (n={n})', fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        I_exacte = integrale_exacte_parabole(f, a1, b1)
        erreur = abs(I_S - I_exacte)
        ax.text(0.02, 0.98, f'I_S = {I_S:.4f}\nErreur = {erreur:.4f}', 
                transform=ax.transAxes, fontsize=9,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Fonction cubique
    for i, n in enumerate([1, 2]):
        ax = axes[1, i]
        I_S, points, valeurs, h = methode_simpson(f_cubique, a2, b2, n)
        
        # Tracé de la courbe
        x_curve = np.linspace(a2, b2, 1000)
        y_curve = f_cubique(x_curve)
        ax.plot(x_curve, y_curve, 'r-', linewidth=2, label='f(x) cubique')
        
        # Tracé des paraboles
        for j in range(n):
            x_parabole = points[2*j:2*j+3]
            y_parabole = valeurs[2*j:2*j+3]
            poly = lagrange_interpolation(x_parabole, y_parabole)
            x_parabole_curve = np.linspace(x_parabole[0], x_parabole[2], 100)
            y_parabole_curve = poly(x_parabole_curve)
            ax.plot(x_parabole_curve, y_parabole_curve, 'b--', linewidth=1.5, alpha=0.8)
            ax.fill_between(x_parabole_curve, 0, y_parabole_curve, alpha=0.3, color='lightblue')
            ax.plot(x_parabole, y_parabole, 'bo', markersize=4)
        
        ax.set_title(f'Fonction cubique (n={n})', fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        I_exacte = integrale_exacte_cubique(f_cubique, a2, b2)
        erreur = abs(I_S - I_exacte)
        ax.text(0.02, 0.98, f'I_S = {I_S:.4f}\nErreur = {erreur:.4f}', 
                transform=ax.transAxes, fontsize=9,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
