import os
import tarfile
import tempfile
import paramiko
import time

SERVER_IP = "192.168.0.182"
SERVER_USER = "server"
SERVER_PASS = "1"

LOCAL_STUDIO_DIR = r"D:\down1\jun\stitch_madenmore_3d_creative_studio\stitch_madenmore_3d_creative_studio"
LOCAL_MADENMORE_DIR = r"D:\Siddhant\projects\MadeNMore"
LOCAL_HOMELAB_DIST = r"D:\Siddhant\projects\HomeLab OS\frontend\dist"

def make_studio_tarball(output_tar_path):
    print("[*] Creating clean tarball for MadeNMore 3D Creative Studio (excluding cache & node_modules)...")
    def filter_tar(tarinfo):
        name = tarinfo.name
        if "node_modules" in name or ".git" in name or ".next" in name:
            return None
        return tarinfo
    
    with tarfile.open(output_tar_path, "w:gz") as tar:
        tar.add(LOCAL_STUDIO_DIR, arcname="stitch_madenmore_3d_creative_studio", filter=filter_tar)
    print(f"   [OK] Tarball created ({os.path.getsize(output_tar_path) / (1024*1024):.2f} MB)")

def make_madenmore_tarball(output_tar_path):
    print("[*] Creating tarball for MadeNMore Store & Persistence API...")
    def filter_tar(tarinfo):
        name = tarinfo.name
        if "node_modules" in name or ".git" in name:
            return None
        return tarinfo
    
    with tarfile.open(output_tar_path, "w:gz") as tar:
        tar.add(LOCAL_MADENMORE_DIR, arcname="MadeNMore", filter=filter_tar)
    print(f"   [OK] MadeNMore Tarball created ({os.path.getsize(output_tar_path) / (1024*1024):.2f} MB)")

def run_ssh(client, cmd, timeout=300):
    print(f"[*] Running remote: {cmd[:100]}...", flush=True)
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

def deploy():
    temp_dir = tempfile.gettempdir()
    studio_tar = os.path.join(temp_dir, "studio_app.tar.gz")
    madenmore_tar = os.path.join(temp_dir, "madenmore_app.tar.gz")
    
    make_studio_tarball(studio_tar)
    make_madenmore_tarball(madenmore_tar)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f"Connecting to remote server {SERVER_IP}...")
    client.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS)

    sftp = client.open_sftp()
    
    print("Uploading Studio Tarball to /home/server/studio_app.tar.gz...")
    sftp.put(studio_tar, "/home/server/studio_app.tar.gz")
    
    print("Uploading MadeNMore Tarball to /home/server/madenmore_app.tar.gz...")
    sftp.put(madenmore_tar, "/home/server/madenmore_app.tar.gz")

    print("Uploading start_web_services.sh...")
    with sftp.file('/home/server/start_web_services.sh', 'w') as f:
        f.write(STARTUP_SCRIPT)
    sftp.chmod('/home/server/start_web_services.sh', 0o755)
    sftp.close()

    # Extract MadeNMore
    run_ssh(client, "mkdir -p /home/server/apps && tar -xzf /home/server/madenmore_app.tar.gz -C /home/server/apps/")
    run_ssh(client, "cd /home/server/apps/MadeNMore && npm install --production=false")

    # Extract Studio and install/build
    run_ssh(client, "mkdir -p /home/server/apps/Stitch3DStudio && tar -xzf /home/server/studio_app.tar.gz -C /home/server/apps/Stitch3DStudio/")
    run_ssh(client, "cd /home/server/apps/Stitch3DStudio/stitch_madenmore_3d_creative_studio && npm install && npm run build")

    # Create desktop shortcuts
    shortcuts_script = """
cat << 'EOF' > /home/server/Desktop/MadeNMore-3D-Store.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=MadeNMore 3D Store
Comment=Open MadeNMore 3D Print Store & Inventory
Exec=xdg-open http://192.168.0.183
Icon=applications-internet
Terminal=false
Categories=Network;WebBrowser;
EOF

cat << 'EOF' > /home/server/Desktop/MadeNMore-3D-Studio.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=MadeNMore 3D Studio
Comment=Open MadeNMore 3D Creative Studio Next.js App
Exec=xdg-open http://192.168.0.185
Icon=applications-graphics
Terminal=false
Categories=Network;WebBrowser;
EOF

chmod +x /home/server/Desktop/*.desktop || true
"""
    run_ssh(client, shortcuts_script)

    # Launch services
    print("[*] Launching all updated services...")
    run_ssh(client, "bash /home/server/start_web_services.sh")

    client.close()
    
    if os.path.exists(studio_tar):
        os.remove(studio_tar)
    if os.path.exists(madenmore_tar):
        os.remove(madenmore_tar)

    print("\n[OK] Deployment completed successfully!")

if __name__ == "__main__":
    deploy()
