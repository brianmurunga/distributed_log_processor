import sqlite3
import json

DB_FILE = "database/logs.db"

def create_table():
    """Creates a table for storing logs"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            level TEXT,
            message TEXT,
            user TEXT
        )
    ''')
    conn.commit()
    conn.close()

def store_log(log_entry):
    """Stores a log entry into the database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Handle JSON and unstructured logs differently
    try:
        log_data = json.loads(log_entry)
        cursor.execute("INSERT INTO logs (timestamp, level, message, user) VALUES (?, ?, ?, ?)",
                       (log_data["timestamp"], log_data["level"], log_data["message"], log_data["user"]))
    except json.JSONDecodeError:  # Unstructured log
        parts = log_entry.strip().split(" - ")
        level = parts[0].split("] ")[1]
        timestamp = parts[0][1:].split("]")[0]
        message = parts[1]
        cursor.execute("INSERT INTO logs (timestamp, level, message, user) VALUES (?, ?, ?, ?)",
                       (timestamp, level, message, "unknown"))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    print("✅ Database and table set up!")
