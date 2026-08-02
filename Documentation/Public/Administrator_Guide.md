# HomeLab OS v1.0.0 — Administrator Guide

## Server Management Operations

### 1. Monitoring System Health
Access `/health` in the dashboard or query `GET /api/v1/health/summary` to retrieve overall system score (0-100 gauge), CPU load, RAM usage, and SMART drive alerts.

### 2. Managing Encrypted Vault
- Query Vault state via `GET /api/v1/vault/status`.
- Unlock container via `POST /api/v1/vault/unlock` with passphrase.
- Lock container via `POST /api/v1/vault/lock`.

### 3. Remote Control & Terminal Sandbox
- Execute terminal commands via `POST /api/v1/remote/terminal`.
- Browse server storage via `GET /api/v1/filemanager/browse?path=/location`.
