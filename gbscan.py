# Import the necessary libraries
import argparse
import concurrent.futures
import socket
import os
import subprocess

# Function to scan a single port
def port_scan(target, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((target,port))
        if result == 0:
            print("Port {} is open.".format(port))
            return port

# Function to enumerate services on an open port using nmap
def service_enum(target, port):
    try:
        print("Enumerating port {}:".format(port))
        # Run nmap with the -sV option for version detection and -p to specify the port
        result = subprocess.check_output(['nmap', '-sV', '-p', str(port), target])
        print(result.decode('utf-8'))  # Decoding byte string into text and printing it
    except Exception as e:
        # If an error occurs (e.g. nmap is not installed), print the error message
        print(f"An error occurred during service enumeration: {e}")

# Function to brute force directories using gobuster
def brute_force_directories(target, wordlist_file):
    try:
        print("Running gobuster on target {}".format(target))
        # Run gobuster with dir mode, -u for url, -w for wordlist
        subprocess.run(['gobuster', 'dir', '-u', target, '-w', wordlist_file], text=True)
    except Exception as e:
        # If an error occurs (e.g. gobuster is not installed), print the error message
        print(f"An error occurred during gobuster execution: {e}")


# Create a new argument parser
# Create a new argument parser
parser = argparse.ArgumentParser(description="A simple pentest script.")
parser.add_argument("-t", "--target", required=True, help="Target IP address.")
parser.add_argument("-p", "--ports", nargs="+", default=[22, 80, 443], type=int, help="Ports to scan.")
parser.add_argument("-a","--all-ports", action="store_true", help="Scan all ports (overrides --ports).")
parser.add_argument("-w", "--wordlist-file", type=argparse.FileType('r'), required=True, help="File with wordlist for gobuster.")

# Parse command-line arguments
args = parser.parse_args()

# If --all-ports is set, ignore the --ports argument and scan all ports
if args.all_ports:
    args.ports = range(1, 1000)

open_ports = []
try:
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(port_scan, args.target, port) for port in args.ports}
        for future in concurrent.futures.as_completed(futures):
            port = future.result()
            if port is not None:
                open_ports.append(port)

    for port in open_ports:
        service_enum(args.target, port)

    brute_force_directories(args.target, args.wordlist_file.name)

except KeyboardInterrupt:
    print("\nExiting...")
    try:
        for future in futures:
            future.cancel()
    except:
        pass