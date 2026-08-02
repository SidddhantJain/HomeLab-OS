# HomeLab OS v1.0.0 Stable

> A lightweight, self-hosted operating platform providing personal private cloud management, developer workspace control, storage administration, encrypted vault integration, network management, automated backups, and cross-platform hardware monitoring.

---

## 🚀 Official Release Version: `v1.0.0`

HomeLab OS v1.0.0 is officially feature-complete, stabilized, and ready for production deployment across **Linux**, **Windows**, and **macOS**.

---

## 💻 Quickstart Setup

### Requirements
- Python 3.10+
- Node.js 20+
- Docker Engine v24.0+ (Mandatory for Production Server Deployment; Optional for local Dev)

### Local Development Setup
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

# 3. Run Frontend UI (React + Vite)
cd ../frontend
npm install
npm run dev

# 4. Run Pytest Suite
python -m pytest tests/backend -q

# 5. Run Pre-Commit Security Audit
bash scripts/security_scan.sh
```

- **Local API Specs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Local Dashboard**: [http://localhost:5173](http://localhost:5173)

---

## 🖥️ Server Production Deployment
Run the automated server installer:
```bash
# 1. Run requirements check
bash deployment/requirements_check.sh

# 2. Install & start HomeLab OS container stack
bash deployment/install.sh
```

---

## 📚 Final Production Release Documentation Suite

All production release documentation is available in `Documentation/Public/`:

- 🏗️ [Architecture Final Specification](Documentation/Public/Architecture_Final.md)
- 🚀 [Production Deployment Guide](Documentation/Public/Production_Deployment_Guide.md)
- ⚙️ [Administrator Guide](Documentation/Public/Administrator_Guide.md)
- 💻 [Developer Guide](Documentation/Public/Developer_Guide.md)
- 🔒 [Security Guide](Documentation/Public/Security_Guide.md)
- 🛠️ [Maintenance Guide](Documentation/Public/Maintenance_Guide.md)
- 📦 [Backup & Recovery Guide](Documentation/Public/Backup_Recovery_Guide.md)
- 📄 [v1.0.0 Release Summary](Documentation/Public/Release_Summary_v1.0.0.md)
- ⚠️ [Known Limitations](Documentation/Public/Known_Limitations.md)
- 🔭 [v2.0 Future Roadmap](Documentation/Public/Roadmap_v2.md)
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
HomeLab OS v1.0.0 Release.
