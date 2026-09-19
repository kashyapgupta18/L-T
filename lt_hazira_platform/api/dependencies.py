"""FastAPI dependency injection providers."""
from lt_hazira_platform.ml.inference import FailurePredictor

_predictor_instance = None

def get_failure_predictor() -> FailurePredictor:
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = FailurePredictor()
    return _predictor_instance
