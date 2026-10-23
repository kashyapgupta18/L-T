"""Integration test executing full analytics and prediction workflow."""
import unittest
import pandas as pd
from lt_hazira_platform.analytics.oee_calculator import calculate_oee
from lt_hazira_platform.analytics.alert_rules import evaluate_machine_alerts

class TestEndToEnd(unittest.TestCase):
    def test_pipeline_integration(self):
        # 1. Compute OEE
        oee = calculate_oee(7.0, 1.0, 95, 12.0, 2)
        self.assertGreater(oee.oee, 0.70)
        
        # 2. Check alert thresholds
        machine_status = [{
            "machine_id": 1,
            "wear_index": 88.0,
            "failure_risk": 0.65
        }]
        alerts = evaluate_machine_alerts(machine_status)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["severity"], "CRITICAL")

if __name__ == "__main__":
    unittest.main()
