import paramiko
import time

SERVER_IP = "192.168.0.182"
SERVER_USER = "server"
SERVER_PASS = "1"

def deploy_updates():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Connecting to SSH server 192.168.0.182...")
    client.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS)

    print("1. Pulling latest code from GitHub into /home/server/HomeLab-OS...")
    stdin, stdout, stderr = client.exec_command("cd /home/server/HomeLab-OS && git fetch origin && git reset --hard origin/main")
    print("GIT PULL OUT:\n", stdout.read().decode('utf-8', 'ignore').encode('ascii', 'replace').decode('ascii'))
    print("GIT PULL ERR:\n", stderr.read().decode('utf-8', 'ignore').encode('ascii', 'replace').decode('ascii'))

    print("2. Rebuilding frontend assets...")
    stdin, stdout, stderr = client.exec_command("cd /home/server/HomeLab-OS/frontend && npm install --silent && npm run build")
    print("BUILD OUT:\n", stdout.read().decode('utf-8', 'ignore').encode('ascii', 'replace').decode('ascii'))

    print("3. Updating Virtual IP Aliases and Nginx config...")
    stdin, stdout, stderr = client.exec_command("bash /home/server/setup_virtual_ips.sh && echo 1 | sudo -S systemctl restart nginx")
    print("VIP OUT:\n", stdout.read().decode('utf-8', 'ignore').encode('ascii', 'replace').decode('ascii'))

    print("4. Restarting Web Services via start_web_services.sh...")
    stdin, stdout, stderr = client.exec_command("nohup bash /home/server/start_web_services.sh > /home/server/web_services_start.log 2>&1 &")
    print("SERVICES START TRIGGERED.")

    print("5. Rebooting the remote server system...")
    stdin, stdout, stderr = client.exec_command("echo 1 | sudo -S reboot")
    print("REBOOT COMMAND DISPATCHED.")
    client.close()

if __name__ == "__main__":
    deploy_updates()
