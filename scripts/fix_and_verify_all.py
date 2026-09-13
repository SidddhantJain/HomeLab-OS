import sys
import time
import requests
import paramiko

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SERVER_IP = "192.168.0.182"
SERVER_USER = "server"
SERVER_PASS = "1"

NGINX_CONF = """# HomeLab OS Multi-App Unified Nginx Routing & Virtual IP Configuration

# 1. Primary HomeLab OS Portal (192.168.0.182 & Default Fallback)
server {
    listen 80 default_server;
    server_name 192.168.0.182 homelab.local localhost "";

    root /home/server/HomeLab-OS/frontend/dist;
    index index.html;

    # SPA Client-Side Routing: fallback to index.html for /login, /server-management, etc.
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API Routing to FastAPI backend (Port 8000)
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /openapi.json {
        proxy_pass http://127.0.0.1:8000/openapi.json;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 2. MadeNMore 3D Print Store & Inventory (Dedicated VIP 192.168.0.186 & 192.168.0.183)
server {
    listen 80;
    server_name 192.168.0.186 192.168.0.183 store.madenmore.local;

    location / {
        proxy_pass http://127.0.0.1:5174;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /api/ {
        proxy_pass http://127.0.0.1:4000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

# 3. FiscalFlow Wealth Platform (Dedicated VIP 192.168.0.184)
server {
    listen 80;
    server_name 192.168.0.184 fiscalflow.local;

    location / {
        proxy_pass http://127.0.0.1:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

# 4. MadeNMore 3D Creative Studio Next.js 16 (Dedicated VIP 192.168.0.185)
server {
    listen 80;
    server_name 192.168.0.185 studio.madenmore.local;

    location / {
        proxy_pass http://127.0.0.1:5175;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
"""

SETUP_VIP_SERVICE = """[Unit]
Description=HomeLab OS Virtual IP Aliases (192.168.0.183-187)
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/home/server/setup_virtual_ips.sh

[Install]
WantedBy=multi-user.target
"""

SETUP_VIP_SH = """#!/bin/bash
IFACE=$(ip route | grep default | awk '{print $5}' | head -n 1)
if [ -z "$IFACE" ]; then
  IFACE="wlx98ded016af8f"
fi

echo "Configuring Virtual IP aliases on $IFACE..."
sysctl -w net.ipv4.ip_forward=1 net.ipv4.conf.all.arp_ignore=0 net.ipv4.conf.all.arp_announce=0 net.ipv4.ip_nonlocal_bind=1 >/dev/null 2>&1 || true

for ip in 183 184 185 186 187; do
  ip addr add 192.168.0.$ip/24 dev "$IFACE" 2>/dev/null || true
  which arping >/dev/null 2>&1 && arping -c 2 -U -I "$IFACE" "192.168.0.$ip" >/dev/null 2>&1 || true
done

echo "VIP setup complete on $IFACE."
"""

def fix_server():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS)

    def run(cmd):
        print(f"\n---> [CMD] {cmd}")
        stdin, stdout, stderr = client.exec_command(cmd)
        if 'sudo' in cmd:
            stdin.write('1\n')
            stdin.flush()
        out = stdout.read().decode('utf-8', 'replace').strip()
        err = stderr.read().decode('utf-8', 'replace').strip()
        if out:
            print("[OUT]\n" + out)
        if err:
            print("[ERR]\n" + err)
        return out

    # Step 1: Fix Permissions so www-data can read frontend/dist
    print("\n[Step 1] Fixing file permissions...")
    run("echo 1 | sudo -S chmod 755 /home/server")
    run("echo 1 | sudo -S chmod -R 755 /home/server/HomeLab-OS/frontend/dist")

    # Step 2: Install arping if missing
    print("\n[Step 2] Installing arping tool for gratuitous ARP...")
    run("echo 1 | sudo -S apt-get install -y arping iputils-arping || true")

    # Step 3: Upload Virtual IP setup script & service
    print("\n[Step 3] Setting up Virtual IP service...")
    sftp = client.open_sftp()
    with sftp.file('/home/server/setup_virtual_ips.sh', 'w') as f:
        f.write(SETUP_VIP_SH)
    sftp.chmod('/home/server/setup_virtual_ips.sh', 0o755)

    with sftp.file('/home/server/homelab_vip.conf', 'w') as f:
        f.write(NGINX_CONF)

    with sftp.file('/home/server/homelab-vip.service', 'w') as f:
        f.write(SETUP_VIP_SERVICE)
    sftp.close()

    run("echo 1 | sudo -S cp /home/server/homelab-vip.service /etc/systemd/system/homelab-vip.service")
    run("echo 1 | sudo -S systemctl daemon-reload")
    run("echo 1 | sudo -S systemctl enable --now homelab-vip.service")
    run("echo 1 | sudo -S bash /home/server/setup_virtual_ips.sh")

    # Step 4: Install and Reload Nginx
    print("\n[Step 4] Applying Nginx Configuration...")
    run("echo 1 | sudo -S rm -f /etc/nginx/sites-enabled/default")
    run("echo 1 | sudo -S cp /home/server/homelab_vip.conf /etc/nginx/conf.d/homelab_vip.conf")
    run("echo 1 | sudo -S nginx -t")
    run("echo 1 | sudo -S systemctl restart nginx")

    # Step 5: Test on remote localhost
    print("\n[Step 5] Testing endpoints locally on remote server...")
    run("curl -s -I http://127.0.0.1/login")
    run("curl -s -I http://127.0.0.1/server-management")
    run("curl -s -I http://192.168.0.182/login")
    run("curl -s -I http://192.168.0.183/")
    run("curl -s -I http://192.168.0.184/")
    run("curl -s -I http://192.168.0.185/")

    client.close()

    # Step 6: Test from this Windows machine
    print("\n[Step 6] Testing HTTP connectivity directly from client PC...")
    endpoints = [
        ("HomeLab OS (Base)", "http://192.168.0.182/"),
        ("HomeLab OS (Login SPA)", "http://192.168.0.182/login"),
        ("HomeLab OS (Server Management SPA)", "http://192.168.0.182/server-management"),
        ("HomeLab OS API (Status)", "http://192.168.0.182/api/v1/system/status"),
        ("HomeLab OS API (Services List)", "http://192.168.0.182/api/v1/services/list"),
        ("MadeNMore Store (VIP 192.168.0.183)", "http://192.168.0.183/"),
        ("FiscalFlow (VIP 192.168.0.184)", "http://192.168.0.184/"),
        ("MadeNMore 3D Studio (VIP 192.168.0.185)", "http://192.168.0.185/"),
        ("MadeNMore Direct Port 5174", "http://192.168.0.182:5174/"),
        ("MadeNMore 3D Studio Direct Port 5175", "http://192.168.0.182:5175/"),
    ]

    for name, url in endpoints:
        try:
            r = requests.get(url, timeout=5)
            status = "✅ OK" if r.status_code == 200 else f"⚠️ {r.status_code}"
            print(f"[{status}] {name} -> {url} (Status: {r.status_code}, Length: {len(r.content)} bytes)")
        except Exception as e:
            print(f"[❌ FAIL] {name} -> {url} ({e})")

if __name__ == "__main__":
    fix_server()
