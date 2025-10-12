import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# --- Fonctions importées de lagrange.py et spline_quadratique.py ---

def lagrange_interpolation(x_points, y_points, x_interp):
    n = len(x_points)
    x_interp = np.asarray(x_interp)
    P_x = np.zeros_like(x_interp, dtype=float)
    for i in range(n):
        L_i = np.ones_like(x_interp, dtype=float)
        for j in range(n):
            if i != j:
                L_i *= (x_interp - x_points[j]) / (x_points[i] - x_points[j])
        P_x += y_points[i] * L_i
    return P_x

def calcul_coefficients_spline_quadratique(x, y, f_prime_0):
    n = len(x) - 1
    a = np.zeros(n)
    b = np.zeros(n)
    c = np.zeros(n)
    z = np.zeros(n+1)
    z[0] = f_prime_0
    for i in range(n):
        z[i+1] = 2 * (y[i+1] - y[i]) / (x[i+1] - x[i]) - z[i]
    for i in range(n):
        c[i] = y[i]
        b[i] = z[i]
        a[i] = (z[i+1] - z[i]) / (2 * (x[i+1] - x[i]))
    return a, b, c

def evaluer_spline(x_eval, x, a, b, c):
    n = len(x) - 1
    i = 0
    while i < n and x_eval > x[i+1]:
        i += 1
    if i >= n:
        i = n - 1
    return a[i] * (x_eval - x[i])**2 + b[i] * (x_eval - x[i]) + c[i]

# --- Script de comparaison ---

if __name__ == "__main__":
    # Définir la fonction à approximer et sa dérivée
    x_sym = sp.Symbol('x')
    func_expr = sp.sin(x_sym) + 0.5 * x_sym
    f_prime_expr = sp.diff(func_expr, x_sym)
    
    f = sp.lambdify(x_sym, func_expr, 'numpy')
    f_prime = sp.lambdify(x_sym, f_prime_expr, 'numpy')

    # Points d'interpolation communs
    x_nodes = np.linspace(0, 2 * np.pi, 8)
    y_nodes = f(x_nodes)

    # Points de tracé
    x_plot = np.linspace(x_nodes[0], x_nodes[-1], 400)
    y_true = f(x_plot)

    # 1. Calcul de l'erreur pour Lagrange
    y_lagrange = lagrange_interpolation(x_nodes, y_nodes, x_plot)
    erreur_lagrange = np.abs(y_lagrange - y_true)

    # 2. Calcul de l'erreur pour la spline quadratique
    f_prime_0 = f_prime(x_nodes[0])
    a, b, c = calcul_coefficients_spline_quadratique(x_nodes, y_nodes, f_prime_0)
    y_spline = np.array([evaluer_spline(xi, x_nodes, a, b, c) for xi in x_plot])
    erreur_spline = np.abs(y_spline - y_true)

    # 3. Tracé comparatif des erreurs
    plt.figure(figsize=(12, 7))
    plt.plot(x_plot, erreur_lagrange, 'r-', label='Erreur de Lagrange')
    plt.plot(x_plot, erreur_spline, 'b--', label='Erreur de la Spline Quadratique')
    plt.title('Comparaison des Erreurs d\'Approximation')
    plt.xlabel('x')
    plt.ylabel('Erreur absolue')
    plt.legend()
    plt.grid(True)
    plt.yscale('log') # Échelle logarithmique pour mieux voir les petites erreurs
    plt.show()

    print(f"Erreur maximale (Lagrange): {np.max(erreur_lagrange):.6f}")
    print(f"Erreur maximale (Spline):   {np.max(erreur_spline):.6f}")
