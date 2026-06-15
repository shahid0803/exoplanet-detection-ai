# 🌌 AI-Enabled Detection of Exoplanets from Noisy Astronomical Light Curves

## Technical Report

**Author:** Shahid Ali
**Project:** AI-Enabled Detection of Exoplanets from Noisy Astronomical Light Curves
**Dataset:** NASA TESS Light Curves
**Tools:** Python, NumPy, SciPy, Pandas, Astropy, Lightkurve, Scikit-Learn, Matplotlib

---

# 📖 Abstract

The discovery of exoplanets using transit photometry requires identifying extremely small periodic decreases in stellar brightness. Real astronomical observations are often contaminated by instrumental noise, stellar variability, and blending from nearby stars, making signal detection challenging.

This project presents an AI-assisted pipeline that automatically detects periodic transit-like signals from noisy TESS light curves, estimates key transit parameters, and classifies detected events into astrophysical categories. The system combines signal-processing techniques with machine learning-inspired classification to identify potential exoplanet candidates while reducing false positives.

---

# 🎯 Objectives

The primary objectives of this project are:

* Detect periodic brightness dips in noisy stellar light curves.
* Distinguish between exoplanet transits and other astrophysical phenomena.
* Estimate important transit parameters:

  * Orbital Period
  * Transit Depth
  * Transit Duration
* Calculate Signal-to-Noise Ratio (SNR).
* Visualize detected events and generate analysis reports.

---

# 🛰️ Dataset

The project utilizes light curve observations from NASA's **Transiting Exoplanet Survey Satellite (TESS)** mission.

### Target Star

**Pi Mensae (TIC 261136679)**

### Data Format

* FITS (Flexible Image Transport System)
* Time-series photometric observations
* Flux measurements representing stellar brightness over time

---

# ⚙️ Methodology

## 1. Data Preprocessing

Raw TESS observations contain invalid measurements and instrumental artifacts.

The preprocessing stage performs:

* Removal of missing values (NaNs)
* Flux normalization
* Outlier filtering
* Noise reduction

This improves signal quality while preserving genuine transit features.

---

## 2. Signal Detection

Periodic signals are identified using the **Lomb–Scargle Periodogram**, a widely used technique for detecting periodicity in unevenly sampled astronomical data.

### Detection Workflow

```text
Light Curve
      ↓
Period Search
      ↓
Peak Identification
      ↓
Transit Candidate Detection
```

The algorithm evaluates multiple candidate periods and ranks them according to detection significance.

---

## 3. Transit Parameter Estimation

For each detected candidate, the following parameters are estimated:

### Orbital Period

Time interval between repeated transit events.

### Transit Depth

Relative decrease in stellar brightness during transit.

### Transit Duration

Total duration of the transit event.

### Signal-to-Noise Ratio (SNR)

Detection confidence calculated using:

SNR = Transit Depth / Noise Level

Higher SNR values indicate stronger confidence in the detected signal.

---

## 4. Classification Framework

Detected events are categorized using rule-based AI classification.

| Condition     | Classification      |
| ------------- | ------------------- |
| SNR < 5       | Noise               |
| Depth < 0.001 | Exoplanet Candidate |
| Depth < 0.05  | Possible Transit    |
| Depth ≥ 0.05  | Eclipsing Binary    |

The classifier reduces false detections and prioritizes scientifically interesting candidates.

---

# 📊 Results

The pipeline was tested using real TESS observations of **Pi Mensae**.

## Detected Candidates

| Candidate | Period (days) | Depth   | SNR   | Duration (days) | Classification      |
| --------- | ------------- | ------- | ----- | --------------- | ------------------- |
| 1         | 23.632        | 0.00022 | 19.02 | 0.139           | Exoplanet Candidate |
| 2         | 17.282        | 0.00017 | 16.60 | 0.191           | Exoplanet Candidate |
| 3         | 2.353         | 0.00003 | 16.13 | 0.474           | Exoplanet Candidate |
| 4         | 9.243         | 0.00007 | 15.22 | 0.500           | Exoplanet Candidate |
| 5         | 4.614         | 0.00005 | 14.78 | 0.474           | Exoplanet Candidate |

### Best Candidate

* Period: **23.632 days**
* Depth: **0.00022**
* Duration: **0.139 days**
* SNR: **19.02**

This candidate exhibited the strongest periodic transit-like signal among all detected events.

---

# 📈 Visualization

The pipeline automatically generates:

* Light Curve Plots
* Transit Candidate Graphs
* Detection Results Tables
* CSV Export Files

Generated outputs:

```text
results.csv
pi_mensae_lightcurve.png
lightcurve.png
```

These visualizations assist in validating candidate detections and communicating results effectively.

---

# 🔬 Uncertainty Estimation

Several factors contribute to uncertainty:

* Detector noise
* Stellar variability
* Sampling cadence
* Instrumental systematics

Confidence in detected events is quantified using Signal-to-Noise Ratio (SNR).

Candidates with higher SNR values are considered more reliable.

---

# 🚀 Future Improvements

Potential enhancements include:

* Box Least Squares (BLS) transit detection
* Deep Learning classification models
* Multi-sector TESS analysis
* Automated false-positive rejection
* Transit model fitting using astrophysical transit equations
* Confidence interval estimation via bootstrap sampling

---

# ✅ Conclusion

This project successfully demonstrates an AI-enabled pipeline for exoplanet detection using real NASA TESS observations.

The developed system:

* Detects periodic transit-like signals
* Estimates physical transit parameters
* Classifies astrophysical events
* Generates visual and tabular outputs
* Operates on real astronomical datasets

The results show that the proposed pipeline can efficiently identify promising exoplanet candidates and serve as a foundation for more advanced machine-learning-based astronomical surveys.

---

## 📚 References

1. NASA TESS Mission
2. Astropy Collaboration
3. Lightkurve Documentation
4. Lomb–Scargle Periodogram Method
5. Transit Photometry Techniques

---

**Project Repository:** https://github.com/shahid0803/exoplanet-detection-ai

**Report Version:** 1.0
