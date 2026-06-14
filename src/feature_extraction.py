"""Feature extraction for transit classification."""

import numpy as np
from scipy import stats
from typing import Dict, Tuple


class FeatureExtractor:
    """Extract features from light curves for machine learning."""
    
    def __init__(self):
        pass
    
    def extract_statistical_features(self, flux: np.ndarray) -> Dict[str, float]:
        """
        Extract basic statistical features.
        
        Parameters
        ----------
        flux : np.ndarray
            Flux values
            
        Returns
        -------
        features : dict
            Statistical features
        """
        features = {
            'mean': np.mean(flux),
            'std': np.std(flux),
            'median': np.median(flux),
            'mad': np.median(np.abs(flux - np.median(flux))),
            'skewness': stats.skew(flux),
            'kurtosis': stats.kurtosis(flux),
            'min': np.min(flux),
            'max': np.max(flux),
            'range': np.max(flux) - np.min(flux),
        }
        return features
    
    def extract_transit_features(self, phase: np.ndarray, flux: np.ndarray,
                                period: float, depth: float, duration: float) -> Dict[str, float]:
        """
        Extract transit-specific features.
        
        Parameters
        ----------
        phase : np.ndarray
            Phase values
        flux : np.ndarray
            Folded flux values
        period : float
            Transit period
        depth : float
            Transit depth
        duration : float
            Transit duration
            
        Returns
        -------
        features : dict
            Transit features
        """
        # Find transit center
        transit_center_idx = np.argmin(flux)
        transit_center = phase[transit_center_idx]
        
        # Transit region
        transit_width = duration / period
        transit_mask = np.abs(phase - transit_center) < transit_width / 2
        out_transit_mask = ~transit_mask
        
        transit_flux = flux[transit_mask]
        out_transit_flux = flux[out_transit_mask]
        
        features = {
            'period': period,
            'depth': depth,
            'duration': duration,
            'transit_width': transit_width,
            'transit_center': transit_center,
            'transit_sharpness': np.abs(np.min(flux) - np.median(out_transit_flux)) / np.std(out_transit_flux),
            'ingress_egress_ratio': self._compute_ingress_egress_ratio(phase, flux, transit_center, transit_width),
            'out_of_transit_variance': np.var(out_transit_flux),
            'transit_point_count': np.sum(transit_mask),
        }
        
        return features
    
    def _compute_ingress_egress_ratio(self, phase: np.ndarray, flux: np.ndarray,
                                     transit_center: float, transit_width: float) -> float:
        """
        Compute ratio of ingress to egress duration.
        
        Parameters
        ----------
        phase : np.ndarray
            Phase values
        flux : np.ndarray
            Flux values
        transit_center : float
            Transit center phase
        transit_width : float
            Transit width in phase
            
        Returns
        -------
        ratio : float
            Ingress/egress ratio
        """
        ingress_width = transit_width / 4
        egress_width = transit_width / 4
        
        ingress_mask = (phase >= transit_center - transit_width/2) & \
                      (phase <= transit_center - transit_width/2 + ingress_width)
        egress_mask = (phase >= transit_center + transit_width/2 - egress_width) & \
                     (phase <= transit_center + transit_width/2)
        
        if np.sum(ingress_mask) == 0 or np.sum(egress_mask) == 0:
            return 1.0
        
        ingress_slope = np.abs(np.polyfit(phase[ingress_mask], flux[ingress_mask], 1)[0])
        egress_slope = np.abs(np.polyfit(phase[egress_mask], flux[egress_mask], 1)[0])
        
        if egress_slope == 0:
            return 1.0
        
        return ingress_slope / egress_slope
    
    def extract_eclipse_features(self, phase: np.ndarray, flux: np.ndarray) -> Dict[str, float]:
        """
        Extract features specific to eclipsing binaries.
        
        Parameters
        ----------
        phase : np.ndarray
            Phase values
        flux : np.ndarray
            Folded flux values
            
        Returns
        -------
        features : dict
            Eclipse features
        """
        # Check for multiple dips (primary + secondary eclipse)
        minima_indices = self._find_local_minima(flux)
        
        features = {
            'n_dips': len(minima_indices),
            'dip_symmetry': self._compute_dip_symmetry(phase, flux),
            'dip_depth_variation': self._compute_dip_depth_variation(phase, flux, minima_indices),
        }
        
        return features
    
    def _find_local_minima(self, flux: np.ndarray, threshold: float = 0.01) -> np.ndarray:
        """
        Find local minima in flux.
        
        Parameters
        ----------
        flux : np.ndarray
            Flux values
        threshold : float
            Minimum depth for local minimum
            
        Returns
        -------
        indices : np.ndarray
            Indices of local minima
        """
        minima = []
        for i in range(1, len(flux) - 1):
            if flux[i] < flux[i-1] and flux[i] < flux[i+1]:
                depth = np.median(flux) - flux[i]
                if depth > threshold * np.median(flux):
                    minima.append(i)
        
        return np.array(minima)
    
    def _compute_dip_symmetry(self, phase: np.ndarray, flux: np.ndarray) -> float:
        """
        Compute symmetry of dips around phase 0.5.
        
        Parameters
        ----------
        phase : np.ndarray
            Phase values
        flux : np.ndarray
            Flux values
            
        Returns
        -------
        symmetry : float
            Symmetry metric (0 = symmetric, 1 = asymmetric)
        """
        first_half = flux[phase < 0.5]
        second_half = flux[phase >= 0.5]
        
        if len(first_half) == 0 or len(second_half) == 0:
            return 0.0
        
        depth_diff = np.abs(np.min(first_half) - np.min(second_half))
        max_depth = max(np.abs(np.min(first_half)), np.abs(np.min(second_half)))
        
        if max_depth == 0:
            return 0.0
        
        return depth_diff / max_depth
    
    def _compute_dip_depth_variation(self, phase: np.ndarray, flux: np.ndarray,
                                    minima_indices: np.ndarray) -> float:
        """
        Compute variation in dip depths (indicator of blending).
        
        Parameters
        ----------
        phase : np.ndarray
            Phase values
        flux : np.ndarray
            Flux values
        minima_indices : np.ndarray
            Indices of local minima
            
        Returns
        -------
        variation : float
            Depth variation metric
        """
        if len(minima_indices) < 2:
            return 0.0
        
        depths = np.abs(np.median(flux) - flux[minima_indices])
        return np.std(depths) / np.mean(depths)
    
    def extract_all_features(self, phase: np.ndarray, flux: np.ndarray,
                            period: float, depth: float, duration: float) -> Dict[str, float]:
        """
        Extract all features for classification.
        
        Parameters
        ----------
        phase : np.ndarray
            Phase values
        flux : np.ndarray
            Folded flux values
        period : float
            Period
        depth : float
            Depth
        duration : float
            Duration
            
        Returns
        -------
        all_features : dict
            All extracted features
        """
        features = {}
        
        # Statistical features
        stat_features = self.extract_statistical_features(flux)
        features.update({f'stat_{k}': v for k, v in stat_features.items()})
        
        # Transit features
        transit_features = self.extract_transit_features(phase, flux, period, depth, duration)
        features.update({f'transit_{k}': v for k, v in transit_features.items()})
        
        # Eclipse features
        eclipse_features = self.extract_eclipse_features(phase, flux)
        features.update({f'eclipse_{k}': v for k, v in eclipse_features.items()})
        
        return features
