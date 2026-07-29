"""
HomeLab OS — Role-Based Access Control (RBAC) Permission Model

Governs access policies across platform boundaries (storage, vault, workspace, projects).
"""

from __future__ import annotations

import enum
from typing import Optional, List, Dict
from sqlalchemy.orm import Session

from app.models.permission import Role, Permission
from app.models.audit import AuditLog
from app.core.homelab_core import HomelabCore
from app.core.event_bus import Event


class SystemRole(str, enum.Enum):
    ADMIN = "ADMIN"
    DEVELOPER = "DEVELOPER"
    USER = "USER"
    GUEST = "GUEST"


class ActionType(str, enum.Enum):
    READ = "READ"
    WRITE = "WRITE"
    DELETE = "DELETE"
    MOUNT = "MOUNT"
    UNMOUNT = "UNMOUNT"
    BACKUP = "BACKUP"
    RESTORE = "RESTORE"


class PermissionModel:
    """Manages role-based policy maps and evaluates resource access queries."""

    @staticmethod
    def initialize_default_roles_and_permissions(db: Session) -> None:
        """Seed default roles and access policies into the database if missing."""
        # Seed Roles
        role_map: Dict[str, Role] = {}
        for r_enum in SystemRole:
            role = db.query(Role).filter(Role.name == r_enum.value).first()
            if not role:
                role = Role(name=r_enum.value, description=f"Default {r_enum.value} system role.")
                db.add(role)
                db.commit()
                db.refresh(role)
            role_map[r_enum.value] = role

        # Seed default policies if no permission exists
        if db.query(Permission).count() == 0:
            default_policies = [
                # Admin has full access to all resources
                (SystemRole.ADMIN, "storage", ActionType.READ),
                (SystemRole.ADMIN, "storage", ActionType.WRITE),
                (SystemRole.ADMIN, "storage", ActionType.DELETE),
                (SystemRole.ADMIN, "storage", ActionType.MOUNT),
                (SystemRole.ADMIN, "storage", ActionType.UNMOUNT),
                (SystemRole.ADMIN, "storage", ActionType.BACKUP),
                (SystemRole.ADMIN, "storage", ActionType.RESTORE),
                (SystemRole.ADMIN, "vault", ActionType.READ),
                (SystemRole.ADMIN, "vault", ActionType.WRITE),
                (SystemRole.ADMIN, "workspace", ActionType.READ),
                (SystemRole.ADMIN, "workspace", ActionType.WRITE),
                (SystemRole.ADMIN, "projects", ActionType.READ),
                (SystemRole.ADMIN, "projects", ActionType.WRITE),

                # Developer access
                (SystemRole.DEVELOPER, "storage", ActionType.READ),
                (SystemRole.DEVELOPER, "workspace", ActionType.READ),
                (SystemRole.DEVELOPER, "workspace", ActionType.WRITE),
                (SystemRole.DEVELOPER, "projects", ActionType.READ),
                (SystemRole.DEVELOPER, "projects", ActionType.WRITE),

                # User access
                (SystemRole.USER, "storage", ActionType.READ),
                (SystemRole.USER, "workspace", ActionType.READ),

                # Guest access
                (SystemRole.GUEST, "storage", ActionType.READ),
            ]

            for r_val, res, act in default_policies:
                p = Permission(
                    role_id=role_map[r_val.value].id,
                    resource=res,
                    action=act.value,
                    is_allowed=True
                )
                db.add(p)
            db.commit()

    @staticmethod
    def check_permission(db: Session, username: str, role_name: str, resource: str, action: str) -> bool:
        """Evaluate if the specified role is permitted to perform action on resource."""
        # Setup defaults if database is not seeded
        PermissionModel.initialize_default_roles_and_permissions(db)

        role = db.query(Role).filter(Role.name == role_name.upper()).first()
        if not role:
            return False

        # Query explicit permission rule
        perm = db.query(Permission).filter(
            Permission.role_id == role.id,
            Permission.resource == resource,
            Permission.action == action.upper()
        ).first()

        core = HomelabCore.instance()
        is_allowed = perm.is_allowed if perm else False

        if not is_allowed:
            # Audit denied event
            core.event_bus.publish(
                Event(
                    name="permission.denied",
                    source="permissions_engine",
                    payload={"user": username, "resource": resource, "action": action}
                )
            )
        else:
            # Audit granted event
            core.event_bus.publish(
                Event(
                    name="permission.granted",
                    source="permissions_engine",
                    payload={"user": username, "resource": resource, "action": action}
                )
            )

        return is_allowed
