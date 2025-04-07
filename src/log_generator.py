import sqlite3
import random
import time
from faker import Faker

fake = Faker()
LOG_LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]

def generate_structured_log():
    """Generate a single fake log entry."""
    return {
        "timestamp": fake.date_time().strftime("%Y-%m-%d %H:%M:%S"),
        "level": random.choice(LOG_LEVELS),
        "message": fake.sentence(),
        "user": fake.user_name()
    }

def save_log_to_db(log_entry):
    """Insert a single log entry into the database."""
    try:
        conn = sqlite3.connect("logs.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO logs (timestamp, level, message, user)
            VALUES (?, ?, ?, ?)
        """, (log_entry["timestamp"], log_entry["level"], log_entry["message"], log_entry["user"]))
        conn.commit()
    except sqlite3.Error as e:
        print("❌ Database error:", e)
    finally:
        conn.close()

def generate_logs(count=5, delay=0):
    """Generate and insert multiple logs with optional delay."""
    for i in range(count):
        log = generate_structured_log()
        save_log_to_db(log)
        print(f"✅ Log {i + 1}/{count} saved:", log)
        if delay > 0:
            time.sleep(delay)

# Manual testing
if __name__ == "__main__":
    generate_logs(count=5, delay=0.5)  # delay time to simulate real-time logs
