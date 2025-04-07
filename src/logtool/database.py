import sqlite3
from datetime import datetime, timedelta

DB_NAME = "logs.db"

def setup_database():
    """
    Initialize the SQLite database and create the logs table if it doesn't exist.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                level TEXT,
                message TEXT,
                user TEXT
            )
        """)

        conn.commit()
        print("✅ Database and logs table are ready.")
    
    except sqlite3.DatabaseError as e:
        print(f"[Error] Failed to set up database: {e}")
    
    finally:
        conn.close()


def delete_old_logs(days):
    """
    Delete logs older than the specified number of days.

    Args:
        days (int): Logs older than this number of days will be deleted.
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    cutoff_str = cutoff_date.strftime("%Y-%m-%d %H:%M:%S")

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM logs WHERE timestamp < ?", (cutoff_str,))
        conn.commit()
        print(f"🧹 Deleted logs older than {days} days.")
    
    except sqlite3.DatabaseError as e:
        print(f"[Error] Failed to delete old logs: {e}")
    
    finally:
        conn.close()


# Auto-run only if executed directly
if __name__ == "__main__":
    setup_database()
