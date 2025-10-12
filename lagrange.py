import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Fonction de calcul de Lagrange (inchangée) ---

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

# --- Classe pour l'interface graphique ---

class LagrangeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interpolation de Lagrange Interactive")

        # Frame pour les entrées
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Fonction f(x):").pack(side=tk.LEFT, padx=5)
        self.func_entry = tk.Entry(input_frame, width=30)
        self.func_entry.insert(0, "sin(x) + 0.5*x")
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
            f = sp.lambdify(x_sym, func_expr, 'numpy')
        except (sp.SympifyError, SyntaxError):
            messagebox.showerror("Erreur", f"Fonction invalide: {func_str}")
            return

        # Points d'interpolation et de tracé
        x_nodes = np.linspace(0, 2 * np.pi, 9)
        y_nodes = f(x_nodes)
        x_plot = np.linspace(x_nodes[0], x_nodes[-1], 400)
        y_true = f(x_plot)

        # Calcul de l'interpolation et de l'erreur
        y_lagrange = lagrange_interpolation(x_nodes, y_nodes, x_plot)
        erreur = np.abs(y_lagrange - y_true)

        # Nettoyer et redessiner le graphique
        self.fig.clear()

        # Premier sous-graphique : Fonction et Polynôme
        ax1 = self.fig.add_subplot(2, 1, 1)
        ax1.plot(x_plot, y_true, 'b-', label=f'Fonction: ${sp.latex(func_expr)}$')
        ax1.plot(x_nodes, y_nodes, 'ro', label='Points d\'interpolation')
        ax1.plot(x_plot, y_lagrange, 'g--', label='Polynôme de Lagrange')
        ax1.legend()
        ax1.grid(True)
        ax1.set_title('Approximation par Polynôme de Lagrange')
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')

        # Deuxième sous-graphique : Erreur
        ax2 = self.fig.add_subplot(2, 1, 2)
        ax2.plot(x_plot, erreur, 'm-', label='Erreur absolue')
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
    app = LagrangeApp(root)
    root.mainloop()