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

## 🏗️ Platform Core & Subsystems

HomeLab OS has been consolidated into a modular, event-driven software platform:

- **HomeLab Core**: The central coordinator singleton orchestrating service registries and lifecycles.
- **Event Bus**: In-process pub/sub system enabling decoupled inter-service communications.
- **Server State Machine**: Enforces valid server states (BOOTING, RUNNING, MAINTENANCE, UPDATING, etc.).
- **Hardware Abstraction Layer (HAL)**: Unified Python interfaces query CPU, RAM, Network, Battery, and Thermals safely across environments.
- **Scheduler Framework**: Central job engine pausing automatically during high-load system states.
- **Telemetry Framework**: Unified health status scoring, warning metrics, and alert collectors.
- **Plugin System**: Structured extension discovery and sandboxed plugin layouts under `plugins/`.
- **YAML Configuration System**: Human-readable configuration sets under `config/` merging with dotenv settings.
- **Frontend SDK**: Unified client abstraction layer inside the React application (`frontend/src/sdk/`).
- **Migration Framework**: Coordinates database schema updates (Alembic), YAML structures, and Docker profiles.

---

## 📂 Repository Structure

```text
homeos-v1/
├── backend/            # FastAPI Python application core
│   ├── app/
│   │   ├── core/       # HomeLab Core, Event Bus, State Machine, Telemetry, Scheduler, Configs
│   │   ├── hardware/   # Hardware Abstraction Layer (HAL)
│   │   ├── services/   # Isolated platform services (12 service packages)
│   │   └── api/        # REST controllers and routers
├── frontend/           # React + Vite + Tailwind CSS dashboard UI
│   ├── src/sdk/        # Frontend Client SDK for API requests
├── config/             # YAML configurations (system, storage, vault, docker, etc.)
├── plugins/            # Extensible platform plugin directories
├── database/           # Baseline SQL schemas & migrations
├── deployment/         # Server deployment scripts (install, update, uninstall, health)
├── installer/          # Dual-layer installers (Windows Remote Assistant & Linux Native)
├── release/            # Release metadata & versioned channel archives (stable, beta, nightly)
├── scripts/            # Security audit pre-commit scan script
├── docs/               # Architecture design specifications
├── Documentation/
│   ├── Public/         # SRS, SAD, DB Schema, API Specs, Storage/Vault/Phase 3 specifications
│   │   ├── [Storage Service Architecture](Documentation/Public/Storage_Service_Architecture.md)
│   │   ├── [Vault Service Architecture](Documentation/Public/Vault_Service_Architecture.md)
│   │   ├── [External HDD Setup Guide](Documentation/Public/External_HDD_Setup_Guide.md)
│   │   ├── [LUKS Vault Design](Documentation/Public/LUKS_Vault_Design.md)
│   │   ├── [Storage & Vault API Documentation](Documentation/Public/Storage_API_Documentation.md)
│   │   ├── [Workspace Service Architecture](Documentation/Public/Workspace_Service_Architecture.md)
│   │   ├── [Project Service Architecture](Documentation/Public/Project_Service_Architecture.md)
│   │   ├── [Backup Architecture](Documentation/Public/Backup_Architecture.md)
│   │   ├── [Snapshot Architecture](Documentation/Public/Snapshot_Architecture.md)
│   │   ├── [Permission Model](Documentation/Public/Permission_Model.md)
│   │   ├── [Documentation Service Architecture](Documentation/Public/Documentation_Service_Architecture.md)
│   │   ├── [Download Service Architecture](Documentation/Public/Download_Service_Architecture.md)
│   │   └── [All Phases Master Checklist](Documentation/Public/All_Phases_Checklist.md)
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

