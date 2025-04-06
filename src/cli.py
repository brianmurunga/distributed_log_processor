import argparse
from query_logs import fetch_logs_by_date

def main():
    parser = argparse.ArgumentParser(
        description="Distributed Log Processor - CLI Tool"
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Example command: query logs
    query_parser = subparsers.add_parser('query', help='Query logs by date range')
    query_parser.add_argument('--start', required=True, help='Start date (YYYY-MM-DD)')
    query_parser.add_argument('--end', required=True, help='End date (YYYY-MM-DD)')

    args = parser.parse_args()

    if args.command == 'query':
        print(f"Fetching logs from {args.start} to {args.end}")

if __name__ == '__main__':
    main()
