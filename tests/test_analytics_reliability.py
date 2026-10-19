"""Unit tests for MTBF and MTTR metrics."""
import unittest
import pandas as pd
from lt_hazira_platform.analytics.mtbf_mttr_calculator import calculate_reliability_metrics

class TestReliabilityMetrics(unittest.TestCase):
    def test_mtbf_mttr(self):
        maint_df = pd.DataFrame([
            {"maintenance_type": "Corrective", "duration_hours": 4.0},
            {"maintenance_type": "Corrective", "duration_hours": 6.0},
            {"maintenance_type": "Preventive", "duration_hours": 2.0}
        ])
        res = calculate_reliability_metrics(maint_df, total_operating_hours=1000.0)
        self.assertEqual(res["failure_count"], 2)
        self.assertEqual(res["mttr_hours"], 5.0)
        self.assertEqual(res["mtbf_hours"], 495.0)

if __name__ == "__main__":
    unittest.main()
