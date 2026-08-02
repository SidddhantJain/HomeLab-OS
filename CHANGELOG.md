# Changelog

All notable changes to the HomeLab OS project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
