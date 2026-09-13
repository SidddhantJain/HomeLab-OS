import os
import tarfile
import tempfile
import paramiko
import time
import urllib.request

SERVER_IP = "192.168.0.182"
SERVER_USER = "server"
SERVER_PASS = "1"

LOCAL_HOMELAB_DIR = r"d:\Siddhant\projects\HomeLab OS"

def make_homelab_tarball(output_tar_path):
    print("[*] Creating clean HomeLab OS tarball...")
    def filter_tar(tarinfo):
        name = tarinfo.name
        if any(x in name for x in ["node_modules", ".venv", "__pycache__", ".git", ".idea", ".vscode", ".pytest_cache", ".next"]):
            return None
        return tarinfo
    
    with tarfile.open(output_tar_path, "w:gz") as tar:
        tar.add(LOCAL_HOMELAB_DIR, arcname="HomeLab-OS", filter=filter_tar)
    print(f"   [OK] HomeLab OS Tarball created ({os.path.getsize(output_tar_path) / (1024*1024):.2f} MB)")

def run_ssh(client, cmd, timeout=300):
    print(f"[*] Executing remote: {cmd[:100]}...", flush=True)
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', 'ignore')
    err = stderr.read().decode('utf-8', 'ignore')
    if out.strip():
        print(out[:500].encode('ascii', 'replace').decode('ascii'))
    if err.strip():
        print("ERR:", err[:300].encode('ascii', 'replace').decode('ascii'))
    return out, err

STARTUP_SCRIPT = """#!/bin/bash
# HomeLab OS Multi-App Unified Service Launcher
# 1. Bind Virtual IP Aliases & Restart Nginx
bash /home/server/setup_virtual_ips.sh
echo 1 | sudo -S systemctl restart nginx || true

# 2. Terminate legacy background processes
pkill -9 -f uvicorn || true
pkill -9 -f "node server/api.js" || true
pkill -9 -f "next-server" || true
pkill -9 -f "next start" || true
pkill -9 -f next || true
pkill -9 -f "http.server 5173" || true
pkill -9 -f "http.server 5174" || true
pkill -9 -f "http.server 5175" || true
sleep 1

# 3. Start HomeLab OS Core Backend (Port 8000)
nohup /home/server/HomeLab-OS/.venv/bin/python3 -m uvicorn app.main:app --app-dir /home/server/HomeLab-OS/backend --host 0.0.0.0 --port 8000 >/home/server/homelab_backend.log 2>&1 &

# 4. Start FiscalFlow Backend (Port 8081 / VIP 192.168.0.184)
nohup /home/server/apps/FiscalFlow/backend/.venv/bin/python3 -m uvicorn app.main:app --app-dir /home/server/apps/FiscalFlow/backend --host 0.0.0.0 --port 8081 >/home/server/fiscal.log 2>&1 &

# 5. Start HomeLab OS Production Frontend (Port 5173 / VIP 192.168.0.182)
nohup python3 -m http.server 5173 --bind 0.0.0.0 --directory /home/server/HomeLab-OS/frontend/dist >/home/server/homelab_frontend.log 2>&1 &

# 6. Start MadeNMore 3D Store & Persistence API Server (Port 5174 / VIP 192.168.0.183 & Port 4000)
cd /home/server/apps/MadeNMore
nohup env PORT=5174 node server/api.js >/home/server/madenmore.log 2>&1 &
nohup env PORT=4000 node server/api.js >/home/server/madenmore_api.log 2>&1 &

# 7. Start MadeNMore 3D Creative Studio Next.js 16 Web Application (Port 5175 / VIP 192.168.0.185)
cd /home/server/apps/Stitch3DStudio/stitch_madenmore_3d_creative_studio
nohup npx next start -p 5175 -H 0.0.0.0 >/home/server/stitch3d.log 2>&1 &

echo "All HomeLab OS services and web applications successfully launched!"
"""

SYSTEMD_UNIT = """[Unit]
Description=HomeLab OS Unified Multi-App Daemon
After=network.target network-online.target nginx.service
Wants=network-online.target

[Service]
Type=forking
User=server
Group=server
WorkingDirectory=/home/server
ExecStart=/bin/bash /home/server/start_web_services.sh
Restart=on-failure
RestartSec=5s
KillMode=process
TimeoutSec=60

[Install]
WantedBy=multi-user.target
"""

