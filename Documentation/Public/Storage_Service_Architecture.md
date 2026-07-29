# Storage Service Architecture

## Purpose

The Storage Service manages physical disks, monitors health diagnostics (SMART status), coordinates filesystem mounts, and updates host configuration layers on the Dell Inspiron 5558 production server.

## Components

1. **StorageDetector**: Interfaces with the Hardware Abstraction Layer (HAL) to discover connected devices (SSD, USB HDD, etc.), UUID mappings, and capacity constraints.
2. **StorageManager**: Performs mount and unmount operations on registered disk partitions.
3. **StorageHealthAnalyzer**: Decodes SMART metrics, sector maps, and thermal thresholds.

## Decoupled Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      FastAPI Routing                    │
└───────────────────────────┬─────────────────────────────┘
                            │ API Request
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    Storage Service                      │
│  ┌──────────────────┐ ┌──────────────────────────────┐  │
│  │ StorageDetector  │ │        StorageManager        │  │
│  └────────┬─────────┘ └──────────────┬───────────────┘  │
│           │                          │                  │
│           ▼                          ▼                  │
│  ┌──────────────────┐ ┌──────────────────────────────┐  │
│  │   HAL Storage    │ │   SQL StorageMount Tables    │  │
│  └──────────────────┘ └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Telemetry Metrics Published
- `storage.mount_status` (1.0 = mounted, 0.0 = unmounted)
- `storage.capacity_gb`
- `storage.read_write_health`
