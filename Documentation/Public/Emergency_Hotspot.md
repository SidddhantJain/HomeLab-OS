# Emergency Hotspot Recovery Architecture

## Overview
Monitors primary Wi-Fi / WAN network interfaces. When primary connectivity is lost, HomeLab OS automatically enables a local Wi-Fi Access Point (AP) hotspot (`HomeLab-Emergency-Recovery`) so users can access local server administration without network hardware access.

## Operations
- Automatic activation upon connection loss.
- Automatic deactivation upon primary Wi-Fi / WAN restoration.
- Configurable SSID, passphrase, and timeout duration.
