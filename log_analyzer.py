import argparse

def parse_log_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()   # list of strings

    for line in lines:
        print(line.strip())

    return lines


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Analyze log files")

    parser.add_argument('filename', help='The log file to analyze')
    parser.add_argument('--errors', action='store_true', help='Show only errors')
    parser.add_argument('--export', help='Export results to JSON file')

    # Parse the command-line arguments and store them
    args = parser.parse_args()


    print("----------------LOG ANALYSIS REPORT----------------\n")
    print(f"File: {args.filename}\n")

    # read the file
    parse_log_file(args.filename)

if __name__ == "__main__":
    main()