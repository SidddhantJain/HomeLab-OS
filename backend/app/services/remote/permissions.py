"""
HomeLab OS — Remote Permission Model
"""

from typing import Set, Dict


class RemotePermissionModel:
    """Evaluates remote action permissions based on role hierarchy."""

    ROLE_PERMISSIONS: Dict[str, Set[str]] = {
        "REMOTE_VIEWER": {"VIEW_STATUS"},
        "REMOTE_OPERATOR": {"VIEW_STATUS", "RUN_COMMAND", "ACCESS_TERMINAL", "MANAGE_FILES"},
        "REMOTE_ADMIN": {"VIEW_STATUS", "RUN_COMMAND", "ACCESS_TERMINAL", "MANAGE_FILES", "SHUTDOWN_SERVER", "UPDATE_SYSTEM"}
    }

    @classmethod
    def is_permitted(cls, role: str, permission: str) -> bool:
        allowed = cls.ROLE_PERMISSIONS.get(role, set())
        return permission in allowed
