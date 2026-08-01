# Remote Management & Server Control Layer

Secure remote server administration without exposing raw SSH ports.

## Structure
- `commands.py`: Controlled command execution router
- `terminal.py`: Terminal sandbox with pattern filtering
- `security.py`: Device registration and 2FA TOTP verification
- `permissions.py`: Remote RBAC permission rules (REMOTE_ADMIN, REMOTE_OPERATOR, REMOTE_VIEWER)
- `events.py`: Remote activity event definitions
- `service.py`: Main BaseService subclass managing session and audit logging
