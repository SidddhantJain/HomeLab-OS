# Storage Service

The Storage Service coordinates discovering physical disk assets, tracking mount paths, checking SMART diagnostics, and publishing telemetry alerts across the HomeLab OS platform.

## Design Structure

```text
storage/
├── __init__.py    # package entry exports
├── service.py     # BaseService lifecycle coordinator
├── manager.py     # Mount/unmount executor logic
├── detector.py    # Discovers partition UUIDs & connection profiles
├── health.py      # Parses SMART logs & device warnings
├── models.py      # Exposes database mappings
└── events.py      # Event type names
```

## Subscribed Events

This service publishes:
- `storage.detected`: Fired when storage scans complete.
- `storage.mounted`: Fired when a disk partition is mounted.
- `storage.unmounted`: Fired when a partition is safely unmounted.
- `storage.health_warning`: Fired on critical temperature/sector alerts.
