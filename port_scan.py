import socket
import argparse

# Function to scan a single port
def scan_port(host, port, timeout=1.0):
    """Attempts to connect to a host:port. Returns True if open, False otherwise."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return result == 0
    except socket.gaierror:
        raise ValueError(f"Invalid host: {host}")
    except OverflowError:
        raise ValueError(f"Invalid port number: {port}")
    except Exception as e:
        print(f"Error scanning port {port}: {e}")
        return False

# Main function to parse arguments and run the scan
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Python Port Scanner")
    parser.add_argument("host", help="Target host (e.g., 127.0.0.1 or scanme.nmap.org)")
    parser.add_argument("--ports", help="Port range, e.g. 20-25 or 22,80,443", required=True)
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout per port in seconds (default: 1.0)")
    args = parser.parse_args()

    # Parse port range
    ports = set()
    try:
        for part in args.ports.split(","):
            if "-" in part:
                start, end = map(int, part.split("-"))
                if start < 1 or end > 65535 or start > end:
                    raise ValueError("Invalid port range.")
                ports.update(range(start, end+1))
            else:
                port = int(part)
                if port < 1 or port > 65535:
                    raise ValueError("Invalid port number.")
                ports.add(port)
    except Exception as e:
        print(f"Error parsing ports: {e}")
        exit(1)

    print(f"Scanning {args.host} on ports: {sorted(ports)}")
    for port in sorted(ports):
        try:
            is_open = scan_port(args.host, port, args.timeout)
            status = "OPEN" if is_open else "closed"
            print(f"Port {port}: {status}")
        except ValueError as ve:
            print(f"Error: {ve}")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break