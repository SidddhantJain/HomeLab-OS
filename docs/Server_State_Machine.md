# Server State Machine Design

## Purpose

The Server State Machine defines the **formal lifecycle** of the HomeLab OS deployment server. All services observe the current state and react accordingly, replacing ad-hoc boolean flags with a single, authoritative source of truth.

## Scope

- Enumerates all valid server states.
- Enforces transition rules (invalid transitions raise `ValueError`).
- Notifies registered listeners on every state change.
- Maintains an auditable transition history.

## State Diagram

```text
                         ┌──────────┐
                    ┌───►│ OFFLINE  │◄──────────────────────┐
                    │    └────┬─────┘                       │
                    │         │                             │
                    │         ▼                             │
                    │    ┌──────────┐                       │
                    │    │ BOOTING  │                       │
                    │    └────┬─────┘                       │
                    │         │                             │
                    │         ▼                             │
                    │    ┌──────────┐                       │
                    ├────│ STARTING │                       │
                    │    └────┬─────┘                       │
                    │         │                             │
                    │         ▼                             │
                    │    ┌──────────┐                       │
                    │    │ RUNNING  │◄────────────┐         │
                    │    └──┬─┬─┬─┬─┘            │         │
                    │       │ │ │ │               │         │
                    │       │ │ │ └──► BACKUP ────┘         │
                    │       │ │ └────► UPDATING ──► RESTORING
                    │       │ └──────► MAINTENANCE─┘        │
                    │       │                               │
                    │       ▼                               │
                    │    SHUTTING_DOWN ──────────────────────┘
                    └────────────────────────────────────────
```

## Transition Rules

| From | Allowed Targets |
|---|---|
| `BOOTING` | `STARTING`, `OFFLINE` |
| `STARTING` | `RUNNING`, `OFFLINE` |
| `RUNNING` | `MAINTENANCE`, `BACKUP`, `UPDATING`, `SHUTTING_DOWN` |
| `MAINTENANCE` | `RUNNING`, `SHUTTING_DOWN` |
| `BACKUP` | `RUNNING`, `SHUTTING_DOWN` |
| `UPDATING` | `RUNNING`, `RESTORING`, `SHUTTING_DOWN` |
| `RESTORING` | `RUNNING`, `SHUTTING_DOWN` |
| `SHUTTING_DOWN` | `OFFLINE` |
| `OFFLINE` | `BOOTING` |

## Design Rationale

A finite state machine was chosen because:
1. It makes impossible states unrepresentable — services cannot accidentally set the server to an illegal combination.
2. Transition listeners allow the Event Bus to broadcast `server.state_changed` events automatically.
3. The auditable history supports compliance and post-incident analysis.

## Integration with Event Bus

Every state transition emits a `server.state_changed` event:

```python
Event(
    name="server.state_changed",
    source="homelab_core",
    payload={"previous": "STARTING", "current": "RUNNING"}
)
```

## Future Extensibility

- **Conditional transitions**: Add guard functions that must return `True` before a transition is allowed (e.g. "all backup jobs must finish before SHUTTING_DOWN").
- **Distributed state**: Synchronise state across multiple HomeLab nodes via the Event Bus.

## Known Limitations

- Single-server only. Multi-node consensus is not yet implemented.

## Relationship with Other Modules

| Module | Relationship |
|---|---|
| HomeLab Core | Owns the State Machine instance |
| Event Bus | Receives `server.state_changed` events |
| Scheduler | Pauses jobs during MAINTENANCE, BACKUP, UPDATING |
| Monitoring | Reports server state to the Dashboard |
