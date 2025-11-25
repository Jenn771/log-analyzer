import argparse
import json
from datetime import datetime

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

def print_period(logs):
    if not logs:
        print("Period: No log entries found\n")
        return

    total_entries = len(logs)
    lastlog = logs[total_entries - 1]

    if logs[0]['date'] != lastlog['date']:
        print(f"Period: {logs[0]['date']} to {lastlog['date']} ({logs[0]['time']} - {lastlog['time']})\n")
    else:
        print(f"Period: {logs[0]['date']} ({logs[0]['time']} - {lastlog['time']})\n")

def print_summary(logs):
    print("SUMMARY")
    print("-"*30)

    total_entries = len(logs)
    print(f"{'Total Entries:':<20} {total_entries}")

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

def print_response_times(logs):
    times = []
    for d in logs:
        rt = d['response_time']
        if rt is None:
            continue
        
        num = int(rt.rstrip("ms"))
        times.append(num)

    if not times:
        print("No response time data available.\n")
        return

    average_time = sum(times) / len(times)
    fastest_time = min(times)
    slowest_time = max(times)

    print("RESPONSE TIMES")
    print("-"*30)

    print(f"{'Average:':<20}{average_time:.0f}ms")
    print(f"{'Fastest:':<20}{fastest_time:.0f}ms")
    print(f"{'Slowest:':<20}{slowest_time:.0f}ms\n")

def print_top_endpoints(logs):
    endpoint_counts = {}

    for d in logs:
        endpoint = d['endpoint']

        if endpoint is None:
            continue

        endpoint_counts[endpoint] = endpoint_counts.get(endpoint, 0) + 1

    if not endpoint_counts:
        print("No endpoint data available.\n")
        return
    
    print("TOP ENDPOINTS")
    print("-"*30)
    for endpoint, count in endpoint_counts.items():
        label = "request" if count == 1 else "requests"
        print(f"{endpoint:<20} {count} {label}")
    
    print()

def print_errors_detected(logs):
    print("ERRORS DETECTED")
    print("-"*30)

    for d in logs:
        level = d['level']

        if level == "ERROR":
            print(f"[{d['time']}] {d['method']} {d['endpoint']} - {d['message']}")

    print()
 
def generate_report_data(logs, filename):
    total_entries = len(logs)
    
    # Metadata
    metadata = {
        "filename": filename,
        "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_entries": total_entries,
        "time_range": {
            "start": f"{logs[0]['date']} {logs[0]['time']}" if logs else None,
            "end": f"{logs[total_entries-1]['date']} {logs[total_entries-1]['time']}" if logs else None
        }
    }

    # Log levels summary
    level_counts = {}
    for log in logs:
        level = log['level']
        level_counts[level] = level_counts.get(level, 0) + 1

    summary = {
        "total_entries": total_entries,
        "log_levels": level_counts
    }

    # Response times
    times = []
    for d in logs:
        rt = d['response_time']
        if rt is None:
            continue
        
        num = int(rt.rstrip("ms"))
        times.append(num)

    response_times = {}
    if times:
        response_times = {
            "average_ms": round(sum(times) / len(times)),
            "min_ms": min(times),
            "max_ms": max(times)
        }

    # Errors list
    errors = []

    for d in logs:
        if d['level'] == "ERROR":
            error_entry = {
                "timestamp": f"{d['date']} {d['time']}",
                "level": d['level'],
                "endpoint": d['endpoint'],
                "method": d['method'],
                "status_code": int(d['status']) if d['status'] else None,
                "response_time": int(d['response_time'].rstrip('ms')) if d['response_time'] else None,
                "message": d['message']
            }
            errors.append(error_entry)

    # Build final report
    report = {
        "metadata": metadata,
        "summary": summary,
        "response_times": response_times,
        "errors": errors
    }

    return report

def export_to_json(data, filename):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error exporting to JSON: {e}")

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Analyze log files")
    parser.add_argument('filename', help='The log file to analyze')
    parser.add_argument('--errors', action='store_true', help='Show only errors')
    parser.add_argument('--export', help='Export results to JSON file')

    args = parser.parse_args()
    
    logs = parse_log_file(args.filename)

    # Filter to show only errors
    if args.errors:
        logs = [log for log in logs if log['level'] == "ERROR"]

    print("----------------LOG ANALYSIS REPORT----------------\n")
    print(f"File: {args.filename}")


    print_period(logs)
    print_summary(logs)
    print_response_times(logs)
    print_top_endpoints(logs)
    print_errors_detected(logs)

    if args.export:
        report_data = generate_report_data(logs, args.filename)
        export_to_json(report_data, args.export)


if __name__ == "__main__":
    main()