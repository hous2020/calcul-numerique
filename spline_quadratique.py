import numpy as np
import matplotlib.pyplot as plt

def calcul_coefficients_spline_quadratique(x, y):
   
    n = len(x) - 1  # n+1 points => n intervalles
    
    # Initialisation des tableaux de coefficients
    a = np.zeros(n)
    b = np.zeros(n)
    c = np.zeros(n)
    
    # Calcul des z_i (dérivées aux points x_i)
    z = np.zeros(n+1)
    z[0] = 1  # Condition z_0 = 0 pour fixer la solution
    
    # Calcul récursif des z_i
    for i in range(n):
        z[i+1] = 2 * (y[i+1] - y[i]) / (x[i+1] - x[i]) - z[i]
    
    # Calcul des coefficients a_i, b_i, c_i
    for i in range(n):
        c[i] = y[i]  # c_i = y_i
        b[i] = z[i]  # b_i = z_i
        a[i] = (z[i+1] - z[i]) / (2 * (x[i+1] - x[i]))  
    return a, b, c

def evaluer_spline(x_eval, x, a, b, c):
    
    n = len(x) - 1
    
    # Trouver l'intervalle [x_i, x_{i+1}] contenant x_eval
    i = 0
    while i < n and x_eval > x[i+1]:
        i += 1
    
    if i >= n:  # Si x_eval est hors de l'intervalle [x_0, x_n]
        i = n - 1
    
    # Évaluer s_i(x) = a_i * (x - x_i)^2 + b_i * (x - x_i) + c_i
    return a[i] * (x_eval - x[i])**2 + b[i] * (x_eval - x[i]) + c[i]

def test_spline_quadratique():
    """
    Teste la spline quadratique sur une fonction simple.
    """
    # Définir une fonction de test
    def f(x):
        return np.sin(x)  
    # Créer des points d'échantillonnage
    x = np.linspace(0, 2*np.pi, 7)  # 7 points équidistants
    y = f(x)
    
    # Calculer les coefficients de la spline
    a, b, c = calcul_coefficients_spline_quadratique(x, y)
    
    # Créer des points pour tracer la spline
    x_plot = np.linspace(0, 2*np.pi, 200)
    y_plot = np.array([evaluer_spline(xi, x, a, b, c) for xi in x_plot])
    
    # Tracer la fonction originale et la spline
    plt.figure(figsize=(10, 6))
    plt.plot(x_plot, f(x_plot), 'b-', label='Fonction originale (s(x))')
    plt.plot(x_plot, y_plot, 'r--', label='Spline quadratique')
    plt.plot(x, y, 'ko', label='Points d\'interpolation')
    plt.legend()
    plt.grid(True)
    plt.title('Approximation par spline quadratique')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig('spline_quadratique.png')
    plt.show()
    
    # Calculer l'erreur d'approximation
    erreur = np.abs(f(x_plot) - y_plot)
    print(f"Erreur maximale: {erreur.max():.6f}")
    print(f"Erreur moyenne: {erreur.mean():.6f}")

if __name__ == "__main__":
    test_spline_quadratique()