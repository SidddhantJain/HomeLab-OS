# Development Environment Setup

## Environment Clarification

> [!IMPORTANT]
> **Environment 1 (Development Machine)**: For software engineering, code editing, and testing. **Docker is OPTIONAL**. Developers can run FastAPI (`uvicorn app.main:app`) and React (`npm run dev`) directly on host OS using SQLite/local databases without Docker.
>
> **Environment 2 (Deployment Server - Dell Inspiron 5558 / Ubuntu 24.04 LTS)**: Production runtime platform. **Docker and Docker Compose are MANDATORY**.

---

## Developer Machine Prerequisites

### Required Software
1. **Git**: Version control system.
   ```bash
   sudo apt install git
   ```
2. **Python 3.12+**: Backend language and runtime.
   ```bash
   sudo apt install python3 python3-pip python3-venv
   ```
3. **Node.js 20+ & npm**: Frontend runtime and build tool.
   ```bash
   # Install Node.js LTS via NVM or NodeSource
   ```
4. **Docker & Docker Compose**: **OPTIONAL for Development Environment**, MANDATORY for Production Server.

---

## Local Development Setup

### 1. Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run backend API server
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install

# Run frontend Vite dev server
npm run dev
```

---

## Development vs Production Pipeline

```text
Developer Machine ──► Git Push ──► Release Package ──► Installer ──► HomeLab Server (Docker Runtime)
```