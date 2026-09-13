import paramiko

SERVER_IP = "192.168.0.182"
SERVER_USER = "server"
SERVER_PASS = "1"

def inspect_services():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS)

    stdin, stdout, stderr = client.exec_command("cat /home/server/start_web_services.sh; crontab -l || true; ls -la /etc/systemd/system/homelab* || true")
    out = stdout.read().decode('utf-8', 'ignore')
    print("SERVICES CONFIG:\n", out.encode('ascii', 'replace').decode('ascii'))
    client.close()

if __name__ == "__main__":
    inspect_services()
