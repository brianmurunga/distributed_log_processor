import json
import random
import time
from faker import Faker

fake = Faker()
LOG_LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]

def generate_structured_log():
    log_entry = {
        "timestamp": fake.date_time().strftime("%Y-%m-%d %H:%M:%S"),
        "level": random.choice(LOG_LEVELS),
        "message": fake.sentence(),
        "user": fake.user_name()
    }
    return json.dumps(log_entry)

def generate_unstructured_log():
    timestamp = fake.date_time().strftime("%Y-%m-%d %H:%M:%S")
    level = random.choice(LOG_LEVELS)
    message = fake.sentence()
    return f"[{timestamp}] {level} - {message}"

def write_logs(filename="logs/sample.log", num_lines=10):
    with open(filename, "w") as file:
        for _ in range(num_lines):
            log_type = random.choice(["structured", "unstructured"])
            log_entry = generate_structured_log() if log_type == "structured" else generate_unstructured_log()
            file.write(log_entry + "\n")

if __name__ == "__main__":
    write_logs()
    print("✅ Sample logs generated!")
