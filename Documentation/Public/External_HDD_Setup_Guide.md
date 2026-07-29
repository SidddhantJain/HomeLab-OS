# External HDD Deployment Guide

## Target Hardware
- **Model**: Dell Inspiron 5558
- **External Storage**: 1TB External USB HDD (formatted to `ext4`)
- **Mount Target**: `/mnt/homelab-storage`

## Physical Configuration

1. Connect the 1TB External HDD to a high-speed USB 3.0 port on the Inspiron 5558.
2. Locate the device path using the HAL or query:
   ```bash
   lsblk -f
   ```
3. Find the disk UUID (e.g. `8ec510bf-65ba-491a-afba-22b0a9db911e`).

## Platform Integration

Ensure that the storage configurations inside `config/storage.yml` match:
```yaml
storage:
  external_drive:
    enabled: true
    auto_mount: true
    mount_point: /mnt/homelab-storage
    filesystem: ext4
    health_monitoring: true
```

The `StorageService` automatically resolves this UUID during platform startup and manages partitions without human intervention.
