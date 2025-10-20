"""
Comparaison complète des méthodes d'intégration numérique
- Méthode des rectangles (gauche, droite, milieu)
- Méthode des trapèzes
- Méthode de Simpson
"""

import numpy as np
import matplotlib.pyplot as plt
from methode_rectangles import methode_rectangles_gauche, methode_rectangles_droite, methode_rectangles_milieu
from methode_trapezes import methode_trapezes
from methode_simpson import methode_simpson, integrale_exacte_parabole, integrale_exacte_cubique

def f_parabole(x):
    """Fonction parabolique : f(x) = 0.1 * x^2"""
    return 0.1 * x**2

def f_cubique(x):
    """Fonction cubique : f(x) = x^3 - 2x^2 + x + 1"""
    return x**3 - 2*x**2 + x + 1

def f_periodique(x):
    """Fonction périodique : f(x) = 1.5 + 0.6*sin(2πx/2.5) + 0.3*cos(4πx/2.5)"""
    return 1.5 + 0.6 * np.sin(2 * np.pi * x / 2.5) + 0.3 * np.cos(4 * np.pi * x / 2.5)

def f_exponentielle(x):
    """Fonction exponentielle : f(x) = e^(-x/2)"""
    return np.exp(-x/2)

def calculer_erreur(approximation, exacte):
    """Calcule l'erreur absolue et relative"""
    erreur_absolue = abs(approximation - exacte)
    erreur_relative = erreur_absolue / abs(exacte) if exacte != 0 else float('inf')
    return erreur_absolue, erreur_relative

def comparer_methodes_complet(f, a, b, n_points, nom_fonction="f(x)"):
    """
    Comparaison complète de toutes les méthodes d'intégration
    """
    print(f"\n{'='*80}")
    print(f"COMPARAISON DES MÉTHODES D'INTÉGRATION")
    print(f"Fonction: {nom_fonction} sur [{a}, {b}]")
    print(f"Nombre de points d'évaluation: {n_points}")
    print(f"{'='*80}")
    
    # Calcul de l'intégrale exacte (si disponible)
    try:
        if f == f_parabole:
            I_exacte = integrale_exacte_parabole(f, a, b)
        elif f == f_cubique:
            I_exacte = integrale_exacte_cubique(f, a, b)
        else:
            # Approximation numérique pour les autres fonctions
            from scipy.integrate import quad
            I_exacte, _ = quad(f, a, b)
        print(f"Intégrale exacte: I = {I_exacte:.10f}")
    except:
        I_exacte = None
        print("Intégrale exacte: Non disponible")
    
    print(f"\n{'Méthode':<20} {'Valeur':<15} {'Erreur abs.':<12} {'Erreur rel.':<12}")
    print("-" * 80)
    
    # Méthode des rectangles (gauche)
    I_rect_g, _, _, _ = methode_rectangles_gauche(f, a, b, n_points)
    if I_exacte is not None:
        err_abs, err_rel = calculer_erreur(I_rect_g, I_exacte)
        print(f"{'Rectangles gauche':<20} {I_rect_g:<15.8f} {err_abs:<12.2e} {err_rel:<12.2e}")
    else:
        print(f"{'Rectangles gauche':<20} {I_rect_g:<15.8f} {'N/A':<12} {'N/A':<12}")
    
    # Méthode des rectangles (droite)
    I_rect_d, _, _, _ = methode_rectangles_droite(f, a, b, n_points)
    if I_exacte is not None:
        err_abs, err_rel = calculer_erreur(I_rect_d, I_exacte)
        print(f"{'Rectangles droite':<20} {I_rect_d:<15.8f} {err_abs:<12.2e} {err_rel:<12.2e}")
    else:
        print(f"{'Rectangles droite':<20} {I_rect_d:<15.8f} {'N/A':<12} {'N/A':<12}")
    
    # Méthode des rectangles (milieu)
    I_rect_m, _, _, _ = methode_rectangles_milieu(f, a, b, n_points)
    if I_exacte is not None:
        err_abs, err_rel = calculer_erreur(I_rect_m, I_exacte)
        print(f"{'Rectangles milieu':<20} {I_rect_m:<15.8f} {err_abs:<12.2e} {err_rel:<12.2e}")
    else:
        print(f"{'Rectangles milieu':<20} {I_rect_m:<15.8f} {'N/A':<12} {'N/A':<12}")
    
    # Méthode des trapèzes
    I_trap, _, _, _ = methode_trapezes(f, a, b, n_points)
    if I_exacte is not None:
        err_abs, err_rel = calculer_erreur(I_trap, I_exacte)
        print(f"{'Trapèzes':<20} {I_trap:<15.8f} {err_abs:<12.2e} {err_rel:<12.2e}")
    else:
        print(f"{'Trapèzes':<20} {I_trap:<15.8f} {'N/A':<12} {'N/A':<12}")
    
    # Méthode de Simpson (n = n_points // 2)
    n_simpson = n_points // 2
    if n_simpson >= 1:
        I_simpson, _, _, _ = methode_simpson(f, a, b, n_simpson)
        if I_exacte is not None:
            err_abs, err_rel = calculer_erreur(I_simpson, I_exacte)
            print(f"{'Simpson (n='+str(n_simpson)+')':<20} {I_simpson:<15.8f} {err_abs:<12.2e} {err_rel:<12.2e}")
        else:
            print(f"{'Simpson (n='+str(n_simpson)+')':<20} {I_simpson:<15.8f} {'N/A':<12} {'N/A':<12}")
    
    return {
        'exacte': I_exacte,
        'rectangles_gauche': I_rect_g,
        'rectangles_droite': I_rect_d,
        'rectangles_milieu': I_rect_m,
        'trapezes': I_trap,
        'simpson': I_simpson if n_simpson >= 1 else None
    }

