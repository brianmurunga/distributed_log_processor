from flask import Flask, render_template, request, send_file
from datetime import datetime
import os
from io import StringIO
import csv
from collections import Counter

from logtool.query_logs import fetch_logs_by_date
from logtool.export_logs import export_logs_to_csv

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    logs = []
    start_date = end_date = None
    log_levels = []
    log_counts = []
    
    if request.method == 'POST':
        start_date = request.form['start_date'] + ' 00:00:00'
        end_date = request.form['end_date'] + ' 23:59:59'
        logs = fetch_logs_by_date(start_date, end_date)
        
        # Count log levels if logs exist
        if logs:
            log_levels = [log[2] for log in logs]
            level_counts = Counter(log_levels)
            log_levels = list(level_counts.keys())
            log_counts = list(level_counts.values())
    
    return render_template(
        "index.html", 
        logs=logs, 
        start=start_date, 
        end=end_date,
        log_levels=log_levels, 
        log_counts=log_counts
    )

@app.route('/export', methods=['POST'])
def export():
    start_date = request.form['start_date'] + ' 00:00:00'
    end_date = request.form['end_date'] + ' 23:59:59'
    logs = fetch_logs_by_date(start_date, end_date)

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Timestamp', 'Level', 'Message', 'User'])
    writer.writerows(logs)
    output.seek(0)

    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)