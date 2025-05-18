import numpy as np
import matplotlib.pyplot as plt

# String params
L = 1.0               # string length [m]
N = 200               # number of spatial points
dx = L / (N - 1)      # step in space
c = 100.0             # wave speed [m/s]
rho = 0.01            # linear density [kg/m]
gamma = 12.82         # damping [1/s]
gamma = gamma/10000

# Time params
T_total = 0.1         # simulation time [s]
dt = 1e-5             # time step [s]
steps = int(T_total / dt)

# Current and field params
I0 = 0.2              # current [A]
f = 150.0             # fudamental frequency [Hz]
B0 = 0.1              # magnetic field [T]

# Magnetic field ONLY in the middle part of the string
magnet_width = int(0.1 * N)
magnet_center = N // 2
magnet_indices = range(magnet_center - magnet_width // 2,
                       magnet_center + magnet_width // 2)

# I(t) function
def current(t, harmonics=[(1.5, 0.9), (2, 0.45), (4, 0.6), (5, 0.7)]):
    signal = I0 * np.sin(2 * np.pi * f * t)
    for k, amp in harmonics:
        signal += amp * np.sin(2 * np.pi * f * k * t)
    return signal

# Initialization
y = np.zeros(N)
y_new = np.zeros(N)
y_old = np.zeros(N)
F_t = []

# Main time loop
for step in range(steps):
    t = step * dt
    I_t = current(t)  # signal with optional harmonics
    F = np.zeros(N)

    # Calculating Lorentz force (step-by-step)
    F[magnet_indices] = I_t * B0 * dx  # simplified force on distance

    # Recall force in given step
    F_t.append(F[N//2])

    # Differential scheme (spatiotemporal)
    for i in range(1, N - 1):
        y_new[i] = (2 - gamma*dt) * y[i] - y_old[i] + dt**2 * (
            c**2 * (y[i+1] - 2*y[i] + y[i-1]) / dx**2 + F[i] / rho
        )
        y_new[i] /= (1 + gamma*dt)

    # Boundary conditions
    y_new[0] = y_new[-1] = 0

    # time step increment
    y_old[:] = y[:]
    y[:] = y_new[:]

# Plots: displacment and and Lorentz force in time
x = np.linspace(0, L, N)
time = np.linspace(0, T_total, steps)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(x, y, label="y(x, t_final)")
plt.title("Shape of a string in final time")
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(time, F_t)
plt.title("Lorentz force over time F(t)")
plt.xlabel("t [s]")
plt.ylabel("F [N]")
plt.grid()

plt.tight_layout()
plt.show()
