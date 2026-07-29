# Backup Service

The Backup Service manages local, external HDD, and network backups of the workspaces.

## Directory Structure

```text
backup/
├── __init__.py
├── service.py       # Main BaseService class orchestrating schedules
├── manager.py       # Backup copying logic
├── models.py        # Exposes database mappings
├── scheduler.py     # Task schedule bindings
└── events.py        # Event definition strings
```
