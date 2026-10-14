"""Unit tests for chunked batch loading into database."""
import unittest
import pandas as pd
from tests.conftest import create_in_memory_db
from lt_hazira_platform.etl.batch_loader import load_chunks

class TestETLLoader(unittest.TestCase):
    def setUp(self):
        self.conn = create_in_memory_db()

    def tearDown(self):
        self.conn.close()

    def test_chunk_loading(self):
        df = pd.DataFrame([
            {"date_id": 2, "plant_id": 1, "machine_id": 1, "shift_id": 1, "product_id": 1,
             "units_produced": 90, "units_defective": 1, "operating_hours": 7.0,
             "downtime_hours": 1.0, "energy_kwh": 310.0, "wear_index": 33.0}
        ])
        loaded = load_chunks(df, "fact_production", self.conn, chunk_size=10)
        self.assertEqual(loaded, 1)

if __name__ == "__main__":
    unittest.main()
