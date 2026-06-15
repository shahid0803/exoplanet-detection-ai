from lightkurve import read
import matplotlib.pyplot as plt

print("Loading TESS light curve...")

lc = read("pi_mensae.fits")

print(lc)

plt.figure(figsize=(12,5))
plt.plot(lc.time.value, lc.flux.value, ".", markersize=1)

plt.xlabel("Time (days)")
plt.ylabel("Flux")
plt.title("Pi Mensae - TESS Light Curve")

plt.grid(True)

plt.savefig("pi_mensae_lightcurve.png")

print("Plot saved!")