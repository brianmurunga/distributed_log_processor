from flask import Flask, render_template, request, send_file, jsonify
import sqlite3
from datetime import datetime, date
import csv
import io
import json

app = Flask(__name__)
DATABASE = "logs.db"

def get_unique_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT user FROM logs WHERE user IS NOT NULL ORDER BY user")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users

def get_log_level_counts(logs):
    level_counts = {}
    for log in logs:
        level = log[2]
        level_counts[level] = level_counts.get(level, 0) + 1
    return level_counts

@app.route("/", methods=["GET", "POST"])
def index():
    logs = []
    start = end = user_filter = None
    users = get_unique_users()

    if request.method == "POST":
        start = request.form.get("start_date")
        end = request.form.get("end_date")
        user_filter = request.form.get("user_filter")

        query = "SELECT * FROM logs WHERE 1=1"
        params = []

        if start and end:
            query += " AND DATE(timestamp) BETWEEN ? AND ?"
            params.extend([start, end])
        elif start:
            query += " AND DATE(timestamp) >= ?"
            params.append(start)
        elif end:
            query += " AND DATE(timestamp) <= ?"
            params.append(end)

        if user_filter:
            query += " AND user = ?"
            params.append(user_filter)

        query += " ORDER BY timestamp DESC"

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(query, params)
        logs = cursor.fetchall()
        conn.close()

    return render_template("index.html", 
                         logs=logs, 
                         start=start, 
                         end=end,
                         user_filter=user_filter,
                         users=users,
                         log_levels=list(get_log_level_counts(logs).keys()) if logs else [],
                         log_counts=list(get_log_level_counts(logs).values()) if logs else [],
                         today=date.today().isoformat())

@app.route("/all")
def show_all_logs():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC")
    logs = cursor.fetchall()
    conn.close()
    
    return render_template("index.html",
                         logs=logs,
                         start=None,
                         end=None,
                         user_filter=None,
                         users=get_unique_users(),
                         log_levels=list(get_log_level_counts(logs).keys()),
                         log_counts=list(get_log_level_counts(logs).values()),
                         today=date.today().isoformat())

@app.route("/export", methods=["POST"])
def export_logs():
    start = request.form.get("start_date")
    end = request.form.get("end_date")
    user_filter = request.form.get("user_filter")
    format = request.form.get("format", "csv")

    query = "SELECT * FROM logs WHERE 1=1"
    params = []

    if start and end:
        query += " AND DATE(timestamp) BETWEEN ? AND ?"
        params.extend([start, end])
    elif start:
        query += " AND DATE(timestamp) >= ?"
        params.append(start)
    elif end:
        query += " AND DATE(timestamp) <= ?"
        params.append(end)

    if user_filter:
        query += " AND user = ?"
        params.append(user_filter)

    query += " ORDER BY timestamp DESC"

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(query, params)
    logs = cursor.fetchall()
    conn.close()

    if format == "json":
        output = io.StringIO()
        json.dump([dict(zip(['id', 'timestamp', 'level', 'message', 'user'], row)) for row in logs], output)
        output.seek(0)
        return send_file(
            io.BytesIO(output.read().encode("utf-8")),
            mimetype="application/json",
            as_attachment=True,
            download_name=f"logs_{start or 'all'}_to_{end or 'all'}.json"
        )
    elif format == "txt":
        output = io.StringIO()
        for log in logs:
            output.write(f"{log[0]}\t{log[1]}\t{log[2]}\t{log[3]}\t{log[4]}\n")
        output.seek(0)
        return send_file(
            io.BytesIO(output.read().encode("utf-8")),
            mimetype="text/plain",
            as_attachment=True,
            download_name=f"logs_{start or 'all'}_to_{end or 'all'}.txt"
        )
    else:  # CSV (default)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Timestamp", "Level", "Message", "User"])
        writer.writerows(logs)
        output.seek(0)
        return send_file(
            io.BytesIO(output.read().encode("utf-8")),
            mimetype="text/csv",
            as_attachment=True,
            download_name=f"logs_{start or 'all'}_to_{end or 'all'}.csv"
        )

if __name__ == "__main__":
    app.run(debug=True)