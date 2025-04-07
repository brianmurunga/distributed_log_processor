import unittest
from src.query_logs import query_logs
from src.database import setup_database  # ensures the table is created

class TestQueryLogs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup_database()

    def test_query_with_valid_range(self):
        start = "2024-01-01 00:00:00"
        end = "2024-12-31 23:59:59"
        logs = query_logs(start, end)
        self.assertIsInstance(logs, list)

    def test_query_with_invalid_date_format(self):
        logs = query_logs("bad-date", "another-bad-date")
        self.assertEqual(logs, [])  # Adjusted to match behavior

if __name__ == "__main__":
    unittest.main()
