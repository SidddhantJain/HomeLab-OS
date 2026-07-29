# Detailed Repository Structure

This document describes the structured file layout of the HomeLab OS v1 repository, reflecting the consolidated architecture and core platform subsystems.

```text
homelab-os/
├── backend/                  # FastAPI Python application core
│   ├── app/
│   │   ├── main.py           # REST entrypoint & server boot orchestrator
│   │   ├── api/              # API router controllers (auth, storage, vault, projects, etc.)
│   │   ├── core/             # Central core subsystem coordinators
│   │   │   ├── homelab_core.py       # Core singleton service registry & lifecycle controller
│   │   │   ├── event_bus.py          # Decoupled in-process event publish/subscribe engine
│   │   │   ├── server_state.py       # ServerState enum & state machine transition rules
│   │   │   ├── base_service.py       # BaseService abstract contract
│   │   │   ├── scheduler.py          # Unified system task/cron scheduler framework
│   │   │   ├── telemetry.py          # Unified health & alert metric aggregator
│   │   │   ├── config_loader.py      # Multi-file YAML config aggregator loader
│   │   │   ├── migration_manager.py  # Versioned migration runner (configs, vault, etc.)
│   │   │   ├── config.py             # dotenv based environment settings
│   │   │   ├── security.py           # Bcrypt & JWT helper methods
│   │   │   └── database.py           # SQLAlchemy DB engines
│   │   ├── hardware/         # Hardware Abstraction Layer (HAL)
│   │   │   ├── __init__.py   # Subsystem exports
│   │   │   ├── cpu.py        # CPU loads & hardware info
│   │   │   ├── memory.py     # RAM & swap space analytics
│   │   │   ├── storage.py    # Physical disk partitions & mounts
│   │   │   ├── network.py    # Interface details & traffic I/O
│   │   │   ├── battery.py    # Laptop battery status query
│   │   │   ├── temperature.py# Thermal zones & fan diagnostics
│   │   │   └── power.py      # Ubuntu energy profile management shims
│   │   ├── services/         # Isolated platform services (scaffolding modules)
│   │   │   ├── authentication/
│   │   │   ├── storage/
│   │   │   ├── vault/
│   │   │   ├── monitoring/
│   │   │   ├── automation/
│   │   │   ├── scheduler/
│   │   │   ├── notifications/
│   │   │   ├── projects/
│   │   │   ├── workspace/
│   │   │   ├── updates/
│   │   │   ├── hardware/
│   │   │   └── plugins/
│   │   ├── models/           # SQLAlchemy DB entities
│   │   └── schemas/          # Pydantic validation shapes
├── frontend/                 # React + Vite + Tailwind CSS dashboard UI
│   ├── src/
│   │   ├── sdk/              # Unified Frontend Client SDK to communicate with backend APIs
│   │   │   ├── index.js      # Main SDK class orchestrator
│   │   │   ├── AuthSDK.js
│   │   │   ├── SystemSDK.js
│   │   │   ├── StorageSDK.js
│   │   │   ├── VaultSDK.js
│   │   │   ├── ProjectsSDK.js
│   │   │   ├── WorkspaceSDK.js
│   │   │   ├── MonitoringSDK.js
│   │   │   └── NotificationsSDK.js
│   │   ├── components/       # Reusable components
│   │   ├── pages/            # View routers
│   │   └── styles/           # Main Tailwind configurations
├── config/                   # Structured YAML configuration modules
│   ├── system.yml
│   ├── storage.yml
│   ├── vault.yml
│   ├── projects.yml
│   ├── docker.yml
│   ├── notifications.yml
│   ├── scheduler.yml
│   └── users.yml
├── plugins/                  # Extensible platform plugin directories
│   ├── backup/
│   ├── docker/
│   ├── github/
│   ├── gitea/
│   ├── immich/
│   ├── jellyfin/
│   ├── media/
│   ├── network/
│   └── custom/
├── database/                 # Alembic migrations & initial DB seed scripts
├── deployment/               # Bash installation, update, uninstall, & health verification scripts
├── installer/                # Native deployment assistants for Windows & Linux
├── release/                  # Releases delivery channels (stable, beta, nightly) and metadata
├── scripts/                  # Security audits and scanner utilities
├── docs/                     # Platform architecture design documents
├── Documentation/
│   ├── Public/               # General design documents and specifications
│   └── Private/              # Strictly ignored files (passwords, server keys, SSH nodes)
└── tests/                    # Backend Pytest unit and integration suites
```
