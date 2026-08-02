# HomeLab OS v1.0.0 — Security Guide

## Security Architecture & Best Practices
- **Authentication**: OAuth2 Password Flow + JWT Bearer Tokens with configurable expiration (`jwt_expiration_minutes`).
- **Authorization**: Role-Based Access Control (RBAC) layers enforcing `admin`, `operator`, and `viewer` privileges.
- **Path Traversal Safeguards**: All file manager operations sanitize path parameters via canonical absolute path resolution.
- **Terminal Sandbox**: Remote terminal operations run within restricted command validation layers.
- **Secrets Isolation**: Strict repository protection excluding `.env`, private keys, certificates, and `Documentation/Private/` from Git tracking.
