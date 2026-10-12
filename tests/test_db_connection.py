"""Unit tests for SQLite database connection manager."""
import unittest
from tests.conftest import create_in_memory_db

class TestDatabaseConnection(unittest.TestCase):
    def setUp(self):
        self.conn = create_in_memory_db()

    def tearDown(self):
        self.conn.close()

    def test_query_execution(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) AS cnt FROM fact_production;")
        res = cursor.fetchone()
        self.assertEqual(res["cnt"], 1)

if __name__ == "__main__":
    unittest.main()
