# HomeLab OS — Master Implemented Features & Architecture Specification (v1.5.2 / v2.0)

> **Document Version**: 1.5.2-FINAL  
> **Status**: Official Master Documentation of Implemented System Features  
> **Target Scope**: Backend FastAPI Core, React Web UI, Native PySide6 Desktop Manager, Oracle VM HAL, Storage Vault & Multi-Server Ecosystem.

---

## 🏛️ 1. Platform Foundation & Core Services (`HomelabCore`)

- **Core Service Registry (`HomelabCore`)**: Centralized thread-safe singleton managing service dependency injection and lifecycle hooks across all platform domains.
- **Event Bus Subsystem (`event_bus.py`)**: Asynchronous, topic-based pub-sub event bus enabling decoupled communication between services (`storage.*`, `vault.*`, `docker.*`, `workspace.*`, `network.*`).
- **Server Finite State Machine (FSM)**: Manages lifecycle states: `STATE_INIT` ➔ `STATE_STARTING` ➔ `STATE_RUNNING` ➔ `STATE_MAINTENANCE` ➔ `STATE_DEGRADED` ➔ `STATE_SHUTDOWN`.
- **Dynamic Cross-Platform Hardware Abstraction Layer (HAL)**: Hardware detection engine supporting Linux (Ubuntu/Debian Server), Windows (WMI/Win32 APIs), and macOS without hardcoded hardware assumptions.
- **Structured JSON Production Logger (`logging.py`)**: High-throughput JSON logging engine with correlation IDs for automated log indexing and error tracing.

---

## 🔒 2. Security, Authentication & Encrypted Vault Engine

- **JWT Authentication & Token Revocation**: Secure JSON Web Token authentication with active token revocation DB storage (`TokenRevocation`).
- **Multi-Tenant Role-Based Access Control (RBAC)**: Fine-grained resource permission policies governing `ADMIN`, `DEVELOPER`, `USER`, and `GUEST` roles across storage, vault, container, and workspace resources.
- **Sparse LUKS2 Encrypted Storage Vault**:
  - Encrypted file-container vault supporting `LOCKED`, `UNLOCKING`, `UNLOCKED`, and `DEGRADED` states.
  - Automatic loop-device creation, cryptsetup LUKS2 volume mounting, zero-knowledge recovery key scaffolding, and 24h health sweeps.
- **Security Audit Log Subsystem (`audit.py`)**: Encrypted audit trail recording administrative actions, login attempts, vault unlocks, and remote command executions.

---

## 💾 3. Storage Intelligence & Drive Management

- **Partition & Storage Controller**: Mount/unmount drive controls, filesystem formatting (ext4, NTFS, Btrfs, ZFS detection), and usage telemetry.
- **S.M.A.R.T Drive Diagnostics Engine**: Real-time SMART drive health checks, temperature monitoring, bad sector count tracking, and predictive drive failure warnings.
- **Automated Storage Cleanup Engine**: Intelligent trash scrubbing, old container log pruning, and snapshot retention sweeps.

---

## 🐳 4. Docker Container Management & 1-Click App Catalog

- **Docker Container Lifecycle Engine**: Real-time container state controls (Start, Stop, Restart, Pause, Unpause, Remove), container CPU/RAM resource limits, and streaming stdout/stderr log inspector.
- **1-Click Production App Catalog (`compose_catalog.py`)**: Pre-configured production templates for:
  - **Immich** (Self-hosted photo/video backup)
  - **Jellyfin** (Media streaming server)
  - **Nextcloud** (Personal cloud storage & office)
  - **Vaultwarden** (Bitwarden-compatible password manager)
  - **Home Assistant** (Smart home automation hub)
  - **Paperless-ngx** (Document OCR & archive)
  - **Pi-hole / AdGuard** (DNS ad-blocking & filtering)
  - **Grafana & Prometheus** (System metrics & visual dashboarding)
  - **Gitea / Woodpecker** (Self-hosted Git server & CI/CD)

---

## 🖥️ 5. Oracle VM VirtualBox Hypervisor Subsystem

- **VirtualBox HAL REST API (`/api/v1/virtualbox/vms`)**:
  - Full REST management layer interfacing with Oracle VM VirtualBox.
  - Controls: Start VM (headless/gui), Pause, Resume, PowerOff, Save State, and take VM snapshots.
  - Real-time guest VM telemetry (CPU allocation, assigned RAM, storage vdi state).

