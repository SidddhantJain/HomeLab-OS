# HomeLab Core Framework Architecture

## Purpose

The HomeLab Core is the **central coordinator** of the HomeLab OS platform. Every service, plugin, and subsystem communicates through the Core rather than referencing one another directly. This eliminates tight coupling and enables the platform to scale from a single-server home lab to a multi-node deployment without architectural changes.

## Scope

- Owns the global **Event Bus** for inter-service communication.
- Owns the **Server State Machine** governing the platform lifecycle.
- Maintains a **Service Registry** for runtime discovery.
- Provides **Telemetry** and **Health** aggregation points.

## Design Rationale

A centralised coordinator pattern was chosen over a service mesh because:
1. HomeLab OS targets a single low-power server (Dell Inspiron 5558, 8 GB RAM). A service mesh would introduce unacceptable memory overhead.
2. All services run within a single Python process behind FastAPI, making an in-process coordinator both simpler and faster.
3. The Event Bus abstraction allows future migration to Redis Pub/Sub or NATS for multi-process deployments without changing service code.

## Architecture Diagram

```text
┌──────────────────────────────────────────────────────────┐
│                      HomeLab Core                        │
│                                                          │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│   │  Event Bus   │  │ State Machine│  │  Service      │  │
│   │  (Pub/Sub)   │  │ (Lifecycle)  │  │  Registry     │  │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│          │                 │                 │           │
├──────────┼─────────────────┼─────────────────┼───────────┤
│          ▼                 ▼                 ▼           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │ Auth Service │  │Storage Svc  │  │ Vault Svc   │      │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤      │
│  │ Project Svc  │  │Workspace Mgr│  │ Update Svc  │      │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤      │
│  │ Scheduler   │  │Notification │  │ Monitoring  │      │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤      │
│  │ Automation  │  │ Hardware Svc│  │ Plugin Mgr  │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
└──────────────────────────────────────────────────────────┘
```

## Future Extensibility

- **Multi-server mode**: Replace the in-process Event Bus with Redis Pub/Sub; services remain unchanged.
- **Plugin Marketplace**: Plugins register through the Service Registry and subscribe to events.
- **Mobile / Desktop clients**: Consume the same REST API surface backed by Core-coordinated services.

## Known Limitations

- The current implementation is a singleton within a single process. Horizontal scaling requires the Event Bus backend to be externalised.

## Relationship with Other Modules

| Module | Relationship |
|---|---|
| Event Bus | Owned by Core; used by all services |
| Server State Machine | Owned by Core; governs lifecycle |
| Service Registry | Owned by Core; enables runtime discovery |
| Telemetry Collector | Aggregates health from registered services |
| Configuration Manager | Loads YAML config consumed by services |
