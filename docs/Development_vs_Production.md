# Development vs. Production Environment Architecture

> **CRITICAL ARCHITECTURAL RULE**: HomeLab OS consists of TWO separate environments. They must never be confused or merged.

---

## 💻 Environment 1: Development Environment

### Purpose
Local software engineering, feature development, unit testing, documentation, and release packaging.

### Target Hardware
Developer Laptop / Desktop (macOS, Linux, or Windows).

### Requirements & Tools
- **Python**: 3.12+ for FastAPI backend development and Pytest execution.
- **Node.js**: 20+ & npm for React Vite frontend development.
- **Git**: Source code control.
- **Docker**: **OPTIONAL** for development. Developers can run FastAPI (`uvicorn app.main:app`) and React (`npm run dev`) directly on host OS using SQLite/local databases without Docker.

---

## 🚀 Environment 2: Deployment Server (Production Runtime)

### Purpose
24/7 self-hosted operating platform runtime.

### Target Hardware Specifications
- **Hardware Model**: Dell Inspiron 5558
- **CPU**: Intel Core i7-5500U
- **RAM**: 8GB DDR3L
- **Storage**: 240GB SSD (System Root) + 1TB External HDD (Storage / Backups)
- **Operating System**: Ubuntu 24.04 LTS Server

### Requirements & Tools
- **Docker Engine**: **MANDATORY**. All production services run inside containerized isolations.
- **Docker Compose**: **MANDATORY**. Orchestrates multi-container stack (`postgres`, `redis`, `backend`, `frontend`).
- **Nginx / Reverse Proxy**: Manages SSL termination and route proxying.

---

## 📊 Summary Comparison Matrix

| Attribute | Environment 1 (Development) | Environment 2 (Deployment Server) |
|---|---|---|
| **Primary Goal** | Writing code, testing, building releases | Production runtime, hosting private cloud |
| **Target OS** | Windows / macOS / Linux Developer Laptop | Ubuntu 24.04 LTS (Dell Inspiron 5558) |
| **Docker Requirement** | **OPTIONAL** (Python/Node can run natively) | **MANDATORY** (Docker Engine & Compose) |
| **Database** | SQLite in-memory / local PostgreSQL | Containerized PostgreSQL 16 & Redis 7 |
| **Services Execution** | Local `uvicorn` & `vite` processes | Containerized Docker Compose stack |