def etude_convergence(f, a, b, nom_fonction="f(x)"):
    """
    Étude de la convergence des différentes méthodes
    """
    print(f"\n{'='*80}")
    print(f"ÉTUDE DE CONVERGENCE - {nom_fonction}")
    print(f"Intervalle: [{a}, {b}]")
    print(f"{'='*80}")
    
    # Calcul de l'intégrale exacte
    try:
        if f == f_parabole:
            I_exacte = integrale_exacte_parabole(f, a, b)
        elif f == f_cubique:
            I_exacte = integrale_exacte_cubique(f, a, b)
        else:
            from scipy.integrate import quad
            I_exacte, _ = quad(f, a, b)
    except:
        print("Impossible de calculer l'intégrale exacte")
        return
    
    # Différents nombres de points
    n_points_list = [5, 10, 20, 50, 100]
    
    print(f"\n{'n_points':<10} {'Rect. milieu':<15} {'Trapèzes':<15} {'Simpson':<15} {'Erreur R.M.':<12} {'Erreur T.':<12} {'Erreur S.':<12}")
    print("-" * 100)
    
    for n in n_points_list:
        # Rectangles milieu
        I_rect_m, _, _, _ = methode_rectangles_milieu(f, a, b, n)
        err_rect = abs(I_rect_m - I_exacte)
        
        # Trapèzes
        I_trap, _, _, _ = methode_trapezes(f, a, b, n)
        err_trap = abs(I_trap - I_exacte)
        
        # Simpson
        n_simpson = n // 2
        if n_simpson >= 1:
            I_simpson, _, _, _ = methode_simpson(f, a, b, n_simpson)
            err_simpson = abs(I_simpson - I_exacte)
        else:
            I_simpson = None
            err_simpson = None
        
        print(f"{n:<10} {I_rect_m:<15.8f} {I_trap:<15.8f} {I_simpson if I_simpson else 'N/A':<15} {err_rect:<12.2e} {err_trap:<12.2e} {err_simpson if err_simpson else 'N/A':<12}")

