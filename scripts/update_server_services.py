import paramiko
import time

SERVER_IP = "192.168.0.182"
SERVER_USER = "server"
SERVER_PASS = "1"

SCRIPT_CONTENT = """#!/bin/bash
# Automatically bind Virtual IPs and Nginx proxy
bash /home/server/setup_virtual_ips.sh
echo 1 | sudo -S systemctl restart nginx || true

pkill -9 -f uvicorn || true
pkill -9 -f http.server || true
pkill -9 -f node || true
pkill -9 -f vite || true
sleep 1

nohup /home/server/HomeLab-OS/.venv/bin/python3 -m uvicorn app.main:app --app-dir /home/server/HomeLab-OS/backend --host 0.0.0.0 --port 8000 >/home/server/homelab_backend.log 2>&1 &
nohup /home/server/apps/FiscalFlow/backend/.venv/bin/python3 -m uvicorn app.main:app --app-dir /home/server/apps/FiscalFlow/backend --host 0.0.0.0 --port 8081 >/home/server/fiscal.log 2>&1 &
cd /home/server/HomeLab-OS/frontend && (nohup npm run dev -- --host 0.0.0.0 --port 5173 --strictPort >/home/server/homelab_frontend.log 2>&1 &)
nohup python3 -m http.server 5174 --bind 0.0.0.0 --directory /home/server/apps/MadeNMore/dist >/home/server/madenmore.log 2>&1 &
nohup python3 -m http.server 5175 --bind 0.0.0.0 --directory /home/server/apps/Stitch3DStudio/stitch_madenmore_3d_studio_website/madenmore_homepage >/home/server/stitch.log 2>&1 &
"""

SERVICE_CONTENT = """[Unit]
Description=HomeLab OS & Multi-App Web Services
After=network.target nginx.service

[Service]
Type=forking
User=server
WorkingDirectory=/home/server
ExecStart=/bin/bash /home/server/start_web_services.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
"""

def update_and_reboot():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Connecting to SSH server 192.168.0.182...")
    client.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS)

    sftp = client.open_sftp()
    
    # 1. Update start_web_services.sh
    print("1. Updating /home/server/start_web_services.sh...")
    with sftp.file('/home/server/start_web_services.sh', 'w') as f:
        f.write(SCRIPT_CONTENT)
    sftp.chmod('/home/server/start_web_services.sh', 0o755)

    # 2. Update systemd service
    print("2. Installing systemd auto-start service...")
    with sftp.file('/tmp/homelab-web.service', 'w') as f:
        f.write(SERVICE_CONTENT)
    sftp.close()

    setup_cmds = (
        "cd /home/server/HomeLab-OS && git fetch origin && git reset --hard origin/main && "
        "cd /home/server/HomeLab-OS/frontend && npm run build && "
        "echo 1 | sudo -S mv /tmp/homelab-web.service /etc/systemd/system/homelab-web.service && "
        "echo 1 | sudo -S systemctl daemon-reload && "
        "echo 1 | sudo -S systemctl enable homelab-web.service && "
        "(crontab -l 2>/dev/null | grep -v 'start_web_services.sh'; echo '@reboot /home/server/start_web_services.sh') | crontab - && "
        "echo 1 | sudo -S reboot"
    )

    print("3. Executing git pull, build, systemd enable, and server reboot command...")
    stdin, stdout, stderr = client.exec_command(setup_cmds)
    out_str = stdout.read().decode('utf-8', 'ignore')
    err_str = stderr.read().decode('utf-8', 'ignore')
    print("OUT:\n", out_str.encode('ascii', 'replace').decode('ascii'))
    if err_str:
        print("ERR:\n", err_str.encode('ascii', 'replace').decode('ascii'))

    print("Reboot command sent to remote server!")
    client.close()

if __name__ == "__main__":
    update_and_reboot()
