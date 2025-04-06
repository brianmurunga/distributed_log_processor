import sqlite3

def is_db_healthy(db_path="logs.db"):
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA integrity_check")
        conn.close()
        return True
    except sqlite3.DatabaseError:
        return False
