import paramiko
import time

HOST = "192.168.0.180"
USER = "media-server"
PASS = "1"
TARGET_DIR = "/home/media-server/HomeLab-OS"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=HOST, port=22, username=USER, password=PASS)

print("Killing old processes...")
client.exec_command("pkill -f uvicorn; pkill -f vite")
time.sleep(1)

print("Starting FastAPI Backend (Port 8000)...")
backend_cmd = f"cd {TARGET_DIR}/backend && nohup ../.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 > ../homelab_backend.log 2>&1 < /dev/null &"
client.exec_command(backend_cmd)

print("Starting React Frontend (Port 5173)...")
frontend_cmd = f"cd {TARGET_DIR}/frontend && nohup npm run dev -- --host 0.0.0.0 --port 5173 > ../homelab_frontend.log 2>&1 < /dev/null &"
client.exec_command(frontend_cmd)

time.sleep(4)

print("Checking remote backend status...")
stdin, stdout, stderr = client.exec_command("curl -s http://127.0.0.1:8000/api/v1/system/status")
res = stdout.read().decode().strip()
print("Response:", res if res else "Starting...")

client.close()
