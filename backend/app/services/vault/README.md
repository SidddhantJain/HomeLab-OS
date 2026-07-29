# Encrypted Vault Service

The Vault Service manages the encrypted partition lifecycle, providing a secure workspace boundary using Linux LUKS2 mappings.

## Design Structure

```text
vault/
├── __init__.py    # package entry exports
├── service.py     # BaseService lifecycle coordinator
├── manager.py     # Lock/unlock state orchestration
├── encryption.py  # LUKS loop device mapping
├── lifecycle.py   # State transitions
├── models.py      # Database models
└── events.py      # Event definitions
```

## State Machine
```text
LOCKED ──► UNLOCKING ──► UNLOCKED ──► LOCKING ──► LOCKED
```

## Security Design
- The system never stores vault master keys or passwords in the database.
- Bcrypt is used solely for standard application logins, and LUKS security keys remain entirely isolated on the host storage disk boundary.
