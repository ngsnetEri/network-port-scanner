#!/usr/bin/env python3
"""
tiny_port_scan.py
A small, practical port scanner I made while learning Python sockets.
Usage:
    python3 tiny_port_scan.py 127.0.0.1 20 1024

Notes:
- Fast and not stealthy — just for lab practice on your own machines.
- If you use it on a network that is not yours, get permission first.
- Author: Ngsnet (learning and experimenting)
"""
import socket
import sys

def scan(target, start_port, end_port):
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("Could not resolve host:", target)
        return

    print(f"Scanning {target_ip} from {start_port} to {end_port} (quick scan)")
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.2)
        try:
            sock.connect((target_ip, port))
        except Exception:
            # closed / filtered — keep moving
            pass
        else:
            print(f"Open: {port}")
        finally:
            sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 tiny_port_scan.py <host> <start> <end>")
        sys.exit(1)

    host_arg = sys.argv[1]
    try:
        start_arg = int(sys.argv[2])
        end_arg = int(sys.argv[3])
    except ValueError:
        print("Start and end ports must be integers.")
        sys.exit(1)

    scan(host_arg, start_arg, end_arg)
