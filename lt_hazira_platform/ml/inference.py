"""Real-time single-sample failure risk inference engine."""
import joblib
import pandas as pd
from pathlib import Path
from typing import Dict, Any
from lt_hazira_platform.core.config import config
from lt_hazira_platform.core.exceptions import ModelInferenceError

class FailurePredictor:
    def __init__(self, model_path: Path = None):
        self.model_path = model_path or config.model_path
        self._model = None

    def _load_model(self):
        if self._model is None:
            if not self.model_path.exists():
                raise ModelInferenceError(f"Model file not found at {self.model_path}")
            self._model = joblib.load(self.model_path)

    def predict_risk(self, features: Dict[str, Any]) -> float:
        self._load_model()
        df = pd.DataFrame([features])
        prob = self._model.predict_proba(df)[0, 1]
        return round(float(prob), 4)
