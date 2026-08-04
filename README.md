# HomeLab OS — Self-Hosted Operating Platform

> A lightweight, self-hosted operating platform providing personal private cloud management, developer workspace control, storage administration, encrypted LUKS vault, network management, automated backups, cross-platform hardware monitoring, VirtualBox hypervisor control, and a native PySide6 desktop management console.

---

## 🚀 Active Release: `v1.5.2` (Native Desktop Console & Telemetry Release)

HomeLab OS v1.5.2 is officially feature-complete, stabilized, and deployed across production server hardware (**Dell Inspiron 5558** target node `@192.168.0.180`).

- **Native PySide6 Desktop Console**: 13 management modules (Dashboard, PyQtGraph Monitoring, Storage, LUKS Vault, Docker, VirtualBox, Workspace, Network Map, WinSCP File Manager, Tabbed SSH Terminal, Automation Builder, Plugin App Store, Settings & RDP Launcher).
- **Oracle VM VirtualBox HAL**: REST API (`/api/v1/virtualbox/vms`) and PySide6 VM management.
- **Real-Time Telemetry**: Non-zero CPU & RAM hardware utilization sampling over interval delta.
- **Dynamic LAN API Host Resolution**: Auto-adapting host connections over LAN IP / domain.

---

## 💻 Quickstart Setup

### Requirements
- Python 3.10+
- Node.js 20+
- PySide6 / Qt 6.11+
- Docker Engine v24.0+ (Mandatory for Production Server Deployment; Optional for local Dev)

### Local Development & PySide6 Desktop Manager Setup
```bash
# 1. Clone repository
git clone https://github.com/SidddhantJain/HomeLab-OS.git
cd HomeLab-OS

# 2. Run Backend API (FastAPI)
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 3. Launch PySide6 Native Desktop Manager Console
python manager/main.py

# 4. Run Pytest Suite & Manager Headless Tests
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
- 📄 [v1.0.0 Release Summary](Documentation/Public/Release_Summary_v1.0.0.md)
- ⚠️ [Known Limitations](Documentation/Public/Known_Limitations.md)
- 🔭 [Master Roadmap v2.0 – v5.0](Documentation/Public/Roadmap_v2.md) *(v2.0 100+ App Store & DR Vault, v2.5 Polyglot Engine, v3.0 Edge AI Copilot & NVR, v3.5 OCR & Solar Scheduler, v4.0 Bare-Metal Type-1 Hypervisor ISO, v5.0 Sovereign P2P Federation)*
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
HomeLab OS v1.5.2 Release.
