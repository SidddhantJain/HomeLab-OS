# HomeLab OS — Self-Hosted Operating Platform

> A lightweight, self-hosted operating platform providing personal private cloud management, developer workspace control, storage administration, encrypted LUKS vault, multi-node cluster federation, automated backups, cross-platform hardware monitoring, VirtualBox hypervisor control, high-performance Rust PyO3 core, WASM sandbox, Android native companion, GPU transcode load balancing, and a native PySide6 desktop management console.

---

## 🚀 Active Release: `v5.0.0` (Sovereign P2P Federation & Post-Quantum Cryptography Release)

HomeLab OS v5.0.0 is officially feature-complete, stabilized, fully tested (92 backend and 23 PySide6 desktop navigation modules passing), and ready for production deployment.

- **🌐 Decentralized Sovereign P2P Federation (`federation`)**: Interconnect private home server clusters across trusted nodes for encrypted offsite block-level backup streams, federated media sharing, and shared storage quota management.
- **🔒 Post-Quantum Cryptography Subsystem (`quantum_crypto`)**: Kyber-1024 Key Encapsulation Mechanism (KEM) and Dilithium-5 Post-Quantum Digital Signatures securing LUKS vaults, P2P mesh links, and binary integrity checksums.
- **🤖 Local AI Multi-Agent Orchestration Framework (`ai_agents`)**: Autonomous multi-agent AI orchestration engine spawning specialized sub-agents (*System Diagnostician*, *Power/Thermal Controller*, *Zero-Trust Security Guard*, *Backup Auditor*).
- **📦 Standalone `.exe` Setup Installer Builder (`scripts/build_windows_setup_installer.py`)**: PyInstaller & Inno Setup script creating single-click zero-dependency Windows setup installer executables (`release/installers/HomeLabOS-Setup-v5.0.0.exe`).
- **🔴 Bare-Metal Type-1 MicroVM Hypervisor Engine (`hypervisor`)**: KVM / QEMU / LXC microVM lifecycle management, CPU core pinning, PCIe GPU / NVMe passthrough auto-detection, and Virtual SAN block storage pools.
- **✨ Easy 1-Click Non-Technical Setup & Launchers**: Interactive setup wizard (`python scripts/easy_setup_wizard.py`), 1-click double-click launchers (`start_server.bat` / `start_server.sh`, `start_manager.bat` / `start_manager.sh`), automated desktop shortcuts, and plain-English user setup guide ([`Non_Technical_Setup_Guide.md`](file:///d:/Siddhant/projects/HomeLab%20OS/Documentation/Public/Non_Technical_Setup_Guide.md)).
- **🖥️ Native PySide6 Desktop Console**: 23 management modules (Dashboard, Monitoring, Storage, Vault, AI Copilot, Mesh Network, NVR Analytics, Power Optimizer, Type-1 Hypervisor, Sovereign P2P Federation, Docker, VirtualBox, Live Migration, GPU Balancer, WASM Plugins, Mobile Sync, Workspace, Network Map, Remote Console, Remote Desktop RDP, Automation Builder, Plugin App Store, Settings).

---

## 💻 Quickstart Setup (1-Click Non-Technical & Developer)

### 🌟 Easy 1-Click Setup (Non-Technical Users)
```bash
# 1. Run Interactive Setup Wizard (Auto-configures keys, database, and launcher icons)
python scripts/easy_setup_wizard.py

# 2. Launch Server Engine (1-Click)
start_server.bat       # On Windows (or ./start_server.sh on Linux/macOS)

# 3. Launch Desktop Controller Manager (1-Click)
start_manager.bat      # On Windows (or ./start_manager.sh on Linux/macOS)
```

### 💻 Developer Quickstart
```bash
# 1. Clone repository & install dependencies
git clone https://github.com/SidddhantJain/HomeLab-OS.git
cd HomeLab-OS
pip install -r backend/requirements.txt

# 2. Run Backend API (FastAPI)
python -m uvicorn app.main:app --reload --port 8000 --app-dir backend

# 3. Launch PySide6 Native Desktop Manager Console (23 Modules)
python manager/main.py

# 4. Run Full-Spectrum Test Suite (92 Backend Tests + 23 Manager Pages)
python -m pytest tests/backend -q
python scripts/test_pyside_manager.py

# 5. Run Pre-Commit Security Audit
bash scripts/security_scan.sh
```

- **Local API Specs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Local Dashboard**: [http://localhost:5173](http://localhost:5173)

---

## 📚 Master Release Documentation & Future Roadmap

All documentation is available in `Documentation/Public/`:

- 🏗️ [Architecture Final Specification](Documentation/Public/Architecture_Final.md)
- 🚀 [Production Deployment Guide](Documentation/Public/Production_Deployment_Guide.md)
- ⚙️ [Administrator Guide](Documentation/Public/Administrator_Guide.md)
- 💻 [Developer Guide](Documentation/Public/Developer_Guide.md)
- 🔒 [Security Guide](Documentation/Public/Security_Guide.md)
- 🛠️ [Maintenance Guide](Documentation/Public/Maintenance_Guide.md)
- 📦 [Backup & Recovery Guide](Documentation/Public/Backup_Recovery_Guide.md)
- 📄 [v2.5.0 Release Summary & Walkthrough](Documentation/Public/Master_Roadmap_Analysis_And_Extensions.md)
- ⚠️ [Known Limitations](Documentation/Public/Known_Limitations.md)
- 🔭 [Master Roadmap v2.5 – v5.0](Documentation/Public/Roadmap_v2.md) *(v3.0 Edge AI Copilot & NVR, v3.5 OCR & Solar Scheduler, v4.0 Bare-Metal Type-1 Hypervisor ISO, v5.0 Sovereign P2P Federation)*
- 📋 [All Phases Master Checklist](Documentation/Public/All_Phases_Checklist.md)

---

## 🔒 Security & Privacy Protocol
Before pushing code, execute the security pre-commit scanner:
```bash
bash scripts/security_scan.sh
```
All credentials, tokens, and private infrastructure keys remain isolated in `Documentation/Private/`.

---

## 📄 License
HomeLab OS v2.5.0 Release.
