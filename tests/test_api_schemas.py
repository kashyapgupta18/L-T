"""Unit tests for Pydantic schema validation."""
import unittest
from lt_hazira_platform.api.schemas import PredictionRequest, PredictionResponse

class TestAPISchemas(unittest.TestCase):
    def test_valid_request(self):
        req = PredictionRequest(
            wear_index=45.0,
            days_since_last_maintenance=12.0,
            prev_shift_downtime=0.0
        )
        self.assertEqual(req.wear_index, 45.0)

    def test_invalid_wear(self):
        with self.assertRaises(ValueError):
            PredictionRequest(
                wear_index=150.0, # Exceeds 100.0 max
                days_since_last_maintenance=5.0
            )

if __name__ == "__main__":
    unittest.main()
