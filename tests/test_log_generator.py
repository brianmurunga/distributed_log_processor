import unittest
import sqlite3
import os
from logtool.log_generator import generate_structured_log, save_log_to_db
from logtool.database import setup_database

DB_PATH = "logs.db"

class TestLogGenerator(unittest.TestCase):

    def setUp(self):
        """Ensure the database and logs table exist before tests."""
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        setup_database()

    def test_generate_structured_log(self):
        log = generate_structured_log()
        self.assertIn("timestamp", log)
        self.assertIn("level", log)
        self.assertIn("message", log)
        self.assertIn("user", log)

    def test_save_log_to_db(self):
        log = generate_structured_log()
        save_log_to_db(log)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs WHERE message = ?", (log["message"],))
        result = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(result)

if __name__ == "__main__":
    unittest.main()
