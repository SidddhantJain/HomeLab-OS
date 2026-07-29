# Changelog

All notable changes to the **HomeLab OS** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v1.1.0-pre-phase2] - 2026-07-29

### Added
- **HomeLab Core coordinator**: Singleton architecture orchestrating platform lifecycles and service registry registration.
- **Internal Event Bus**: Lightweight in-process event broker supporting wildcard string channel patterns (e.g. `storage.*`).
- **Server State Machine**: Governs formal server lifecycles (BOOTING, STARTING, RUNNING, MAINTENANCE, etc.) with enforced transition path mappings.
- **Hardware Abstraction Layer (HAL)**: Host-independent modules for query cpu, memory, disk storage, network, thermal zones, battery state, and energy profile profiles.
- **Scheduler Framework**: Standardized time-aware job execution runner (interval, cron, one-shot) integrated with server states.
- **Telemetry Framework**: Aggregates health values, logs performance metrics, and maintains warning status records.
- **Plugin System Layout**: Plugin scanning directories, version validation engines, and permissions limits.
- **YAML Configuration Aggregation**: Multi-file configuration aggregator loading settings under `config/` merging with dotenv credentials.
- **Frontend Client SDK**: React client SDK abstraction wrapping all platform endpoints to simplify UI-level fetch flows.
- **Unified Migration Manager**: Orchestrates multi-dimensional state updates (Alembic schema, Docker files, configs, vaults).

## [v1.0.0-phase1] - 2026-07-28

### Added
- **Repository Structure**: Established standardized directory layout (`backend/`, `frontend/`, `database/`, `docker/`, `scripts/`, `configs/`, `docs/`, `tests/`).
- **FastAPI Core Backend**:
  - Implemented application startup, CORS middleware, and environment configuration management with `pydantic-settings`.
  - Added root API `GET /` returning `{"name": "HomeLab OS", "version": "v1.0", "status": "running"}`.
  - Implemented API modules (`auth`, `system`, `storage`, `projects`, `vault`).
- **PostgreSQL & Database Layer**:
  - Implemented SQLAlchemy 2.0 ORM models for `User`, `AuditLog`, and `SystemMetric`.
  - Setup Alembic database migration environment and schema initialization scripts (`database/schema.sql`).
- **Authentication & Security**:
  - Implemented secure password hashing using direct `bcrypt` library with salting and length safety.
  - Created JWT token generation and verification with `python-jose`.
  - Added `POST /api/v1/auth/register` and `POST /api/v1/auth/login` API endpoints with audit logging.
- **React Frontend Dashboard**:
  - Built Vite + React 18 + Tailwind CSS dark-mode dashboard interface with glassmorphism aesthetics.
  - Implemented reusable UI components (`Navbar`, `Sidebar`, `Card`, `StatusIndicator`).
  - Added `Dashboard` page with realtime CPU, RAM, and Storage telemetry cards.
  - Added `Login` page supporting JWT authentication and `Settings` placeholder page.
- **Docker Compose Stack**:
  - Configured containerization for `postgres:16-alpine`, `redis:7-alpine`, `backend` (FastAPI), and `frontend` (React + Nginx).
  - Included health checks and persistent volume drivers (`postgres_data`, `redis_data`).
- **Automated Testing Suite**:
  - Created Pytest suite in `tests/backend/` validating root endpoint, user registration, JWT login, and system status API.
