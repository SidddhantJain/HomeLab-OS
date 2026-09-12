# HomeLab OS — Self-Hosted Operating Platform

> A lightweight, self-hosted operating platform providing personal private cloud management, developer workspace control, storage administration, encrypted LUKS vault, multi-node cluster federation, automated backups, cross-platform hardware monitoring, VirtualBox hypervisor control, high-performance Rust PyO3 core, WASM sandbox, Android native companion, GPU transcode load balancing, and a native PySide6 desktop management console.

---

## 🚀 Active Release: `v3.0.0` (Autonomous Edge AI & Zero-Trust Mesh Release)

HomeLab OS v3.0.0 is officially feature-complete, stabilized, fully tested (84 backend and 21 PySide6 desktop navigation modules passing), and ready for production deployment.

- **🤖 Local AI Infrastructure Copilot (`ai_copilot`)**: Autonomous log diagnostics, system query assistant, and incident remediation leveraging local Ollama/vLLM models (Llama-3, Mistral, Qwen).
- **🔒 Zero-Trust WireGuard & Tailscale Mesh Network (`mesh_network`)**: Cross-node peer-to-peer encrypted mesh VPN topology, ACL policy enforcement, and live node key rotation.
- **📹 Frigate NVR Video Analytics Engine (`nvr_analytics`)**: AI object detection (person, car, animal), live camera feed integration, thermal alert streaming, and event clipping.
- **⚡ Autonomous Power & Thermal Optimizer (`power_optimizer`)**: Dynamic CPU governor scaling, thermal throttling control, UPS power monitoring, and eco-mode scheduler.
- **🦀 High-Performance Rust PyO3 Core & WASM Sandbox**: Low-latency (< 2ms) telemetry gathering, AES-256-GCM vault acceleration, and WASI plugin sandbox engine (< 30 MB idle RAM footprint).
- **📱 Android Companion & WebRTC Remote Terminal**: Biometric authentication, FCM push alerts, client SHA-256 media auto-upload deduplication, and WebRTC P2P remote terminal signaling.
- **🖥️ Native PySide6 Desktop Console**: 21 management modules (Dashboard, PyQtGraph Monitoring, Storage, LUKS Vault, Docker, VirtualBox, Live Migration, GPU Balancer, WASM Plugins, Mobile Sync, Workspace, Network Map, WinSCP File Manager, Tabbed SSH Terminal, Automation Builder, Plugin App Store, Settings, RDP Launcher, AI Copilot Console, Zero-Trust Mesh, Frigate NVR Analytics, & Power Optimizer).

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

# 3. Launch PySide6 Native Desktop Manager Console (21 Modules)
python manager/main.py

# 4. Run Full-Spectrum Test Suite (84 Backend Tests)
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
