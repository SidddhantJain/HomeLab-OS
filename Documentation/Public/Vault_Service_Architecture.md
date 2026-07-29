# Vault Service Architecture

## Purpose

The Vault Service manages the encrypted storage lifecycle on the platform. It provides a cryptographically secure, separate space for private developer configurations, credentials, and vault tables.

## Lifecycle States

```
LOCKED ──► UNLOCKING ──► UNLOCKED ──► LOCKING ──► LOCKED
```

- **LOCKED**: Container loop device is closed. File content is unreadable binary data.
- **UNLOCKING**: Validating password and executing `cryptsetup open` commands.
- **UNLOCKED**: Loop device decrypted and mounted to `/mnt/vault`. Exposing active files.
- **LOCKING**: Closing maps and finalizing safely.

## Component Operations

- **VaultManager**: Orchestrates access credentials verification, checks transition rules, and updates metadata state tables.
- **VaultEncryptionManager**: Executes LUKS2 block-level instructions and maps files to loop devices.
