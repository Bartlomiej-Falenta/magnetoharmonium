# magnetoharmonium
Hammond Organ-like, Lorentz Force actuated chordophone instrument

The whole idea behind instrument is based on two physical phenomena - waves on a string, and Lorentz force working on a conductor in magnetic field.

**The first is described by folowing PDE (partial differential equation):**

$$\boxed{\frac{\partial ^{2} y}{\partial t^{2}}+\gamma\frac{\partial y}{\partial t}-v^{2}\frac{\partial ^{2} y}{\partial x^{2}}=\frac{1}{\rho}F\left( l,t \right)}$$

**The next one, the Lorentz force, is in this case described by the following:**

$$\boxed{\overrightarrow{F}=I\overrightarrow{l}\times\overrightarrow{B}}$$

**This would result with:**

$$\boxed{\frac{\partial ^{2} y}{\partial t^{2}}+\gamma\frac{\partial y}{\partial t}-v^{2}\frac{\partial ^{2} y}{\partial x^{2}}=\frac{I(t)}{\rho}\overrightarrow{l}\times\overrightarrow{B}}$$

~~Which is actually complicated to solve, I guess. I didn't solve it properly yet.~~ Ok, I realized I could just solve it with some basic Python packages – now the simulations and their resulting images are available in ```magnetoharmonium/simulations/``` folder, while videos got uploaded to YouTube playlist: https://www.youtube.com/playlist?list=PLDlz_sgCRQ_A4HcRTX_j7dR-LInD_T1PA
Though simulating it wasn't particularly necesseary, since all I needed was to estimate currents necesarry to drive individual strings. And, as it turns out, those are around 0.5-5 A. Which was reasonable value, possible to achieve with usual power amplifiers, which I already did succesfully on smaller scale with stereo amp connected to two strings and signal fed from electronic synthesizer or an organ.

Current clonewheel synthesis engine is made in SigmaStudio **specifically** for ADAU1467, which is listed in parts list. It's *generally* based around actual signal path in Hammond organ and likes of them, with current version of algorithm being this:

![IMAGE OF A CURRENT ALGORITHM](/design_files/dsp_code/Clonewheel_algorithm.png)
