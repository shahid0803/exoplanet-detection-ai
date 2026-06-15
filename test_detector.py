import sys
sys.path.append("src")

import numpy as np
from signal_detection import SignalDetector

# Create fake light curve
time = np.linspace(0, 30, 3000)

# Normal stellar brightness
flux = np.ones_like(time)

# Fake planet:
period = 5.0          # days
duration = 0.2        # days
depth = 0.02          # 2%

for i in range(len(time)):
    phase = time[i] % period
    if phase < duration:
        flux[i] -= depth

# Add random noise
flux += np.random.normal(0, 0.003, len(flux))

detector = SignalDetector()

detections = detector.detect(time, flux)

print("Detections:")
print("\nDetected Signals:\n")

for i, d in enumerate(detections):
    print(f"Candidate {i+1}")
    print(f"  Period   : {d['period']:.3f} days")
    print(f"  Depth    : {d['depth']:.4f}")
    print(f"  SNR      : {d['snr']:.2f}")
    print(f"  Duration : {d['duration']:.3f} days")
    print()