# gbscan.py

## Description
This Python script provides a simple penetration testing utility. It is capable of scanning specified ports on a target IP address, enumerating services on any open ports using nmap, and using gobuster to brute force directories.

## Requirements
The script requires Python 3 to run, as well as the following dependencies:

- [nmap](https://nmap.org/): This tool is used to enumerate services on open ports.
- [gobuster](https://github.com/OJ/gobuster): This tool is used for directory brute forcing.

Please make sure these are installed and accessible from your PATH before running the script.

## Usage
To use the script, you will need to provide a target IP address, a list of ports to scan, and a wordlist file for gobuster.

The command-line arguments are:

- `-t`, `--target`: Target IP address. (required)
- `-p`, `--ports`: Ports to scan. Default are ports 22, 80, and 443. (optional)
- `-a`, `--all-ports`: Scan all ports. (optional)
- `-w`, `--wordlist-file`: File path to the wordlist for gobuster. (required)

Here is an example of how to run the script:

```bash
python gbscan.py -t <target_IP> -p 22 80 443 -w <path_to_wordlist>
