import paramiko
import time

HOST = "192.168.0.180"
USER = "media-server"
PASS = "1"
TARGET_DIR = "/home/media-server/HomeLab-OS"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=HOST, port=22, username=USER, password=PASS)

print("Stopping any previous running instances...")
client.exec_command("pkill -f uvicorn; pkill -f vite")
time.sleep(1)

print("Starting FastAPI Backend (Port 8000) with SQLite storage...")
launch_backend = (
    f"cd {TARGET_DIR}/backend && "
    f"export PYTHONPATH={TARGET_DIR}/backend && "
    "export DATABASE_URL=sqlite:///./homelab.db && "
    f"nohup {TARGET_DIR}/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 > {TARGET_DIR}/homelab_backend.log 2>&1 < /dev/null &"
)
client.exec_command(launch_backend)

print("Starting React Frontend (Port 5173)...")
launch_frontend = (
    f"cd {TARGET_DIR}/frontend && "
    f"nohup npm run dev -- --host 0.0.0.0 --port 5173 > {TARGET_DIR}/homelab_frontend.log 2>&1 < /dev/null &"
)
client.exec_command(launch_frontend)

time.sleep(4)

print("Reading backend log...")
stdin, stdout, stderr = client.exec_command(f"cat {TARGET_DIR}/homelab_backend.log")
print("--- Backend Log ---")
print(stdout.read().decode())

print("Testing status API endpoint...")
stdin, stdout, stderr = client.exec_command("curl -s http://127.0.0.1:8000/api/v1/system/status")
print("--- Status API Response ---")
print(stdout.read().decode())

client.close()
