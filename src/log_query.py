import sqlite3

DB_FILE = "database/logs.db"

def get_logs_by_level(level="ERROR"):
    """Fetch logs by severity level"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs WHERE level = ?", (level,))
    logs = cursor.fetchall()
    conn.close()
    return logs

if __name__ == "__main__":
    logs = get_logs_by_level("ERROR")
    for log in logs:
        print(log)
