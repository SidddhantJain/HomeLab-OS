# Plugin System Architecture

## Purpose

The Plugin System allows third-party extensions and local modular components to integrate with the HomeLab OS platform without altering the main codebase. This makes customizing services simple and safe.

## Scope

- Scans the `plugins/` directory and parses `manifest.json` metadata.
- Validates minimum platform version compatibility.
- Coordinates plugin states (disabled, active, loaded).
- Sets up permission scopes for plugins.

## Plugin Structure

Every plugin must reside in a subdirectory of `plugins/` (categorized by function, e.g. `plugins/media/jellyfin`) and contain at least:
1. `manifest.json`: Metadata, permissions, and entrypoints.
2. Entrypoint file (e.g. `main.py` or `index.js`).

### Manifest Example (`manifest.json`)
```json
{
  "id": "jellyfin-sync",
  "name": "Jellyfin Sync",
  "version": "1.0.0",
  "description": "Synchronises local media directories with Jellyfin library scans.",
  "author": "HomeLab Team",
  "entrypoint": "main.py",
  "required_permissions": [
    "storage.read",
    "network.outbound"
  ],
  "min_core_version": "v1.0"
}
```

## Security & Permission Isolation

Plugins are assigned strict permission tokens during startup:
- `storage.read` / `storage.write`: Disk/filesystem access scope.
- `network.outbound`: Network egress boundaries.
- `system.control`: Access to host lifecycle (reboot, shutdown).
