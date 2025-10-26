#!/usr/bin/env python3
"""
count_ports.py
Counts lines containing 'Open:' from scan_results.txt and prints the total.
Usage: place a scan_results.txt file in the repo root, then run:
    python3 count_ports.py
"""
count = 0
try:
    with open('scan_results.txt', 'r') as f:
        for line in f:
            if 'Open:' in line:
                count += 1
    print(f'Total open ports found: {count}')
except FileNotFoundError:
    print("No scan_results.txt file found. Run tiny_port_scan.py and save output to scan_results.txt first.")
