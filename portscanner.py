import socket
import termcolor

def scan(target, ports):
    print('\n' + termcolor.colored(f"Starting Scan For {target}", 'blue'))
    for port in range(1, ports + 1):
        scan_port(target, port)

def scan_port(ipaddress, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  
        sock.connect((ipaddress, port))
        print(termcolor.colored(f"[+] Port {port} is Open on {ipaddress}", 'green'))
        sock.close()
    except:
        pass  


if __name__ == "__main__":
    target = input("[*] Enter Target(s) to Scan (split them using commas): ").strip()
    ports = int(input("[*] Enter number of ports to scan: "))

    if ',' in target:
        print(termcolor.colored("[*] Scanning multiple targets", 'green'))
        for ip_addr in target.split(','):
            scan(ip_addr.strip(), ports)
    else:
        scan(target, ports)
