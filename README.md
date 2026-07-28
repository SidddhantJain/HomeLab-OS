# HomeLab OS v1

> A lightweight, self-hosted operating platform providing personal private cloud management, developer workspace control, storage administration, encrypted vault integration, automated backups, and hardware monitoring.

---

## ⚠️ Important Architecture Clarification: Two Environments

HomeLab OS strictly separates the **Development Environment** from the **Production Deployment Server**.

```text
┌─────────────────────────────────────────┐       ┌─────────────────────────────────────────┐
│     Environment 1: Development          │       │      Environment 2: Production          │
├─────────────────────────────────────────┤       ├─────────────────────────────────────────┤
│ • Hardware: Developer Laptop/Desktop    │       │ • Hardware: Dell Inspiron 5558          │
│ • OS: macOS / Linux / Windows           │       │ • OS: Ubuntu 24.04 LTS                  │
│ • Goal: Writing code, testing features  │       │ • Goal: 24/7 Production Runtime         │
│ • Docker: OPTIONAL                      │ ─────►│ • Docker Engine: MANDATORY              │
│ • Database: SQLite / Local Postgres     │       │ • Docker Compose: MANDATORY             │
└─────────────────────────────────────────┘       └─────────────────────────────────────────┘
```

---

## 🔄 Deployment Pipeline

```text
Developer Machine ──► Git Repository ──► Release Package ──► Installer ──► Deployment Server (Docker Stack)
```

1. **Developer Machine**: Code written, tested via Pytest, and scanned for security violations.
2. **Git Repository**: Pushed to `origin/main` after automated pre-commit audit (`scripts/security_scan.sh`).
3. **Release Package**: Versioned Tarballs generated under `release/packages/` following SemVer (`Major.Minor.Patch`).
4. **Installer**: Windows Remote Assistant (`installer/windows/`) or Native Linux Script (`installer/linux/`).
5. **Deployment Server**: Executed on Ubuntu 24.04 LTS via `/deployment/install.sh`.

---

## 💻 For Developers (Environment 1)

### Requirements
- Python 3.12+
- Node.js 20+
- Git
- **Docker is OPTIONAL** for development.

### Quickstart Developer Setup
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
python -m pytest tests/backend

# 5. Run Security Audit Scan
bash scripts/security_scan.sh
```

- **Local API Specs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Local Dashboard**: [http://localhost:3000](http://localhost:3000)

---

## 🖥️ For Server Deployment (Environment 2)

### Target Server Hardware Specifications
- **Server Model**: Dell Inspiron 5558
- **CPU**: Intel Core i7-5500U (2 Cores, 4 Threads @ 2.40GHz)
- **RAM**: 8GB DDR3L
- **System Drive**: 240GB SSD
- **External Storage**: 1TB External HDD
- **Operating System**: Ubuntu 24.04 LTS
- **Runtime Requirement**: **Docker Engine & Docker Compose (MANDATORY)**

### Production Server Installation
Run the automated server installer:
```bash
# 1. Run requirements check
bash deployment/requirements_check.sh

# 2. Install & start HomeLab OS container stack
bash deployment/install.sh

# 3. Verify server health
bash deployment/health_check.sh
```

- **Production Dashboard**: [http://<server-ip>:3000](http://<server-ip>:3000)
- **Production API**: [http://<server-ip>:8000/api/v1/system/status](http://<server-ip>:8000/api/v1/system/status)

---

## 📂 Repository Structure

```text
homeos-v1/
├── backend/            # FastAPI Python application core
├── frontend/           # React + Vite + Tailwind CSS dashboard UI
├── database/           # Baseline SQL schemas & migrations
├── deployment/         # Server deployment scripts (install, update, uninstall, health)
├── installer/          # Dual-layer installers (Windows Remote Assistant & Linux Native)
├── release/            # Release metadata (version.json, packages)
├── scripts/            # Security audit pre-commit scan script
├── configs/            # System & proxy configurations
├── docs/               # System architecture & deployment pipeline specs
├── Documentation/
│   ├── Public/         # SRS, SAD, DB Schema, API Specs (Committed to Git)
│   └── Private/        # Credentials, IP addresses, SSH keys (STRICTLY IGNORED BY GIT)
└── tests/              # Backend Pytest automated tests
```

---

## 🔒 Security & Privacy Rules

- **Documentation Separation**: All private credentials, server IP addresses, SSH keys, and vault passphrases belong in `Documentation/Private/` which is protected by `.gitignore`.
- **Pre-Commit Security Audit**: Before pushing code to `origin/main`, execute:
  ```bash
  bash scripts/security_scan.sh
  ```

---

## 📄 License
Privately developed for HomeLab OS Project.
