"""Data preprocessing module for light curve analysis."""

import numpy as np
from scipy import signal
from scipy.interpolate import UnivariateSpline
import pandas as pd
from typing import Tuple, Optional


class LightCurvePreprocessor:
    """Preprocess astronomical light curves."""
    
    def __init__(self, detrending_method: str = "savitzky_golay", 
                 window_length: int = 101, polyorder: int = 3):
        """
        Initialize preprocessor.
        
        Parameters
        ----------
        detrending_method : str
            Method for detrending: 'savitzky_golay', 'polynomial', 'spline'
        window_length : int
            Window length for Savitzky-Golay filter
        polyorder : int
            Polynomial order for detrending
        """
        self.detrending_method = detrending_method
        self.window_length = window_length
        self.polyorder = polyorder
    
    def detrend(self, time: np.ndarray, flux: np.ndarray, 
                flux_err: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detrend light curve to remove instrumental trends.
        
        Parameters
        ----------
        time : np.ndarray
            Time values
        flux : np.ndarray
            Flux values
        flux_err : np.ndarray, optional
            Flux uncertainties
            
        Returns
        -------
        detrended_flux : np.ndarray
            Detrended flux
        trend : np.ndarray
            Removed trend component
        """
        # Remove NaNs
        mask = ~(np.isnan(flux) | np.isnan(time))
        time_clean = time[mask]
        flux_clean = flux[mask]
        
        if self.detrending_method == "savitzky_golay":
            trend = signal.savgol_filter(flux_clean, self.window_length, self.polyorder)
        elif self.detrending_method == "polynomial":
            coeffs = np.polyfit(time_clean, flux_clean, self.polyorder)
            trend = np.polyval(coeffs, time_clean)
        elif self.detrending_method == "spline":
            spl = UnivariateSpline(time_clean, flux_clean, s=len(flux_clean))
            trend = spl(time_clean)
        else:
            raise ValueError(f"Unknown detrending method: {self.detrending_method}")
        
        detrended_flux = flux_clean - trend + np.median(flux_clean)
        
        return detrended_flux, trend
    
    def normalize(self, flux: np.ndarray) -> np.ndarray:
        """
        Normalize flux to unit median.
        
        Parameters
        ----------
        flux : np.ndarray
            Flux values
            
        Returns
        -------
        normalized_flux : np.ndarray
            Normalized flux
        """
        median_flux = np.median(flux)
        return flux / median_flux
    
    def remove_outliers(self, flux: np.ndarray, sigma: float = 3.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Remove outliers using median absolute deviation.
        
        Parameters
        ----------
        flux : np.ndarray
            Flux values
        sigma : float
            Number of MAD away from median to consider as outlier
            
        Returns
        -------
        cleaned_flux : np.ndarray
            Flux with outliers set to NaN
        outlier_mask : np.ndarray
            Boolean mask for outliers
        """
        median = np.median(flux)
        mad = np.median(np.abs(flux - median))
        threshold = sigma * mad
        
        outlier_mask = np.abs(flux - median) > threshold
        cleaned_flux = flux.copy()
        cleaned_flux[outlier_mask] = np.nan
        
        return cleaned_flux, outlier_mask
    
    def process(self, time: np.ndarray, flux: np.ndarray, 
                flux_err: Optional[np.ndarray] = None,
                normalize: bool = True, remove_outliers: bool = True) -> dict:
        """
        Full preprocessing pipeline.
        
        Parameters
        ----------
        time : np.ndarray
            Time values
        flux : np.ndarray
            Flux values
        flux_err : np.ndarray, optional
            Flux uncertainties
        normalize : bool
            Whether to normalize flux
        remove_outliers : bool
            Whether to remove outliers
            
        Returns
        -------
        processed_data : dict
            Dictionary containing processed light curve data
        """
        # Remove initial NaNs
        mask = ~(np.isnan(flux) | np.isnan(time))
        time = time[mask]
        flux = flux[mask]
        if flux_err is not None:
            flux_err = flux_err[mask]
        
        # Remove outliers
        if remove_outliers:
            flux, outlier_mask = self.remove_outliers(flux, sigma=3.0)
            # Interpolate over outliers
            valid_idx = ~np.isnan(flux)
            if np.sum(valid_idx) > 10:
                flux = np.interp(time, time[valid_idx], flux[valid_idx])
        
        # Detrend
        detrended_flux, trend = self.detrend(time, flux, flux_err)
        
        # Normalize
        if normalize:
            detrended_flux = self.normalize(detrended_flux)
        
        return {
            'time': time,
            'flux': detrended_flux,
            'flux_err': flux_err,
            'trend': trend,
            'original_flux': flux
        }
