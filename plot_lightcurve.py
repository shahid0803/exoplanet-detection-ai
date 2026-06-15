import numpy as np
import matplotlib.pyplot as plt

# Synthetic light curve
time = np.linspace(0, 30, 3000)

flux = np.ones_like(time)

period = 5.0
duration = 0.2
depth = 0.02

for i in range(len(time)):
    phase = time[i] % period
    if phase < duration:
        flux[i] -= depth

flux += np.random.normal(0, 0.003, len(flux))

plt.figure(figsize=(12,5))
plt.plot(time, flux, '.', markersize=2)

plt.xlabel("Time (days)")
plt.ylabel("Normalized Flux")
plt.title("Synthetic Exoplanet Transit Signal")

plt.grid(True)

plt.savefig("lightcurve.png")
print("Plot saved as lightcurve.png")