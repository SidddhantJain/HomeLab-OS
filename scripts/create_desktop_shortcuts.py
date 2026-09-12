#!/usr/bin/env python3
"""
HomeLab OS — Automated Desktop Shortcut Creator
Places 1-click double-click desktop icons for Server and Desktop Manager Console.
"""

import os
import sys
import platform

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def create_shortcuts():
    system = platform.system()
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    
    if not os.path.exists(desktop_dir):
        print(f"Desktop folder not found at {desktop_dir}. Skipping desktop shortcut creation.")
        return

    if system == "Windows":
        try:
            import winshell
            from win32com.client import Dispatch

            # 1. Server Shortcut
            server_bat = os.path.join(root_dir, "start_server.bat")
            server_shortcut = os.path.join(desktop_dir, "HomeLab OS Server.lnk")
            shell = Dispatch('WScript.Shell')
            sc1 = shell.CreateShortCut(server_shortcut)
            sc1.Targetpath = server_bat
            sc1.WorkingDirectory = root_dir
            sc1.Description = "Launch HomeLab OS Backend Server Engine"
            sc1.save()

            # 2. Manager Shortcut
            manager_bat = os.path.join(root_dir, "start_manager.bat")
            manager_shortcut = os.path.join(desktop_dir, "HomeLab OS Desktop Manager.lnk")
            sc2 = shell.CreateShortCut(manager_shortcut)
            sc2.Targetpath = manager_bat
            sc2.WorkingDirectory = root_dir
            sc2.Description = "Launch HomeLab OS PySide6 Desktop Manager Console"
            sc2.save()

            print(f"  ✅ Created Windows desktop shortcuts: '{server_shortcut}' & '{manager_shortcut}'")
        except Exception as e:
            print(f"  ℹ️ Notice: Windows desktop shortcut creation skipped ({e}). Double-click 'start_server.bat' & 'start_manager.bat' directly in repository root.")
    else:
        print("  ℹ️ Linux/macOS shortcut: Use root 'start_server.sh' and 'start_manager.sh' scripts directly.")

if __name__ == "__main__":
    create_shortcuts()
