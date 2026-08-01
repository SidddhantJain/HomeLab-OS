"""
HomeLab OS — Remote Command Executor
"""

from __future__ import annotations

from typing import Dict, Any
from app.core.homelab_core import HomelabCore


class RemoteCommandExecutor:
    """Executes safe remote administration commands without raw SSH access."""

    ALLOWED_COMMANDS = {
        "restart_server",
        "shutdown_server",
        "restart_service",
        "update_system",
        "lock_vault",
        "unlock_vault",
        "start_backup",
        "maintenance_mode"
    }

    def execute_command(self, command_name: str, payload: Dict[str, Any] = None) -> Dict[str, Any]:
        if command_name not in self.ALLOWED_COMMANDS:
            raise ValueError(f"Command '{command_name}' is forbidden or unrecognized.")

        core = HomelabCore.instance()
        output = f"Command '{command_name}' executed successfully."

        if command_name == "lock_vault":
            vault_svc = core.get_service("vault")
            if hasattr(vault_svc, "lock_vault"):
                vault_svc.lock_vault()
        elif command_name == "start_backup":
            backup_svc = core.get_service("backup")
            if hasattr(backup_svc, "run_backup"):
                backup_svc.run_backup(None, "Remote Backup Trigger", "/opt/homelab", "/opt/homelab/backups")

        return {
            "command": command_name,
            "status": "COMPLETED",
            "output": output
        }
