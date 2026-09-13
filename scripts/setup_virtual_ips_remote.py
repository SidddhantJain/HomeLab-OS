import paramiko

def setup_virtual_ips():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.0.182", username="server", password="1")
    
    script_content = """#!/bin/bash
IFACE=$(ip route | grep default | awk '{print $5}' | head -n 1)
if [ -z "$IFACE" ]; then
  IFACE="wlx98ded016af8f"
fi

echo "Setting up Virtual IP aliases on interface: $IFACE..."
echo 1 | sudo -S ip addr add 192.168.0.183/24 dev "$IFACE" 2>/dev/null || true
echo 1 | sudo -S ip addr add 192.168.0.184/24 dev "$IFACE" 2>/dev/null || true
echo 1 | sudo -S ip addr add 192.168.0.185/24 dev "$IFACE" 2>/dev/null || true
echo 1 | sudo -S ip addr add 192.168.0.186/24 dev "$IFACE" 2>/dev/null || true
echo 1 | sudo -S ip addr add 192.168.0.187/24 dev "$IFACE" 2>/dev/null || true

echo "✅ Virtual IP Aliases Active on Interface $IFACE:"
ip addr show "$IFACE" | grep "inet "
"""

    sftp = client.open_sftp()
    with sftp.open("/home/server/setup_virtual_ips.sh", "w") as f:
        f.write(script_content)
    sftp.chmod("/home/server/setup_virtual_ips.sh", 0o755)
    sftp.close()

    stdin, stdout, stderr = client.exec_command("bash /home/server/setup_virtual_ips.sh")
    out_str = stdout.read().decode('utf-8', 'ignore')
    err_str = stderr.read().decode('utf-8', 'ignore')
    print("OUT:\n", out_str.encode('ascii', 'replace').decode('ascii'))
    if err_str:
        print("ERR:\n", err_str.encode('ascii', 'replace').decode('ascii'))
    client.close()

if __name__ == "__main__":
    setup_virtual_ips()
