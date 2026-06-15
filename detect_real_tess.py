import sys
sys.path.append("src")

from src.signal_detection import SignalDetector
from src.classifier import TransitClassifier

from lightkurve import read
import numpy as np
import pandas as pd

print("Loading TESS data...")

lc = read("pi_mensae.fits")

time = lc.time.value
flux = lc.flux.value

# Remove bad values
mask = np.isfinite(time) & np.isfinite(flux)

time = time[mask]
flux = flux[mask]

# Normalize flux
flux = flux / np.median(flux)

print("Running detector...")

detector = SignalDetector()
classifier = TransitClassifier()

detections = detector.detect(time, flux)

print("\nDetected Signals:\n")

results = []

for i, d in enumerate(detections[:5]):

    label = classifier.classify(
        d["depth"],
        d["duration"],
        d["snr"]
    )

    results.append({
        "Candidate": i + 1,
        "Class": label,
        "Period_days": round(d["period"], 3),
        "Depth": round(d["depth"], 6),
        "SNR": round(d["snr"], 2),
        "Duration_days": round(d["duration"], 3)
    })

    print(f"Candidate {i+1}")
    print(f"Class     : {label}")
    print(f"Period    : {d['period']:.3f} days")
    print(f"Depth     : {d['depth']:.5f}")
    print(f"SNR       : {d['snr']:.2f}")
    print(f"Duration  : {d['duration']:.3f} days")
    print("-" * 40)

df = pd.DataFrame(results)

df.to_csv("results.csv", index=False)

print("\nResults saved to results.csv")