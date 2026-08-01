# Network Device Inventory Specification

## Database Model Schema
- `NetworkDevice`: IP, MAC, Hostname, Friendly Name, Vendor, Operating System, Connection Type, Last Seen, Signal Strength, Online Status.
- `NetworkInterface`: Local and remote network interfaces.
- `NetworkHistory`: Recorded device latency (ms) and packet loss (%).
- `DeviceAlias`: User-defined local friendly names.
- `NetworkEvent`: Network audit events log.
