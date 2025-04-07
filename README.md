# 🧠 Distributed Log Processor

A lightweight distributed log processing system built with Python and SQLite. It supports structured log generation, querying, exporting, and visualization — perfect for learning, prototyping, or extending.

## 📁 Project Structure

```
cli.py
database.py
export_logs.py
log_generator.py
query_logs.py
visualize_logs.py
requirements.txt
README.md
```

## 🔧 Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🧪 Usage

```bash
python log_generator.py
python cli.py query --start 2024-03-25 --end 2024-03-30
python cli.py export --start 2024-03-25 --end 2024-03-30 --filename logs.csv
python cli.py delete --days 10
```

## 📊 Visualize Logs

```python
from query_logs import query_logs
from visualize_logs import plot_log_levels

logs = query_logs("2024-03-01 00:00:00", "2024-03-31 23:59:59")
plot_log_levels(logs)
```