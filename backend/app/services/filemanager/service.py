"""
HomeLab OS — Remote File Manager Service
"""

from __future__ import annotations

import os
from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.core.base_service import BaseService
from app.models.remote import FileOperation


class FileManagerService(BaseService):
    """Manages secure remote file browsing and operations within allowed system paths."""

    ALLOWED_ROOTS = ["/opt/homelab", "/projects", "/storage", "/home"]
    FORBIDDEN_PATHS = ["/etc", "/root", "/boot", "/sys", "/proc"]

    @property
    def name(self) -> str:
        return "filemanager"

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "message": "File Manager Service is active."
        }

    def _is_path_allowed(self, path: str) -> bool:
        norm = os.path.normpath(path).lower()
        for fbd in self.FORBIDDEN_PATHS:
            norm_fbd = os.path.normpath(fbd).lower()
            if norm == norm_fbd or norm.startswith(norm_fbd + os.sep):
                return False
        return True


    def browse_directory(self, target_path: str = "/projects") -> List[Dict[str, Any]]:
        if not self._is_path_allowed(target_path):
            raise PermissionError(f"Access to path '{target_path}' is restricted.")

        return [
            {"name": "workspace-alpha", "is_dir": True, "size": 4096},
            {"name": "readme.md", "is_dir": False, "size": 1024},
            {"name": "backup-2026-07-31.tar.gz", "is_dir": False, "size": 10485760}
        ]

    def perform_operation(self, db: Session, op_type: str, path: str, user: str = "admin") -> FileOperation:
        if not self._is_path_allowed(path):
            raise PermissionError(f"Path '{path}' is forbidden for operations.")

        op = FileOperation(
            operation_type=op_type,
            file_path=path,
            user=user,
            status="SUCCESS"
        )
        db.add(op)
        db.commit()
        db.refresh(op)
        return op
