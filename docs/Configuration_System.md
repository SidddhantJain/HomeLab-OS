# Configuration System Design

## Purpose

The Configuration System manages settings and profile information across HomeLab OS services. It combines dotenv environment variables (for secrets, database keys, and passwords) with human-readable YAML configurations (for service parameters, scheduler intervals, and UI options).

## Scope

- Aggregates configuration files under `config/`.
- Merges runtime settings with safe fallbacks.
- Provides a clean fallback parser if external YAML libraries are missing.

## Configuration Layout

```text
HomeLab OS Configuration
├── .env (Credentials, Keys, Host Ports)
└── config/
     ├── system.yml (Global parameters)
     ├── storage.yml (Disk arrays, auto-mount flags)
     ├── vault.yml (LUKS config, timeouts)
     ├── projects.yml (Developer workspace directories)
     ├── docker.yml (Subnet configurations, compose labels)
     ├── notifications.yml (SMTP and webhook credentials)
     ├── scheduler.yml (Job cron and interval schedules)
     └── users.yml (Password lengths, authentication policies)
```

## Loader Usage

The loader provides an simple dictionary query interface:

```python
from app.core.config_loader import ConfigLoader

loader = ConfigLoader()
loader.load_all()

# Retrieve values
auto_mount = loader.get("storage", "auto_mount", default=False)
```