---

## 🌐 6. Network Intelligence, Topology & Remote Controls

- **Network Discovery Engine**: Automated mDNS, SSDP, ARP scan, and MAC vendor resolution for zero-config LAN device discovery.
- **Network Topology & Device Inventory**: Dynamic LAN map classifying connected devices (IP, MAC, Hostname, Manufacturer, Status) with custom friendly naming.
- **Remote Action Triggers**: Integrated Wake-on-LAN (WOL) magic packet dispatcher, ICMP Ping diagnostic runner, and HTTP availability probes.
- **Cloudflare Tunnel & WireGuard Mesh Integration (`network_tunnel.py`)**: Auto-configuring secure outbound Cloudflare Tunnels and WireGuard VPN mesh overlays.
- **Emergency Access Point Hotspot Failover (`HomeLab-Emergency-Recovery`)**: Automated fallback to host AP hotspot mode if primary LAN connectivity drops.

---

## 🛠️ 7. Workspace, Remote Execution & Workflow Automation

- **Workspace & Project Intelligence Engine**: Git status tracking, automated technology stack detection (Python, Node.js, Rust, Go, C++), and directory snapshot creation.
- **Visual Workflow Builder (`workflow.py`)**: Drag-and-drop workflow execution engine based on `Trigger -> Condition -> Action` rules.
- **Tabbed Remote Terminal Sandbox (`remote.py`)**: Low-latency WebSocket SSH terminal sandbox supporting multi-session interactive shell sessions.
- **Remote File Manager & Transfer Engine**: Resumable file transfer manager (`transfers.py`) supporting upload/download pause, resume, and integrity checksum verification.

---

## 💻 8. Native PySide6 Desktop Manager Console (`manager/`)

A 13-module cross-platform native PySide6 desktop suite featuring:

| Module Page | Description |
| :--- | :--- |
| 📊 **Dashboard** | Real-time 0-100 Health Score gauge, live CPU/RAM/Disk gauges, active container counts, and server state |
| 📈 **PyQtGraph Monitoring** | High-precision non-zero hardware monitoring charts updated over delta intervals |
| 💾 **Storage Manager** | Partition table visualizer, mount/unmount triggers, and S.M.A.R.T health scores |
| 🔒 **LUKS Vault Manager** | Encrypted vault status indicator, unlock passphrase prompt, and container creation wizard |
| 🐳 **Docker Manager** | Container lifecycle controls, real-time container log viewer, and app deployment |
| 📦 **VirtualBox Manager** | VM list control, start/pause/poweroff buttons, snapshot manager, and guest state |
| 💻 **Workspace & Git** | Active code workspaces, Git branch inspector, git commit logs, and technology stack badges |
| 🌐 **Network Topology** | Graphical LAN device tree, MAC vendor badges, ping latency test, and WOL launcher |
| 🖥️ **Remote Desktop / RDP** | 1-Click RDP / VNC remote desktop connection launcher |
| 🐚 **Tabbed SSH Terminal** | Multi-tab embedded interactive SSH terminal console |
| 📁 **WinSCP File Manager** | Dual-pane remote/local file transfer UI with SFTP integration |
| ⚡ **Automation Builder** | Visual trigger-condition-action workflow rule editor |
| ⚙️ **Settings & App Store** | System configuration, API endpoint launcher, JWT token manager, and plugin app store |

---

## 📊 9. Database Architecture & Entity Schema (`backend/app/models/`)

- **User & Security**: `User`, `Permission`, `Session`, `TokenRevocation`, `AuditLog`.
- **System & Metrics**: `Metric`, `MetricsHistory`, `PowerState`, `Job`, `Update`.
- **Storage & Encrypted Vault**: `StorageDrive`, `StoragePartition`, `VaultContainer`, `Snapshot`.
- **Containers & Applications**: `DockerContainer`, `CatalogApp`, `Plugin`.
- **Workspace & Projects**: `Workspace`, `Project`, `FileTransfer`.
- **Network & Multi-Server**: `NetworkDevice`, `ServerGroup`, `ManagedServer`, `ServerProfile`, `ServerConnection`, `ServerCertificate`, `ClusterNode`.
- **Automation & Alerts**: `WorkflowRule`, `Alert`, `NotificationChannel`, `ActivityFeed`.

---
*HomeLab OS v1.5.2 / v2.0 Baseline Master Implemented Features Specification*
