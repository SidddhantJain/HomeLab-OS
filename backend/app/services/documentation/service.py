"""
HomeLab OS — Documentation Service

Markdown rendering, wiki indexing, and documentation searching.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List


class DocumentationService:
    """Provides internal wiki and rendered project markdown sheets."""

    def __init__(self) -> None:
        self._doc_paths = ["docs", "Documentation/Public"]

    @property
    def name(self) -> str:
        return "documentation"

    def initialize(self) -> None:
        """Startup configuration checks."""
        pass

    def shutdown(self) -> None:
        """Shutdown hook."""
        pass

    def health(self) -> Dict[str, Any]:
        """Telemetry health checks."""
        return {
            "status": "healthy",
            "message": "Documentation service is active."
        }

    # ------------------------------------------------------------------
    # Documentation Operations
    # ------------------------------------------------------------------

    def render_markdown(self, file_path: str) -> str:
        """Read and render target markdown text content."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Documentation file '{file_path}' does not exist.")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except OSError as e:
            return f"Error reading document: {e}"

    def search_docs(self, query: str) -> List[Dict[str, Any]]:
        """Index and search within public document locations."""
        results: List[Dict[str, Any]] = []
        for path in self._doc_paths:
            if not os.path.exists(path):
                continue
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".md"):
                        full_path = os.path.join(root, file)
                        try:
                            with open(full_path, "r", encoding="utf-8") as f:
                                content = f.read()
                                if query.lower() in content.lower() or query.lower() in file.lower():
                                    results.append({
                                        "title": file,
                                        "path": full_path,
                                        "snippet": content[:150] + "..."
                                    })
                        except OSError:
                            continue
        return results
