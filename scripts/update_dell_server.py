import paramiko
import time

HOST = "192.168.0.180"
PORT = 22
USER = "media-server"
PASS = "1"
TARGET_DIR = "/home/media-server/HomeLab-OS"

print("=" * 70)
print(f" Updating HomeLab OS to v1.5.0 on {USER}@{HOST}")
print("=" * 70)

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=HOST, port=PORT, username=USER, password=PASS)

# 1. Git pull latest code from origin/main
print("\n[Step 1/3] Fetching latest code from GitHub (origin/main)...")
cmd_git = f"cd {TARGET_DIR} && git fetch --all && git reset --hard origin/main"
stdin, stdout, stderr = client.exec_command(cmd_git)
print(stdout.read().decode())
print(stderr.read().decode())

# 2. Restart systemd services
print("\n[Step 2/3] Restarting homelab-backend and homelab-frontend systemd services...")
cmd_restart = f"echo '{PASS}' | sudo -S systemctl restart homelab-backend homelab-frontend"
stdin, stdout, stderr = client.exec_command(cmd_restart)
stdin.write(f"{PASS}\n")
stdin.flush()
print(stdout.read().decode())

time.sleep(3)

# 3. Verify server status
print("\n[Step 3/3] Verifying server health status after update...")
stdin, stdout, stderr = client.exec_command("curl -s http://127.0.0.1:8000/api/v1/system/status")
res = stdout.read().decode().strip()
print("Response:", res)

client.close()

print("\n" + "=" * 70)
print(" SERVER UPDATE TO v1.5.0 SUCCESSFUL!")
print("=" * 70)
