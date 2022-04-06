import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, sin, pi, cos

class WaveFunction:
    def __init__(self, n, lx, p=0, ly=0):
        self.smoothness = 100

        self.n, self.p = n, p
        self.lx, self.ly = lx, ly

        self.psi = np.asarray([[self._psi(xi, yi) for xi in self.x] for yi in self.y])


    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, value):
        if not isinstance(value, int):
            raise ValueError
        self._n = value

    @property
    def p(self):
        return self._p

    @p.setter
    def p(self, value):
        if not isinstance(value, int):
            raise ValueError
        self._p = value

    @property
    def lx(self):
        return self._lx

    @lx.setter
    def lx(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError
        self._lx = value
        self.x = np.linspace(0, self._lx, self.smoothness)

    @property
    def ly(self):
        return self._ly

    @ly.setter
    def ly(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError
        self._ly = value
        self.y = np.linspace(0, self._ly, self.smoothness)


    def _psi(self, x:float, y:float = 0):
        if self.p == 0 or self.ly == 0:
            return sqrt(2 / self.lx) * sin(self.n * pi * x / self.lx)
        return 2 / sqrt(self.lx * self.ly) * sin(self.n * pi * x / self.lx) * sin(self.p * pi * y / self.ly)

    def _re_psi(self, x, t):
        return self._psi(x) * cos(t) if self.p == 0 or self.ly == 0 else None

    def _im_psi(self, x, t):
        return self._psi(x) * sin(t) if self.p == 0 or self.ly == 0 else None


class Plot:
    # ax, x, y, title, xlabel, ylabel               2D PLOT
    # ax, x, y, z, tile, xlabel, ylabel, zlabel     3D PLOT
    def __init__(self, *args):
        if len(args) > 6:
            ax, x, y, z, title, xlabel, ylabel, zlabel = args
            ax.plot_surface(x, y, z, cmap='viridis')
            ax.set_title(title)
            ax.set_xticks([]), ax.set_yticks([]), ax.set_zticks([])
            ax.set_xlabel(xlabel), ax.set_ylabel(ylabel), ax.set_zlabel(zlabel)
        else:
            ax, x, y, title, xlabel, ylabel = args
            ax.plot(x, y)
            ax.set_title(title)
            ax.set_xticks([]), ax.set_yticks([])
            ax.set_xlabel(xlabel), ax.set_ylabel(ylabel)

def main():
    # Just modify the quantum numbers n, p and the spacial parameters l, h

    n, p = 3, 0
    l, h = 1, 1

    wave_function = WaveFunction(n, l, p, h)
    if wave_function.p == 0 or wave_function.ly == 0:
        fig = plt.figure(figsize=plt.figaspect(0.5))
        ax1, ax2 = fig.subplots(1, 2)
        x, y = wave_function.x, wave_function.psi[0]

        Plot(ax1, x, y, r'$\psi(x)$', "L", r'$\psi(x)$')
        Plot(ax2, x, y ** 2, r'$|\psi(x)|^2$', "L", r'$|\psi(x)|^2$')

        plt.show()
        return

    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    x, y = np.meshgrid(wave_function.x, wave_function.y)
    z = wave_function.psi
    Plot(ax1, x, y, z, r'$\Psi(x, y)$', "L", "H", r'$\Psi(x, y)$')
    Plot(ax2, x, y, z ** 2, r'$|\Psi(x, y)|^2$', "L", "H", r'$|\Psi(x, y)|^2$')
    plt.show()
    return

if __name__ == '__main__':
    main()
