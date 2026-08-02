# HomeLab OS v1.0.0 — Known Limitations

## Documented v1.0.0 Scope Boundaries
1. **Desktop Manager Native UI**: HomeLab Manager desktop backend scaffolding (`manager/backend/server_discovery.py`) is delivered; native Electron/Tauri frontend shell is scheduled for v2.0.
2. **LUKS Vault on Windows Bare-Metal**: LUKS2 container encryption requires WSL2 or Linux host kernel when running on Windows bare-metal.
3. **Emergency Hotspot Hardware**: Automatic Wi-Fi AP hotspot failover requires host Wi-Fi network interface supporting Master/Access-Point mode.
