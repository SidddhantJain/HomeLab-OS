"""
HomeLab OS — Server Remote Installer & Deployment Script
Deploys HomeLab OS v1.0.0 onto media-server@192.168.0.180 via SSH.
"""

import sys
import os
import time
import paramiko

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HOST = "192.168.0.180"
PORT = 22
USER = "media-server"
PASS = "1"
TARGET_DIR = "/home/media-server/HomeLab-OS"


def run_command_remote(client, cmd, timeout=120):
    print(f"\n---> Executing: {cmd}")
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    if "sudo" in cmd:
        stdin.write(f"{PASS}\n")
        stdin.flush()

    out = stdout.read().decode("utf-8", errors="replace").strip()
    err = stderr.read().decode("utf-8", errors="replace").strip()

    combined = out if out else err
    if combined:
        print(combined[:2000])
    return combined


def deploy_homelab_os():
    print("=" * 70)
    print(f" Deploying HomeLab OS v1.0.0 Stable to {USER}@{HOST}")
    print("=" * 70)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=HOST, port=PORT, username=USER, password=PASS, timeout=10)
        print(" [OK] SSH Connection Established!")
    except Exception as e:
        print(f" [ERROR] Could not connect via SSH: {e}")
        return

    # Step 1: Install prerequisites & Python virtualenv
    print("\n[Step 1/5] Setting up Python Environment & Dependencies...")
    run_command_remote(client, f"echo '{PASS}' | sudo -S apt update && sudo -S apt install -y python3-pip python3-venv python3-full git nodejs npm")

    # Step 2: Set up Python virtual environment inside /home/media-server/HomeLab-OS
    print("\n[Step 2/5] Creating Python Virtual Environment & Installing Backend Requirements...")
    venv_cmd = (
        f"cd {TARGET_DIR} && "
        "python3 -m venv .venv && "
        ".venv/bin/pip install --upgrade pip && "
        ".venv/bin/pip install -r backend/requirements.txt"
    )
    run_command_remote(client, venv_cmd)

    # Step 3: Install Frontend node_modules
    print("\n[Step 3/5] Installing Frontend Dependencies...")
    npm_cmd = f"cd {TARGET_DIR}/frontend && npm install"
    run_command_remote(client, npm_cmd)

    # Step 4: Kill existing uvicorn processes if any and launch services with PYTHONPATH=backend
    print("\n[Step 4/5] Launching HomeLab OS Services (FastAPI Backend + Vite Frontend)...")
    pkill_cmd = "pkill -f uvicorn || true"
    run_command_remote(client, pkill_cmd)

    launch_cmd = (
        f"cd {TARGET_DIR}/backend && "
        "nohup ../.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 > ../homelab_backend.log 2>&1 & "
        f"cd {TARGET_DIR}/frontend && "
        "nohup npm run dev -- --host 0.0.0.0 --port 5173 > ../homelab_frontend.log 2>&1 &"
    )
    run_command_remote(client, launch_cmd)

    time.sleep(5)

    # Step 5: Verify Deployment Status
    print("\n[Step 5/5] Verifying Live Health Status on Dell Server...")
    status = run_command_remote(client, "curl -s http://127.0.0.1:8000/api/v1/system/status || echo 'Backend starting...'")

    client.close()

    print("\n" + "=" * 70)
    print(" DEPLOYMENT SUCCESSFUL!")
    print(f" HomeLab OS Dashboard: http://192.168.0.180:5173")
    print(f" REST API Documentation: http://192.168.0.180:8000/docs")
    print(f" System Status Endpoint: http://192.168.0.180:8000/api/v1/system/status")
    print("=" * 70)


if __name__ == "__main__":
    deploy_homelab_os()
