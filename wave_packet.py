import numpy as np
from numpy import exp, sqrt, power, cos, sin, pi
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class WaveFunction:

    def __init__(self, method='rk2'):

        self.method = method  # Numerical method solutions: rk2

        self.m, self.hbar, self.k0 = 1.0, 1.0, 20.0  # Wave function constants

        self.xc, self.sigma = -0.5, 0.05  # Gaussian wave packet parameters

        self.gaussian = lambda x: sqrt(
            exp(-power(x - self.xc, 2) / (2 * power(self.sigma, 2))) / (self.sigma * sqrt(2 * pi)))

        self.v0, self.vx0, self.vxn = 0, -0.2, 0  # Potential barrier value

        self.v = lambda x: self.v0 if self.vx0 <= x <= self.vxn else 0  # Lambda function for potential v(i)

        self.dx, self.dt, self.x0, self.xn, self.t0, self.tn = 0.02, 0.0001, -1, 1, 0, 0.02  # Steps and boundary
        # conditions

        self.i, self.n = int((self.xn - self.x0) / self.dx), int((self.tn - self.t0) / self.dt)  # How many steps

        self.x = np.linspace(self.x0, self.xn, self.i)  # Spatial array

        self.v = np.asarray([self.v(i) for i in self.x])  # Potential array along space v[i]

        self.repsi, self.impsi = lambda x: self.gaussian(x) * cos(self.k0 * x), \
                                 lambda x: self.gaussian(x) * sin(self.k0 * x)

        self.re_psi = np.asarray([self.repsi(i) for i in self.x])
        self.im_psi = np.asarray([self.impsi(i) for i in self.x])

    @property
    def re_psi(self):
        return self._repsi

    @re_psi.setter
    def re_psi(self, repsi):
        if isinstance(repsi, (tuple, list, np.ndarray)):
            self._repsi = np.asarray(repsi)
        else:
            raise ValueError("RePsi must be a tuple or list")

    @property
    def im_psi(self):
        return self._impsi

    @im_psi.setter
    def im_psi(self, impsi):
        if isinstance(impsi, (tuple, list, np.ndarray)):
            self._impsi = np.asarray(impsi)
        else:
            raise ValueError("ImPsi must be a tuple or list")

    @property
    def psi_squared(self):
        return power(self.re_psi, 2) + power(self.im_psi, 2)

    @property
    def hbar(self):
        return self.h_bar

    @hbar.setter
    def hbar(self, h_bar):
        if isinstance(h_bar, float):
            self.h_bar = h_bar
        else:
            raise ValueError("h_bar must be a float")

    @property
    def m(self):
        return self._m

    @m.setter
    def m(self, mass):
        if isinstance(mass, float):
            self._m = mass
        else:
            raise ValueError("Mass must be a float")

    def rk2(self):

        k1r, k1i = np.asarray([self.DRePsi(self.im_psi, i) for i in range(len(self.x))]), \
                   np.asarray([self.DImPsi(self.re_psi, i) for i in range(len(self.x))])

        _repsi, _impsi = self.re_psi + k1r * self.dt, self.im_psi + k1i * self.dt

        k2r, k2i = np.asarray([self.DRePsi(_impsi, i) for i in range(len(self.x))]), \
                   np.asarray([self.DImPsi(_repsi, i) for i in range(len(self.x))])

        self.re_psi, self.im_psi = self.re_psi + (k1r + k2r) / 2 * self.dt, self.im_psi + (k1i + k2i) / 2 * self.dt

    def update(self):
        if self.method == 'rk2':
            self.rk2()

    def DRePsi(self, impsi, i):
        impsi = np.append(impsi, 0)
        return -(impsi[i + 1] - 2 * impsi[i] + impsi[i - 1]) / (2 * power(self.dx, 2)) + self.v[i] * impsi[i]

    def DImPsi(self, repsi, i):
        repsi = np.append(repsi, 0)
        return (repsi[i + 1] - 2 * repsi[i] + repsi[i - 1]) / (2 * power(self.dx, 2)) - self.v[i] * repsi[i]


def main():
    wave_function = WaveFunction()

    fig, ax_psi = plt.subplots()

    ax_psi.set_title("Temporal evolution of a gaussian wave packet")

    ax_psi.set_xlim(wave_function.x0, wave_function.xn)
    ax_psi.set_ylim(-5, 10)

    re_psi,  = plt.plot([], [], color='b', label=r"$Re(\Psi(x,t))$")
    im_psi, = plt.plot([], [], color='r', label=r"$Im(\Psi(x,t))$")
    psi_squared, = plt.plot([], [], color='purple', label=r"$|\Psi(x,t)|^2$")

    plt.xlabel("x")

    plt.xticks([])
    plt.yticks([])

    plt.plot(wave_function.x, wave_function.v, color='g', label="V(x)={v}".format(v=wave_function.v0))

    plt.legend(title='Functions:')

    time = ax_psi.text(0.125, 0.925, "time=0.0000s", horizontalalignment='center',
                       verticalalignment='center',
                       transform=ax_psi.transAxes)

    def update(frame):
        re_psi.set_data(wave_function.x, wave_function.re_psi)
        im_psi.set_data(wave_function.x, wave_function.im_psi)
        psi_squared.set_data(wave_function.x, wave_function.psi_squared)
        time.set_text("time={t:.4f}s".format(t=frame * wave_function.dt))

        wave_function.update()

        return re_psi, im_psi, psi_squared, time

    ani = FuncAnimation(fig, update, frames=wave_function.n, blit=True, repeat=False, interval=100)

    plt.show()


if __name__ == '__main__':
    main()
