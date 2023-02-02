import socket 
import re

def is_valid_ip_address(ip_address):
    pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return bool(re.match(pattern, ip_address))

def is_valid_port_range(port_range):
    pattern = r"^\d+-\d+$"
    if re.match(pattern, port_range):
        start, end = map(int, port_range.split("-"))
        if start >= 0 and end <= 65535 and start <= end:
            return True
    return False

class PortScanner:
    def __init__(self, ip_address, port_range):
        self.ip_address = ip_address
        self.port_range = port_range
        
    def run_scan(self):
        print("Running port scan on {} for port range {}...".format(self.ip_address, self.port_range))
        start, end = map(int, self.port_range.split("-"))
        for port in range(start, end+1):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((self.ip_address, port))
                if result == 0:
                    service = socket.getservbyport(port)
                    print("[+] Port {} is open. The service thats running is {}".format(port,service))
                    sock.close()
                else:
                    print("[-] Port {} is closed.".format(port))
                    sock.close()
            except socket.error:
                print("[*] Error while connecting to port {}.".format(port))

while True:
    ip_address = input("Enter an IP address (or 'q' to quit): ")
    if ip_address == 'q':
        break
    if is_valid_ip_address(ip_address):
        port_range = input("Enter a port range (or 'q' to quit): ")
        if port_range == 'q':
            break
        if is_valid_port_range(port_range):
            scanner = PortScanner(ip_address, port_range)
            scanner.run_scan()
        else:
            print("The port range is not valid.")
    else:
        print("The IP address is not valid.")
