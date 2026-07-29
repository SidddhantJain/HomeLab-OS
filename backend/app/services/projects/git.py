"""
HomeLab OS — Project Git Repository Integrator

Parses repo config profiles, linking with external git remotes.
"""

from __future__ import annotations

import subprocess
from typing import Dict, Any


class GitIntegrator:
    """Manages workspace git tracking and commits validation."""

    def __init__(self) -> None:
        pass

    def get_repo_details(self, path: str) -> Dict[str, Any]:
        """Query host git properties of the directory path."""
        try:
            # Query branch
            branch = subprocess.run(
                ["git", "-C", path, "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True, text=True, check=False
            ).stdout.strip()
            
            # Query origin url
            remote_url = subprocess.run(
                ["git", "-C", path, "config", "--get", "remote.origin.url"],
                capture_output=True, text=True, check=False
            ).stdout.strip()

            return {
                "branch": branch or "main",
                "remote_url": remote_url or "local-only",
                "is_repo": bool(branch)
            }
        except Exception:
            return {"branch": "main", "remote_url": "local-only", "is_repo": False}
