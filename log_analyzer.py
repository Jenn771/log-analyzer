import argparse

def parse_log_file(filename):
    parsed_logs = []

    with open(filename, "r") as f:
        lines = f.readlines()   # list of strings

    for line in lines:
        parts = line.split()

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
    print(f"File: {args.filename}\n")

    # Parse the log file
    logs = parse_log_file(args.filename)

if __name__ == "__main__":
    main()