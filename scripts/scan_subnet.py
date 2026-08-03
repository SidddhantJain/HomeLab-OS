import socket
import concurrent.futures

def check_ip(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    res = s.connect_ex((ip, 22))
    s.close()
    if res == 0:
        return ip
    return None

print("Scanning LAN subnet 192.168.0.x for SSH port 22...")
active_ips = []
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    futures = [executor.submit(check_ip, f"192.168.0.{i}") for i in range(100, 255)]
    for f in concurrent.futures.as_completed(futures):
        ip = f.result()
        if ip:
            active_ips.append(ip)
            print(f" [FOUND] Active SSH host at: {ip}")

if not active_ips:
    print(" No active SSH hosts found on 192.168.0.x subnet.")
