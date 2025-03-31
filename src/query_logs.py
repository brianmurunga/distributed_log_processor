import sqlite3

# Function to fetch logs based on criteria
def fetch_logs(level=None, user=None):
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()

    query = "SELECT * FROM logs WHERE 1=1"
    params = []

    if level:
        query += " AND level = ?"
        params.append(level)
    if user:
        query += " AND user = ?"
        params.append(user)

    cursor.execute(query, params)
    logs = cursor.fetchall()
    conn.close()
    
    return logs

# Example: Fetch all logs with level "ERROR"
if __name__ == "__main__":
    error_logs = fetch_logs(level="ERROR")
    for log in error_logs:
        print(log)
