import paramiko
import time

HOST = "192.168.0.180"
USER = "media-server"
PASS = "1"
TARGET_DIR = "/home/media-server/HomeLab-OS"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=HOST, port=22, username=USER, password=PASS)

# 1. Backend Service
backend_unit = f"""[Unit]
Description=HomeLab OS FastAPI Backend Engine
After=network.target

[Service]
Type=simple
User={USER}
WorkingDirectory={TARGET_DIR}/backend
Environment="PYTHONPATH={TARGET_DIR}/backend"
Environment="DATABASE_URL=sqlite:///{TARGET_DIR}/backend/homelab.db"
ExecStart={TARGET_DIR}/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
"""

# 2. Frontend Service
frontend_unit = f"""[Unit]
Description=HomeLab OS React Vite UI Dashboard
After=network.target homelab-backend.service

[Service]
Type=simple
User={USER}
WorkingDirectory={TARGET_DIR}/frontend
ExecStart=/usr/bin/npm run dev -- --host 0.0.0.0 --port 5173
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
"""

print("Installing homelab-backend.service...")
cmd1 = f"echo '{backend_unit}' | sudo -S tee /etc/systemd/system/homelab-backend.service"
stdin, stdout, stderr = client.exec_command(cmd1)
stdin.write(f"{PASS}\n")
stdin.flush()
stdout.read()

print("Installing homelab-frontend.service...")
cmd2 = f"echo '{frontend_unit}' | sudo -S tee /etc/systemd/system/homelab-frontend.service"
stdin, stdout, stderr = client.exec_command(cmd2)
stdin.write(f"{PASS}\n")
stdin.flush()
stdout.read()

print("Reloading systemd daemon and enabling services on boot...")
cmd3 = f"echo '{PASS}' | sudo -S systemctl daemon-reload && sudo -S systemctl enable --now homelab-backend homelab-frontend"
stdin, stdout, stderr = client.exec_command(cmd3)
stdin.write(f"{PASS}\n")
stdin.flush()
stdout.read()

time.sleep(3)

print("Checking systemd status...")
stdin, stdout, stderr = client.exec_command("sudo systemctl status homelab-backend --no-pager")
stdin.write(f"{PASS}\n")
stdin.flush()
print("--- Backend Service Status ---")
print(stdout.read().decode())

stdin, stdout, stderr = client.exec_command("sudo systemctl status homelab-frontend --no-pager")
stdin.write(f"{PASS}\n")
stdin.flush()
print("--- Frontend Service Status ---")
print(stdout.read().decode())

client.close()
