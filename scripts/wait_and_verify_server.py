import paramiko
import time
import urllib.request

SERVER_IP = "192.168.0.182"
SERVER_USER = "server"
SERVER_PASS = "1"

def wait_for_server():
    print("Waiting for remote Linux server 192.168.0.182 to finish rebooting...")
    start_time = time.time()
    while time.time() - start_time < 90:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS, timeout=3)
            print("[SSH ONLINE] Connected to Linux server!")

            # Check if /home/server/HomeLab-OS is a git repo or clone it
            cmd = (
                "if [ ! -d /home/server/HomeLab-OS/.git ]; then "
                "  echo 'Cloning repository into /home/server/HomeLab-OS...'; "
                "  rm -rf /home/server/HomeLab-OS_old; "
                "  mv /home/server/HomeLab-OS /home/server/HomeLab-OS_old 2>/dev/null || true; "
                "  git clone https://github.com/SidddhantJain/HomeLab-OS.git /home/server/HomeLab-OS; "
                "  cp -rn /home/server/HomeLab-OS_old/.venv /home/server/HomeLab-OS/ 2>/dev/null || true; "
                "fi && "
                "cd /home/server/HomeLab-OS && git fetch origin && git reset --hard origin/main && "
                "cd frontend && npm run build && "
                "bash /home/server/start_web_services.sh"
            )
            stdin, stdout, stderr = client.exec_command(cmd)
            out_str = stdout.read().decode('utf-8', 'ignore')
            err_str = stderr.read().decode('utf-8', 'ignore')
            print("DEPLOYMENT OUT:\n", out_str.encode('ascii', 'replace').decode('ascii'))
            if err_str:
                print("DEPLOYMENT ERR:\n", err_str.encode('ascii', 'replace').decode('ascii'))

            client.close()
            break
        except Exception as e:
            print(f"Waiting for SSH... ({e})")
            time.sleep(3)

if __name__ == "__main__":
    wait_for_server()
