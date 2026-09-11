# HomeLab OS — Self-Hosted Operating Platform

> A lightweight, self-hosted operating platform providing personal private cloud management, developer workspace control, storage administration, encrypted LUKS vault, multi-node cluster federation, automated backups, cross-platform hardware monitoring, VirtualBox hypervisor control, high-performance Rust PyO3 core, WASM sandbox, Android native companion, GPU transcode load balancing, and a native PySide6 desktop management console.

---

## 🚀 Active Release: `v2.5.0` (Polyglot Core & Mobile Ecosystem Release)

HomeLab OS v2.5.0 is officially feature-complete, stabilized, fully tested (76 backend and 17 PySide6 desktop navigation modules passing), and ready for production deployment.

- **🦀 High-Performance Rust PyO3 Telemetry Subsystem**: Low-latency (< 2ms) telemetry gathering and AES-256-GCM vault cryptographic acceleration via `homelab-core-rs` PyO3 FFI bridge, reducing idle RAM footprint to **< 30 MB**.
- **📦 Drag-and-Drop Live Container & VM Migration Engine**: Zero-downtime container volume snapshot streaming, execution state freezing, and cluster node migration.
- **🎬 Hardware GPU Transcode Load Balancer**: Intel QuickSync Video (i7-5500U) & NVIDIA NVENC auto-detection and task load balancing.
- **🧩 WASM / WASI Plugin Sandbox Engine**: WebAssembly runtime (Wasmtime) sandbox for running 3rd-party extensions in Rust, Go, C, or TypeScript with zero root elevation risk.
- **📱 Android Companion & WebRTC Remote Terminal**: Biometrics, FCM push alerts, client SHA-256 media auto-upload deduplication, and low-latency P2P WebRTC live terminal signaling.
- **🔒 Closed-Source Binary Obfuscation Pipeline**: Nuitka C-extension compilation and PyArmor code protection builder (`scripts/build_obfuscated_binaries.py`).
- **🖥️ Native PySide6 Desktop Console**: 17 management modules (Dashboard, PyQtGraph Monitoring, Storage, LUKS Vault, Docker, VirtualBox, Live Migration, GPU Balancer, WASM Plugins, Mobile Sync, Workspace, Network Map, WinSCP File Manager, Tabbed SSH Terminal, Automation Builder, Plugin App Store, Settings & RDP Launcher).

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

# 3. Launch PySide6 Native Desktop Manager Console (17 Modules)
python manager/main.py

# 4. Run Full-Spectrum Test Suite (76 Backend Tests)
python -m pytest tests/backend -q
python scripts/test_pyside_manager.py

# 5. Run Closed-Source Binary Packaging Builder
python scripts/build_obfuscated_binaries.py

# 6. Run Pre-Commit Security Audit
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
