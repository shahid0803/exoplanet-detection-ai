# AI-Enabled Detection of Exoplanets from Noisy Astronomical Light Curves

## Project Overview

This project develops an AI-based data analysis pipeline capable of automatically detecting exoplanet transit signals from noisy astronomical light curve data. The pipeline identifies periodic dips in stellar brightness, classifies them into different astrophysical phenomena, and estimates associated physical parameters.

## Objectives

1. **Identify periodic signals** in noisy astronomical light curves
2. **Classify dips** into transits, eclipses, blends, and other astrophysical categories
3. **Estimate transit parameters**: orbital period, transit duration, and transit depth
4. **Provide confidence levels** and signal-to-noise ratios for detected events
5. **Visualize results** with clear, publication-quality plots

## Project Structure

```
exoplanet-detection-ai/
├── data/
│   ├── raw/                    # Raw TESS light curves
│   ├── processed/              # Preprocessed light curves
│   └── training/               # Labeled training datasets
├── src/
│   ├── preprocessing.py        # Data cleaning and normalization
│   ├── signal_detection.py     # Period detection algorithms
│   ├── feature_extraction.py   # Feature engineering for classification
│   ├── classifier.py           # ML model for transit classification
│   ├── parameter_estimation.py # Transit parameter fitting
│   └── visualization.py        # Plotting utilities
├── models/
│   └── trained_models/         # Serialized ML models
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_signal_detection.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_pipeline_evaluation.ipynb
├── scripts/
│   ├── download_tess_data.py   # Utility to download TESS data
│   ├── run_pipeline.py         # Main execution script
│   └── evaluate_pipeline.py    # Performance evaluation
├── tests/
│   ├── test_preprocessing.py
│   ├── test_signal_detection.py
│   └── test_classifier.py
├── results/
│   ├── detections.csv          # Detected signals
│   ├── classifications.csv     # Classification results
│   └── figures/                # Output visualizations
├── requirements.txt
├── config.yaml
└── REPORT.md                   # Final technical report
```

## Installation

```bash
git clone https://github.com/shahid0803/exoplanet-detection-ai.git
cd exoplanet-detection-ai
pip install -r requirements.txt
```

## Quick Start

### 1. Download TESS Data
```bash
python scripts/download_tess_data.py --sector 1 --output data/raw/
```

### 2. Run the Pipeline
```bash
python scripts/run_pipeline.py --input data/raw/ --output results/
```

### 3. View Results
Results are saved in `results/` with classifications, detections, and visualizations.

## Key Technologies

- **Python 3.8+**: Core programming language
- **NumPy, SciPy**: Numerical computing and signal processing
- **Pandas**: Data manipulation and analysis
- **Scikit-learn**: Machine learning algorithms
- **TensorFlow/Keras**: Deep learning models (optional)
- **Lightkurve**: Astronomical light curve analysis
- **Matplotlib, Seaborn**: Visualization
- **Astropy**: Astronomical utilities

## Methodology

### Phase 1: Signal Detection
- Detrending using polynomial fitting or Savitzky-Golay filter
- Period detection using Lomb-Scargle periodogram
- Transit candidate identification via BLS (Box Least Squares) algorithm

### Phase 2: Feature Extraction
- Transit depth, duration, and period
- Signal-to-Noise Ratio (SNR) calculation
- Statistical features (skewness, kurtosis, median absolute deviation)
- Folded light curve characteristics

### Phase 3: Classification
- Multi-class classifier distinguishing:
  - **Transits**: Planetary transit signals
  - **Eclipses**: Eclipsing binary systems
  - **Blends**: Contamination from background/foreground sources
  - **False Positives**: Other noise artifacts

### Phase 4: Parameter Estimation
- Transit period refinement
- Transit depth and duration fitting using transit models
- Confidence interval estimation via bootstrap resampling

## Expected Outputs

1. **Detections CSV**: List of detected signals with confidence scores
2. **Classifications CSV**: Signal classification (transit/eclipse/blend/false positive)
3. **Parameter Table**: Orbital period, transit depth, duration for each detection
4. **Visualizations**:
   - Original light curves with detected signals
   - Folded light curves at detected periods
   - Classification probability plots
5. **Technical Report**: 3-page methodology and results summary

## Evaluation Metrics

- **Detection Accuracy**: Precision, recall, F1-score on validation set
- **Classification Accuracy**: Per-class accuracy and confusion matrix
- **Parameter Estimation Error**: MAE/RMSE for period, depth, duration
- **Robustness**: Performance on varying noise levels and contamination

## Usage Examples

See `notebooks/` directory for detailed Jupyter notebooks demonstrating:
- Data exploration and preprocessing
- Signal detection techniques
- Model training and validation
- Full pipeline evaluation on test datasets

## Data Sources

- **TESS Archive**: https://archive.stsci.edu/tess/tic_ctl.html
- **Training Data**: Curated datasets with known exoplanets, false positives, and eclipsing binaries

## Contributing

Fork the repository and submit pull requests with improvements to:
- Detection algorithms
- Classification models
- Parameter estimation methods
- Visualization quality

## License

MIT License - See LICENSE file for details

## References

- NASA TESS Mission: https://tess.mit.edu/
- Lightkurve Documentation: https://docs.lightkurve.org/
- Transit Detection Review: Cloutier et al. (2020)
- BLS Algorithm: Kovács et al. (2002)

## Contact

For questions or suggestions, please open an issue on GitHub.
