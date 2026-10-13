"""Unit tests for synthetic data generator constraints."""
import unittest
import pandas as pd
from lt_hazira_platform.etl.validators import validate_production_dataframe
from lt_hazira_platform.core.exceptions import DataValidationError

class TestETLGenerate(unittest.TestCase):
    def test_valid_production_df(self):
        df = pd.DataFrame([{
            "date_id": 1, "plant_id": 1, "machine_id": 1, "shift_id": 1, "product_id": 1,
            "units_produced": 100, "units_defective": 2, "operating_hours": 7.5,
            "downtime_hours": 0.5, "energy_kwh": 350.0, "wear_index": 25.0
        }])
        validated = validate_production_dataframe(df)
        self.assertEqual(len(validated), 1)

    def test_invalid_hours(self):
        df = pd.DataFrame([{
            "date_id": 1, "plant_id": 1, "machine_id": 1, "shift_id": 1, "product_id": 1,
            "units_produced": 100, "units_defective": 2, "operating_hours": 9.5,
            "downtime_hours": 0.5, "energy_kwh": 350.0, "wear_index": 25.0
        }])
        with self.assertRaises(DataValidationError):
            validate_production_dataframe(df)

if __name__ == "__main__":
    unittest.main()
