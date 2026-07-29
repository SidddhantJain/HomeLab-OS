# Encrypted Vault Recovery Architecture

## Design Overview

To ensure data availability without compromising confidentiality, HomeLab OS implements a zero-knowledge recovery protocol using **Shamir's Secret Sharing (SSS)**.

## Security Constraints

1. **No Key Storage**: The platform never stores the vault password, master key, recovery keys, or key shares in the database, configuration files, git repositories, or logs.
2. **In-Memory Recombination**: Recovery key shares are provided by separate system trust administrators at runtime. Secret recombination occurs strictly in temporary memory. Once the vault is opened, the key is immediately purged from RAM.
3. **Audited Process**: The initiation, verification of individual shares, and completion of recovery workflows trigger audited events (`vault.recovery_initiated`, `vault.recovery_share_verified`, and `vault.recovery_completed`).

## Workflow

```
Trust Administrator 1 ──► Share 1 ──┐
                                     ├──► Recombination ──► Decrypt LUKS
Trust Administrator 2 ──► Share 2 ──┘
```

1. The administrator initiates recovery via `initiate_recovery`.
2. Administrators submit their shares via `verify_recovery_share`.
3. SSS reconstructs the vault passphrase in memory.
4. LUKS container is decrypted via cryptsetup.
