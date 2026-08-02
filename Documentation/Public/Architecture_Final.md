# HomeLab OS v1.0.0 — Final Architecture Specification

## Executive Overview
HomeLab OS v1.0.0 is an open-source, modular, event-driven personal server platform built entirely in **Python (FastAPI)** and **React**.

---

## 🏛️ System Layering & Component Architecture

```mermaid
graph TD
    Client[React Dashboard / Mobile API / Desktop Manager] --> Gateway[FastAPI Router Gateway /api/v1 & /api/v2]
    Gateway --> Auth[Auth & Security / JWT / RBAC]
    Gateway --> Core[HomelabCore Singleton Service Registry]
    Core --> EventBus[In-Memory Event Bus]
    Core --> StateEngine[Server State Machine Engine]
    Core --> HAL[Hardware Abstraction Layer]

    Core --> Storage[Storage Pool & Partition Manager]
    Core --> Vault[LUKS2 Encrypted Vault Service]
    Core --> Workspace[Workspace & Project Intelligence]
    Core --> Network[Network Discovery & Topology Engine]
    Core --> Remote[Remote Management & Terminal Sandbox]
    Core --> Health[Health Score Engine & Diagnostics]

    Storage --> DB[(PostgreSQL / SQLite Database)]
    Vault --> DB
    Workspace --> DB
    Network --> DB
```

---

## 🔑 Core Services Summary
- **HomelabCore**: Central service registry singleton managing service initialization and lifecycles.
- **EventBus**: Async pub/sub event dispatcher supporting typed event topics across all services.
- **StateEngine**: System state transition engine (`BOOTING`, `RUNNING`, `MAINTENANCE`, `EMERGENCY_RECOVERY`, `SHUTTING_DOWN`).
- **HAL Layer**: Hardware query layer dynamically reading host metrics (CPU, RAM, Temp, Network) across Linux, Windows, and macOS.
- **Storage & Vault**: Partition mounting/unmounting, SMART health checks, and Sparse LUKS encrypted vault container management.
- **Network Engine**: LAN discovery via ARP, mDNS, SSDP, DHCP inspection, topology graph generation, and device alert rules.
