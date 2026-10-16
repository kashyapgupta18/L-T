"""Unit tests for industrial OEE calculations."""
import unittest
from lt_hazira_platform.analytics.oee_calculator import calculate_oee

class TestOEECalculator(unittest.TestCase):
    def test_perfect_shift(self):
        res = calculate_oee(8.0, 0.0, 100, 12.5, 0)
        self.assertEqual(res.availability, 1.0)
        self.assertEqual(res.performance, 1.0)
        self.assertEqual(res.quality, 1.0)
        self.assertEqual(res.oee, 1.0)

    def test_reduced_shift(self):
        # 6 hours operating out of 8 -> 0.75 availability
        res = calculate_oee(6.0, 2.0, 50, 10.0, 5)
        self.assertEqual(res.availability, 0.75)
        self.assertAlmostEqual(res.quality, 0.9, places=2)
        self.assertGreater(res.oee, 0.0)

if __name__ == "__main__":
    unittest.main()
