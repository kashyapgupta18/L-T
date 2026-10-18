"""Unit tests for energy efficiency and kWh/unit profiling."""
import unittest
import pandas as pd
from lt_hazira_platform.analytics.energy_profiler import compute_energy_intensity

class TestEnergyProfiler(unittest.TestCase):
    def test_energy_metrics(self):
        df = pd.DataFrame([
            {"machine_id": 1, "energy_kwh": 500.0, "units_produced": 100},
            {"machine_id": 1, "energy_kwh": 400.0, "units_produced": 80}
        ])
        res = compute_energy_intensity(df)
        self.assertEqual(len(res), 1)
        self.assertEqual(res.iloc[0]["total_energy_kwh"], 900.0)
        self.assertAlmostEqual(res.iloc[0]["avg_kwh_per_unit"], 5.0, places=2)

if __name__ == "__main__":
    unittest.main()
