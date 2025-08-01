import argparse
import nmap


def port_scanning(ip_range):
    """Scan the given IP range for hosts with RDP (port 3389) open."""
    nm = nmap.PortScanner()
    data = nm.scan(ip_range, '3389')
    hosts = []
    for host in data.get('scan', {}):
        if data['scan'][host]['tcp'][3389]['state'] == 'open':
            hosts.append(host)
    return hosts


def main():
    parser = argparse.ArgumentParser(description="Scan for open RDP ports")
    parser.add_argument("target", help="IP range to scan, e.g. 192.168.1.0/24")
    args = parser.parse_args()
    results = port_scanning(args.target)
    for host in results:
        print(host)


if __name__ == "__main__":
    main()
