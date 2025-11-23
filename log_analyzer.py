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

    # Log levels summary
    print("SUMMARY")
    print("-"*27)
    print(f"Total Entries: {total_entries}")

    all_levels = {}
    for log in logs:
        level = log['level']
        all_levels[level] = all_levels.get(level, 0) + 1
    
    for level, count in all_levels.items():
        print(f"{level:<15} {count} ({(count / total_entries) * 100:.2f}%)")



if __name__ == "__main__":
    main()