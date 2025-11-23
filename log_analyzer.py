import argparse

def parse_log_file(filename):
    parsed_logs = []

    with open(filename, "r") as f:
        lines = f.readlines()   # list of strings

    for line in lines:
        parts = line.split()

        if not parts:
            continue

        log_entry = {
            'date': parts[0],
            'time': parts[1],
            'level': parts[2]
        }

        # Request logs
        if len(parts) >= 7 and parts[3] in ['GET', 'POST', 'PUT', 'DELETE']:
            log_entry['method'] = parts[3]
            log_entry['endpoint'] = parts[4]
            log_entry['status'] = parts[5]
            log_entry['response_time'] = parts[6]

            # message if it exists
            if len(parts) > 7 and parts[7] == '-':
                log_entry['message'] = ' '.join(parts[8:])
            else:
                log_entry['message'] = ''

        else:
            log_entry['method'] = None
            log_entry['endpoint'] = None
            log_entry['status'] = None
            log_entry['response_time'] = None
            log_entry['message'] = ' '.join(parts[3:])
        
        
        parsed_logs.append(log_entry)
    
    return parsed_logs
    
def print_summary(logs):
    print("SUMMARY")
    print("-"*30)

    total_entries = len(logs)
    print(f"Total Entries:      {total_entries}")

    # count log levels
    level_counts = {}
    for log in logs:
        level = log['level']
        level_counts[level] = level_counts.get(level, 0) + 1
    
    # print levels with percentages
    for level, count in level_counts.items():
        pct = (count / total_entries) * 100
        print(f"{level:<20} {count} ({pct:.2f}%)")

    print()

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Analyze log files")
    parser.add_argument('filename', help='The log file to analyze')
    parser.add_argument('--errors', action='store_true', help='Show only errors')
    parser.add_argument('--export', help='Export results to JSON file')

    args = parser.parse_args()


    print("----------------LOG ANALYSIS REPORT----------------\n")
    print(f"File: {args.filename}")

    # Parse the log file
    logs = parse_log_file(args.filename)

    # Time period
    total_entries = len(logs)
    lastlog = logs[total_entries - 1]
    if logs[0]['date'] != lastlog['date']:
        print(f"Period: {logs[0]['date']} to {lastlog['date']} ({logs[0]['time']} - {lastlog['time']})\n")
    else:
        print(f"Period: {logs[0]['date']} ({logs[0]['time']} - {lastlog['time']})\n")


    print_summary(logs)


if __name__ == "__main__":
    main()