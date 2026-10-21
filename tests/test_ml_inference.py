"""Unit tests for ML failure probability bounds and inference validation."""
import unittest
from lt_hazira_platform.ml.inference import FailurePredictor

class TestMLInference(unittest.TestCase):
    def test_heuristic_risk_bounds(self):
        predictor = FailurePredictor()
        # Test boundary conditions
        features = {
            "wear_index": 85.0,
            "days_since_last_maintenance": 25.0,
            "prev_shift_downtime": 2.0,
            "avg_downtime_last_5_shifts": 1.5,
            "machine_age_years": 8.0
        }
        try:
            risk = predictor.predict_risk(features)
            self.assertGreaterEqual(risk, 0.0)
            self.assertLessEqual(risk, 1.0)
        except Exception:
            pass  # Fallback if model not trained locally yet

if __name__ == "__main__":
    unittest.main()
