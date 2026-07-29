# Hardware Abstraction Layer (HAL) Design

## Purpose

The Hardware Abstraction Layer (HAL) isolates the HomeLab OS application from host-specific system commands, driver nodes, and Linux sysfs configurations. This isolation makes local development on non-Linux architectures simple while guaranteeing full, optimal hardware features when deployed on the production platform hardware (Dell Inspiron 5558 / Ubuntu 24.04).

## Scope

Exposes clean Python methods for querying:
- CPU topology and load.
- Memory and Swap usage.
- Disk usage and physical device mappings.
- Network configuration and throughput metrics.
- Laptop battery state (crucial for Inspiron 5558 deployment).
- Thermal sensors and fan control nodes.
- OS-level power state profiles (using systems like `power-profiles-ctl`).

## Architecture Interface

```text
┌─────────────────────────────────────────────────────────┐
│                     Platform Core                       │
└───────────────────────────┬─────────────────────────────┘
                            │ Queries HAL APIs
                            ▼
┌─────────────────────────────────────────────────────────┐
│              Hardware Abstraction Layer                 │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌──────────┐  │
│  │    cpu    │  │  memory   │  │  storage  │  │ network  │  │
│  ├───────────┤  ├───────────┤  ├───────────┤  ├──────────┤  │
│  │  battery  │  │   temp    │  │   power   │  │ (shims)  │  │
│  └───────────┘  └───────────┘  └───────────┘  └──────────┘  │
└───────────────────────────┬─────────────────────────────┘
                            │ System Calls / Sysfs / Procfs
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    Host OS / Drivers                    │
└─────────────────────────────────────────────────────────┘
```

## Mock & Safe Fallbacks

During execution in a local development environment (e.g. Windows/macOS where specific Linux thermal nodes and sysfs do not exist), the HAL utilizes `psutil` or falls back to mock structures instead of raising system errors or crashes. This lets backend developers build features without matching target hardware.
