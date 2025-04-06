import csv

def export_logs_to_csv(logs, filename):
    """Export given logs to a CSV file."""
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Timestamp", "Log Level", "Message"])
        writer.writerows(logs)
