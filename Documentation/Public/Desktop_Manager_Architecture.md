# HomeLab Manager Desktop Architecture

## Overview
HomeLab Manager is the desktop application companion for HomeLab OS server instances, providing multi-server discovery, remote pairing, trusted connection management, and status monitoring.

## Architecture
- **Backend Core**: Python desktop daemon (`manager/backend/server_discovery.py`).
- **Frontend UI**: React desktop manager interface (`manager/frontend/`).
- **Shared Schemas**: Shared certificate store and RPC definitions (`manager/shared/`).

```
┌─────────────────────────────────────────┐
│        HomeLab Manager Desktop          │
│   (Python + React Desktop Interface)    │
└────────────────────┬────────────────────┘
                     │
    ┌────────────────┴────────────────┐
    │                                 │
HomeLab Server A                 HomeLab Server B
 (127.0.0.1:8000)                (192.168.1.150)
```
