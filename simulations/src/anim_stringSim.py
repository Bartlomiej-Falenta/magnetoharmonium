import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# String params
L = 1.0
N = 200
dx = L / (N - 1)
c = 100.0
rho = 0.01
gamma = 1.0

# Time and discretization
T_total = 0.02
dt = 1e-5
steps = int(T_total / dt)
frame_skip = 5  # How many steps between frames

# Magnet and current params
I0 = 0.2
f = 150.0
B0 = 0.1

# Magnet area of operation
magnet_width = int(0.1 * N)
magnet_center = N // 2
magnet_indices = range(magnet_center - magnet_width // 2,
                       magnet_center + magnet_width // 2)

# Definition of current signal with harmonic components
def current(t, harmonics=[(1.5, 0.3), (2, 0.4), (4, 0.2), (5, 0.7)]):
    signal = I0 * np.sin(2 * np.pi * f * t)
    for k, amp in harmonics:
        signal += amp * np.sin(2 * np.pi * f * k * t)
    return signal

# Init
y = np.zeros(N)
y_new = np.zeros(N)
y_old = np.zeros(N)

frames = []  # here we save x in each frame of animation
x = np.linspace(0, L, N)

# Main loop
for step in range(steps):
    t = step * dt
    I_t = current(t, harmonics=[(1.5, 0.9), (2, 0.45), (4, 0.6), (5, 0.7)])  # add harmonics
    F = np.zeros(N)
    F[magnet_indices] = I_t * B0 * dx

    # Finite difference method solution
    for i in range(1, N - 1):
        y_new[i] = (2 - gamma*dt) * y[i] - y_old[i] + dt**2 * (
            c**2 * (y[i+1] - 2*y[i] + y[i-1]) / dx**2 + F[i] / rho
        )
        y_new[i] /= (1 + gamma*dt)

    y_new[0] = y_new[-1] = 0  # boundary conditions

    # Save frame
    if step % frame_skip == 0:
        frames.append(y.copy())

    # Update
    y_old[:] = y[:]
    y[:] = y_new[:]

# Animation
fig, ax = plt.subplots()
line, = ax.plot(x, frames[0])
ax.set_ylim(-0.00000008, 0.00000008)    # depending on harmonics and other paramters, you may need to rescale it
ax.set_xlabel("x [m]")
ax.set_ylabel("y(x, t)")
ax.set_title("String vibrations caused by Lorentz force")

def update(frame):
    line.set_ydata(frame)
    return line,

ani = FuncAnimation(fig, update, frames=frames, interval=50, blit=True)
plt.show()

mp4_path = "/[PASTE YOUR OWN PATH HERE]/animation of lorentz force on string.mp4"
writer = FFMpegWriter(fps=30)
ani.save(mp4_path, writer=writer)
mp4_path
