import sqlite3
import random
import time
from faker import Faker

fake = Faker()
LOG_LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]

# Function to generate a thousand
def generate_structured_log(num_entries=1000):
    return {
        "timestamp": fake.date_time().strftime("%Y-%m-%d %H:%M:%S"),
        "level": random.choice(LOG_LEVELS),
        "message": fake.sentence(),
        "user": fake.user_name()
    }

# Function to insert a log into the database
def save_log_to_db(log_entry):
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


# Generate and store 5 logs for testing
if __name__ == "__main__":
    for _ in range(5):
        log = generate_structured_log()
        save_log_to_db(log)
        print("✅ Log saved:", log)
