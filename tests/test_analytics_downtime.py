"""Unit tests for downtime Pareto distribution."""
import unittest
import pandas as pd
from lt_hazira_platform.analytics.downtime_analyzer import analyze_downtime_by_machine_type

class TestDowntimeAnalyzer(unittest.TestCase):
    def test_pareto_ranking(self):
        df = pd.DataFrame([
            {"machine_type": "CNC Cutting", "downtime_hours": 100.0},
            {"machine_type": "Welding Robot", "downtime_hours": 50.0},
            {"machine_type": "Rolling Mill", "downtime_hours": 25.0}
        ])
        res = analyze_downtime_by_machine_type(df)
        self.assertEqual(res.iloc[0]["machine_type"], "CNC Cutting")
        self.assertAlmostEqual(res.iloc[-1]["cumulative_percentage"], 100.0, places=1)

if __name__ == "__main__":
    unittest.main()