DESKTOP_SHORTCUTS = """
mkdir -p /home/server/Desktop

cat << 'EOF' > /home/server/Desktop/HomeLab-OS-Manager.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=HomeLab OS Desktop Manager
Comment=Launch HomeLab OS Native Server-Side Management Console
Exec=bash -c 'cd /home/server/HomeLab-OS && .venv/bin/python manager/main.py'
Icon=utilities-system-monitor
Path=/home/server/HomeLab-OS
Terminal=false
Categories=System;Management;Settings;
EOF

cat << 'EOF' > /home/server/Desktop/HomeLab-OS-Server.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=HomeLab OS Web Services Control
Comment=Restart and Manage All HomeLab OS Web Services & Virtual IPs
Exec=bash -c 'bash /home/server/start_web_services.sh; read -p "Press enter to exit..."'
Icon=network-server
Path=/home/server
Terminal=true
Categories=System;Management;
EOF

cat << 'EOF' > /home/server/Desktop/HomeLab-OS-Web.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=HomeLab OS Web Dashboard
Comment=Open HomeLab OS Web Platform
Exec=xdg-open http://192.168.0.182
Icon=applications-internet
Terminal=false
Categories=Network;WebBrowser;
EOF

cat << 'EOF' > /home/server/Desktop/MadeNMore-3D-Store.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=MadeNMore 3D Store
Comment=Open MadeNMore 3D Print Store & Inventory Management
Exec=xdg-open http://192.168.0.183
Icon=applications-internet
Terminal=false
Categories=Network;WebBrowser;
EOF

cat << 'EOF' > /home/server/Desktop/MadeNMore-3D-Studio.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=MadeNMore 3D Creative Studio
Comment=Open MadeNMore 3D Creative Studio Next.js 16 Web Application
Exec=xdg-open http://192.168.0.185
Icon=applications-graphics
Terminal=false
Categories=Network;WebBrowser;
EOF

cat << 'EOF' > /home/server/Desktop/FiscalFlow.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=FiscalFlow Wealth Platform
Comment=Open FiscalFlow Financial Platform
Exec=xdg-open http://192.168.0.184
Icon=accessories-calculator
Terminal=false
Categories=Network;WebBrowser;
EOF

chmod +x /home/server/Desktop/*.desktop || true
"""

def deploy():
    temp_dir = tempfile.gettempdir()
    tar_path = os.path.join(temp_dir, "homelab_os_update.tar.gz")
    
    make_homelab_tarball(tar_path)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f"Connecting to remote server {SERVER_IP}...")
    client.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS)

    sftp = client.open_sftp()
    
    print("Uploading HomeLab OS Tarball to /home/server/homelab_os_update.tar.gz...")
    sftp.put(tar_path, "/home/server/homelab_os_update.tar.gz")

    print("Uploading start_web_services.sh...")
    with sftp.file('/home/server/start_web_services.sh', 'w') as f:
        f.write(STARTUP_SCRIPT)
    sftp.chmod('/home/server/start_web_services.sh', 0o755)

    print("Uploading systemd unit...")
    with sftp.file('/home/server/homelab-os.service', 'w') as f:
        f.write(SYSTEMD_UNIT)

    sftp.close()

    # Extract update
    run_ssh(client, "tar -xzf /home/server/homelab_os_update.tar.gz -C /home/server/")
    
    # Configure dependencies
    run_ssh(client, "cd /home/server/HomeLab-OS && .venv/bin/pip install --upgrade pip && .venv/bin/pip install PySide6 psutil requests")

    # Install systemd service & enable on boot
    run_ssh(client, "echo 1 | sudo -S cp /home/server/homelab-os.service /etc/systemd/system/homelab-os.service && echo 1 | sudo -S systemctl daemon-reload && echo 1 | sudo -S systemctl enable homelab-os.service || true")

    # Setup crontab auto-startup fallback
    run_ssh(client, '(crontab -l 2>/dev/null | grep -v "start_web_services"; echo "@reboot sleep 5 && bash /home/server/start_web_services.sh >/home/server/autostart.log 2>&1") | crontab -')

    # Configure desktop shortcuts
    run_ssh(client, DESKTOP_SHORTCUTS)

    # Launch services
    print("[*] Launching all updated services...")
    run_ssh(client, "bash /home/server/start_web_services.sh")

    client.close()
    
    if os.path.exists(tar_path):
        os.remove(tar_path)

    print("\n[OK] Server update completed successfully!")

if __name__ == "__main__":
    deploy()
