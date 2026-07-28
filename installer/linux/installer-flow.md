# Native Linux Installer Flow

The Native Linux Installer runs directly on the deployment server (Dell Inspiron 5558 running Ubuntu 24.04 LTS).

---

## 🔄 Installation Workflow

```text
User / SSH Command
       │
       ▼
installer/linux/install.sh
       │
       ├─► 1. Dependency Check (Docker, Docker Compose, Storage)
       ├─► 2. Directory Provisioning (/opt/homelab, /var/log/homelab)
       ├─► 3. Environment Configuration (.env generation)
       ├─► 4. Docker Stack Deployment (docker compose up -d)
       └─► 5. Health Verification (health_check.sh)
```

1. **Step 1: Check Hardware & Software Dependencies**: Validates Docker, Docker Compose, RAM (>= 2GB), free disk space (>= 5GB).
2. **Step 2: Provision Root System Paths**: Creates `/opt/homelab`, `/var/log/homelab`, `/mnt/storage`, `/mnt/vault`.
3. **Step 3: Provision `.env` Secrets**: Generates strong JWT secrets and database credentials.
4. **Step 4: Launch Containerized Stack**: Executes `docker compose up -d --build` for postgres, redis, backend, frontend.
5. **Step 5: Execute Health Verification**: Verifies all HTTP endpoints and database connections before reporting completion.
