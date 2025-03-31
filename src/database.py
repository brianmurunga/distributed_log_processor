import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect("logs.db")
cursor = conn.cursor()

# Create the logs table
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    level TEXT,
    message TEXT,
    user TEXT
)
""")

# Commit and close
conn.commit()
conn.close()

print("✅ Database and logs table created successfully!")
