# PyScan

## Description
This project provides a simple, yet effective Python-based port scanner similar in functionality to Nmap. Utilizing the power of asyncio, it efficiently scans specified ports on target hosts or networks. The scanner supports scanning individual IPs, CIDR blocks, or a list of either, and offers flexibility in selecting specific ports or ranges, including common ports.

## Features
- Asynchronous scanning for high efficiency.
- Ability to scan individual IP addresses or entire CIDR ranges.
- Option to specify ports individually, as a range, or scan the top common ports.
- Time-efficient, scanning large batches of ports simultaneously.

## Requirements
- Python 3.7 or higher.
- Basic knowledge of network protocols and port scanning.

## Usage
To use the scanner, run the script with the desired target and port options. Here are some example usages:

```bash
# Scan a single IP for common ports
python pyscan.py --top-ports 192.168.1.1

# Scan a range of IPs for a specific port
python pyscan.py -p 80 192.168.1.0/24

# Scan multiple IPs for a range of ports
python pyscan.py -p 80-100 192.168.1.1,192.168.1.2
```

## Arguments
- `-p`: Specify ports, e.g., 80,443 or 80-100 or - for all ports.
- `--top-ports`: Scan the common ports list.
- `target`: Target IP, CIDR, or comma-separated sequence of these.

## Disclaimer
Port scanning can be seen as intrusive. Always ensure you have permission to scan the network and IP addresses.

## License
This project is released under GPL-3.0 License.
