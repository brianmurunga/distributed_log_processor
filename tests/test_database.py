import unittest
import os
import sqlite3
from logtool.database import setup_database, delete_old_logs

DB_PATH = "logs.db"

class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        """Ensure fresh DB setup before each test."""
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        setup_database()

    def test_setup_database_creates_table(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logs'")
        table = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(table)

    def test_delete_old_logs(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Insert sample old log
        cursor.execute("""
            INSERT INTO logs (timestamp, level, message, user)
            VALUES ('2000-01-01 00:00:00', 'INFO', 'Old log', 'tester')
        """)
        conn.commit()

        # Delete logs older than 30 days
        delete_old_logs(days=30)

        cursor.execute("SELECT * FROM logs WHERE message = 'Old log'")
        result = cursor.fetchall()
        conn.close()
        self.assertEqual(result, [])  # Expect empty result

if __name__ == "__main__":
    unittest.main()
