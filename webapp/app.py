from flask import Flask, render_template, request, redirect, send_file, flash
import sqlite3
from datetime import datetime, date
import csv
import io
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flashing messages
DATABASE = "logs.db"

def get_unique_users():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT user FROM logs WHERE user IS NOT NULL ORDER BY user")
        return [row[0] for row in cursor.fetchall()]

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

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            logs = cursor.fetchall()

    return render_template("index.html",
                           logs=logs,
                           start=start,
                           end=end,
                           user_filter=user_filter,
                           users=users,
                           log_levels=list(get_log_level_counts(logs).keys()) if logs else [],
                           log_counts=list(get_log_level_counts(logs).values()) if logs else [],
                           today=date.today().isoformat())

@app.route("/all", methods=["GET"])
def show_all_logs():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC")
        logs = cursor.fetchall()

    return render_template("index.html",
                           logs=logs,
                           start=None,
                           end=None,
                           user_filter=None,
                           users=get_unique_users(),
                           log_levels=list(get_log_level_counts(logs).keys()),
                           log_counts=list(get_log_level_counts(logs).values()),
                           today=date.today().isoformat())

@app.route("/upload", methods=["GET", "POST"])
def upload_logs():
    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename.endswith(".csv"):
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_input = csv.reader(stream)
            next(csv_input, None)  # Skip header

            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                for row in csv_input:
                    if len(row) >= 5:
                        cursor.execute("INSERT INTO logs (id, timestamp, level, message, user) VALUES (?, ?, ?, ?, ?)", row[:5])
                conn.commit()
            flash("Logs uploaded successfully!", "success")
            return redirect("/")
        else:
            flash("Please upload a valid CSV file.", "danger")
            return redirect("/upload")
    return '''
    <!DOCTYPE html>
    <html lang="en" data-bs-theme="dark">
    <head>
        <meta charset="UTF-8">
        <title>Upload Logs</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="p-5 bg-dark text-white">
        <h2>📤 Upload Logs</h2>
        <form method="POST" enctype="multipart/form-data">
            <div class="mb-3">
                <label for="file" class="form-label">Select CSV File</label>
                <input class="form-control" type="file" name="file" accept=".csv" required>
            </div>
            <button type="submit" class="btn btn-primary">Upload</button>
            <a href="/" class="btn btn-secondary">Back</a>
        </form>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''

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

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        logs = cursor.fetchall()

    filename = f"logs_{start or 'all'}_to_{end or 'all'}"

    if format == "json":
        output = io.StringIO()
        json.dump([dict(zip(['id', 'timestamp', 'level', 'message', 'user'], row)) for row in logs], output)
        output.seek(0)
        return send_file(io.BytesIO(output.read().encode("utf-8")),
                         mimetype="application/json",
                         as_attachment=True,
                         download_name=f"{filename}.json")
    elif format == "txt":
        output = io.StringIO()
        for log in logs:
            output.write(f"{log[0]}\t{log[1]}\t{log[2]}\t{log[3]}\t{log[4]}\n")
        output.seek(0)
        return send_file(io.BytesIO(output.read().encode("utf-8")),
                         mimetype="text/plain",
                         as_attachment=True,
                         download_name=f"{filename}.txt")
    else:  # default to CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Timestamp", "Level", "Message", "User"])
        writer.writerows(logs)
        output.seek(0)
        return send_file(io.BytesIO(output.read().encode("utf-8")),
                         mimetype="text/csv",
                         as_attachment=True,
                         download_name=f"{filename}.csv")

if __name__ == "__main__":
    app.run(debug=True)
