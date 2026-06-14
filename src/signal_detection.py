"""Signal detection module for identifying periodic transit signals."""

import numpy as np
from scipy import signal as scipy_signal
from scipy.ndimage import uniform_filter1d
from typing import Tuple, List, Dict, Optional
import warnings


class SignalDetector:
    """Detect periodic signals in light curves using Box Least Squares."""
    
    def __init__(self, min_period: float = 0.5, max_period: float = 100.0,
                 snr_threshold: float = 5.0, min_transits: int = 2):
        """
        Initialize signal detector.
        
        Parameters
        ----------
        min_period : float
            Minimum search period in days
        max_period : float
            Maximum search period in days
        snr_threshold : float
            Minimum signal-to-noise ratio for detection
        min_transits : int
            Minimum number of transits required
        """
        self.min_period = min_period
        self.max_period = max_period
        self.snr_threshold = snr_threshold
        self.min_transits = min_transits
    
    def compute_lomb_scargle(self, time: np.ndarray, flux: np.ndarray,
                            freq_min: float = 0.01, freq_max: float = 2.0,
                            resolution: float = 0.0001) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute Lomb-Scargle periodogram.
        
        Parameters
        ----------
        time : np.ndarray
            Time values
        flux : np.ndarray
            Flux values
        freq_min : float
            Minimum frequency (1/day)
        freq_max : float
            Maximum frequency (1/day)
        resolution : float
            Frequency resolution
            
        Returns
        -------
        frequencies : np.ndarray
            Frequency array
        power : np.ndarray
            Power spectrum
        """
        # Normalize flux
        flux_normalized = (flux - np.mean(flux)) / np.std(flux)
        
        # Lomb-Scargle periodogram
        angular_freqs = 2 * np.pi * np.arange(freq_min, freq_max, resolution)
        power = scipy_signal.lombscargle(time, flux_normalized, angular_freqs, normalize=True)
        frequencies = angular_freqs / (2 * np.pi)
        
        return frequencies, power
    
    def fold_light_curve(self, time: np.ndarray, flux: np.ndarray,
                        period: float, t0: Optional[float] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Fold light curve at given period.
        
        Parameters
        ----------
        time : np.ndarray
            Time values
        flux : np.ndarray
            Flux values
        period : float
            Folding period
        t0 : float, optional
            Reference time (defaults to first observation)
            
        Returns
        -------
        phase : np.ndarray
            Phase values [0, 1]
        flux_folded : np.ndarray
            Folded flux values
        """
        if t0 is None:
            t0 = time[0]
        
        phase = ((time - t0) / period) % 1.0
        sorted_indices = np.argsort(phase)
        
        return phase[sorted_indices], flux[sorted_indices]
    
    def estimate_transit_depth(self, phase: np.ndarray, flux: np.ndarray,
                              transit_width: float = 0.1) -> Tuple[float, float]:
        """
        Estimate transit depth from folded light curve.
        
        Parameters
        ----------
        phase : np.ndarray
            Phase values [0, 1]
        flux : np.ndarray
            Folded flux values
        transit_width : float
            Expected transit width in phase units
            
        Returns
        -------
        depth : float
            Transit depth (fraction of flux decrease)
        snr : float
            Signal-to-noise ratio
        """
        # Find transit center (minimum flux)
        transit_center = phase[np.argmin(flux)]
        
        # Define transit and out-of-transit regions
        transit_mask = np.abs(phase - transit_center) < transit_width / 2
        out_transit_mask = ~transit_mask
        
        if np.sum(out_transit_mask) < 10:
            return 0.0, 0.0
        
        transit_flux = flux[transit_mask]
        out_transit_flux = flux[out_transit_mask]
        
        # Calculate depth
        out_transit_median = np.median(out_transit_flux)
        transit_median = np.median(transit_flux)
        depth = (out_transit_median - transit_median) / out_transit_median
        
        # Calculate SNR
        noise = np.std(out_transit_flux)
        if noise > 0:
            snr = depth / noise * np.sqrt(np.sum(transit_mask))
        else:
            snr = 0.0
        
        return depth, snr
    
    def box_least_squares(self, time: np.ndarray, flux: np.ndarray,
                         period: float, min_duration: float = 0.01,
                         max_duration: float = 0.5) -> Dict:
        """
        Box Least Squares algorithm for transit detection.
        
        Parameters
        ----------
        time : np.ndarray
            Time values
        flux : np.ndarray
            Flux values
        period : float
            Period to test
        min_duration : float
            Minimum transit duration in days
        max_duration : float
            Maximum transit duration in days
            
        Returns
        -------
        results : dict
            Detection results including depth, SNR, duration
        """
        # Fold light curve
        phase, flux_folded = self.fold_light_curve(time, flux, period)
        
        # Try different transit durations
        best_snr = 0
        best_depth = 0
        best_duration = 0
        
        durations = np.linspace(min_duration / period, max_duration / period, 20)
        
        for duration in durations:
            depth, snr = self.estimate_transit_depth(phase, flux_folded, duration)
            if snr > best_snr:
                best_snr = snr
                best_depth = depth
                best_duration = duration * period
        
        return {
            'period': period,
            'depth': best_depth,
            'snr': best_snr,
            'duration': best_duration,
            'phase': phase,
            'flux_folded': flux_folded
        }
    
    def detect(self, time: np.ndarray, flux: np.ndarray,
              n_periods: int = 1000) -> List[Dict]:
        """
        Detect transit signals in light curve.
        
        Parameters
        ----------
        time : np.ndarray
            Time values
        flux : np.ndarray
            Flux values
        n_periods : int
            Number of periods to test
            
        Returns
        -------
        detections : list
            List of detected signals
        """
        detections = []
        
        # Search periods logarithmically
        periods = np.logspace(np.log10(self.min_period), 
                             np.log10(self.max_period), n_periods)
        
        for period in periods:
            result = self.box_least_squares(time, flux, period)
            
            if result['snr'] >= self.snr_threshold and result['depth'] > 0:
                detections.append(result)
        
        # Sort by SNR
        detections.sort(key=lambda x: x['snr'], reverse=True)
        
        # Remove duplicate detections (aliases)
        filtered_detections = self._filter_aliases(detections)
        
        return filtered_detections
    
    def _filter_aliases(self, detections: List[Dict], period_tol: float = 0.01) -> List[Dict]:
        """
        Filter out period aliases.
        
        Parameters
        ----------
        detections : list
            Detected signals
        period_tol : float
            Period tolerance for considering duplicates
            
        Returns
        -------
        filtered : list
            Filtered detections
        """
        if not detections:
            return []
        
        filtered = [detections[0]]
        
        for det in detections[1:]:
            is_alias = False
            for fdet in filtered:
                period_ratio = det['period'] / fdet['period']
                if abs(period_ratio - round(period_ratio)) < period_tol:
                    is_alias = True
                    break
            
            if not is_alias:
                filtered.append(det)
        
        return filtered
