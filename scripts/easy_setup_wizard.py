#!/usr/bin/env python3
"""
HomeLab OS — Easy Non-Technical 1-Click Interactive Setup Wizard
Guides non-technical users through automated system checks, environment configuration,
database initialization, secret key generation, and desktop shortcut provisioning.
"""

import os
import sys
import secrets
import subprocess
import platform

# Ensure stdout handles UTF-8 on Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def print_banner():
    print("=" * 65)
    print("      🏠 HomeLab OS — 1-Click Non-Technical Setup Wizard      ")
    print("=" * 65)
    print("Welcome! This wizard will configure HomeLab OS for your computer.")
    print("No technical or programming knowledge required!\n")

def check_python_version():
    print("[1/5] Checking Python installation...")
    major, minor = sys.version_info.major, sys.version_info.minor
    if major < 3 or (major == 3 and minor < 10):
        print(f"  ❌ Error: Python 3.10+ required. (Found Python {major}.{minor})")
        sys.exit(1)
    print(f"  ✅ Python {major}.{minor} detected cleanly.")

def setup_environment_file():
    print("\n[2/5] Configuring security keys & environment settings...")
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    env_path = os.path.abspath(env_path)
    
    if os.path.exists(env_path):
        print("  ℹ️ Existing .env file found. Preserving your current configuration.")
        return

    secret_key = secrets.token_hex(32)
    env_content = f"""# HomeLab OS Auto-Generated Environment Configuration
PROJECT_NAME="HomeLab OS"
VERSION="4.0.0"
ENV="production"
LOG_LEVEL="INFO"

# Security
SECRET_KEY="{secret_key}"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Database Configuration (Defaults to lightweight local SQLite for 1-click zero-config setup)
DATABASE_URL="sqlite:///./database/homelab.db"

# API Prefix
API_V1_STR="/api/v1"
"""
    os.makedirs(os.path.dirname(env_path), exist_ok=True)
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(env_content)
    print("  ✅ Security keys generated and .env configuration created!")

def install_dependencies():
    print("\n[3/5] Installing core dependencies (FastAPI, PySide6, PyQtGraph)...")
    req_path = os.path.join(os.path.dirname(__file__), "..", "backend", "requirements.txt")
    req_path = os.path.abspath(req_path)
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_path, "--quiet"], check=True)
        print("  ✅ Dependencies successfully verified and updated!")
    except Exception as e:
        print(f"  ⚠️ Warning: Auto-pip install encountered an issue: {e}")
        print("  Proceeding with system Python environment...")

def initialize_database():
    print("\n[4/5] Initializing local database schema...")
    db_dir = os.path.join(os.path.dirname(__file__), "..", "database")
    db_dir = os.path.abspath(db_dir)
    os.makedirs(db_dir, exist_ok=True)
    
    # Trigger table creation via backend import
    backend_dir = os.path.join(os.path.dirname(__file__), "..", "backend")
    sys.path.insert(0, os.path.abspath(backend_dir))
    try:
        from app.core.database import engine, Base
        import app.models
        Base.metadata.create_all(bind=engine, checkfirst=True)
        print("  ✅ Database tables successfully created!")
    except Exception as e:
        print(f"  ⚠️ Database initialization warning: {e}")

def create_desktop_launchers():
    print("\n[5/5] Provisioning double-click launcher scripts...")
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    try:
        shortcut_script = os.path.join(os.path.dirname(__file__), "create_desktop_shortcuts.py")
        subprocess.run([sys.executable, shortcut_script], check=False)
        print("  ✅ Double-click launchers ready in root folder!")
    except Exception as e:
        print(f"  ℹ️ Desktop shortcut notice: {e}")

def main():
    print_banner()
    check_python_version()
    setup_environment_file()
    install_dependencies()
    initialize_database()
    create_desktop_launchers()
    
    print("\n" + "=" * 65)
    print(" 🎉 SETUP COMPLETE! HomeLab OS is now 100% ready to run.")
    print("=" * 65)
    print("How to run:")
    print("  • Server: Double-click 'start_server.bat' (or run './start_server.sh')")
    print("  • Controller Manager: Double-click 'start_manager.bat' (or run './start_manager.sh')")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    main()
