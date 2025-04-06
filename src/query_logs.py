import sqlite3


def fetch_logs_by_date(start_date, end_date):
    """Fetch logs within a specific date range."""
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()

    query = """
        SELECT * FROM logs 
        WHERE timestamp BETWEEN ? AND ?
    """
    cursor.execute(query, (start_date, end_date))
    
    logs = cursor.fetchall()
    conn.close()
    
    return logs

# Example Usage
if __name__ == "__main__":
    start = "2024-03-25 00:00:00"
    end = "2024-03-30 23:59:59"
    
    logs = fetch_logs_by_date(start, end)
    for log in logs:
        print(log)
