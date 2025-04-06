import argparse
from query_logs import fetch_logs_by_date
from database import delete_old_logs
from export_logs import export_logs_to_csv
from visualize_logs import plot_log_levels  # Optional: Only if you created visualize_logs.py

def main():
    parser = argparse.ArgumentParser(
        description="Distributed Log Processor - CLI Tool"
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Query command
    query_parser = subparsers.add_parser('query', help='Query logs by date range')
    query_parser.add_argument('--start', required=True, help='Start date (YYYY-MM-DD)')
    query_parser.add_argument('--end', required=True, help='End date (YYYY-MM-DD)')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete logs older than X days')
    delete_parser.add_argument('--days', type=int, required=True, 
                               help='Days to retain (delete logs older than this)')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export logs to CSV')
    export_parser.add_argument('--start', required=True, help='Start date (YYYY-MM-DD)')
    export_parser.add_argument('--end', required=True, help='End date (YYYY-MM-DD)')
    export_parser.add_argument('--filename', required=True, help='CSV file name to export')

    # Visualize command (Optional)
    visualize_parser = subparsers.add_parser('visualize', help='Visualize log levels over time')
    visualize_parser.add_argument('--start', required=True, help='Start date (YYYY-MM-DD)')
    visualize_parser.add_argument('--end', required=True, help='End date (YYYY-MM-DD)')

    args = parser.parse_args()

    if args.command == 'query':
        logs = fetch_logs_by_date(args.start + " 00:00:00", args.end + " 23:59:59")
        for log in logs:
            print(log)

    elif args.command == 'delete':
        delete_old_logs(args.days)
        print(f"✅ Deleted logs older than {args.days} days.")

    elif args.command == 'export':
        logs = fetch_logs_by_date(args.start + " 00:00:00", args.end + " 23:59:59")
        export_logs_to_csv(logs, args.filename)
        print(f"✅ Logs exported to '{args.filename}'")

    elif args.command == 'visualize':
        logs = fetch_logs_by_date(args.start + " 00:00:00", args.end + " 23:59:59")
        plot_log_levels(logs)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
