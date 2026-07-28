Detailed Repository Structure

Document 7: Detailed Repository Structure

Repository:

homelab-os/
Root Structure
homelab-os

│
├── backend/
├── frontend/
├── database/
├── docker/
├── services/
├── scripts/
├── configs/
├── docs/
├── tests/
├── deployment/
└── tools/
Backend

Technology:

FastAPI

backend/

├── app/
│
├── main.py
│
├── api/
│   ├── auth.py
│   ├── users.py
│   ├── storage.py
│   ├── vault.py
│   ├── projects.py
│   ├── workspace.py
│   └── system.py
│
├── core/
│   ├── security.py
│   ├── config.py
│   └── database.py
│
├── models/
│
├── schemas/
│
├── services/
│
│   ├── docker_manager.py
│   ├── storage_manager.py
│   ├── backup_engine.py
│   ├── snapshot_engine.py
│   ├── notification.py
│   └── power_manager.py
│
└── tests/
Frontend

React:

frontend/

├── src/

│
├── pages/

│   ├── Dashboard.jsx
│   ├── Storage.jsx
│   ├── Vault.jsx
│   ├── Projects.jsx
│   ├── Workspace.jsx
│   ├── Maintenance.jsx
│   └── Settings.jsx
│
├── components/

│   ├── Charts
│   ├── Cards
│   ├── Tables
│   └── Buttons
│
├── api/

│   └── client.js
│
└── styles/
Database
database/

├── migrations/
├── schema.sql
├── seeds.sql
└── backups/
Docker
docker/

├── compose/

│
├── postgres.yml
├── gitea.yml
├── monitoring.yml
├── documentation.yml
└── homelab-core.yml
Documentation
docs/

├── architecture/
│
├── security/
│
├── api/
│
├── installation/
│
├── user-guide/
│
└── development/
Scripts

Automation:

scripts/

├── install.sh
├── backup.sh
├── restore.sh
├── update.sh
├── health_check.sh
└── maintenance.sh
Configuration
configs/

├── docker/
├── nginx/
├── firewall/
├── system/
└── secrets/
Tests
tests/

├── backend/
├── frontend/
├── integration/
└── security/
