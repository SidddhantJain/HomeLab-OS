# LUKS Vault Design

## Cryptographic Parameters

- **Encryption Layer**: LUKS2 (Linux Unified Key Setup)
- **Algorithm**: `aes-xts-plain64`
- **Key Length**: 256-bit
- **Filesystem**: `ext4`
- **Volume Size**: 100GB loopback partition image

## Security Constraints

1. **Password Isolation**: The master vault password is never saved to system memory or databases. Verification is delegated to the LUKS header validation via `cryptsetup`.
2. **Locked State Isolation**: When locked, the filesystem mapping is destroyed and all directories under the mount path return empty lists.
3. **Decoupled Hashing**: Standard application logins use `bcrypt` password verification. Vault decryption bypasses the application database entirely.
