import os
import sys
import time
import requests
import paramiko

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SERVER_IP = "192.168.0.182"
SERVER_USER = "server"
SERVER_PASS = "1"
REMOTE_HOMELAB_DIR = "/home/server/HomeLab-OS"

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
pkill -9 -f "serve_spa.py" || true
pkill -9 -f "http.server" || true
pkill -9 -f "5173" || true
sleep 1

# 3. Start HomeLab OS Core Backend (Port 8000)
nohup /home/server/HomeLab-OS/.venv/bin/python3 -m uvicorn app.main:app --app-dir /home/server/HomeLab-OS/backend --host 0.0.0.0 --port 8000 >/home/server/homelab_backend.log 2>&1 &

# 4. Start FiscalFlow Backend (Port 8081 / VIP 192.168.0.184)
nohup /home/server/apps/FiscalFlow/backend/.venv/bin/python3 -m uvicorn app.main:app --app-dir /home/server/apps/FiscalFlow/backend --host 0.0.0.0 --port 8081 >/home/server/fiscal.log 2>&1 &

# 5. Start HomeLab OS Production SPA Frontend (Port 5173 / VIP 192.168.0.182)
nohup python3 /home/server/HomeLab-OS/frontend/serve_spa.py 5173 /home/server/HomeLab-OS/frontend/dist >/home/server/homelab_frontend.log 2>&1 &

# 6. Start MadeNMore 3D Store & Persistence API Server (Port 5174 / VIP 192.168.0.183 & Port 4000)
cd /home/server/apps/MadeNMore
nohup env PORT=5174 node server/api.js >/home/server/madenmore.log 2>&1 &
nohup env PORT=4000 node server/api.js >/home/server/madenmore_api.log 2>&1 &

# 7. Start MadeNMore 3D Creative Studio Next.js 16 Web Application (Port 5175 / VIP 192.168.0.185)
cd /home/server/apps/Stitch3DStudio/stitch_madenmore_3d_creative_studio
nohup npx next start -p 5175 -H 0.0.0.0 >/home/server/stitch3d.log 2>&1 &

echo "All HomeLab OS services and web applications successfully launched!"
"""

def upload_directory_sftp(sftp, local_dir, remote_dir):
    for root, dirs, files in os.walk(local_dir):
        rel_path = os.path.relpath(root, local_dir).replace('\\', '/')
        target_dir = remote_dir if rel_path == '.' else f"{remote_dir}/{rel_path}"
        try:
            sftp.stat(target_dir)
        except IOError:
            sftp.mkdir(target_dir)
        
        for file in files:
            local_file = os.path.join(root, file)
            remote_file = f"{target_dir}/{file}"
            sftp.put(local_file, remote_file)

def deploy_and_test():
    print("=" * 70)
    print(" HomeLab OS — Deploying SPA Routing Fix & Syncing to Server")
    print("=" * 70)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS)

    sftp = client.open_sftp()

    print("[1/5] Uploading frontend/serve_spa.py...")
    sftp.put("frontend/serve_spa.py", f"{REMOTE_HOMELAB_DIR}/frontend/serve_spa.py")
    sftp.chmod(f"{REMOTE_HOMELAB_DIR}/frontend/serve_spa.py", 0o755)

    print("[2/5] Uploading backend...")
    upload_directory_sftp(sftp, "backend", f"{REMOTE_HOMELAB_DIR}/backend")

    print("[3/5] Syncing frontend/dist...")
    upload_directory_sftp(sftp, "frontend/dist", f"{REMOTE_HOMELAB_DIR}/frontend/dist")

    print("[4/5] Updating startup scripts on server...")
    with sftp.file("/home/server/start_web_services.sh", "w") as f:
        f.write(STARTUP_SCRIPT)
    sftp.chmod("/home/server/start_web_services.sh", 0o755)
    sftp.close()

    print("[5/5] Restarting services on server...")
    stdin, stdout, stderr = client.exec_command("bash /home/server/start_web_services.sh")
    out = stdout.read().decode('utf-8', 'replace').strip()
    err = stderr.read().decode('utf-8', 'replace').strip()
    print("OUTPUT:\n", out)
    if err:
        print("ERRORS:\n", err)

    time.sleep(3)

    # Check permissions
    client.exec_command("echo 1 | sudo -S chmod 755 /home/server && echo 1 | sudo -S chmod -R 755 /home/server/HomeLab-OS/frontend/dist")

    client.close()

    print("\n" + "=" * 70)
    print(" VERIFYING ALL URLS FROM CLIENT MACHINE")
    print("=" * 70)

    test_urls = [
        ("HomeLab OS Direct Port 5173 (Base)", "http://192.168.0.182:5173/"),
        ("HomeLab OS Direct Port 5173 (/login SPA)", "http://192.168.0.182:5173/login"),
        ("HomeLab OS Direct Port 5173 (/server-management SPA)", "http://192.168.0.182:5173/server-management"),
        ("HomeLab OS VIP 182 (Base)", "http://192.168.0.182/"),
        ("HomeLab OS VIP 182 (/login SPA)", "http://192.168.0.182/login"),
        ("HomeLab OS API (Status)", "http://192.168.0.182:8000/api/v1/system/status"),
        ("MadeNMore Store (VIP 192.168.0.183)", "http://192.168.0.183/"),
        ("MadeNMore Store Direct Port 5174", "http://192.168.0.182:5174/"),
        ("MadeNMore API (Port 4000)", "http://192.168.0.182:4000/api/all"),
        ("FiscalFlow (VIP 192.168.0.184)", "http://192.168.0.184/"),
        ("MadeNMore 3D Studio (VIP 192.168.0.185)", "http://192.168.0.185/"),
        ("MadeNMore 3D Studio Direct Port 5175", "http://192.168.0.182:5175/"),
    ]

    all_passed = True
    for label, url in test_urls:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                print(f" [PASS - 200 OK] {label} -> {url} ({len(r.content)} bytes)")
            else:
                print(f" [WARN - {r.status_code}] {label} -> {url}")
                all_passed = False
        except Exception as ex:
            print(f" [FAIL] {label} -> {url} : {ex}")
            all_passed = False

    if all_passed:
        print("\n🎉 ALL SERVICES, SPAs, AND VIP URLS ARE FULLY VERIFIED & WORKING!")

if __name__ == "__main__":
    deploy_and_test()
