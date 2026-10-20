"""Unit tests for machine learning pre-shift feature transformations."""
import unittest
import pandas as pd
from lt_hazira_platform.ml.feature_engineering import engineer_preshift_features, FEATURE_COLS

class TestMLFeatures(unittest.TestCase):
    def test_feature_generation(self):
        df = pd.DataFrame([{"wear_index": 50.0}])
        features = engineer_preshift_features(df)
        for col in FEATURE_COLS:
            self.assertIn(col, features.columns)
            self.assertFalse(features[col].isnull().any())

if __name__ == "__main__":
    unittest.main()
