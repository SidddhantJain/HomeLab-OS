import paramiko

SERVER_IP = "192.168.0.182"
SERVER_USER = "server"
SERVER_PASS = "1"

def fix_paths():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS)

    stdin, stdout, stderr = client.exec_command("ls -la /home/server/apps/MadeNMore; ls -la /home/server/apps/MadeNMore/dist || true")
    out = stdout.read().decode('utf-8', 'ignore')
    print("MADENMORE DIR:\n", out.encode('ascii', 'replace').decode('ascii'))
    client.close()

if __name__ == "__main__":
    fix_paths()
