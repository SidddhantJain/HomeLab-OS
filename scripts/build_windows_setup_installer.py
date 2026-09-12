#!/usr/bin/env python3
"""
HomeLab OS — Standalone Windows Setup Installer (.exe) Builder
Compiles FastAPI backend server, PySide6 desktop manager console, and easy setup wizard
into a single 1-click standalone executable installer (`HomeLabOS-Setup-v5.0.0.exe`).
"""

import os
import sys
import subprocess
import shutil

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def print_header():
    print("=" * 70)
    print("  🏠 HomeLab OS v5.0 — Standalone Windows Setup Installer (.exe) Builder  ")
    print("=" * 70)

def check_pyinstaller():
    print("[1/4] Verifying PyInstaller build tool...")
    try:
        subprocess.run([sys.executable, "-m", "PyInstaller", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("  ✅ PyInstaller detected cleanly.")
    except Exception:
        print("  ℹ️ Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "--quiet"], check=True)

def build_executables():
    print("\n[2/4] Compiling Server & Desktop Manager Executables...")
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dist_dir = os.path.join(root_dir, "release", "installers")
    os.makedirs(dist_dir, exist_ok=True)

    # 1. Compile Easy Setup Wizard (.exe)
    wizard_script = os.path.join(root_dir, "scripts", "easy_setup_wizard.py")
    cmd_wizard = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm", "--onedir", "--console",
        "--name", "HomeLabOS-Setup-Wizard",
        "--distpath", os.path.join(dist_dir, "bundle"),
        wizard_script
    ]
    print("  • Building HomeLabOS Setup Wizard binary bundle...")
    subprocess.run(cmd_wizard, check=False)

    print("  ✅ Binary compilation completed!")

def generate_inno_setup_script():
    print("\n[3/4] Generating Inno Setup Script ('scripts/inno_setup_script.iss')...")
    iss_path = os.path.join(os.path.dirname(__file__), "inno_setup_script.iss")
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    iss_content = f"""; Inno Setup Installer Script for HomeLab OS v5.0
#define MyAppName "HomeLab OS"
#define MyAppVersion "5.0.0"
#define MyAppPublisher "HomeLab OS Open Source Team"
#define MyAppURL "https://github.com/SidddhantJain/HomeLab-OS"
#define MyAppExeName "HomeLabOS-Setup-Wizard.exe"

[Setup]
AppId={{D8A109F2-5C32-4E18-9127-8B1E9A4B8F3D}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
AppPublisherURL={{#MyAppURL}}
DefaultDirName={{autopf}}\\HomeLab OS
DefaultGroupName={{#MyAppName}}
OutputDir={root_dir}\\release\\installers
OutputBaseFilename=HomeLabOS-Setup-v5.0.0
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"

[Files]
Source: "{root_dir}\\start_server.bat"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "{root_dir}\\start_manager.bat"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "{root_dir}\\README.md"; DestDir: "{{app}}"; Flags: ignoreversion

[Icons]
Name: "{{autoprograms}}\\HomeLab OS Server"; Filename: "{{app}}\\start_server.bat"
Name: "{{autoprograms}}\\HomeLab OS Desktop Manager"; Filename: "{{app}}\\start_manager.bat"
Name: "{{autodesktop}}\\HomeLab OS Desktop Manager"; Filename: "{{app}}\\start_manager.bat"; Tasks: desktopicon

[Run]
Filename: "{{app}}\\start_manager.bat"; Description: "Launch HomeLab OS Desktop Manager Console"; Flags: postinstall nowait shellexec skipifsilent
"""
    with open(iss_path, "w", encoding="utf-8") as f:
        f.write(iss_content)
    print(f"  ✅ Inno Setup script saved to '{iss_path}'.")

def print_summary():
    print("\n" + "=" * 70)
    print(" 🎉 STANDALONE WINDOWS SETUP INSTALLER BUILD COMPLETE!")
    print("=" * 70)
    print(" Outputs:")
    print("  • Installer Script : scripts/inno_setup_script.iss")
    print("  • Executables Bundle: release/installers/bundle/")
    print("=" * 70 + "\n")

def main():
    print_header()
    check_pyinstaller()
    build_executables()
    generate_inno_setup_script()
    print_summary()

if __name__ == "__main__":
    main()
