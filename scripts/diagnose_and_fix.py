import sys
import paramiko

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('192.168.0.182', username='server', password='1')

def run(cmd):
    print(f"\n=== [CMD] {cmd} ===")
    stdin, stdout, stderr = client.exec_command(cmd)
    if 'sudo' in cmd:
        stdin.write('1\n')
        stdin.flush()
    out = stdout.read().decode('utf-8', 'replace').strip()
    err = stderr.read().decode('utf-8', 'replace').strip()
    if out:
        print("[OUT]\n" + out)
    if err:
        print("[ERR]\n" + err)
    return out

run('echo 1 | sudo -S systemctl status nginx --no-pager')
run('echo 1 | sudo -S ss -tlpn')
run('ip addr')
run('echo 1 | sudo -S cat /etc/nginx/conf.d/homelab_vip.conf || true')
run('echo 1 | sudo -S ls -la /etc/nginx/sites-enabled/ || true')
run('curl -s -I http://127.0.0.1/login')
run('curl -s -I http://127.0.0.1/')
run('curl -s -I -H "Host: 192.168.0.183" http://127.0.0.1/')
run('curl -s -I http://127.0.0.1:5173/login || true')
run('curl -s -I http://127.0.0.1:5174/ || true')
run('curl -s -I http://127.0.0.1:8000/api/v1/system/status || true')

client.close()
