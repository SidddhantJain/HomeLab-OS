# HomeLab Manager Desktop Roadmap

## Purpose

HomeLab Manager is the planned cross-platform desktop application (Windows, macOS, Linux) that will serve as the hardware administrator controller, vault key distributor, and emergency rescue console for HomeLab OS server nodes.

## Core Capabilities

1. **Local Vault Key Delivery**: Securely uploads Master Keys and encryption files to the HomeLab node over local TLS without sending keys through external proxies.
2. **Network Discovery**: Scans local subnets for active HomeLab server installations using mDNS/zero-configuration multicast DNS.
3. **Rescue Console**: Connects via serial/SSH/HTTP/TCP direct interfaces to restore server states, restart frozen system containers, and fix configuration errors during offline windows.
4. **Hardware Monitoring**: Integrates sensor metrics, warning lights, and power profiles into native desktop system tray notifications.

## Technology Options

- **Tauri + React + Rust**: Highly recommended for its small footprint, native desktop integrations, and high performance.
- **Electron + React**: A solid alternative, though it has a larger footprint.
- **Golang (Fyne/Wails)**: A lightweight alternative if Rust is not preferred.

## Roadmap Phases

- **Phase 1: Zero-Config Discovery**: Integrate local network subnet pinging, mDNS discovery, and basic status displays.
- **Phase 2: Vault Operations**: Setup LUKS remote unlocking keys, backup retrieval triggers, and master seed storage.
- **Phase 3: Host Diagnostics**: Connect SSH shells directly to Docker containers and local log views.
