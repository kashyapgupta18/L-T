"""Data distribution drift detection for production feature tracking."""
import numpy as np
from scipy.stats import ks_2samp
from typing import Dict

def detect_feature_drift(baseline: np.ndarray, current: np.ndarray, alpha: float = 0.05) -> Dict[str, Any]:
    stat, p_value = ks_2samp(baseline, current)
    return {
        "statistic": round(float(stat), 4),
        "p_value": round(float(p_value), 4),
        "drift_detected": bool(p_value < alpha)
    }
