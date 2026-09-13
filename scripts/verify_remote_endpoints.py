import paramiko
import urllib.request
import time

SERVER_IP = "192.168.0.182"
SERVER_USER = "server"
SERVER_PASS = "1"

def test_endpoints():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS)

    print("Launching services on remote server...")
    stdin, stdout, stderr = client.exec_command("bash /home/server/start_web_services.sh")
    out = stdout.read().decode('utf-8', 'ignore')
    print(out.encode('ascii', 'replace').decode('ascii'))
    
    time.sleep(5)

    print("\n--- Process List ---")
    stdin, stdout, stderr = client.exec_command("ps aux | grep -E 'node|uvicorn|next|http.server' | grep -v grep")
    out = stdout.read().decode('utf-8', 'ignore')
    print(out.encode('ascii', 'replace').decode('ascii'))

    print("\n--- Recent Logs ---")
    stdin, stdout, stderr = client.exec_command("tail -n 10 /home/server/madenmore.log /home/server/stitch3d.log /home/server/homelab_backend.log")
    out = stdout.read().decode('utf-8', 'ignore')
    print(out.encode('ascii', 'replace').decode('ascii'))
    client.close()

    endpoints = [
        ("HomeLab OS VIP (182)", "http://192.168.0.182/"),
        ("HomeLab OS Port 5173", "http://192.168.0.182:5173/"),
        ("HomeLab OS API (8000)", "http://192.168.0.182:8000/docs"),
        ("MadeNMore Store VIP (183)", "http://192.168.0.183/"),
        ("MadeNMore Store Port 5174", "http://192.168.0.182:5174/"),
        ("MadeNMore API (4000/all)", "http://192.168.0.182:4000/api/all"),
        ("FiscalFlow VIP (184)", "http://192.168.0.184/docs"),
        ("FiscalFlow Port 8081", "http://192.168.0.182:8081/docs"),
        ("MadeNMore Studio VIP (185)", "http://192.168.0.185/"),
        ("MadeNMore Studio Port 5175", "http://192.168.0.182:5175/"),
    ]

    print("\n--- Testing HTTP Endpoints from Local Host ---")
    for name, url in endpoints:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                print(f"   [OK] {name:30} -> {url} (HTTP {resp.getcode()})")
        except Exception as e:
            print(f"   [FAIL] {name:30} -> {url} : {e}")

if __name__ == "__main__":
    test_endpoints()
