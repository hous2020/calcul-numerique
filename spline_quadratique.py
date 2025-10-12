import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Fonctions de calcul de la spline (inchangées) ---

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

# --- Classe pour l'interface graphique ---

class SplineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spline Quadratique Interactive")

        # Frame pour les entrées
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Fonction f(x):").pack(side=tk.LEFT, padx=5)
        self.func_entry = tk.Entry(input_frame, width=30)
        self.func_entry.insert(0, "sin(x)")
        self.func_entry.pack(side=tk.LEFT, padx=5)

        plot_button = tk.Button(input_frame, text="Générer le graphique", command=self.plot)
        plot_button.pack(side=tk.LEFT, padx=5)

        # Zone pour le graphique Matplotlib
        self.fig = plt.figure(figsize=(10, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        # Afficher le graphique initial
        self.plot()

    def plot(self):
        func_str = self.func_entry.get()
        if not func_str:
            messagebox.showerror("Erreur", "Veuillez entrer une fonction.")
            return

        x_sym = sp.Symbol('x')
        try:
            func_expr = sp.sympify(func_str)
        except (sp.SympifyError, SyntaxError):
            messagebox.showerror("Erreur", f"Fonction invalide: {func_str}")
            return

        f_prime_expr = sp.diff(func_expr, x_sym)
        f = sp.lambdify(x_sym, func_expr, 'numpy')
        f_prime = sp.lambdify(x_sym, f_prime_expr, 'numpy')

        x_min, x_max = 0, 2 * np.pi
        x = np.linspace(x_min, x_max, 7)
        y = f(x)

        try:
            f_prime_0 = f_prime(x[0])
        except Exception as e:
            messagebox.showerror("Erreur de calcul", f"Impossible d'évaluer la dérivée en x=0.\n{e}")
            return

        a, b, c = calcul_coefficients_spline_quadratique(x, y, f_prime_0)

        x_plot = np.linspace(x_min, x_max, 200)
        y_plot = np.array([evaluer_spline(xi, x, a, b, c) for xi in x_plot])
        erreur = np.abs(f(x_plot) - y_plot)

        # Nettoyer et redessiner le graphique
        self.fig.clear()

        # Premier sous-graphique : Fonction et Spline
        ax1 = self.fig.add_subplot(2, 1, 1)
        ax1.plot(x_plot, f(x_plot), 'b-', label=f'Fonction: ${sp.latex(func_expr)}$')
        ax1.plot(x_plot, y_plot, 'r--', label='Spline quadratique')
        ax1.plot(x, y, 'ko', label='Points d\'interpolation')
        ax1.legend()
        ax1.grid(True)
        ax1.set_title('Approximation par spline quadratique')
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')

        # Deuxième sous-graphique : Erreur
        ax2 = self.fig.add_subplot(2, 1, 2)
        ax2.plot(x_plot, erreur, 'g-', label='Erreur d\'approximation')
        ax2.legend()
        ax2.grid(True)
        ax2.set_title('Erreur d\'approximation')
        ax2.set_xlabel('x')
        ax2.set_ylabel('Erreur')

        self.fig.tight_layout()
        self.canvas.draw()

# --- Point d'entrée de l'application ---

if __name__ == "__main__":
    root = tk.Tk()
    app = SplineApp(root)
    root.mainloop()