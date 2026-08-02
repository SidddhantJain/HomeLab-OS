# HomeLab OS v1.0.0 — Known Limitations

## Documented Scope Boundaries & Hardware Constraints

1. **Desktop Manager Application**: HomeLab Manager desktop backend scaffolding (`manager/backend/server_discovery.py`) is delivered; native Tauri/Electron desktop application shell is scheduled for v2.0.
2. **Mobile Companion Applications**: Mobile companion APIs are 100% functional and documented across all 15+ modules; native iOS/Android client apps are scheduled for v2.0.
3. **Cluster Federation**: Multi-node primary/secondary cluster federation is planned for v2.0.
4. **Plugin Marketplace**: Includes core framework support and curated Docker template catalogs; community package publishing will be introduced in a future release.
5. **LUKS Vault on Windows Bare-Metal**: LUKS2 container encryption requires WSL2 or a Linux host kernel when running on Windows bare-metal.
6. **Hardware Capabilities**: Hardware-specific capabilities (such as Wake-on-LAN, SMART data, thermal sensors, and power management) depend on underlying OS drivers, device support, and kernel permissions.
