import paramiko

SERVER_IP = "192.168.0.182"
SERVER_USER = "server"
SERVER_PASS = "1"

NGINX_CONF = """# HomeLab OS Multi-App Unified Nginx Routing & Virtual IP Configuration

# 1. Primary HomeLab OS Portal (192.168.0.182 & Default Fallback)
server {
    listen 80 default_server;
    listen 192.168.0.182:80;
    server_name 192.168.0.182 homelab.local _;

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

# 2. MadeNMore 3D Print Store & Inventory (Dedicated VIP 192.168.0.183)
server {
    listen 192.168.0.183:80;
    server_name 192.168.0.183 store.madenmore.local;

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
    listen 192.168.0.184:80;
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
    listen 192.168.0.185:80;
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

SETUP_VIP_SH = """#!/bin/bash
IFACE=$(ip route | grep default | awk '{print $5}' | head -n 1)
if [ -z "$IFACE" ]; then
  IFACE="wlx98ded016af8f"
fi

echo "Setting up Virtual IP aliases on interface: $IFACE..."
echo 1 | sudo -S sysctl -w net.ipv4.ip_forward=1 net.ipv4.conf.all.arp_ignore=0 net.ipv4.conf.all.arp_announce=0 >/dev/null 2>&1 || true

for ip in 183 184 185 186 187; do
  echo 1 | sudo -S ip addr add 192.168.0.$ip/24 dev "$IFACE" 2>/dev/null || true
  which arping >/dev/null 2>&1 && arping -c 1 -U -I "$IFACE" "192.168.0.$ip" >/dev/null 2>&1 || true
done

echo "Active IPs on $IFACE:"
ip addr show "$IFACE" | grep "inet "
"""

def update_nginx_and_vips():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS)

    sftp = client.open_sftp()
    
    print("[*] Uploading /home/server/setup_virtual_ips.sh...")
    with sftp.file('/home/server/setup_virtual_ips.sh', 'w') as f:
        f.write(SETUP_VIP_SH)
    sftp.chmod('/home/server/setup_virtual_ips.sh', 0o755)

    print("[*] Uploading /home/server/homelab_vip.conf...")
    with sftp.file('/home/server/homelab_vip.conf', 'w') as f:
        f.write(NGINX_CONF)
    sftp.close()

    print("[*] Installing Nginx configuration...")
    stdin, stdout, stderr = client.exec_command("echo 1 | sudo -S cp /home/server/homelab_vip.conf /etc/nginx/conf.d/homelab_vip.conf && bash /home/server/setup_virtual_ips.sh && echo 1 | sudo -S nginx -t && echo 1 | sudo -S systemctl restart nginx")
    out = stdout.read().decode('utf-8', 'ignore')
    err = stderr.read().decode('utf-8', 'ignore')
    print("OUT:\n", out.encode('ascii', 'replace').decode('ascii'))
    if err:
        print("ERR:\n", err.encode('ascii', 'replace').decode('ascii'))

    client.close()
    print("[OK] Nginx & Virtual IPs updated successfully!")

if __name__ == "__main__":
    update_nginx_and_vips()
