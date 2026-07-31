# Advanced Monitoring & Observability Layer

Tracks CPU, RAM, Disk, Temperature, Network, Battery, Power State, Container statuses, and stores historical metrics.

## Structure
- `collector.py`: Collects HAL hardware metrics
- `thresholds.py`: Evaluates warning/critical thresholds
- `history.py`: Database history metrics store
- `service.py`: Main BaseService subclass orchestrating monitoring runs
- `events.py`: Event definition names
