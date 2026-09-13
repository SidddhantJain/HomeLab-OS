import paramiko
import os

SERVER_IP = "192.168.0.182"
SERVER_USER = "server"
SERVER_PASS = "1"

LOCAL_DIST = r"D:\Siddhant\projects\HomeLab OS\frontend\dist"
REMOTE_DIST = "/home/server/HomeLab-OS/frontend/dist"

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

def sync_and_start():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Connecting to SSH server...")
    client.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS)

    sftp = client.open_sftp()
    print("Uploading compiled frontend dist bundle to remote server...")
    upload_dir(sftp, LOCAL_DIST, REMOTE_DIST)
    sftp.close()

    print("Restarting web services on server...")
    stdin, stdout, stderr = client.exec_command("bash /home/server/start_web_services.sh")
    out_str = stdout.read().decode('utf-8', 'ignore')
    err_str = stderr.read().decode('utf-8', 'ignore')
    print("OUT:\n", out_str.encode('ascii', 'replace').decode('ascii'))
    if err_str:
        print("ERR:\n", err_str.encode('ascii', 'replace').decode('ascii'))
    client.close()

if __name__ == "__main__":
    sync_and_start()
