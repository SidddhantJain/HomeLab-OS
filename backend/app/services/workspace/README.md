# Workspace Manager Service

The Workspace Manager coordinates physical workspace folders, tracks metadata updates, checks permissions policies, and synchronizes files.

## Directory Structure

```text
workspace/
├── __init__.py
├── service.py       # Main BaseService subclass orchestrating loops
├── manager.py       # Clone operations & disk folder sizes
├── models.py        # Exposes database mappings
├── events.py        # Event definition strings
└── permissions.py   # Workspace permissions middleware check shims
```
