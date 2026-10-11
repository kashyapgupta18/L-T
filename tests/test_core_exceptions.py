"""Unit tests for domain exceptions."""
import unittest
from lt_hazira_platform.core.exceptions import (
    PlatformException, DataValidationError, DatabaseConnectionError, ModelInferenceError
)

class TestExceptions(unittest.TestCase):
    def test_hierarchy(self):
        self.assertTrue(issubclass(DataValidationError, PlatformException))
        self.assertTrue(issubclass(DatabaseConnectionError, PlatformException))
        self.assertTrue(issubclass(ModelInferenceError, PlatformException))

    def test_exception_raising(self):
        with self.assertRaises(DataValidationError):
            raise DataValidationError("Invalid field value")

if __name__ == "__main__":
    unittest.main()
