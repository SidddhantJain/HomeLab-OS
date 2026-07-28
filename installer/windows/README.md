# Windows Remote Installation Assistant

> **CRITICAL ARCHITECTURAL REQUIREMENT**: A Windows `.exe` installer **cannot** directly run or install Linux operating platform containers natively. Therefore, the Windows Installer serves as a **Remote Installation Assistant**.

---

## 🎯 Purpose & Responsibilities

The Windows Remote Installation Assistant is a desktop utility that allows users on a Windows machine to provision and configure HomeLab OS on a remote Ubuntu 24.04 server without needing manual terminal commands.

### Primary Functions

1. **Server Discovery**: Automatically discovers local Linux servers on the LAN using mDNS / Zeroconf or IP scanning.
2. **SSH Connection Setup**: Prompts for server IP, SSH username, and password/private key to establish a secure SSH session.
3. **Deployment Configuration**: Collects basic setup parameters (administrator credentials, domain name, volume paths) and generates an optimized `.env` file.
4. **Trigger Linux Installation**: Uploads deployment scripts and triggers `/deployment/install.sh` on the target Ubuntu server via SSH.
5. **Dashboard Quick Launch**: Displays live installation progress and opens the web dashboard URL (`http://<server-ip>:3000`) once ready.
