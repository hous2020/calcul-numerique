import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Core Calculation Functions ---

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
    a, b, c = np.zeros(n), np.zeros(n), np.zeros(n)
    z = np.zeros(n + 1)
    z[0] = f_prime_0
    for i in range(n):
        z[i+1] = 2 * (y[i+1] - y[i]) / (x[i+1] - x[i]) - z[i]
    for i in range(n):
        c[i], b[i], a[i] = y[i], z[i], (z[i+1] - z[i]) / (2 * (x[i+1] - x[i]))
    return a, b, c

def evaluer_spline(x_eval, x, a, b, c):
    n = len(x) - 1
    i = np.searchsorted(x, x_eval, side='right') - 1
    i = max(0, min(i, n - 1))
    return a[i] * (x_eval - x[i])**2 + b[i] * (x_eval - x[i]) + c[i]

# --- Main GUI Application ---

class AnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analyse Numérique : Interpolation et Approximation")

        # --- Controls Frame ---
        controls_frame = tk.Frame(root, padx=10, pady=10)
        controls_frame.pack()

        # Function Entry
        tk.Label(controls_frame, text="Fonction f(x):").grid(row=0, column=0, sticky='w')
        self.func_entry = tk.Entry(controls_frame, width=30)
        self.func_entry.insert(0, "sin(x)")
        self.func_entry.grid(row=0, column=1, padx=5)

        # Analysis Type
        self.analysis_mode = tk.StringVar(value="compare")
        tk.Radiobutton(controls_frame, text="Comparer Erreurs", variable=self.analysis_mode, value="compare").grid(row=1, column=0, sticky='w')
        tk.Radiobutton(controls_frame, text="Lagrange", variable=self.analysis_mode, value="lagrange").grid(row=1, column=1, sticky='w')
        tk.Radiobutton(controls_frame, text="Spline Quadratique", variable=self.analysis_mode, value="spline").grid(row=1, column=2, sticky='w')

        # Plot Button
        plot_button = tk.Button(controls_frame, text="Générer le graphique", command=self.run_analysis)
        plot_button.grid(row=0, column=2, padx=10)

        # --- Matplotlib Canvas ---
        self.fig = plt.figure(figsize=(12, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.run_analysis() # Initial plot

    def run_analysis(self):
        func_str = self.func_entry.get()
        if not func_str:
            messagebox.showerror("Erreur", "Veuillez entrer une fonction.")
            return

        x_sym = sp.Symbol('x')
        try:
            func_expr = sp.sympify(func_str)
            f = sp.lambdify(x_sym, func_expr, 'numpy')
            f_prime = sp.lambdify(x_sym, sp.diff(func_expr, x_sym), 'numpy')
        except (sp.SympifyError, SyntaxError):
            messagebox.showerror("Erreur", f"Fonction invalide: {func_str}")
            return

        self.fig.clear()
        mode = self.analysis_mode.get()

        x_nodes = np.linspace(0, 2 * np.pi, 9)
        y_nodes = f(x_nodes)
        x_plot = np.linspace(x_nodes[0], x_nodes[-1], 400)
        y_true = f(x_plot)

        # --- Lagrange Calculation ---
        y_lagrange = lagrange_interpolation(x_nodes, y_nodes, x_plot)
        erreur_lagrange = np.abs(y_lagrange - y_true)

        # --- Spline Calculation ---
        try:
            f_prime_0 = f_prime(x_nodes[0])
        except Exception as e:
            messagebox.showerror("Erreur de calcul", f"Impossible d'évaluer la dérivée en x=0.\n{e}")
            return
        a, b, c = calcul_coefficients_spline_quadratique(x_nodes, y_nodes, f_prime_0)
        y_spline = np.array([evaluer_spline(xi, x_nodes, a, b, c) for xi in x_plot])
        erreur_spline = np.abs(y_spline - y_true)

        # --- Plotting ---
        if mode == "lagrange":
            self.plot_single(x_plot, y_true, x_nodes, y_nodes, y_lagrange, erreur_lagrange, f'Lagrange: ${sp.latex(func_expr)}$', 'Polynôme de Lagrange')
        elif mode == "spline":
            self.plot_single(x_plot, y_true, x_nodes, y_nodes, y_spline, erreur_spline, f'Spline: ${sp.latex(func_expr)}$', 'Spline Quadratique')
        else: # Compare
            self.plot_comparison(x_plot, erreur_lagrange, erreur_spline)
        
        self.canvas.draw()

    def plot_single(self, x_plot, y_true, x_nodes, y_nodes, y_approx, erreur, title, approx_label):
        ax1 = self.fig.add_subplot(2, 1, 1)
        ax1.plot(x_plot, y_true, 'b-', label='Fonction originale')
        ax1.plot(x_nodes, y_nodes, 'ro', label='Points d\'interpolation')
        ax1.plot(x_plot, y_approx, 'g--', label=approx_label)
        ax1.set_title(title)
        ax1.legend(); ax1.grid(True)
        ax1.set_xlabel('x'); ax1.set_ylabel('y')

        ax2 = self.fig.add_subplot(2, 1, 2)
        ax2.plot(x_plot, erreur, 'm-', label='Erreur absolue')
        ax2.set_title('Erreur d\'approximation')
        ax2.legend(); ax2.grid(True)
        ax2.set_xlabel('x'); ax2.set_ylabel('Erreur')
        self.fig.tight_layout()

    def plot_comparison(self, x_plot, erreur_lagrange, erreur_spline):
        ax = self.fig.add_subplot(1, 1, 1)
        ax.plot(x_plot, erreur_lagrange, 'r-', label='Erreur de Lagrange')
        ax.plot(x_plot, erreur_spline, 'b--', label='Erreur de la Spline Quadratique')
        ax.set_title('Comparaison des Erreurs d\'Approximation')
        ax.set_xlabel('x'); ax.set_ylabel('Erreur absolue (échelle log)')
        ax.legend(); ax.grid(True)
        ax.set_yscale('log')

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalysisApp(root)
    root.mainloop()
