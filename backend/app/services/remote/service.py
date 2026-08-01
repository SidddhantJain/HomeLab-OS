"""
HomeLab OS — Remote Management Service Implementation
"""

from __future__ import annotations

from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.core.base_service import BaseService
from app.services.remote.commands import RemoteCommandExecutor
from app.services.remote.security import RemoteSecurityManager
from app.services.remote.terminal import TerminalSandbox
from app.models.remote import RemoteAuditLog, RemoteCommand


class RemoteManagementService(BaseService):
    """Integrates remote sessions, execution sandboxes, and audit logging."""

    def __init__(self) -> None:
        self.cmd_executor = RemoteCommandExecutor()
        self.sec_manager = RemoteSecurityManager()
        self.terminal = TerminalSandbox()

    @property
    def name(self) -> str:
        return "remote"

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "message": "Remote Management Layer is active."
        }

    def execute_remote_command(self, db: Session, command_name: str, user: str = "admin", device: str = "remote-client") -> Dict[str, Any]:
        res = self.cmd_executor.execute_command(command_name)

        # Log remote command
        log_entry = RemoteAuditLog(
            user=user,
            device=device,
            action=f"COMMAND:{command_name}",
            result=res.get("status", "SUCCESS")
        )
        db.add(log_entry)

        cmd_entry = RemoteCommand(
            command_name=command_name,
            executed_by=user,
            status=res.get("status", "COMPLETED"),
            output=res.get("output", "")
        )
        db.add(cmd_entry)
        db.commit()

        return res
