"""
HomeLab OS — Project Metadata Analyzer

Parses file layouts to auto-detect language type, framework options,
and runtime specifications.
"""

from __future__ import annotations

import os
from typing import Dict, Any


class MetadataAnalyzer:
    """Detects backend/frontend technologies in the workspace folders."""

    def __init__(self) -> None:
        pass

    def inspect_directory(self, path: str) -> Dict[str, Any]:
        """Scans the directory structure to identify projects taxonomy."""
        details = {
            "language": "unknown",
            "framework": "unknown",
            "runtime": "unknown"
        }

        if not os.path.exists(path):
            return details

        # Inspect common files
        files = os.listdir(path)
        if "package.json" in files:
            details["language"] = "Javascript/Typescript"
            details["framework"] = "React/Node"
            details["runtime"] = "Node.js"
        elif "requirements.txt" in files or "pyproject.toml" in files:
            details["language"] = "Python"
            details["framework"] = "FastAPI/Flask"
            details["runtime"] = "Python 3.12"
        elif "index.html" in files:
            details["language"] = "HTML/CSS"
            details["framework"] = "Vanilla"
            details["runtime"] = "Static"

        return details
