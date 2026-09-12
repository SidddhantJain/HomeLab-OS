# Changelog

All notable changes to the HomeLab OS project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [5.0.0] - 2026-09-12 — Sovereign P2P Federation, Quantum Cryptography & Standalone .exe Installer Release

### Added
- **Sovereign P2P Federation Engine (`federation`)**: Interconnect private server clusters across trusted nodes for encrypted offsite block-level backup streams, federated media sharing, and shared storage quota management.
- **Post-Quantum Cryptography Subsystem (`quantum_crypto`)**: Kyber-1024 Key Encapsulation Mechanism (KEM) and Dilithium-5 Post-Quantum Digital Signatures securing LUKS vaults, P2P mesh links, and binary integrity checksums.
- **Local AI Multi-Agent Orchestration Framework (`ai_agents`)**: Autonomous multi-agent AI orchestration engine spawning specialized sub-agents (*System Diagnostician*, *Power/Thermal Controller*, *Zero-Trust Security Guard*, *Backup Auditor*).
- **Standalone `.exe` Setup Installer Builder (`scripts/build_windows_setup_installer.py`)**: PyInstaller & Inno Setup script creating single-click zero-dependency Windows setup installer executables (`HomeLabOS-Setup-v5.0.0.exe`).
- **PySide6 Manager Console (Module #23)**: `FederationPage` console module for P2P Federation Mesh, Post-Quantum Cryptography, and Local AI Multi-Agent tasks.
- **Full Spectrum Testing & Hardening**: 92+ backend pytest test cases, 23 PySide manager navigation pages passing, installer builder script, and pre-commit security audit.

---

## [1.5.2] - 2026-08-13 — Native Desktop Console & Telemetry Release

### Added
- **PySide6 Desktop System Tray Daemon (`manager/core/daemon.py`)**: Background server health polling service, native OS balloon notifications, system tray icon, and quick-action menu (Quick Lock LUKS Vault, Open Console, Refresh Status).
- **High-DPI Desktop Scaling & Application Metadata (`manager/main.py`)**: Enabled Qt crisp font rendering, high-DPI pixmaps, and signal binding between daemon status alerts and MainWindow activation.
- **Multi-Node Clustering Database Models (`backend/app/models/cluster.py`)**: Initial database schema scaffolding for multi-server pairings (`ClusterNode`, `NodePairingRequest`, `NodeHeartbeat`, `ClusterGroup`).
- **Closed-Source Obfuscation Build Script (`scripts/build_closed_source.py`)**: Automated build script implementing Nuitka C-extension binary compilation and PyArmor byte-code obfuscation for closed-source production releases.
- **Headless Desktop & Cluster Model Automated Test Suite (`scripts/test_pyside_manager.py`)**: Extended automated test runner verifying 13 management pages, daemon status polling, and database model instantiation.

---

## [1.0.0] - 2026-08-02 — Official Stable Release Candidate

### Added
- **Phase 1 Foundation**: Core Service Registry (`HomelabCore`), Event Bus, Server State Machines, Hardware Abstraction Layer, Telemetry metrics, JWT Authentication.
- **Phase 2 Storage & Encrypted Vault**: Mount/Unmount partition controls, SMART health diagnostics, Sparse LUKS2 Encrypted Vault container lifecycle (`LOCKED`, `UNLOCKING`, `UNLOCKED`), 24h health sweeps.
- **Phase 3 Workspace & Automation Core**: Workspace Manager, Project Intelligence, system RBAC permissions, zero-knowledge vault recovery key scaffolding, Snapshot retention, Backup service, Documentation wiki, Download manager.
- **Phase 4 Operational Intelligence & Production Readiness**: Advanced Monitoring, Multi-Channel Notifications (Email, Telegram, Webhooks, Desktop), Automation Workflow Engine, Disaster Recovery System, Docker Management, Update system, Power Management, Remote Control Layer with Terminal Sandbox and Remote File Manager.
- **Phase 5 Network Intelligence & Infrastructure Management**: Network Discovery Engine (ARP, mDNS, SSDP, DHCP, MAC Vendor lookup), Device Inventory, Friendly Device Naming, Network Topology Engine, Device Health & Alert Engine, Remote Actions (WOL, Ping, HTTP), Storage Intelligence, Intelligent Cleanup, Plugin Marketplace Foundation, Docker Application Catalog (Immich, Jellyfin, Nextcloud, Vaultwarden, Gitea, Grafana, Prometheus, Pi-hole, Home Assistant), Emergency AP Hotspot Failover (`HomeLab-Emergency-Recovery`).
- **Phase 6 Desktop & Mobile Ecosystem & UX Integration**: HomeLab Manager Desktop scaffolding (`manager/`), Multi-Server Management DB models (`ManagedServer`, `ServerGroup`, `ServerProfile`, `ServerConnection`, `ServerCertificate`), Mobile Companion APIs, Activity Timeline, Health Score Engine (0-100 gauge), Global Search, Central Settings Center, Resumable File Transfer Manager, Server Migration Assistant Wizard, API Versioning (`/api/v1/` and `/api/v2/`), 12 Architectural Specifications, 41 Pytest Backend Test Suites.
- **Dynamic Universal Cross-Platform Support**: Universal hardware and OS detection across Linux, Windows, and macOS without hardcoded machine models.
- **Production Logging & Stabilization**: Structured JSON logging (`logging.py`), complete configuration validation, official release packaging (`release/v1.0.0/`).
