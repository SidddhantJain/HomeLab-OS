# HomeLab OS — Non-Technical User Setup & Quickstart Guide

> A plain-English step-by-step guide for non-technical users to set up, run, and manage **HomeLab OS** on both the **Server** (host machine) and **Developer / Controller** (desktop control interface).

---

## 🏁 Quickstart Summary (1-Click Automated Setup)

You do **NOT** need to type complex terminal commands or edit configuration code! We have built **1-click automated setup wizards and launchers**.

---

## 🖥️ Step 1: Initial 1-Click Setup (Run Once)

1. Open the project folder on your server or desktop.
2. Run the **Easy Setup Wizard**:
   - **Windows**: Open terminal/cmd in folder and type `python scripts/easy_setup_wizard.py` or double-click `scripts/easy_setup_wizard.py`.
   - **Linux / macOS**: Open terminal in folder and type `python3 scripts/easy_setup_wizard.py`.
3. The wizard will automatically:
   - Verify Python is ready.
   - Install required packages (FastAPI, PySide6, PyQtGraph).
   - Generate secure encryption keys & `.env` configuration file.
   - Create your local database tables (`database/homelab.db`).
   - Create double-click launch shortcuts on your desktop!

---

## 🚀 Step 2: Running the Server Side (HomeLab Server Host)

The **Server** runs in the background and controls storage, microVM hypervisors, AI copilot, backups, and network tunnels.

### 🪟 Windows Server
- Double-click `start_server.bat` in the project root folder.
- A window will pop up showing `Starting HomeLab OS Server on http://localhost:8000 ...`.
- Leave this window open while your server is running.

### 🐧 Linux / macOS Server
- Open terminal and run `./start_server.sh` (or `bash start_server.sh`).
- Server starts on `http://localhost:8000`.

---

## 🎮 Step 3: Running the Controller / Manager Side (Desktop Console)

The **Desktop Controller Manager** is a visual app (built with PySide6) that gives you full control over all 22 system modules!

### 🪟 Windows Desktop Controller
- Double-click `start_manager.bat` in the project root folder (or click the **HomeLab OS Desktop Manager** icon on your Windows Desktop).
- The dark glassmorphism dashboard application will open automatically!

### 🐧 Linux / macOS Desktop Controller
- Open terminal and run `./start_manager.sh` (or `bash start_manager.sh`).

---

## 📊 Overview of 22 Desktop Control Modules

Once the Desktop Manager opens, navigate using the sidebar menu:

1. **📊 Dashboard**: Real-time system health score gauge, CPU/RAM meters, and server state status.
2. **📈 Monitoring**: High-frequency PyQtGraph telemetry curves (CPU, RAM, Disks, Network).
3. **💾 Storage**: Hard drive inventory, partition mounting, and SMART health diagnostics.
4. **🔒 Encrypted Vault**: Zero-knowledge AES-256 LUKS encrypted file storage vault.
5. **🤖 AI Copilot**: Local AI assistant for natural language server management and automated crash diagnostics.
6. **🔒 Zero-Trust Mesh**: Encrypted P2P network overlay (WireGuard / Tailscale mesh topology).
7. **📹 Frigate NVR Analytics**: AI camera object detection, RTSP streams, and thermal alert events.
8. **⚡ Power Optimizer**: Dynamic CPU governor scaling, thermal throttling, and UPS battery monitoring.
9. **🐳 Docker Containers**: Container lifecycle management, image updates, and resource usage.
10. **💻 VirtualBox VMs**: Local hypervisor VM management.
11. **📦 Live Container Migration**: Drag-and-drop live container workload migration between cluster nodes.
12. **🎬 GPU Transcode Load Balancer**: Hardware transcode balancing (Intel QuickSync & NVIDIA NVENC).
13. **🧩 WASM Plugins**: WebAssembly runtime plugin sandbox.
14. **📱 Mobile Companion Sync**: Android companion app pairing, FCM push alerts, and media auto-upload.
15. **💼 Workspace Projects**: Project folder intelligence and Git repository control.
16. **🌐 Network Map**: Connected home network device inventory and topology graph.
17. **💻 Remote SSH Console**: Tabbed SSH terminal with interactive shell sessions.
18. **🖥️ Remote Desktop RDP**: Embedded RDP remote desktop viewer.
19. **⚡ Automation Builder**: Drag-and-drop visual event bus rule builder (`Trigger -> Condition -> Action`).
20. **📦 Plugin App Store**: 100+ app marketplace (Jellyfin, Nextcloud, Home Assistant, Vaultwarden, Immich).
21. **⚙️ Settings**: System theme, user accounts, security tokens, and backup schedules.
22. **🔴 Type-1 MicroVM Hypervisor**: Bare-metal MicroVMs (KVM/LXC), PCIe GPU Passthrough, and Virtual SAN block storage pools.

---

## ❓ Frequently Asked Questions (FAQ)

- **Q: How do I change the default port (8000)?**
  - Edit the `.env` file created in the project root folder.
- **Q: Can I access the Web Dashboard from my browser instead of the Desktop App?**
  - Yes! Open your browser and go to `http://localhost:8000/docs` or `http://localhost:5173`.
- **Q: How do I stop the server?**
  - Simply press `Ctrl + C` in the server window or close the window.
