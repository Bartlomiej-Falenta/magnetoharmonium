import numpy as np
import matplotlib.pyplot as plt

# Parametry struny
L = 1.0               # długość struny [m]
N = 200               # liczba punktów przestrzennych
dx = L / (N - 1)      # krok przestrzenny
c = 100.0             # prędkość fali [m/s]
rho = 0.01            # gęstość liniowa [kg/m]
gamma = 12.82           # tłumienie [1/s]
gamma = gamma/10000

# Parametry czasowe
T_total = 0.1         # czas symulacji [s]
dt = 1e-5             # krok czasowy [s]
steps = int(T_total / dt)

# Parametry prądu i pola
I0 = 0.2              # natężenie prądu [A]
f = 150.0             # częstotliwość podstawowa [Hz]
B0 = 0.1             # pole magnetyczne [T]

# Pole Lorentza tylko w części środkowej struny
magnet_width = int(0.1 * N)
magnet_center = N // 2
magnet_indices = range(magnet_center - magnet_width // 2,
                       magnet_center + magnet_width // 2)

# Funkcja I(t)
def current(t, harmonics=[(1.5, 0.9), (2, 0.45), (4, 0.6), (5, 0.7)]):
    signal = I0 * np.sin(2 * np.pi * f * t)
    for k, amp in harmonics:
        signal += amp * np.sin(2 * np.pi * f * k * t)
    return signal

# Inicjalizacja
y = np.zeros(N)
y_new = np.zeros(N)
y_old = np.zeros(N)
F_t = []

# Główna pętla czasowa
for step in range(steps):
    t = step * dt
    I_t = current(t)  # sygnał z harmonicznymi jeśli chcesz
    F = np.zeros(N)

    # Obliczenie siły Lorentza (skokowo)
    F[magnet_indices] = I_t * B0 * dx  # uproszczona siła na odcinku

    # Zapamiętaj siłę w środku struny do wykresu F(t)
    F_t.append(F[N//2])

    # Schemat różnicowy (centralna różnica w przestrzeni i czasie)
    for i in range(1, N - 1):
        y_new[i] = (2 - gamma*dt) * y[i] - y_old[i] + dt**2 * (
            c**2 * (y[i+1] - 2*y[i] + y[i-1]) / dx**2 + F[i] / rho
        )
        y_new[i] /= (1 + gamma*dt)

    # Warunki brzegowe
    y_new[0] = y_new[-1] = 0

    # Przesunięcie czasowe
    y_old[:] = y[:]
    y[:] = y_new[:]

# Wykresy: położenie i siła Lorentza w czasie
x = np.linspace(0, L, N)
time = np.linspace(0, T_total, steps)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(x, y, label="y(x, t_final)")
plt.title("Kształt struny w końcowym czasie")
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(time, F_t)
plt.title("Siła Lorentza F(t) w środku struny")
plt.xlabel("t [s]")
plt.ylabel("F [N]")
plt.grid()

plt.tight_layout()
plt.show()
