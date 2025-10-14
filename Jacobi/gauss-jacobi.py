import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import re

# --- Fonctions utilitaires de base ---

def calculate_inf_norm(vec):
    """Calcule la norme infinie (max |x_i|) d'un vecteur."""
    return max(abs(val) for val in vec)

def multiply_matrix_vector(A, x):
    """Produit matriciel standard A * x."""
    return [sum(A[i][j] * x[j] for j in range(len(A[0]))) for i in range(len(A))]

def subtract_vectors(v1, v2):
    """Soustrait deux vecteurs : v1 - v2."""
    if len(v1) != len(v2):
        raise ValueError("Les vecteurs doivent avoir la même taille.")
    return [v1[i] - v2[i] for i in range(len(v1))]

def copy_vector(vec):
    """Retourne une copie indépendante du vecteur."""
    return vec[:]

# --- Méthode de Jacobi  ---

def jacobi(A, b, x0, epsilon=1e-9, max_iter=1000):
    """
    Méthode de Jacobi pour résoudre Ax = b.
    Algorithme conforme au pseudocode de l'image.
    """
    n = len(b)
    x_new = copy_vector(x0)  # x_new ← x0
    nb = 0  # nb ← 0
    
    # Calcul du résidu initial
    residu = subtract_vectors(multiply_matrix_vector(A, x_new), b)
    
    # tant que (||Ax_new - b|| > ε) et (nb < MAXITER) faire
    while calculate_inf_norm(residu) > epsilon and nb < max_iter:
        nb += 1  # nb ← nb+1
        
        # Sauvegarder x_new comme x_old pour la formule de Jacobi
        x_old = copy_vector(x_new)
        
        # pour i = 1 à n faire
        for i in range(n):
            # x_i_new ← (b_i - Σ(j≠i) a_ij * x_j_old) / a_ii
            s = sum(A[i][j] * x_old[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]
        
        # Recalculer le résidu
        residu = subtract_vectors(multiply_matrix_vector(A, x_new), b)
    
    return x_new, nb, calculate_inf_norm(residu) <= epsilon

# --- Méthode de Gauss-Seidel (selon l'algorithme ) ---

def gauss_seidel(A, b, x0, epsilon=1e-9, max_iter=1000):
    """
    Méthode de Gauss-Seidel pour résoudre Ax = b.
    Algorithme conforme au pseudocode de l'image.
    L'algorithme de GAUSS-SEIDEL modifie l'algorithme de Jacobi 
    pour utiliser à chaque itération les valeurs x_i^(k+1) déjà calculées.
    """
    n = len(b)
    x_new = copy_vector(x0)  # x_new ← x0
    nb = 0  # nb ← 0
    
    # Calcul du résidu initial
    residu = subtract_vectors(multiply_matrix_vector(A, x_new), b)
    
    # tant que (||Ax_new - b|| > ε) et (nb < MAXITER) faire
    while calculate_inf_norm(residu) > epsilon and nb < max_iter:
        nb += 1  # nb ← nb+1
        
        # Sauvegarder x_new comme x_old AVANT de commencer les calculs
        x_old = copy_vector(x_new)
        
        # pour i = 1 à n faire
        for i in range(n):
            # x_i_new ← (b_i - Σ(j<i) a_ij * x_j_new - Σ(j>i) a_ij * x_j_old) / a_ii
            # Utilise les valeurs déjà calculées dans la même itération (j < i)
            # et les anciennes valeurs pour (j > i)
            s1 = sum(A[i][j] * x_new[j] for j in range(i))  # Σ(j<i) a_ij * x_j_new
            s2 = sum(A[i][j] * x_old[j] for j in range(i + 1, n))  # Σ(j>i) a_ij * x_j_old
            x_new[i] = (b[i] - s1 - s2) / A[i][i]
        
        # Recalculer le résidu
        residu = subtract_vectors(multiply_matrix_vector(A, x_new), b)
    
    return x_new, nb, calculate_inf_norm(residu) <= epsilon

# --- Méthodes avec historique pour les graphiques ---

def jacobi_with_history(A, b, x0, epsilon=1e-9, max_iter=1000):
    """
    Méthode de Jacobi avec historique des erreurs pour les graphiques.
    """
    n = len(b)
    x_new = copy_vector(x0)
    nb = 0
    errors = []
    residuals = []
    
    residu = subtract_vectors(multiply_matrix_vector(A, x_new), b)
    residuals.append(calculate_inf_norm(residu))
    errors.append(calculate_inf_norm(subtract_vectors(x_new, [0]*n)))  # Erreur par rapport à 0
    
    while calculate_inf_norm(residu) > epsilon and nb < max_iter:
        nb += 1
        x_old = copy_vector(x_new)
        
        for i in range(n):
            s = sum(A[i][j] * x_old[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]
        
        residu = subtract_vectors(multiply_matrix_vector(A, x_new), b)
        residuals.append(calculate_inf_norm(residu))
        errors.append(calculate_inf_norm(subtract_vectors(x_new, [0]*n)))
    
    return x_new, nb, calculate_inf_norm(residu) <= epsilon, residuals, errors

def gauss_seidel_with_history(A, b, x0, epsilon=1e-9, max_iter=1000):
    """
    Méthode de Gauss-Seidel avec historique des erreurs pour les graphiques.
    """
    n = len(b)
    x_new = copy_vector(x0)
    nb = 0
    errors = []
    residuals = []
    
    residu = subtract_vectors(multiply_matrix_vector(A, x_new), b)
    residuals.append(calculate_inf_norm(residu))
    errors.append(calculate_inf_norm(subtract_vectors(x_new, [0]*n)))
    
    while calculate_inf_norm(residu) > epsilon and nb < max_iter:
        nb += 1
        x_old = copy_vector(x_new)
        
        for i in range(n):
            s1 = sum(A[i][j] * x_new[j] for j in range(i))
            s2 = sum(A[i][j] * x_old[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - s1 - s2) / A[i][i]
        
        residu = subtract_vectors(multiply_matrix_vector(A, x_new), b)
        residuals.append(calculate_inf_norm(residu))
        errors.append(calculate_inf_norm(subtract_vectors(x_new, [0]*n)))
    
    return x_new, nb, calculate_inf_norm(residu) <= epsilon, residuals, errors

# --- Méthode de Newton (selon l'algorithme de l'image) ---

def newton_method(f, jacobian_f, x0, epsilon=1e-9, max_iter=1000):
    """
    Méthode de Newton pour résoudre f(x) = 0.
    Algorithme conforme au pseudocode de l'image.
    
    Args:
        f: Fonction vectorielle f: R^n -> R^n
        jacobian_f: Fonction qui calcule la matrice Jacobienne de f
        x0: Point initial
        epsilon: Tolérance
        max_iter: Nombre maximum d'itérations
    
    Returns:
        (solution, nb_iterations, converged)
    """
    n = 0  # n ← 0
    
    # répéter
    while True:
        n += 1  # n ← n + 1
        x = copy_vector(x0)  # x ← x0
        b = f(x)  # b ← f(x)
        A = jacobian_f(x)  # A ← ∇f(x)
        
        # résoudre Ay = b
        try:
            y = solve_linear_system(A, b)  # Solution du système linéaire
        except:
            return x0, n, False  # Échec si le système est singulier
        
        x0 = subtract_vectors(x, y)  # x0 ← x - y
        
        # jusqu'à (||x - x0|| ≤ ε) ou (n = NMAX)
        if calculate_inf_norm(subtract_vectors(x, x0)) <= epsilon:
            return x0, n, True  # Convergence réussie
        elif n >= max_iter:
            return x0, n, False  # Échec - maximum d'itérations atteint

def solve_linear_system(A, b):
    """
    Résout le système linéaire Ax = b en utilisant la méthode de Jacobi.
    """
    n = len(b)
    x = [0.0] * n
    x_new = [0.0] * n
    max_iter = 1000
    epsilon = 1e-12
    
    for _ in range(max_iter):
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]
        
        # Vérifier la convergence
        if calculate_inf_norm(subtract_vectors(x_new, x)) < epsilon:
            return x_new
        
        x = copy_vector(x_new)
    
    return x_new

# --- Exemples d'utilisation ---

if __name__ == "__main__":
    A = [
        [10.0, -1.0, 2.0, 0.0],
        [-1.0, 11.0, -1.0, 3.0],
        [2.0, -1.0, 10.0, -1.0],
        [0.0, 3.0, -1.0, 8.0]
    ]
    b = [6.0, 25.0, -11.0, 15.0]
    x0 = [0.0, 0.0, 0.0, 0.0]

    print("\n--- Solution exacte ---")
    print(np.linalg.solve(A, b))
    print("=" * 50)

    print("\n--- Méthode de Jacobi ---")
    sol_jacobi, iter_jacobi, conv_jacobi = jacobi(A, b, x0)
    print(f"Solution : {np.round(sol_jacobi, 4)}")
    print(f"Itérations : {iter_jacobi} | Convergé : {conv_jacobi}")

    print("\n--- Méthode de Gauss-Seidel ---")
    sol_gs, iter_gs, conv_gs = gauss_seidel(A, b, x0)
    print(f"Solution : {np.round(sol_gs, 4)}")
    print(f"Itérations : {iter_gs} | Convergé : {conv_gs}")
    
    print("\n" + "=" * 50)
    print("--- Méthode de Newton (exemple 2D) ---")
    
    # Exemple de système non-linéaire 2D: x² + y² = 4, x - y = 0
    def f_2d(x):
        return [x[0]**2 + x[1]**2 - 4, x[0] - x[1]]
    
    def jacobian_2d(x):
        return [[2*x[0], 2*x[1]], [1, -1]]
    
    x0_newton = [2.0, 2.0]
    sol_newton, iter_newton, conv_newton = newton_method(f_2d, jacobian_2d, x0_newton)
    print(f"Solution : {np.round(sol_newton, 4)}")
    print(f"Itérations : {iter_newton} | Convergé : {conv_newton}")
    print(f"Vérification f(solution) : {np.round(f_2d(sol_newton), 6)}")

# --- Interface Graphique ---

class JacobiGUI:
    """
    Interface graphique pour comparer les méthodes de Jacobi et Gauss-Seidel.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Comparaison des Méthodes de Résolution - Jacobi & Gauss-Seidel")
        self.root.geometry("1400x900")
        
        # Variables
        self.tolerance = tk.DoubleVar(value=1e-9)
        self.max_iterations = tk.IntVar(value=1000)
        self.current_system = 0
        
        # Données fixes prédéfinies
        self.systems = [
            {
                'name': 'Système 4x4 (Diagonale Dominante)',
                'A': [
                    [10.0, -1.0, 2.0, 0.0],
                    [-1.0, 11.0, -1.0, 3.0],
                    [2.0, -1.0, 10.0, -1.0],
                    [0.0, 3.0, -1.0, 8.0]
                ],
                'b': [6.0, 25.0, -11.0, 15.0]
            },
            {
                'name': 'Système 3x3 (Diagonale Dominante)',
                'A': [
                    [4.0, -1.0, 0.0],
                    [-1.0, 4.0, -1.0],
                    [0.0, -1.0, 4.0]
                ],
                'b': [2.0, 6.0, 2.0]
            },
            {
                'name': 'Système 5x5 (Diagonale Dominante)',
                'A': [
                    [6.0, -1.0, 0.0, 0.0, 0.0],
                    [-1.0, 6.0, -1.0, 0.0, 0.0],
                    [0.0, -1.0, 6.0, -1.0, 0.0],
                    [0.0, 0.0, -1.0, 6.0, -1.0],
                    [0.0, 0.0, 0.0, -1.0, 6.0]
                ],
                'b': [1.0, 2.0, 3.0, 4.0, 5.0]
            },
            {
                'name': 'Système 2x2 (Simple)',
                'A': [
                    [3.0, -1.0],
                    [-1.0, 3.0]
                ],
                'b': [1.0, 2.0]
            }
        ]
        
        # Données actuelles
        self.matrix_A = self.systems[0]['A']
        self.vector_b = self.systems[0]['b']
        self.results = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface utilisateur - Seulement les courbes."""
        # Frame principal - Plein écran
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # === SECTION GRAPHIQUES (plein écran) ===
        # Figure matplotlib (plein écran)
        self.fig = Figure(figsize=(18, 12), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Barre d'outils matplotlib
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar = NavigationToolbar2Tk(self.canvas, main_frame)
        toolbar.update()
        
        # Raccourcis clavier
        self.root.bind('<KeyPress-n>', lambda e: self.change_system())
        self.root.bind('<KeyPress-r>', lambda e: self.solve_and_compare())
        self.root.focus_set()  # Pour capturer les touches
        
        # Initialisation automatique
        self.load_current_system()
        self.solve_and_compare()
    
    def load_current_system(self):
        """Charge le système actuel."""
        system = self.systems[self.current_system]
        self.matrix_A = system['A']
        self.vector_b = system['b']
    
    def change_system(self):
        """Change vers le système suivant."""
        self.current_system = (self.current_system + 1) % len(self.systems)
        self.load_current_system()
        self.solve_and_compare()
    
    def solve_and_compare(self):
        """Résout le système et compare les méthodes."""
        try:
            # Utiliser les données fixes actuelles
            A = self.matrix_A
            b = self.vector_b
            
            # Point initial
            x0 = [0.0] * len(b)
            
            # Résoudre avec Jacobi
            sol_jacobi, iter_jacobi, conv_jacobi, res_jacobi, err_jacobi = jacobi_with_history(
                A, b, x0, self.tolerance.get(), self.max_iterations.get()
            )
            
            # Résoudre avec Gauss-Seidel
            sol_gs, iter_gs, conv_gs, res_gs, err_gs = gauss_seidel_with_history(
                A, b, x0, self.tolerance.get(), self.max_iterations.get()
            )
            
            # Solution exacte pour comparaison
            try:
                A_np = np.array(A)
                b_np = np.array(b)
                sol_exacte = np.linalg.solve(A_np, b_np)
            except:
                sol_exacte = None
            
            # Stocker les résultats
            self.results = {
                'Jacobi': {
                    'solution': sol_jacobi,
                    'iterations': iter_jacobi,
                    'converged': conv_jacobi,
                    'residuals': res_jacobi,
                    'errors': err_jacobi
                },
                'Gauss-Seidel': {
                    'solution': sol_gs,
                    'iterations': iter_gs,
                    'converged': conv_gs,
                    'residuals': res_gs,
                    'errors': err_gs
                },
                'exact': sol_exacte
            }
            
            # Afficher seulement les graphiques
            self.plot_convergence()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la résolution:\n{str(e)}")
    
    
    def plot_convergence(self):
        """Affiche les 2 graphiques de convergence : Erreurs et Solutions."""
        if not self.results or 'Jacobi' not in self.results:
            return
        
        self.fig.clear()
        
        # Couleurs et styles améliorés
        colors = {'Jacobi': '#1f77b4', 'Gauss-Seidel': '#ff7f0e', 'Exact': '#2ca02c'}
        markers = {'Jacobi': 'o', 'Gauss-Seidel': 's', 'Exact': '^'}
        
        # Graphique 1: Convergence des Erreurs (à gauche)
        ax1 = self.fig.add_subplot(121)
        ax1.semilogy(self.results['Jacobi']['errors'], color=colors['Jacobi'], 
                    linewidth=4, label='Jacobi', marker=markers['Jacobi'], 
                    markersize=6, markevery=max(1, len(self.results['Jacobi']['errors'])//8))
        ax1.semilogy(self.results['Gauss-Seidel']['errors'], color=colors['Gauss-Seidel'], 
                    linewidth=4, label='Gauss-Seidel', marker=markers['Gauss-Seidel'], 
                    markersize=6, markevery=max(1, len(self.results['Gauss-Seidel']['errors'])//8))
        ax1.set_xlabel('Itération', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Erreur ||x||', fontsize=14, fontweight='bold')
        ax1.set_title('Convergence des Erreurs', fontsize=16, fontweight='bold')
        ax1.legend(fontsize=12)
        ax1.grid(True, alpha=0.4, linestyle='--')
        ax1.tick_params(labelsize=12)
        
        # Graphique 2: Comparaison des Solutions (à droite)
        ax2 = self.fig.add_subplot(122)
        n = len(self.results['Jacobi']['solution'])
        x_indices = list(range(n))
        
        ax2.plot(x_indices, self.results['Jacobi']['solution'], color=colors['Jacobi'], 
                linewidth=4, markersize=10, label='Jacobi', marker=markers['Jacobi'])
        ax2.plot(x_indices, self.results['Gauss-Seidel']['solution'], color=colors['Gauss-Seidel'], 
                linewidth=4, markersize=10, label='Gauss-Seidel', marker=markers['Gauss-Seidel'])
        
        if self.results['exact'] is not None:
            ax2.plot(x_indices, self.results['exact'], color=colors['Exact'], 
                    linewidth=4, markersize=12, label='Solution exacte', marker=markers['Exact'])
        
        ax2.set_xlabel('Composante', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Valeur', fontsize=14, fontweight='bold')
        ax2.set_title('Comparaison des Solutions', fontsize=16, fontweight='bold')
        ax2.legend(fontsize=12)
        ax2.grid(True, alpha=0.4, linestyle='--')
        ax2.tick_params(labelsize=12)
        
        # Titre principal avec instructions
        system_name = self.systems[self.current_system]['name']
        self.fig.suptitle(f'Analyse de Convergence - {system_name}\n\n' +
                         'Raccourcis: N = Système suivant | R = Recalculer | Barre d\'outils pour zoom/pan', 
                         fontsize=16, fontweight='bold', y=0.95)
        
        # Ajustement de l'espacement pour 2 graphiques
        self.fig.tight_layout(rect=[0, 0.05, 1, 0.90])
        self.canvas.draw()

def main_gui():
    """Fonction principale pour lancer l'interface graphique."""
    root = tk.Tk()
    app = JacobiGUI(root)
    root.mainloop()

if __name__ == "__main__":
    # Lancer l'interface graphique
    main_gui()