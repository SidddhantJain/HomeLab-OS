import socket

target = "192.168.0.180"
ports = [22, 80, 443, 8000, 3000, 5173, 2222]

print(f"Scanning target {target}...")
for port in ports:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)
    result = s.connect_ex((target, port))
    if result == 0:
        print(f"  -> Port {port} is OPEN!")
    s.close()
