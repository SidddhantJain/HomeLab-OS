# HomeLab OS — Self-Hosted Operating Platform

> A lightweight, self-hosted operating platform providing personal private cloud management, developer workspace control, storage administration, encrypted LUKS vault, multi-node cluster federation, automated backups, cross-platform hardware monitoring, VirtualBox hypervisor control, and a native PySide6 desktop management console.

---

## 🚀 Active Release: `v2.0.0` (Multi-Node Clustering & Feature Extensions Release)

HomeLab OS v2.0.0 is officially feature-complete, stabilized, fully tested (65 backend, 6 desktop, and 5 frontend test cases passing), and ready for production deployment across physical server hardware.

- **Multi-Node Cluster Federation & Raft Consensus**: 1-click server node pairing, distributed Raft consensus state sync, mTLS node join approvals, and live telemetry heartbeat aggregation.
- **Native PySide6 Desktop Console**: 13 management modules (Dashboard, PyQtGraph Monitoring, Storage, LUKS Vault, Docker, VirtualBox, Workspace, Network Map, WinSCP File Manager, Tabbed SSH Terminal, Automation Builder, Plugin App Store, Settings & RDP Launcher).
- **Oracle VM VirtualBox HAL**: REST API (`/api/v1/virtualbox/vms`) and PySide6 VM management.
- **Smart Container Marketplace & App Catalog**: 1-click Docker Compose stack deployment templates for 100+ self-hosted applications.
- **Automated Disaster Recovery Vault Engine**: Differential block snapshot compression (`zstd`), S3/Backblaze B2 backup replication, and 1-click bare-metal recovery.
- **Dynamic Network & Cloudflare Tunnel Manager**: WireGuard mesh overlay networking, Cloudflare Tunnel integration, and automated DNS record sync.
- **AI S.M.A.R.T Predictive Alerting**: Machine learning drive degradation prediction and multi-channel webhook dispatching (Discord, Telegram, Slack, Email).

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

# 4. Run Full-Spectrum Test Suite (65 Backend Tests)
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
- 📄 [v2.0.0 Release Summary & Walkthrough](Documentation/Public/Master_Roadmap_Analysis_And_Extensions.md)
- ⚠️ [Known Limitations](Documentation/Public/Known_Limitations.md)
- 🔭 [Master Roadmap v2.0 – v5.0](Documentation/Public/Roadmap_v2.md) *(v2.5 High-Performance Polyglot Rust Core, Go Gateway, C++23 eBPF, Tauri 2.0, Flutter, Closed-Source Binary Obfuscation)*
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
HomeLab OS v2.0.0 Release.
