"""
HomeLab OS — Configuration Loader

Centralizes YAML configuration parsing and integrates configuration values
alongside existing Pydantic-based .env environment settings.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional


def load_yaml_config(file_path: str) -> Dict[str, Any]:
    """Parse a YAML configuration file.

    Falls back to a robust custom parser if PyYAML is not installed.
    """
    if not os.path.exists(file_path):
        return {}

    try:
        import yaml
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        # Simple line-by-line fallback parser for basic nested configurations
        return _fallback_yaml_parse(file_path)


def _fallback_yaml_parse(file_path: str) -> Dict[str, Any]:
    """Extremely basic indentation-based YAML parser fallback."""
    result: Dict[str, Any] = {}
    current_key: Optional[str] = None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.split("#")[0].strip()
                if not line or ":" not in line:
                    continue
                k, v = line.split(":", 1)
                k = k.strip()
                v = v.strip()
                if not v:
                    current_key = k
                    result[current_key] = {}
                else:
                    # Clean strings/booleans
                    if v.lower() == "true":
                        val: Any = True
                    elif v.lower() == "false":
                        val = False
                    else:
                        try:
                            val = int(v)
                        except ValueError:
                            try:
                                val = float(v)
                            except ValueError:
                                val = v.strip('"\'')
                    if current_key and line.startswith("  "):
                        result[current_key][k] = val
                    else:
                        result[k] = val
    except IOError:
        pass
    return result


class ConfigLoader:
    """Manages multi-file system configuration loads."""

    def __init__(self, config_dir: str = "./config") -> None:
        self.config_dir = config_dir
        self._configs: Dict[str, Dict[str, Any]] = {}

    def load_all(self) -> None:
        """Scan config directory and parse all configuration files."""
        if not os.path.exists(self.config_dir):
            return

        for filename in os.listdir(self.config_dir):
            if filename.endswith(".yml") or filename.endswith(".yaml"):
                name = os.path.splitext(filename)[0]
                path = os.path.join(self.config_dir, filename)
                self._configs[name] = load_yaml_config(path)

    def get(self, section: str, key: Optional[str] = None, default: Any = None) -> Any:
        """Query configurations by section and key."""
        section_data = self._configs.get(section, {})
        if key is None:
            return section_data
        return section_data.get(key, default)
