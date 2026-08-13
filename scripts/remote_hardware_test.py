"""
HomeLab OS — Remote Hardware Test Runner over SSH
Connects to host (media-server@192.168.0.180) and performs Track B hardware diagnostics.
"""

import sys
import os
import json
import paramiko

# Set UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HOST = "192.168.0.180"
PORT = 22
USER = "media-server"
PASS = "1"

COMMANDS = {
    "hostname_os": "hostname && uname -a && cat /etc/os-release | grep PRETTY_NAME",
    "cpu_info": "lscpu || cat /proc/cpuinfo | grep 'model name' | head -n 4",
    "memory": "free -h",
    "storage_drives": "lsblk -o NAME,SIZE,FSTYPE,TYPE,MOUNTPOINT",
    "disk_space": "df -h",
    "network_interfaces": "ip addr",
    "docker_version": "docker --version && docker ps --format 'table {{.Names}}\\t{{.Status}}\\t{{.Ports}}'",
    "sensors_thermal": "sensors 2>/dev/null || cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null || echo 'No thermal sensors read'",
    "smart_health": "sudo -S smartctl -a /dev/sda 2>/dev/null || echo 'SMART tool skipped or permission required'"
}


def run_remote_diagnostics():
    print("=" * 65)
    print(f" Connecting to Server via SSH: {USER}@{HOST}:{PORT}")
    print("=" * 65)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=HOST, port=PORT, username=USER, password=PASS, timeout=10)
        print(" [OK] SSH Connection Established Successfully!")
    except Exception as e:
        print(f" [ERROR] Could not connect to {HOST}: {e}")
        return

    results = {}

    for key, cmd in COMMANDS.items():
        print(f"\n---> Running Probe [{key}]: {cmd}")
        try:
            stdin, stdout, stderr = client.exec_command(cmd, timeout=10)
            if "sudo" in cmd:
                stdin.write(f"{PASS}\n")
                stdin.flush()
            out = stdout.read().decode("utf-8", errors="replace").strip()
            err = stderr.read().decode("utf-8", errors="replace").strip()

            combined = out if out else err
            results[key] = combined
            print(combined if combined else "[No Output]")
        except Exception as ex:
            print(f" [EXCEPT] {ex}")
            results[key] = str(ex)

    client.close()

    report_path = os.path.join(os.path.dirname(__file__), "..", "release", "remote_hardware_audit.json")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 65)
    print(f" SUCCESS: Remote Hardware Diagnostics Completed!")
    print(f" Audit Report Saved to: {os.path.abspath(report_path)}")
    print("=" * 65)


if __name__ == "__main__":
    run_remote_diagnostics()
