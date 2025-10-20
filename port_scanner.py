import argparse
import socket
import concurrent.futures
import datetime
import os

def scan_port(host, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            if s.connect_ex((host, port)) == 0:
                return port
    except Exception:
        pass
    return None

def main():
    parser = argparse.ArgumentParser(description="Tiny TCP port scanner")
    parser.add_argument("host", help="Target host (IP or hostname)")
    parser.add_argument("start", type=int, help="Start port (e.g. 1)")
    parser.add_argument("end", type=int, help="End port (e.g. 1024)")
    parser.add_argument("--timeout", type=float, default=0.5, help="Socket timeout (seconds)")
    parser.add_argument("--workers", type=int, default=200, help="Number of threads")
    args = parser.parse_args()

    open_ports = []
    ports = range(args.start, args.end + 1)

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(scan_port, args.host, p, args.timeout): p for p in ports}
        for fut in concurrent.futures.as_completed(futures):
            pnum = fut.result()
            if pnum:
                print(f"[+] Open: {pnum}")
                open_ports.append(pnum)

    os.makedirs("reports", exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out_path = f"reports/scan_{args.host}_{stamp}.txt"
    with open(out_path, "w") as f:
        f.write(f"Host: {args.host}\nRange: {args.start}-{args.end}\n\nOpen ports:\n")
        for p in sorted(open_ports):
            f.write(f"{p}\n")

    print(f"\nSaved: {out_path}")

if __name__ == "__main__":
    main()
