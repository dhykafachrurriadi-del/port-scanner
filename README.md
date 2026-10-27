# TCP Port Scanner

A multithreaded TCP port scanner written in Python, built as part of the
Cybersecurity Internship at Syntecxhub.

## Features
- Scan a single port or a custom port range on a host
- Concurrent scanning with threads
- Reports OPEN / CLOSED / TIMEOUT / ERROR for each port
- Prints results and saves timestamped logs to `scan_log.txt`
- Handles invalid input, unresolvable hosts, and Ctrl+C

## Requirements
Python 3. No external libraries needed.

## Usage
    python portscan_task.py

Enter the host, the start port, and the end port when prompted.
To scan a single port, use the same number for both.

## How it works
Each port is checked by its own thread, which tries to open a TCP
connection with a 3-second timeout:
- Connection succeeds -> OPEN
- Connection refused -> CLOSED
- No answer within the timeout -> TIMEOUT
- Any other network error -> ERROR

A lock keeps log writes from different threads from colliding, and a
semaphore limits the scanner to 100 active threads at a time.

## Results
Tested on localhost (127.0.0.1), ports 1-100:
- This threaded version: 3 min 23 s
- Finding: port [137] was open (Windows NetBIOS service)

## Limitations
- TCP only (no UDP scanning)
- Shows which ports are open, but does not assess whether the service
  behind them is secure

## Disclaimer
For educational use. Only scan hosts you own or have permission to test.
