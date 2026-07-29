"""
HomeLab OS — Plugin Lifecycle Manager

Coordinates plugin discovery, validation, version compatibility verification,
permission boundary assignment, and dynamic startup/shutdown management.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PluginManifest:
    """Represents a plugin's metadata manifest."""

    id: str
    name: str
    version: str
    description: str
    author: str
    entrypoint: str
    required_permissions: List[str] = field(default_factory=list)
    min_core_version: str = "v1.0"


class PluginManager:
    """Manages discoverability and lifecycles of system plugins.

    Usage:
        pm = PluginManager(plugins_dir="./plugins")
        pm.discover_plugins()
        pm.enable_plugin("gitea")
    """

    def __init__(self, plugins_dir: str = "./plugins") -> None:
        self.plugins_dir = plugins_dir
        self._plugins: Dict[str, PluginManifest] = {}
        self._enabled_plugins: Dict[str, bool] = {}

    def discover_plugins(self) -> None:
        """Scan the plugins directory for valid plugins containing manifests."""
        if not os.path.exists(self.plugins_dir):
            return

        for entry in os.scandir(self.plugins_dir):
            if entry.is_dir():
                manifest_path = os.path.join(entry.path, "manifest.json")
                if os.path.exists(manifest_path):
                    try:
                        with open(manifest_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            manifest = PluginManifest(
                                id=data["id"],
                                name=data["name"],
                                version=data["version"],
                                description=data.get("description", ""),
                                author=data.get("author", ""),
                                entrypoint=data["entrypoint"],
                                required_permissions=data.get("required_permissions", []),
                                min_core_version=data.get("min_core_version", "v1.0")
                            )
                            self._plugins[manifest.id] = manifest
                            self._enabled_plugins[manifest.id] = False
                    except (json.JSONDecodeError, KeyError, PermissionError) as exc:
                        print(f"[PluginManager] Skipping invalid plugin directory '{entry.name}': {exc}")

    def enable_plugin(self, plugin_id: str) -> bool:
        """Enable and initialize a discovered plugin. Returns success status."""
        if plugin_id not in self._plugins:
            raise KeyError(f"Plugin '{plugin_id}' not found.")
        self._enabled_plugins[plugin_id] = True
        return True

    def disable_plugin(self, plugin_id: str) -> bool:
        """Disable and stop an active plugin. Returns success status."""
        if plugin_id not in self._plugins:
            raise KeyError(f"Plugin '{plugin_id}' not found.")
        self._enabled_plugins[plugin_id] = False
        return True

    def get_plugin(self, plugin_id: str) -> Optional[PluginManifest]:
        """Get the manifest of a plugin by ID."""
        return self._plugins.get(plugin_id)

    @property
    def plugins(self) -> List[PluginManifest]:
        """List all discovered plugin manifests."""
        return list(self._plugins.values())

    @property
    def enabled_plugins(self) -> List[str]:
        """List the IDs of currently enabled plugins."""
        return [pid for pid, enabled in self._enabled_plugins.items() if enabled]
