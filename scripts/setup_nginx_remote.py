import paramiko

SERVER_IP = "192.168.0.182"
SERVER_USER = "server"
SERVER_PASS = "1"

NGINX_CONF = """
# HomeLab OS Virtual IP Dedicated Binding Config
server {
    listen 192.168.0.182:80 default_server;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:5173;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

server {
    listen 192.168.0.183:80;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:5174;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

server {
    listen 192.168.0.184:80;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

server {
    listen 192.168.0.185:80;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:5175;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
"""

def setup_nginx():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS)

    sftp = client.open_sftp()
    with sftp.file('/tmp/homelab_vip.conf', 'w') as f:
        f.write(NGINX_CONF)
    sftp.close()

    cmd = (
        "echo 1 | sudo -S rm -f /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default && "
        "echo 1 | sudo -S mkdir -p /etc/nginx/conf.d && "
        "echo 1 | sudo -S mv /tmp/homelab_vip.conf /etc/nginx/conf.d/homelab_vip.conf && "
        "echo 1 | sudo -S nginx -t && "
        "echo 1 | sudo -S systemctl restart nginx"
    )
    stdin, stdout, stderr = client.exec_command(cmd)
    out_str = stdout.read().decode('utf-8', 'ignore')
    err_str = stderr.read().decode('utf-8', 'ignore')
    print("OUT:\n", out_str.encode('ascii', 'replace').decode('ascii'))
    if err_str:
        print("ERR:\n", err_str.encode('ascii', 'replace').decode('ascii'))
    client.close()

if __name__ == "__main__":
    setup_nginx()
