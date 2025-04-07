import argparse
from logtool.query_logs import query_logs, fetch_logs_by_date
from datetime import datetime
from logtool.export_logs import export_logs_to_csv
from logtool.database import delete_old_logs
from logtool.visualize_logs import plot_log_levels
from logtool.log_generator import generate_structured_log, save_log_to_db

def validate_date(date_str):
    """Validate and return a datetime string in full format."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: '{date_str}'. Use YYYY-MM-DD.")

def main():
    parser = argparse.ArgumentParser(
        description="🛠️ Distributed Log Processor CLI"
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Query logs
    query_parser = subparsers.add_parser('query', help='🔍 Query logs by date range')
    query_parser.add_argument('--start', required=True, type=validate_date, help='Start date (YYYY-MM-DD)')
    query_parser.add_argument('--end', required=True, type=validate_date, help='End date (YYYY-MM-DD)')
    query_parser.add_argument('--plot', action='store_true', help='Visualize log level distribution')

    # Delete old logs
    delete_parser = subparsers.add_parser('delete', help='🧹 Delete logs older than X days')
    delete_parser.add_argument('--days', type=int, required=True, help='Days to retain logs')

    # Export logs
    export_parser = subparsers.add_parser('export', help='📦 Export logs to CSV')
    export_parser.add_argument('--start', required=True, type=validate_date, help='Start date (YYYY-MM-DD)')
    export_parser.add_argument('--end', required=True, type=validate_date, help='End date (YYYY-MM-DD)')
    export_parser.add_argument('--filename', required=True, help='Output CSV filename')

    # Generate logs
    generate_parser = subparsers.add_parser('generate', help='🧪 Generate fake logs for testing')
    generate_parser.add_argument('--count', type=int, default=10, help='Number of logs to generate (default: 10)')

    args = parser.parse_args()

    if args.command == 'query':
        logs = fetch_logs_by_date(args.start, args.end)
        if not logs:
            print("⚠️ No logs found for the given date range.")
        else:
            for log in logs:
                print(log)
            if args.plot:
                plot_log_levels(logs)

    elif args.command == 'delete':
        confirm = input(f"⚠️ Are you sure you want to delete logs older than {args.days} days? (y/n): ")
        if confirm.lower() == 'y':
            delete_old_logs(args.days)
            print(f"✅ Logs older than {args.days} days deleted.")
        else:
            print("❎ Deletion cancelled.")

    elif args.command == 'export':
        logs = query_logs(args.start, args.end)
        if not logs:
            print("⚠️ No logs found to export.")
        else:
            export_logs_to_csv(logs, args.filename)
            print(f"✅ Logs exported to {args.filename}")

    elif args.command == 'generate':
        print(f"Generating {args.count} fake logs...")
        for _ in range(args.count):
            log = generate_structured_log()
            save_log_to_db(log)
        print(f"✅ {args.count} logs generated and saved.")

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
