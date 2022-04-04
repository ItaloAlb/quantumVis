import random
import numpy as np
import matplotlib.pyplot as plt
from math import factorial, sqrt, cos, exp, pi, pow, acos, prod

# Bohr radius in angstrom
a0 = 0.5

# Quantum numbers
n, l, m = 3, 2, 1

# A handle to legendre and laguerre polynomials
class Polynomial:
    @staticmethod
    def assoc_legendre(m: int, n: int, x: float) -> float:
        if n == 0:
            if abs(m) > n:
                return 0.0
            return 1.0
        elif n == 1:
            if m == -1:
                return sqrt(1 - x ** 2) / 2
            if m == 1:
                return - sqrt(1 - x ** 2)
            return x
        elif n == m:
            return (-1) ** n * prod(range(2 * n - 1, 0, -2)) * (1 - x ** 2) ** (n / 2)
        else:
            return ((2 * n - 1) * x * Polynomial.assoc_legendre(m, n - 1, x) - (n + m - 1) *
                    Polynomial.assoc_legendre(m, n - 2, x)) / (n - m)

    @staticmethod
    def assoc_laguerre(m: int, n: int, x: float) -> float:
        if n == 0:
            return 1.0
        elif n == 1:
            return 1 + m - x
        else:
            return ((2 * n - 1 + m - x) * Polynomial.assoc_laguerre(m, n - 1, x) - (n + m - 1) *
                    Polynomial.assoc_laguerre(m, n - 2, x)) / n

# A handle to hydrogen functions
class Hydrogen:
    @staticmethod
    def psi_squared(r, theta):
        _p = 2 * r / (n * a0)
        return pow(2 / (n * a0), 3) * factorial(n - l - 1) / (2 * n * factorial(n + l)) * exp(-_p) * pow(_p, 2 * l) * \
               pow(Polynomial.assoc_laguerre(2 * l + 1, n - l - 1, _p), 2) * (2 * l + 1) * factorial(l - abs(m)) * \
               pow(Polynomial.assoc_legendre(abs(m), l, cos(theta)), 2) / (4 * pi * factorial(l + abs(m)))

def main():
    # Just a random function that fits well for some quantum numbers to limit space coordinates
    limit = 4 * (2 * n + l)

    r, theta = np.linspace(0, limit), np.linspace(0, pi)
    Z = np.asarray([[Hydrogen.psi_squared(r0, theta0) for r0 in r] for theta0 in theta])

    M = np.max(Z) * 1.05

    points_to_plot = 15000
    points_counter = 0

    x, y = [], []

    while points_counter < points_to_plot:
        _x, _y = random.uniform(-limit, limit), random.uniform(-limit, limit)
        _r = sqrt(_x ** 2 + _y ** 2)
        _theta = acos(_y / _r)

        _w = random.uniform(0, M)
        if _w <= Hydrogen.psi_squared(_r, _theta):
            x.append(_x), y.append(_y)
            points_counter += 1

    fig = plt.figure()

    ax = fig.add_subplot()

    ax.set_title("Hydrogen orbital")

    ax.scatter(x, y, s=0.1, color="black")

    plt.xlabel("n = {n}, l = {l}, m = {m}".format(n = n, l = l, m = m))

    plt.xticks([])
    plt.yticks([])

    plt.show()

if __name__ == '__main__':
    main()
