import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lightkurve import read
import tempfile
import os
import sys

# Allow imports from src/
sys.path.append("src")

from src.signal_detection import SignalDetector
from src.classifier import TransitClassifier

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="AI Exoplanet Detection",
    page_icon="🪐",
    layout="wide"
)

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🪐 AI Exoplanet Detection System")
st.markdown(
    """
Detect exoplanet transit signals from noisy astronomical light curves.

Upload a TESS FITS file and run the detection pipeline.
"""
)

# --------------------------------------------------
# Upload
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload TESS FITS File",
    type=["fits"]
)

# --------------------------------------------------
# Run Analysis
# --------------------------------------------------

if uploaded_file:

    st.success("FITS file uploaded successfully.")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".fits") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    try:

        st.info("Loading light curve...")

        lc = read(temp_path)

        time = lc.time.value
        flux = lc.flux.value

        # Remove invalid values
        mask = np.isfinite(time) & np.isfinite(flux)

        time = time[mask]
        flux = flux[mask]

        # Normalize
        flux = flux / np.median(flux)

        # --------------------------------------------------
        # Plot Light Curve
        # --------------------------------------------------

        st.subheader("Light Curve")

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(time, flux, ".", markersize=1)

        ax.set_xlabel("Time (days)")
        ax.set_ylabel("Normalized Flux")
        ax.set_title("Observed Light Curve")

        st.pyplot(fig)

        # --------------------------------------------------
        # Detection Button
        # --------------------------------------------------

        if st.button("🚀 Run Detection"):

            with st.spinner("Analyzing light curve..."):

                detector = SignalDetector()
                classifier = TransitClassifier()

                detections = detector.detect(time, flux)

            st.success(
                f"Detection complete. Found {len(detections)} candidates."
            )

            results = []

            for i, d in enumerate(detections[:10]):

                label = classifier.classify(
                    d["depth"],
                    d["duration"],
                    d["snr"]
                )

                results.append({
                    "Candidate": i + 1,
                    "Class": label,
                    "Period (days)": round(d["period"], 3),
                    "Depth": round(d["depth"], 6),
                    "SNR": round(d["snr"], 2),
                    "Duration (days)": round(
                        d["duration"], 3
                    )
                })

            df = pd.DataFrame(results)

            # --------------------------------------------------
            # Results Table
            # --------------------------------------------------

            st.subheader("Detected Candidates")

            st.dataframe(
                df,
                use_container_width=True
            )

            # --------------------------------------------------
            # Candidate Cards
            # --------------------------------------------------

            st.subheader("Candidate Details")

            for _, row in df.iterrows():

                with st.expander(
                    f"Candidate {row['Candidate']} - {row['Class']}"
                ):

                    st.write(
                        f"**Period:** {row['Period (days)']} days"
                    )

                    st.write(
                        f"**Depth:** {row['Depth']}"
                    )

                    st.write(
                        f"**SNR:** {row['SNR']}"
                    )

                    st.write(
                        f"**Duration:** {row['Duration (days)']} days"
                    )

            # --------------------------------------------------
            # Download CSV
            # --------------------------------------------------

            csv = df.to_csv(index=False)

            st.download_button(
                label="📥 Download Results CSV",
                data=csv,
                file_name="results.csv",
                mime="text/csv"
            )

    except Exception as e:

        st.error(f"Error: {str(e)}")

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")

st.markdown(
    """
**Project:** AI-Enabled Detection of Exoplanets from Noisy Astronomical Light Curves

Built using:
- Lightkurve
- NumPy
- Pandas
- Matplotlib
- Streamlit
"""
)