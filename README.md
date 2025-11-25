# Log Analyzer — Python CLI Tool
A command-line tool that parses server log files, summarizes logs, detects errors, and optionally exports results to JSON.


## Features
* Parse structured log files
* Show summary of log levels (INFO, WARNING, ERROR, etc.)
* Display response time statistics (average, fastest, slowest)
* Show top endpoints
* Detect and list all error logs
* `--errors` flag for error-only mode
* `--export` flag to save results as a JSON report


## Installation

Clone the repository:

```bash
git clone https://github.com/Jenn771/log-analyzer.git
cd log-analyzer
```

## Requirements
* Python 3


## Usage

#### Basic analysis
```bash
python3 log_analyzer.py sample.log
```

#### Show only errors
```bash
python3 log_analyzer.py sample.log --errors
```

#### Export report to JSON
```bash
python3 log_analyzer.py sample.log --export report.json
```

---

## Example Output

```
----------------LOG ANALYSIS REPORT----------------

File: server.log
Period: 2025-11-18 (10:23:45 - 10:30:23)

SUMMARY
------------------------------
Total Entries:       15
INFO                 9 (60.00%)
ERROR                4 (26.67%)
WARNING              2 (13.33%)

RESPONSE TIMES
------------------------------
Average:            416ms
Fastest:            5ms
Slowest:            2341ms

TOP ENDPOINTS
------------------------------
/api/users           3 requests
/api/orders          4 requests
/api/products        3 requests
/api/payment         1 request
/api/cart            1 request

ERRORS DETECTED
------------------------------
[10:24:15] POST /api/orders - Database connection timeout
[10:26:12] POST /api/payment - Payment gateway timeout
[10:27:30] GET /api/orders - Internal server error
[10:29:45] POST /api/orders - Database connection timeout
```

---

## JSON Export Example

```json
{
  "metadata": {
    "filename": "server.log",
    "analyzed_at": "2025-11-25 1:35:41",
    "total_entries": 15,
    "time_range": {
      "start": "2025-11-18 10:23:45",
      "end": "2025-11-18 10:30:23"
    }
  },
  "summary": {
    "total_entries": 15,
    "log_levels": {
      "INFO": 9,
      "ERROR": 4,
      "WARNING": 2
    }
  },
  "response_times": {
    "average_ms": 416,
    "min_ms": 5,
    "max_ms": 2341
  },
  "errors": [
    {
      "timestamp": "2025-11-18 10:24:15",
      "level": "ERROR",
      "endpoint": "/api/orders",
      "method": "POST",
      "status_code": 500,
      "response_time": 1203,
      "message": "Database connection timeout"
    },
    {
      "timestamp": "2025-11-18 10:26:12",
      "level": "ERROR",
      "endpoint": "/api/payment",
      "method": "POST",
      "status_code": 500,
      "response_time": 2341,
      "message": "Payment gateway timeout"
    },
    {
      "timestamp": "2025-11-18 10:27:30",
      "level": "ERROR",
      "endpoint": "/api/orders",
      "method": "GET",
      "status_code": 500,
      "response_time": 156,
      "message": "Internal server error"
    },
    {
      "timestamp": "2025-11-18 10:29:45",
      "level": "ERROR",
      "endpoint": "/api/orders",
      "method": "POST",
      "status_code": 500,
      "response_time": 987,
      "message": "Database connection timeout"
    }
  ]
}
```


## Notes
* Only logs with recognized HTTP methods (`GET`, `POST`, `PUT`, `DELETE`) are treated as request logs.
* Using `--errors` will only display error logs. Other summaries are skipped.
