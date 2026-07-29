"""
HomeLab OS — Project Registry Manager

Coordinates workspace directories scan, fetches technology metadata,
and updates active project registries in database.
"""

from __future__ import annotations

import os
from sqlalchemy.orm import Session
from app.models.project import Project, ProjectMetadata
from app.services.projects.git import GitIntegrator
from app.services.projects.metadata import MetadataAnalyzer


class ProjectManager:
    """Synchronizes local directory paths with database records."""

    def __init__(self) -> None:
        self._git = GitIntegrator()
        self._analyzer = MetadataAnalyzer()

    def register_project(self, db: Session, name: str, path: str, description: Optional[str] = None) -> Project:
        """Register and inspect a local project path."""
        # Query technology details
        tech = self._analyzer.inspect_directory(path)
        git_details = self._git.get_repo_details(path)

        project = Project(
            name=name,
            description=description,
            status="ACTIVE"
        )
        db.add(project)
        db.commit()
        db.refresh(project)

        meta = ProjectMetadata(
            project_id=project.id,
            language=tech["language"],
            framework=tech["framework"],
            repository=git_details["remote_url"],
            runtime=tech["runtime"],
            storage=path
        )
        db.add(meta)
        db.commit()
        db.refresh(project)
        return project

    def get_projects(self, db: Session) -> List[Project]:
        """Fetch all registered projects."""
        return db.query(Project).filter(Project.status != "DELETED").all()

    def get_project(self, db: Session, project_id: str) -> Optional[Project]:
        """Query single project registry detail."""
        return db.query(Project).filter(Project.id == project_id).first()
