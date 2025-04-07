import sqlite3

def fetch_logs_by_date(start_date, end_date):
    """
    Fetch logs from the database between the provided start and end timestamps.

    Args:
        start_date (str): Start datetime in 'YYYY-MM-DD HH:MM:SS' format.
        end_date (str): End datetime in 'YYYY-MM-DD HH:MM:SS' format.

    Returns:
        list: List of log entries as tuples.
    """
    try:
        conn = sqlite3.connect("logs.db")
        cursor = conn.cursor()

        query = """
            SELECT * FROM logs 
            WHERE timestamp BETWEEN ? AND ?
        """
        cursor.execute(query, (start_date, end_date))
        logs = cursor.fetchall()

    except sqlite3.DatabaseError as e:
        print(f"[Error] Database issue: {e}")
        logs = []

    finally:
        conn.close()

    return logs

def query_logs(start_date, end_date):
    """Fetch logs within a specific date range."""
    try:
        conn = sqlite3.connect("logs.db")
        cursor = conn.cursor()

        query = """
            SELECT * FROM logs 
            WHERE timestamp BETWEEN ? AND ?
        """
        cursor.execute(query, (start_date, end_date))
        logs = cursor.fetchall()
        return logs

    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
        return []

    finally:
        conn.close()


# Optional manual test
if __name__ == "__main__":
    start = "2024-03-25 00:00:00"
    end = "2024-03-30 23:59:59"
    
    logs = fetch_logs_by_date(start, end)
    for log in logs:
        print(log)
