import paramiko
import time

HOST = "192.168.0.180"
USER = "media-server"
PASS = "1"
TARGET_DIR = "/home/media-server/HomeLab-OS"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=HOST, port=22, username=USER, password=PASS)

# Create systemd service for homelab backend
systemd_unit = f"""[Unit]
Description=HomeLab OS FastAPI Backend Service
After=network.target

[Service]
Type=simple
User={USER}
WorkingDirectory={TARGET_DIR}/backend
ExecStart={TARGET_DIR}/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
"""

print("Writing systemd service file for HomeLab OS backend...")
cmd_write = f"echo '{systemd_unit}' | sudo -S tee /etc/systemd/system/homelab-backend.service"
stdin, stdout, stderr = client.exec_command(cmd_write)
stdin.write(f"{PASS}\n")
stdin.flush()
print(stdout.read().decode())

print("Enabling and starting homelab-backend service...")
cmd_enable = f"echo '{PASS}' | sudo -S systemctl daemon-reload && sudo -S systemctl enable --now homelab-backend"
stdin, stdout, stderr = client.exec_command(cmd_enable)
stdin.write(f"{PASS}\n")
stdin.flush()
print(stdout.read().decode())

time.sleep(3)

print("Checking service status...")
stdin, stdout, stderr = client.exec_command("sudo systemctl status homelab-backend")
stdin.write(f"{PASS}\n")
stdin.flush()
print(stdout.read().decode())

client.close()
