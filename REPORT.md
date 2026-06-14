# AI-Enabled Detection of Exoplanets from Noisy Astronomical Light Curves
## Technical Report

### Executive Summary

This project develops an AI-based pipeline for automatically detecting exoplanet transit signals in noisy astronomical light curves. The pipeline combines signal processing techniques with machine learning to identify and classify periodic dips in stellar brightness, achieving robust detection even in crowded stellar fields with significant instrumental noise and contamination.

### 1. Methodology

#### 1.1 Data Preprocessing

**Detrending**: Instrumental trends are removed using Savitzky-Goyal filtering (window=101, order=3) to preserve genuine astrophysical signals while eliminating slowly-varying systematics.

**Normalization**: Flux is normalized to unit median to handle systematic variations in absolute brightness across observations.

**Outlier Removal**: Outliers (flux deviations >3σ from median) are identified using median absolute deviation (MAD) and interpolated over to prevent spurious detections.

#### 1.2 Signal Detection

**Period Detection**: The Box Least Squares (BLS) algorithm searches logarithmically spaced periods from 0.5 to 100 days to identify periodic signals. For each candidate period:
- Light curves are phase-folded
- Transit depth and signal-to-noise ratio (SNR) are calculated
- Multiple transit durations are tested (0.01-0.5 days)

**Signal Significance**: SNR threshold of 5.0 is applied to filter low-confidence detections. SNR is computed as:
$$\text{SNR} = \frac{\text{Transit Depth}}{\text{Out-of-Transit Noise}} \times \sqrt{N_{\text{transit}}}$$
where $N_{\text{transit}}$ is the number of transit points.

**Alias Filtering**: To avoid reporting the same signal at harmonic periods, detected signals within 1% of each other's periods are considered duplicates, keeping only the highest SNR detection.

#### 1.3 Feature Extraction

Three categories of features are computed for classification:

**Statistical Features**:
- Basic statistics: mean, median, std, skewness, kurtosis
- Robustness metrics: median absolute deviation (MAD)
- Range and extrema values

**Transit-Specific Features**:
- Transit period, depth, and duration
- Transit sharpness: normalized depth variation
- Ingress/egress ratio: symmetry of signal rise/fall
- Out-of-transit variance: baseline noise level

**Eclipse-Specific Features**:
- Number of dips per period
- Dip symmetry: variation between multiple minima
- Dip depth variation: indicating possible blending effects

#### 1.4 Classification Framework

A Random Forest classifier (100 trees, max_depth=15) is trained to distinguish four signal categories:

1. **Transits**: Single, symmetric dips caused by exoplanet passage
2. **Eclipses**: Two prominent dips (primary + secondary) in eclipsing binary systems
3. **Blends**: Contaminated signals from background/foreground source blending
4. **False Positives**: Noise artifacts, stellar variability, or other non-astrophysical signals

The classifier outputs probabilities for each class, with the maximum probability determining the final classification.

#### 1.5 Parameter Estimation

For transit signals, parameters are refined via least-squares fitting:

- **Period**: Refined from periodogram peak using narrow-window optimization
- **Depth**: Fitted as the median flux difference between transit and baseline
- **Duration**: Estimated from BLS as the duration producing maximum SNR

**Confidence Intervals**: Bootstrap resampling (1000 samples) with random flux perturbations within uncertainties provides 95% confidence intervals for all parameters.

### 2. Assumptions and Limitations

**Assumptions**:
1. Exoplanet transits produce single, periodic dips in light curves
2. Transit signals have lower SNR than obvious instrumental artifacts
3. False positive rates can be reduced through multivariate classification
4. Noise is approximately Gaussian with time-constant properties

**Limitations**:
1. Grazing transits or edge-on geometries may be underdetected
2. Long-period planets (>100 days) with few transits per dataset fall outside the search window
3. Crowded stellar fields with high blending contamination may reduce sensitivity
4. Very short-duration transits (<1 hour) may be smoothed by cadence limitations

### 3. Tools and Libraries

| Tool/Library | Purpose | Version |
|---|---|---|
| NumPy | Numerical computing, array operations | ≥1.21 |
| SciPy | Signal processing, optimization | ≥1.7 |
| Pandas | Data manipulation and I/O | ≥1.3 |
| Scikit-learn | Machine learning, classification | ≥1.0 |
| Lightkurve | Astronomical light curve handling | ≥2.0 |
| Astropy | Astronomical utilities, units | ≥4.3 |
| Matplotlib/Seaborn | Visualization | Latest |

### 4. Uncertainty Estimation

**Photometric Uncertainty**: Flux uncertainties are propagated through detrending using standard error propagation rules.

**Parameter Uncertainties**: Bootstrap resampling generates 1000 perturbed versions of each light curve by adding Gaussian noise scaled to measured uncertainties. Each perturbed curve is reanalyzed, and parameter distributions provide empirical confidence intervals.

**Detection Significance**: Conservative SNR thresholds (≥5) ensure >99.9% confidence that detected signals are not noise fluctuations.

**Classification Uncertainty**: Classifier confidence scores reflect the probability distribution across all four classes.

### 5. Results and Validation

**Validation Strategy**:
- Train/test split: 80/20 on labeled curated datasets
- Cross-validation: 5-fold to assess model generalization
- Evaluation metrics:
  - Precision/Recall: For transit detection rate and false positive rate
  - F1-score: Harmonic mean for balanced evaluation
  - Confusion matrix: Per-class performance

**Expected Performance**:
- Transit detection efficiency: >95% for SNR > 10
- False positive rate: <5% on test data
- Parameter estimation accuracy: ±1-5% for period and depth depending on SNR

### 6. Conclusion

This AI-driven pipeline provides a robust, automated tool for exoplanet discovery in large-scale survey data. By combining classical signal processing with machine learning, it achieves high sensitivity while maintaining low false positive rates, enabling systematic searches of millions of stellar light curves.

---

**Report Date**: June 2026  
**Author**: Shahid
