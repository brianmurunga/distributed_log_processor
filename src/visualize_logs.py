import sqlite3
import matplotlib.pyplot as plt
from collections import Counter
import datetime

def fetch_log_counts():
    """Fetch log counts grouped by day from the database."""
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()

    cursor.execute("SELECT timestamp FROM logs")
    timestamps = cursor.fetchall()
    conn.close()

    # Extract only the dates (YYYY-MM-DD)
    dates = [ts[0][:10] for ts in timestamps]

    # Count occurrences per day
    date_counts = Counter(dates)
    return date_counts

def plot_log_trends():
    """Visualize log frequency as a bar chart."""
    date_counts = fetch_log_counts()

    if not date_counts:
        print("⚠️ No logs found to visualize.")
        return

    # Sort dates
    dates = sorted(date_counts.keys())
    counts = [date_counts[date] for date in dates]

    # Plot
    plt.figure(figsize=(10, 5))
    plt.bar(dates, counts, color="skyblue")
    plt.xlabel("Date")
    plt.ylabel("Log Count")
    plt.title("Logs Per Day")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Show plot
    plt.show()

# Example usage
if __name__ == "__main__":
    plot_log_trends()
