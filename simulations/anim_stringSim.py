import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# Parametry struny
L = 1.0
N = 200
dx = L / (N - 1)
c = 100.0
rho = 0.01
gamma = 1.0

# Czas i dyskretyzacja
T_total = 0.02
dt = 1e-5
steps = int(T_total / dt)
frame_skip = 5  # co ile kroków wyświetlać klatkę

# Parametry elektromagnesu i prądu
I0 = 0.2
f = 150.0
B0 = 0.1

# Obszar działania elektromagnesu
magnet_width = int(0.1 * N)
magnet_center = N // 2
magnet_indices = range(magnet_center - magnet_width // 2,
                       magnet_center + magnet_width // 2)

# Definicja prądu z harmonicznymi
def current(t, harmonics=[(1.5, 0.3), (2, 0.4), (4, 0.2), (5, 0.7)]):
    signal = I0 * np.sin(2 * np.pi * f * t)
    for k, amp in harmonics:
        signal += amp * np.sin(2 * np.pi * f * k * t)
    return signal

# Inicjalizacja
y = np.zeros(N)
y_new = np.zeros(N)
y_old = np.zeros(N)

frames = []  # tu zapisujemy y(x) w kolejnych klatkach animacji
x = np.linspace(0, L, N)

# Główna pętla
for step in range(steps):
    t = step * dt
    I_t = current(t, harmonics=[(1.5, 0.9), (2, 0.45), (4, 0.6), (5, 0.7)])  # dodaj harmoniczne
    F = np.zeros(N)
    F[magnet_indices] = I_t * B0 * dx

    # Rozwiązanie metodą różnic skończonych
    for i in range(1, N - 1):
        y_new[i] = (2 - gamma*dt) * y[i] - y_old[i] + dt**2 * (
            c**2 * (y[i+1] - 2*y[i] + y[i-1]) / dx**2 + F[i] / rho
        )
        y_new[i] /= (1 + gamma*dt)

    y_new[0] = y_new[-1] = 0  # warunki brzegowe

    # Zapamiętaj klatkę
    if step % frame_skip == 0:
        frames.append(y.copy())

    # Aktualizacja
    y_old[:] = y[:]
    y[:] = y_new[:]

# Animacja
fig, ax = plt.subplots()
line, = ax.plot(x, frames[0])
ax.set_ylim(-0.00000008, 0.00000008)
ax.set_xlabel("x [m]")
ax.set_ylabel("y(x, t)")
ax.set_title("Drgania struny pod wpływem siły Lorentza")

def update(frame):
    line.set_ydata(frame)
    return line,

ani = FuncAnimation(fig, update, frames=frames, interval=50, blit=True)
plt.show()

mp4_path = "/home/bartomiejfalenta/Dokumenty/pythonScripts/Magneharm_StringSIM/animacja_struny_lorentza.mp4"
writer = FFMpegWriter(fps=30)
ani.save(mp4_path, writer=writer)

mp4_path