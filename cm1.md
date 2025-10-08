# Approximation polynomiale

Soit une fonction f [a, b] --> R

```
Soit xi tel que x0 = a < x1<x2<...xi<...<xn = b une subdivision de l'intervalle [a,b]
```

## Lagrange

Faire une approximation polynomiale par la methode de Lagrange consiste a trouver un polynome P de degre n tel que:

P(xi) = f(xi) pour  0<= i <= n

```math
P(x) = \Sigma_{i=0}^{n-1}f(xi)L_i(x) \quad
avec \quad
L_i(x) = \Pi_{j=0, j\neq i}^{n-1}\frac{x-x_j}{x_i - x_j}
```

```math

```

## Spline quadratique

On cherche un polynome S(x) defini par morceau, continu et a derviee continue qui est une approximation de f(x).

Posons $z_i = S'(x_i)$ pour tout $i \in [0, n]$, où $z_i$ représente la dérivée de la spline au point $x_i$. Pour fixer une solution unique, nous imposerons la condition $z_0 = S'(x_0) = 0$.

```math
S(x) = \begin{cases}
s_0(x)  &\quad si \quad x \in [x_0, x_1]\\
s_1(x) &\quad si \quad x \in [x_1, x_2]\\
\ldots &\\
s_i(x)& \quad si \quad x \in [x_i, x_{i+1}]\\
\ldots &\\
s_{n-1}(x)& \quad si \quad x \in [x_{n-1}, x_n]

\end{cases}
\\
\text{Hypotheses}\\
H1 -\;s_i(x) \text{ est un polynome de degre 2}\\
H2 -\; S(x_i) = f(x_i)\\
H3 -\;S(x) \; est\; continue\\
H4 -\;S'(x) \; est\; continue, \text{avec } S'(x_i) = z_i \text{ et } z_0 = 0


```

### Mise en equation

#### H1: $ s_i(x)$ est un polynome de degre 2 c'est-a-dire:

$$
s_i(x) = a_i(x - x_i)^2 + b_i(x - x_i) + c_i\\0\leq i\leq n-1\\
\text{Soit 3n inconnues}
$$

#### H2: $ S(x_i)=f(x_i)=y_i$

$$
S(x_i) = c_i = y_i \;\forall i\in[0, n-1]\\
c_i \text{ sont tous determin\'es donc il reste 2n inconnues \`a determiner avec les $n-1$ premieres equations.}\\
\text{Il reste l'equation $ S(x_n) = f(x_n)$}
$$

#### H3: $S(x)$ est continue

$$
s_{i-1}(x_i) = s_i(x_i) \; \forall i \in [1, n-1]
$$

Soit n - 1 equations

#### H4: $S'(x)$ est continue

Rappelons que nous avons posé $z_i = S'(x_i)$ pour tout $i \in [0, n]$, avec $z_0 = 0$.

$$
s_i'(x) = 2a_i(x-x_i) + b_i
$$

En particulier, $s_i'(x_i) = b_i = z_i$ pour tout $i \in [0, n-1]$.

$$
H_4 \Rightarrow s_{i-1}'(x_i) = s_i'(x_i) \Rightarrow z_i = s_i'(x_i) \forall i \in [1, n-1]\\
\text{Soit $n-1$ equations}
$$

#### Bilan: $2n$ inconnues et $1 +(n-1)+(n-1) = 2n-1$ equations

#### Les equations

$$
\begin{cases}
S(x_n) = f(x_n) \Rightarrow s_{n-1}(x_n) = y_n \Rightarrow a_{n-1}(x_n - x_{n-1})^2+b_{n-1}(x_n-x_{n-1})+c_{n-1} = y_n\\
s_{i-1}(x_i) = s_i(x_i) \Rightarrow
\begin{cases}
a_0(x_1-x_{0})^2+b_0(x_1-x_0) + c_0 = c_1\\
a_1(x_2-x_1)^2+b_1(x_2-x_1) + c_1 = c_2\\
\ldots\\
a_i(x_{i+1}-x_i)^2+b_i(x_{i+1}-x_i) + c_i = c_{i+1} \; (Eq2i)\\
\ldots\\
a_{n-2}(x_{n-1}-x_{n-2})^2+b_{n-2}(x_{n-1}-x_{n-2}) + c_{n-2} = c_{n-1}\\
\end{cases}
\\
s_{i-1}'(x_i) = s_i'(x_i) \Rightarrow z_i = z_i \Rightarrow
\begin{cases}
  2a_0(x_1-x_0) + b_0 = b_1 \Rightarrow 2a_0(x_1-x_0) + z_0 = z_1 \Rightarrow 2a_0(x_1-x_0) = z_1 \text{ (car } z_0 = 0 \text{)}\\
  2a_1(x_2-x_1) + b_1 = b_2 \Rightarrow 2a_1(x_2-x_1) + z_1 = z_2\\
  \ldots\\
  2a_i(x_{i+1}-x_i) + b_i = b_{i+1} \Rightarrow 2a_i(x_{i+1}-x_i) + z_i = z_{i+1} \; (Eq3i)\\
  \ldots\\
  2a_{n-2}(x_{n-1}-x_{n-2}) + b_{n-2} = b_{n-1} \Rightarrow 2a_{n-2}(x_{n-1}-x_{n-2}) + z_{n-2} = z_{n-1}\\
\end{cases}
    \Rightarrow
      a_i = \frac{z_{i+1} - z_i}{2(x_{i+1} - x_i)} \; (Eq4i)
\end{cases}
$$

En injectant Eq4i dans Eq2i, on obtient

$$
\frac{z_{i+1} - z_i}{2(x_{i+1} - x_i)}(x_{i+1} - x_i)^2+z_i(x_{i+1} - x_i)+c_i=c_{i+1}\\
\Rightarrow \frac{1}{2}(z_{i+1} - z_i)(x_{i+1} - x_i)+z_i(x_{i+1} - x_i)= c_{i+1}-c_i\\
\Rightarrow (x_{i+1} - x_i)(\frac{1}{2}(z_{i+1} - z_i+2z_i)) = c_{i+1}-c_i\\
\Rightarrow (x_{i+1} - x_i)(\frac{1}{2}(z_{i+1} + z_i)) = c_{i+1}-c_i\\

\Rightarrow 
\frac{1}{2}(z_{i+1} + z_i) = \frac{c_{i+1}-c_i}{x_{i+1} - x_i}
\\
\Rightarrow
z_{i+1} = 2\frac{c_{i+1}-c_i}{x_{i+1} - x_i} - z_i
$$

Avec $c_i = y_i$ et $z_0 = 0$, nous pouvons calculer récursivement toutes les valeurs de $z_i$ :

$$
z_1 = 2\frac{y_1-y_0}{x_1 - x_0} - z_0 = 2\frac{y_1-y_0}{x_1 - x_0} \text{ (car } z_0 = 0 \text{)}\\
z_2 = 2\frac{y_2-y_1}{x_2 - x_1} - z_1\\
\ldots\\
z_{i+1} = 2\frac{y_{i+1}-y_i}{x_{i+1} - x_i} - z_i\\
\ldots
$$

Une fois les $z_i$ calculés, nous pouvons déterminer les coefficients $a_i$ et $b_i$ :

$$
b_i = z_i \text{ pour tout } i \in [0, n-1]\\
a_i = \frac{z_{i+1} - z_i}{2(x_{i+1} - x_i)} \text{ pour tout } i \in [0, n-1]
$$
