"""
HomeLab OS — Workspace Permissions Guard
"""

from __future__ import annotations

from sqlalchemy.orm import Session
from app.core.permissions import PermissionModel


def check_workspace_permission(db: Session, username: str, role: str, action: str) -> bool:
    """Wrapper checking role authorization parameters for workspace targets."""
    return PermissionModel.check_permission(db, username, role, "workspace", action)