def visualiser_comparaison(f, a, b, n_points, nom_fonction="f(x)"):
    """
    Visualisation comparative des méthodes
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Méthode des rectangles (milieu)
    ax1 = axes[0, 0]
    I_rect_m, points, hauteurs, largeur = methode_rectangles_milieu(f, a, b, n_points)
    
    x_curve = np.linspace(a, b, 1000)
    y_curve = f(x_curve)
    ax1.plot(x_curve, y_curve, 'r-', linewidth=2, label=f'{nom_fonction}')
    
    # Rectangles
    for i in range(n_points):
        x_rect = (points[i] + points[i+1]) / 2
        rect = plt.Rectangle((points[i], 0), largeur, hauteurs[i], 
                           linewidth=1, edgecolor='blue', 
                           facecolor='lightblue', alpha=0.7)
        ax1.add_patch(rect)
    
    ax1.set_title(f'Rectangles (milieu) - n={n_points}', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Méthode des trapèzes
    ax2 = axes[0, 1]
    I_trap, points, valeurs, h = methode_trapezes(f, a, b, n_points)
    
    ax2.plot(x_curve, y_curve, 'r-', linewidth=2, label=f'{nom_fonction}')
    
    # Trapèzes
    for i in range(n_points):
        x_trap = [points[i], points[i+1], points[i+1], points[i]]
        y_trap = [0, 0, valeurs[i+1], valeurs[i]]
        trap = plt.Polygon(list(zip(x_trap, y_trap)), 
                          linewidth=1, edgecolor='blue', 
                          facecolor='lightblue', alpha=0.7)
        ax2.add_patch(trap)
    
    ax2.set_title(f'Trapèzes - n={n_points}', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Méthode de Simpson
    ax3 = axes[1, 0]
    n_simpson = n_points // 2
    if n_simpson >= 1:
        I_simpson, points, valeurs, h = methode_simpson(f, a, b, n_simpson)
        
        ax3.plot(x_curve, y_curve, 'r-', linewidth=2, label=f'{nom_fonction}')
        
        # Paraboles de Simpson
        from methode_simpson import lagrange_interpolation
        for i in range(n_simpson):
            x_parabole = points[2*i:2*i+3]
            y_parabole = valeurs[2*i:2*i+3]
            poly = lagrange_interpolation(x_parabole, y_parabole)
            x_parabole_curve = np.linspace(x_parabole[0], x_parabole[2], 100)
            y_parabole_curve = poly(x_parabole_curve)
            ax3.plot(x_parabole_curve, y_parabole_curve, 'b--', linewidth=1.5, alpha=0.8)
            ax3.fill_between(x_parabole_curve, 0, y_parabole_curve, alpha=0.3, color='lightblue')
            ax3.plot(x_parabole, y_parabole, 'bo', markersize=4)
        
        ax3.set_title(f'Simpson - n={n_simpson}', fontweight='bold')
    else:
        ax3.text(0.5, 0.5, 'Simpson non applicable\n(n_points < 2)', 
                transform=ax3.transAxes, ha='center', va='center', fontsize=12)
        ax3.set_title('Simpson - Non applicable', fontweight='bold')
    
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # Graphique de convergence
    ax4 = axes[1, 1]
    n_list = [5, 10, 20, 50, 100]
    erreurs_rect = []
    erreurs_trap = []
    erreurs_simpson = []
    
    try:
        if f == f_parabole:
            I_exacte = integrale_exacte_parabole(f, a, b)
        elif f == f_cubique:
            I_exacte = integrale_exacte_cubique(f, a, b)
        else:
            from scipy.integrate import quad
            I_exacte, _ = quad(f, a, b)
        
        for n in n_list:
            _, _, _, _ = methode_rectangles_milieu(f, a, b, n)
            I_rect_m, _, _, _ = methode_rectangles_milieu(f, a, b, n)
            erreurs_rect.append(abs(I_rect_m - I_exacte))
            
            I_trap, _, _, _ = methode_trapezes(f, a, b, n)
            erreurs_trap.append(abs(I_trap - I_exacte))
            
            n_simpson = n // 2
            if n_simpson >= 1:
                I_simpson, _, _, _ = methode_simpson(f, a, b, n_simpson)
                erreurs_simpson.append(abs(I_simpson - I_exacte))
            else:
                erreurs_simpson.append(None)
        
        ax4.loglog(n_list, erreurs_rect, 'o-', label='Rectangles (milieu)', linewidth=2)
        ax4.loglog(n_list, erreurs_trap, 's-', label='Trapèzes', linewidth=2)
        ax4.loglog([n for n, err in zip(n_list, erreurs_simpson) if err is not None], 
                  [err for err in erreurs_simpson if err is not None], 
                  '^-', label='Simpson', linewidth=2)
        ax4.set_xlabel('Nombre de points')
        ax4.set_ylabel('Erreur absolue')
        ax4.set_title('Convergence des méthodes', fontweight='bold')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
    except:
        ax4.text(0.5, 0.5, 'Convergence non calculable', 
                transform=ax4.transAxes, ha='center', va='center', fontsize=12)
        ax4.set_title('Convergence - Non calculable', fontweight='bold')
    
    plt.tight_layout()
    return fig

def main():
    """
    Fonction principale pour la comparaison complète
    """
    print("COMPARAISON COMPLÈTE DES MÉTHODES D'INTÉGRATION NUMÉRIQUE")
    print("=" * 80)
    
    # Exemples de fonctions
    fonctions = [
        (f_parabole, 0, 5, "f(x) = 0.1x²"),
        (f_cubique, 0, 3, "f(x) = x³ - 2x² + x + 1"),
        (f_periodique, 0, 5, "f(x) = 1.5 + 0.6sin(2πx/2.5) + 0.3cos(4πx/2.5)"),
        (f_exponentielle, 0, 4, "f(x) = e^(-x/2)")
    ]
    
    # Comparaison pour chaque fonction
    for f, a, b, nom in fonctions:
        comparer_methodes_complet(f, a, b, 20, nom)
        etude_convergence(f, a, b, nom)
        
        # Visualisation
        fig = visualiser_comparaison(f, a, b, 10, nom)
        plt.show()
    
    print(f"\n{'='*80}")
    print("CONCLUSIONS:")
    print("- La méthode de Simpson est généralement la plus précise")
    print("- Les rectangles (milieu) sont souvent plus précis que les rectangles (gauche/droite)")
    print("- La méthode des trapèzes offre un bon compromis simplicité/précision")
    print("- Simpson est exact pour les polynômes de degré ≤ 3")
    print("- La convergence de Simpson est généralement en O(h^4)")
    print("- La convergence des trapèzes est en O(h^2)")
    print("- La convergence des rectangles est en O(h)")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
