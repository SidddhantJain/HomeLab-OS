# HomeLab OS Production Deployment System

This directory contains operational scripts designed to install, update, monitor, and uninstall HomeLab OS on the target **Dell Inspiron 5558 / Ubuntu 24.04 LTS** production deployment server.

---

## 🛠️ Operational Scripts

### 1. Requirements Check (`requirements_check.sh`)
Verifies system compatibility prior to deployment.
```bash
bash deployment/requirements_check.sh
```
Checks:
- Operating System (Ubuntu 24.04 LTS recommended)
- Docker Engine installation
- Docker Compose plugin availability
- Memory allocation (minimum 2000 MB)
- Free disk space (minimum 5 GB)

---

### 2. Production Installation (`install.sh`)
Bootstraps directories, environment files, and launches the container stack.
```bash
bash deployment/install.sh
```
Actions:
- Runs `requirements_check.sh`
- Creates system directories (`/opt/homelab`, `/var/log/homelab`, `/mnt/storage`, `/mnt/vault`)
- Provisions `.env` from template with a randomized 64-character secret key
- Starts containers with `docker compose up -d --build`
- Performs post-install health verification

---

### 3. Release Updater (`update.sh`)
Updates deployment code while preserving user data and offering safety rollbacks.
```bash
bash deployment/update.sh
```
Actions:
- Creates timestamped configuration backup in `/opt/homelab/backups/`
- Pulls latest release code from Git
- Rebuilds and restarts Docker service containers
- Runs health checks and prompts for automatic rollback if failure occurs

---

### 4. System Uninstaller (`uninstall.sh`)
Stops containers and cleans temporary deployment files.
```bash
# Standard uninstall (preserves user database & storage volumes)
bash deployment/uninstall.sh

# Full purge (deletes containers AND persistent database volumes)
bash deployment/uninstall.sh --purge
```

---

### 5. Server Health Monitor (`health_check.sh`)
Performs health diagnostics across containers, API endpoints, and databases.
```bash
bash deployment/health_check.sh
```
Checks:
- Docker daemon status
- Container execution state (`homelab_postgres`, `homelab_redis`, `homelab_backend`, `homelab_frontend`)
- FastAPI Core HTTP responsiveness (`http://localhost:8000/`)
- PostgreSQL connectivity (`pg_isready`)
- Storage directory presence (`/mnt/storage`)
