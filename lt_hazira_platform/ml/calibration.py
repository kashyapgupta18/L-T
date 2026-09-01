"""Probability calibration for risk estimation."""
from sklearn.calibration import CalibratedClassifierCV

def calibrate_model(model, X_val, y_val, method: str = "sigmoid"):
    calibrator = CalibratedClassifierCV(estimator=model, method=method, cv="prefit")
    calibrator.fit(X_val, y_val)
    return calibrator
