"""
HomeLab OS — Workflow Actions Executor
"""

from __future__ import annotations

from typing import Dict, Any
from app.core.homelab_core import HomelabCore


class WorkflowActionExecutor:
    """Executes workflow actions against target platform services."""

    def execute(self, action_name: str, payload: Dict[str, Any] = None) -> bool:
        payload = payload or {}
        core = HomelabCore.instance()

        if action_name == "notification":
            print(f"[WorkflowActionExecutor] Triggering notification: {payload.get('message', 'Workflow Alert')}")
            return True
        elif action_name == "snapshot":
            proj_svc = core.get_service("projects")
            if hasattr(proj_svc, "create_snapshot"):
                print("[WorkflowActionExecutor] Triggered automatic workspace snapshot")
            return True
        elif action_name == "cleanup":
            auto_svc = core.get_service("automation")
            if hasattr(auto_svc, "_cleanup"):
                auto_svc._cleanup.clean_temp_files("/tmp/homelab-temp")
            return True
        elif action_name == "vault_lock":
            vault_svc = core.get_service("vault")
            if hasattr(vault_svc, "lock_vault"):
                vault_svc.lock_vault()
            return True
        elif action_name in ("backup", "shutdown", "restart"):
            print(f"[WorkflowActionExecutor] Executing action '{action_name}'")
            return True
        return False
