import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname="192.168.0.180", port=22, username="media-server", password="1")

print("Running uvicorn directly over SSH...")
stdin, stdout, stderr = client.exec_command("cd /home/media-server/HomeLab-OS/backend && ../.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload", timeout=10)

try:
    print(stdout.read().decode())
    print(stderr.read().decode())
except Exception as e:
    print("Output:", e)

client.close()
