import paramiko
import os

SERVER_IP = "192.168.0.182"
SERVER_USER = "server"
SERVER_PASS = "1"

LOCAL_HOMELAB_DIST = r"D:\Siddhant\projects\HomeLab OS\frontend\dist"
REMOTE_HOMELAB_DIST = "/home/server/HomeLab-OS/frontend/dist"

LOCAL_MADENMORE_DIST = r"D:\Siddhant\projects\MadeNMore\dist"
REMOTE_MADENMORE_DIST = "/home/server/apps/MadeNMore/dist"

SCRIPT_CONTENT = """#!/bin/bash
# 1. Bind Virtual IP Aliases & restart Nginx
bash /home/server/setup_virtual_ips.sh
echo 1 | sudo -S systemctl restart nginx || true

# 2. Terminate legacy instances
pkill -9 -f uvicorn || true
pkill -9 -f "node server/api.js" || true
pkill -9 -f "next-server" || true
pkill -9 -f "next start" || true
pkill -9 -f next || true
pkill -9 -f "http.server 5173" || true
pkill -9 -f "http.server 5174" || true
pkill -9 -f "http.server 5175" || true
sleep 1

# 3. Start Backend FastAPI APIs
nohup /home/server/HomeLab-OS/.venv/bin/python3 -m uvicorn app.main:app --app-dir /home/server/HomeLab-OS/backend --host 0.0.0.0 --port 8000 >/home/server/homelab_backend.log 2>&1 &
nohup /home/server/apps/FiscalFlow/backend/.venv/bin/python3 -m uvicorn app.main:app --app-dir /home/server/apps/FiscalFlow/backend --host 0.0.0.0 --port 8081 >/home/server/fiscal.log 2>&1 &

# 4. Start Frontends & Full Apps
nohup python3 -m http.server 5173 --bind 0.0.0.0 --directory /home/server/HomeLab-OS/frontend/dist >/home/server/homelab_frontend.log 2>&1 &

cd /home/server/apps/MadeNMore
nohup env PORT=5174 node server/api.js >/home/server/madenmore.log 2>&1 &
nohup env PORT=4000 node server/api.js >/home/server/madenmore_api.log 2>&1 &

cd /home/server/apps/Stitch3DStudio/stitch_madenmore_3d_creative_studio
nohup npx next start -p 5175 -H 0.0.0.0 >/home/server/stitch3d.log 2>&1 &
"""

def upload_dir(sftp, local_dir, remote_dir):
    try:
        sftp.mkdir(remote_dir)
    except IOError:
        pass
    
    for item in os.listdir(local_dir):
        local_path = os.path.join(local_dir, item)
        remote_path = remote_dir + '/' + item
        if os.path.isdir(local_path):
            upload_dir(sftp, local_path, remote_path)
        else:
            sftp.put(local_path, remote_path)

def deploy_bundles():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Connecting to SSH server 192.168.0.182...")
    client.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS)

    sftp = client.open_sftp()
    
    print("Uploading HomeLab OS production dist...")
    upload_dir(sftp, LOCAL_HOMELAB_DIST, REMOTE_HOMELAB_DIST)
    
    print("Uploading MadeNMore production dist...")
    upload_dir(sftp, LOCAL_MADENMORE_DIST, REMOTE_MADENMORE_DIST)

    print("Updating /home/server/start_web_services.sh...")
    with sftp.file('/home/server/start_web_services.sh', 'w') as f:
        f.write(SCRIPT_CONTENT)
    sftp.chmod('/home/server/start_web_services.sh', 0o755)
    sftp.close()

    print("Launching production web services...")
    stdin, stdout, stderr = client.exec_command("bash /home/server/start_web_services.sh")
    out_str = stdout.read().decode('utf-8', 'ignore')
    err_str = stderr.read().decode('utf-8', 'ignore')
    print("OUT:\n", out_str.encode('ascii', 'replace').decode('ascii'))
    if err_str:
        print("ERR:\n", err_str.encode('ascii', 'replace').decode('ascii'))
    client.close()

if __name__ == "__main__":
    deploy_bundles()
