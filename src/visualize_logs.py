import matplotlib.pyplot as plt
from collections import Counter

def plot_log_levels(logs):
    """Plot bar chart of log levels."""
    levels = [log[2] for log in logs]  # Assuming 3rd column is log_level
    counts = Counter(levels)

    plt.figure(figsize=(8, 5))
    plt.bar(counts.keys(), counts.values(), color='skyblue')
    plt.xlabel("Log Levels")
    plt.ylabel("Count")
    plt.title("Log Level Frequency")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()
