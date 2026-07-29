# Event Bus Architecture

## Purpose

The Event Bus provides **decoupled, asynchronous communication** between all HomeLab OS platform services. Services publish events; interested subscribers react. No service ever calls another service directly.

## Scope

- In-process publish/subscribe message dispatch.
- Glob-style pattern matching for subscriptions (e.g. `storage.*`).
- Typed event payloads via the `Event` dataclass.
- Diagnostic event log for debugging and audit purposes.

## Design Rationale

An in-process event bus was chosen over an external message broker because:
1. **Resource efficiency**: The target hardware has only 8 GB RAM. Redis Pub/Sub or RabbitMQ would consume 50–100 MB unnecessarily during early phases.
2. **Simplicity**: A single-process FastAPI application does not need network-level message passing.
3. **Upgrade path**: The `EventBus` API is designed so that the backend can be swapped to Redis Pub/Sub without changing any publisher or subscriber code.

## Event Naming Convention

Events follow a dot-delimited hierarchy:

```
<domain>.<entity>.<action>
```

Examples:
- `storage.device.mounted`
- `vault.status.unlocked`
- `scheduler.job.completed`
- `server.state_changed`
- `auth.user.logged_in`

## Event Payload Format

Every event is wrapped in the `Event` dataclass:

```python
@dataclass(frozen=True)
class Event:
    name: str                    # e.g. "storage.device.mounted"
    source: str                  # originating service name
    timestamp: datetime          # UTC creation time
    payload: dict[str, Any]      # arbitrary structured data
```

## Publishing Events

```python
from app.core.homelab_core import HomelabCore
from app.core.event_bus import Event

core = HomelabCore.instance()
core.event_bus.publish(Event(
    name="storage.device.mounted",
    source="storage_service",
    payload={"device_id": "dev-hdd-1", "mount_point": "/mnt/storage"}
))
```

## Subscribing to Events

```python
def on_storage_event(event: Event) -> None:
    print(f"Storage event: {event.name} — {event.payload}")

core.event_bus.subscribe("storage.*", on_storage_event)
```

## Future Extensibility

- **Redis Pub/Sub backend**: Replace the in-memory handler list with Redis channels.
- **Event persistence**: Write events to the `audit_logs` database table for compliance.
- **Remote event forwarding**: Relay events to the HomeLab Manager desktop application.

## Known Limitations

- Handlers execute synchronously in the publishing thread. Long-running handlers should offload work to a background task queue.
- No built-in retry or dead-letter mechanism (planned for Phase 3+).

## Relationship with Other Modules

| Module | Relationship |
|---|---|
| HomeLab Core | Owns the singleton Event Bus instance |
| All Services | Publish and subscribe to events |
| Server State Machine | Emits `server.state_changed` via the bus |
| Telemetry | Subscribes to health and metric events |
