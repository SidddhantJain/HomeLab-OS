# Telemetry Framework Design

## Purpose

The Telemetry framework provides structured monitoring, health metrics, alerts, and performance metrics across HomeLab OS services. Instead of printing messages directly to stderr/stdout or scattering status tables across databases, services submit telemetry to a central collector.

## Scope

- In-memory event, alert, and metric aggregation.
- Service health cache updates.
- Aggregated health state scoring (`healthy` | `degraded` | `unhealthy`).
- Automatic alert buffering with severity settings.

## Data Schema

### Telemetry Metric
```json
{
  "name": "system.cpu.usage",
  "value": 42.5,
  "tags": { "core": "all" },
  "timestamp": "2026-07-29T10:00:00Z"
}
```

### Telemetry Alert
```json
{
  "key": "disk_space_low",
  "message": "Disk /dev/sda1 is at 95% capacity.",
  "severity": "critical",
  "timestamp": "2026-07-29T10:00:00Z",
  "resolved": false
}
```

## System Integration

The telemetry collector serves as the data provider for:
- Core status REST APIs consumed by the frontend React dashboard.
- Automated alert triggers (e.g. notifications dispatched on critical thresholds).
- Platform historical logging frameworks.
