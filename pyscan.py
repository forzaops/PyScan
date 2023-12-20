import asyncio
import argparse
import ipaddress
import time
import socket

common_ports = [
    20,    # FTP Data Transfer
    21,    # FTP Control
    22,    # Secure Shell (SSH)
    23,    # Telnet
    25,    # Simple Mail Transfer Protocol (SMTP)
    53,    # Domain Name System (DNS)
    80,    # Hypertext Transfer Protocol (HTTP)
    110,   # Post Office Protocol v3 (POP3)
    111,   # Open Network Computing Remote Procedure Call (ONC RPC)
    135,   # Microsoft RPC
    139,   # NetBIOS Session Service
    143,   # Internet Message Access Protocol (IMAP)
    443,   # HTTP Secure (HTTPS)
    445,   # Microsoft Server Message Block (SMB)
    993,   # IMAP over TLS/SSL
    995,   # POP3 over TLS/SSL
    1433,  # Microsoft SQL Server
    1521,  # Oracle Database
    3306,  # MySQL
    3389,  # Remote Desktop Protocol (RDP)
    5900,  # Virtual Network Computing (VNC)
    8080,  # HTTP alternate
    8443   # HTTPS alternate
]

def resolve_host(target):
    try:
        # Try to interpret target as an IP address first
        ipaddress.ip_address(target)
        return [target]  # Return as a list for consistency
    except ValueError:
        # Not an IP address, try resolving as hostname
        try:
            return [socket.gethostbyname(target)]
        except socket.gaierror:
            print(f"[-] Unable to resolve {target}. Skipping.")
            return []

async def check_port(ip, port):
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=1)
        print(f"[+] Found open port {port} on {ip}")
        writer.close()
        await writer.wait_closed()
    except asyncio.TimeoutError:
        pass
        # print(f"[-] Timeout error on port {port} for {ip}")
    except ConnectionRefusedError:
        pass
        #print(f"[-] Connection refused on port {port} for {ip}")
    except Exception as e:
        pass
        #print(f"[-] Unexpected error on port {port} for {ip}: {e}")

async def scan_target(ip, ports):
    batch_size = 1000  # batch size, adjust as needed
    for i in range(0, len(ports), batch_size):
        batch = ports[i:i + batch_size]
        tasks = [check_port(ip, port) for port in batch]
        await asyncio.gather(*tasks)
    #tasks = [check_port(ip, port) for port in ports]
    #await asyncio.gather(*tasks)

async def main(targets, ports):
    tasks = [scan_target(str(ip), ports) for target in targets for ip in ipaddress.IPv4Network(target, strict=False)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simple Asyncio Port Scanner')
    parser.add_argument('-p', dest='ports', help='Specify ports, e.g., 80,443 or 80-100 or - for all ports')
    parser.add_argument('--top-ports', action='store_true', help='Scan the top 100 most common ports')
    parser.add_argument('target', help='Target IP, CIDR, or comma-separated sequence of these')
    args = parser.parse_args()

    if args.top_ports:
        ports = iter(common_ports)
    elif args.ports == '-':
        ports = range(1, 65536)
    elif '-' in args.ports:
        start, end = map(int, args.ports.split('-'))
        ports = range(start, end + 1)
    else:
        ports = map(int, args.ports.split(','))

    targets = args.target.split(',')
    resolved_targets = [ip for target in targets for ip in resolve_host(target)]  # Resolve each target and flatten the list
    
    start_time = time.time()
    asyncio.run(main(resolved_targets, list(ports)))
    end_time = time.time()
    print(f"Scan completed in {end_time - start_time:.2f} seconds")
