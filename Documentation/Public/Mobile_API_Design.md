# Mobile Application API Specification

## Overview
Outlines REST & WebSocket API interfaces for future Android/iOS mobile application integration.

## Endpoints
- `GET /api/v1/remote/status` (Server Uptime & Hardware Metrics)
- `POST /api/v1/remote/command` (Remote Server Commands)
- `POST /api/v1/power/wakeup` (Wake-on-LAN Trigger)
- `POST /api/v1/vault/lock` (Immediate Vault Lock)
