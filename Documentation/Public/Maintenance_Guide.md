# HomeLab OS v1.0.0 — Maintenance Guide

## System Maintenance & Log Retention
- **Log Management**: Structured JSON logs written to stdout and system log files via [`backend/app/core/logging.py`](file:///d:/Siddhant/projects/HomeLab%20OS/backend/app/core/logging.py).
- **Automated Pruning**: Automated scheduler prunes temp files, orphaned download metadata, and expired telemetry history.
- **Maintenance State**: Put system into maintenance mode via `POST /api/v1/system/maintenance`.
