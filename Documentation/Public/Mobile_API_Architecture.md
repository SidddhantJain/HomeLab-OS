# Mobile Companion API Architecture

## Overview
Exposes REST endpoints for future mobile companion client applications (Android/iOS).

## Supported Modules
- **Authentication**: JWT token login & session tracking (`/api/v1/auth`).
- **Monitoring & Telemetry**: System status, CPU, RAM, Network (`/api/v1/monitoring`).
- **Alerts**: Multi-channel notification rules (`/api/v1/alerts`).
- **Remote Control**: Terminal commands and remote file operations (`/api/v1/remote`).
- **Synchronization**: Offline preference & server profile sync (`/api/v1/sync`).
