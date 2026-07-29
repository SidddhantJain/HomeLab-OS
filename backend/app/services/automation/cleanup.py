"""
HomeLab OS — Cleanup Automation Tasks
"""

from __future__ import annotations

import os
import shutil


class CleanupAutomation:
    """Provides methods for clearing temporary files, expired caches, and rotated logs."""

    @staticmethod
    def clean_temp_files(temp_dir: str = "/tmp") -> int:
        """Removes temporary files under the path."""
        count = 0
        if not os.path.exists(temp_dir):
            return count

        try:
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    count += 1
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    count += 1
        except OSError:
            pass
        return count

    @staticmethod
    def rotate_logs(log_dir: str = "/var/log/homelab") -> None:
        """Rotates files ending with .log inside the target folder."""
        if not os.path.exists(log_dir):
            return

        try:
            for filename in os.listdir(log_dir):
                if filename.endswith(".log"):
                    # Simulating rotation (truncating or archiving)
                    fp = os.path.join(log_dir, filename)
                    if os.path.getsize(fp) > 10 * 1024 * 1024:  # > 10MB
                        with open(fp, "w") as f:
                            f.truncate(0)
        except OSError:
            pass
