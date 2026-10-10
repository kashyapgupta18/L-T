"""Unit tests for platform configuration management."""
import unittest
from lt_hazira_platform.core.config import config
from lt_hazira_platform.core.constants import TOTAL_MACHINES, SHIFT_HOURS

class TestCoreConfig(unittest.TestCase):
    def test_config_paths(self):
        self.assertIsNotNone(config.data_dir)
        self.assertIsNotNone(config.db_path)
        self.assertGreaterEqual(config.prediction_threshold, 0.0)

    def test_domain_constants(self):
        self.assertEqual(TOTAL_MACHINES, 40)
        self.assertEqual(SHIFT_HOURS, 8.0)

if __name__ == "__main__":
    unittest.main()
