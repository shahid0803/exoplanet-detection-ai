# 🚀 AI-Enabled Detection of Exoplanets from Noisy Astronomical Light Curves

## Overview

This project presents an AI-enabled pipeline for detecting exoplanet transit signals from noisy astronomical light curve data obtained from NASA's Transiting Exoplanet Survey Satellite (TESS).

The system automatically processes stellar brightness measurements, detects periodic transit-like signals, estimates key physical parameters, classifies detected events, and generates visualizations and reports.

The project was developed as a solution for the challenge:

**"AI-Enabled Detection of Exoplanets from Noisy Astronomical Light Curves"**

---

## Features

✅ Load and process real TESS light curve data (.fits)

✅ Remove invalid observations and normalize flux measurements

✅ Detect periodic transit-like signals

✅ Estimate:

* Orbital Period
* Transit Depth
* Transit Duration
* Signal-to-Noise Ratio (SNR)

✅ Classify detected events into astrophysical categories

✅ Generate light curve visualizations

✅ Export results to CSV format

✅ Analyze real NASA TESS observations

---

## Project Architecture

```text
TESS Light Curve (.fits)
            │
            ▼
     Preprocessing
            │
            ▼
    Signal Detection
    (Lomb–Scargle)
            │
            ▼
  Parameter Estimation
            │
            ▼
     Classification
            │
            ▼
    Results & Plots
```

---

## Repository Structure

```text
exoplanet-detection-ai/
│
├── src/
│   ├── __init__.py
│   ├── signal_detection.py
│   ├── preprocessing.py
│   ├── feature_extraction.py
│   └── classifier.py
│
├── detect_real_tess.py
├── download_tess.py
├── plot_real_tess.py
├── run.py
├── test_detector.py
│
├── pi_mensae.fits
├── results.csv
├── lightcurve.png
├── pi_mensae_lightcurve.png
│
└── README.md
```

---

## Technologies Used

### Programming Language

* Python 3.12

### Scientific Computing

* NumPy
* SciPy
* Pandas

### Astronomy Libraries

* Lightkurve
* Astropy

### Visualization

* Matplotlib

### Development Environment

* GitHub Codespaces
* Git
* GitHub

---

## Methodology

### 1. Data Preprocessing

The raw TESS light curve is cleaned by:

* Removing NaN values
* Filtering invalid observations
* Normalizing flux measurements

---

### 2. Signal Detection

Periodic signals are detected using the Lomb–Scargle Periodogram.

This method identifies repeating brightness variations within noisy astronomical observations.

---

### 3. Parameter Estimation

For each detected signal, the pipeline estimates:

#### Orbital Period

Time between consecutive transit events.

#### Transit Depth

Relative decrease in stellar brightness.

#### Transit Duration

Length of the transit event.

#### Signal-to-Noise Ratio (SNR)

Confidence level of the detection.

---

### 4. Classification

Detected candidates are automatically classified using signal characteristics:

| Condition     | Classification      |
| ------------- | ------------------- |
| SNR < 5       | Noise               |
| Depth < 0.001 | Exoplanet Candidate |
| Depth < 0.05  | Possible Transit    |
| Depth ≥ 0.05  | Eclipsing Binary    |

---

## Example Results

Analysis of real TESS observations of **Pi Mensae (TIC 261136679)** produced the following candidates:

| Candidate | Period (days) | Depth   | SNR   | Duration (days) | Class               |
| --------- | ------------- | ------- | ----- | --------------- | ------------------- |
| 1         | 23.632        | 0.00022 | 19.02 | 0.139           | Exoplanet Candidate |
| 2         | 17.282        | 0.00017 | 16.60 | 0.191           | Exoplanet Candidate |
| 3         | 2.353         | 0.00003 | 16.13 | 0.474           | Exoplanet Candidate |
| 4         | 9.243         | 0.00007 | 15.22 | 0.500           | Exoplanet Candidate |
| 5         | 4.614         | 0.00005 | 14.78 | 0.474           | Exoplanet Candidate |

---

## Installation

Clone the repository:

```bash
git clone https://github.com/shahid0803/exoplanet-detection-ai.git
cd exoplanet-detection-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install numpy scipy pandas matplotlib astropy lightkurve
```

---

## Usage

### Download TESS Data

```bash
python download_tess.py
```

### Run Exoplanet Detection

```bash
python detect_real_tess.py
```

### Generate Visualizations

```bash
python plot_real_tess.py
```

---

## Output Files

### results.csv

Contains:

* Candidate ID
* Classification
* Period
* Transit Depth
* Duration
* SNR

### Generated Figures

* lightcurve.png
* pi_mensae_lightcurve.png

---

## Future Improvements

* Box Least Squares (BLS) transit search
* Deep learning-based classifiers
* Training on larger labeled TESS datasets
* Automated false-positive rejection
* Multi-sector validation
* Confidence calibration and uncertainty modeling

---

## Conclusion

This project demonstrates how astronomical signal-processing techniques and AI-inspired classification methods can be combined to identify exoplanet candidates in noisy light curve data.

The developed pipeline successfully analyzes real TESS observations, detects periodic transit-like signals, estimates physical parameters, and classifies candidate events with confidence metrics.

---

## Author

**Shahid Ali**

GitHub: https://github.com/shahid0803

---

## License

This project is intended for educational, research, and scientific purposes.
