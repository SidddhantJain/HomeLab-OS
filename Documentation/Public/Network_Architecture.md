# Network Management Center Architecture

## Overview
The Network Management Center discovers LAN devices, maintains a device inventory with friendly names, builds a topology graph, monitors device online/offline states, and provides remote device actions and emergency hotspot recovery.

## Sub-components
- **NetworkDiscoveryEngine**: ARP, mDNS, SSDP, and DHCP inspection with MAC vendor lookup.
- **NetworkTopologyEngine**: Parent-child graph node mapping (Internet -> Router -> HomeLab -> Connected Devices).
- **NetworkActionsExecutor**: Wake-on-LAN, ping, HTTP launch, and SSH triggering.
- **EmergencyHotspotManager**: Automatic emergency AP hotspot failover upon primary Wi-Fi / WAN connection loss.
- **Network API**: `/api/v1/network/devices`, `/topology`, `/actions/ping`, `/actions/wol`, `/emergency/toggle`.

## Architecture Diagram
```
Internet Connection
       │
  Main Router
       │
 ┌─────┴──────────────────┬─────────────────┐
 │                        │                 │
HomeLab Server        Storage NAS      Living Room TV
 (192.168.1.100)      (192.168.1.150)    (192.168.1.180)
```
