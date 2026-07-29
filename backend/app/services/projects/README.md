# Project Intelligence Service

The Projects Service registers local repositories, parses tech stacks, and manages versioned snapshots.

## Directory Structure

```text
projects/
├── __init__.py
├── service.py       # Main BaseService class orchestrating registries
├── manager.py       # Directory scans & metadata creation
├── git.py           # Git status queries
├── metadata.py      # Language and package dependency parsers
├── models.py        # Exposes database mappings
├── events.py        # Event definition strings
└── snapshot/        # Snapshot sub-system folder
    ├── __init__.py
    └── manager.py   # Snapshot logic and retention
```
