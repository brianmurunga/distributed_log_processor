def read_logs(filename="logs/sample.log", num_lines=5):
    """Reads the last `num_lines` from the log file"""
    try:
        with open(filename, "r") as file:
            logs = file.readlines()[-num_lines:]
        return logs
    except FileNotFoundError:
        return ["Log file not found."]

if __name__ == "__main__":
    logs = read_logs()
    for log in logs:
        print(log.strip())  # Print logs line by line
