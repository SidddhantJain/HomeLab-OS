"""
HomeLab OS — Workspace Service Initialization
"""

from app.services.workspace.service import WorkspaceService
from app.services.workspace.events import WorkspaceEvents

__all__ = ["WorkspaceService", "WorkspaceEvents"]
