#!/usr/bin/env python3
"""
HomeLab OS — Automated Desktop Shortcut Creator
Places 1-click double-click desktop icons for Server and Desktop Manager Console.
Supports Windows (.lnk via PowerShell) & Linux (.desktop files).
"""

import os
import sys
import platform
import subprocess

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def get_desktop_dir():
    user_home = os.path.expanduser("~")
    
    # 1. Try standard Desktop path
    std_desktop = os.path.join(user_home, "Desktop")
    if os.path.exists(std_desktop):
        return std_desktop
        
    # 2. Try OneDrive Desktop path (common on Windows)
    onedrive_desktop = os.path.join(user_home, "OneDrive", "Desktop")
    if os.path.exists(onedrive_desktop):
        return onedrive_desktop
        
    # 3. Query via PowerShell on Windows
    if platform.system() == "Windows":
        try:
            ps_cmd = "[Environment]::GetFolderPath('Desktop')"
            res = subprocess.check_output(["powershell", "-NoProfile", "-Command", ps_cmd], text=True).strip()
            if res and os.path.exists(res):
                return res
        except Exception:
            pass

    return std_desktop

def create_windows_shortcut(target_path, shortcut_path, description="", working_dir=""):
    if not working_dir:
        working_dir = os.path.dirname(target_path)
    ps_cmd = (
        f"$s = (New-Object -COM WScript.Shell).CreateShortcut('{shortcut_path}'); "
        f"$s.TargetPath = '{target_path}'; "
        f"$s.WorkingDirectory = '{working_dir}'; "
        f"$s.Description = '{description}'; "
        f"$s.Save()"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True)

def create_shortcuts():
    system = platform.system()
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    desktop_dir = get_desktop_dir()

    print(f"📁 Target Desktop directory: {desktop_dir}")
    os.makedirs(desktop_dir, exist_ok=True)

    if system == "Windows":
        server_bat = os.path.join(root_dir, "start_server.bat")
        manager_bat = os.path.join(root_dir, "start_manager.bat")

        server_shortcut = os.path.join(desktop_dir, "HomeLab OS Server.lnk")
        manager_shortcut = os.path.join(desktop_dir, "HomeLab OS Desktop Manager.lnk")

        try:
            create_windows_shortcut(server_bat, server_shortcut, "Launch HomeLab OS Backend Server Engine", root_dir)
            create_windows_shortcut(manager_bat, manager_shortcut, "Launch HomeLab OS PySide6 Desktop Manager Console", root_dir)
            print(f"  ✅ Created Windows desktop shortcuts:\n     • {server_shortcut}\n     • {manager_shortcut}")
        except Exception as e:
            print(f"  ⚠️ Error creating Windows desktop shortcuts: {e}")
    else:
        # Linux / macOS desktop entries
        server_sh = os.path.join(root_dir, "start_server.sh")
        manager_sh = os.path.join(root_dir, "start_manager.sh")

        desktop_manager_entry = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=HomeLab OS Desktop Manager
Comment=Launch HomeLab OS Native PySide6 Desktop Console
Exec=bash "{manager_sh}"
Path={root_dir}
Icon=utilities-terminal
Terminal=false
Categories=System;Management;
"""

        desktop_server_entry = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=HomeLab OS Server
Comment=Launch HomeLab OS FastAPI Backend Server Engine
Exec=bash "{server_sh}"
Path={root_dir}
Icon=network-server
Terminal=true
Categories=System;Management;
"""

        manager_desktop_file = os.path.join(desktop_dir, "HomeLab-OS-Manager.desktop")
        server_desktop_file = os.path.join(desktop_dir, "HomeLab-OS-Server.desktop")

        try:
            with open(manager_desktop_file, "w", encoding="utf-8") as f:
                f.write(desktop_manager_entry)
            os.chmod(manager_desktop_file, 0o755)

            with open(server_desktop_file, "w", encoding="utf-8") as f:
                f.write(desktop_server_entry)
            os.chmod(server_desktop_file, 0o755)

            print(f"  ✅ Created Linux desktop launchers:\n     • {manager_desktop_file}\n     • {server_desktop_file}")
        except Exception as e:
            print(f"  ⚠️ Error creating Linux desktop launchers: {e}")

if __name__ == "__main__":
    create_shortcuts()
