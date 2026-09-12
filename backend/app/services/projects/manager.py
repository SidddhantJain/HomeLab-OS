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

    def auto_scan_workspace_dir(self, db: Session, root_path: str = None) -> List[Project]:
        """Auto-scan root projects directory and register all sub-projects."""
        if not root_path:
            if os.path.exists(r"D:\Siddhant\projects"):
                root_path = r"D:\Siddhant\projects"
            elif os.path.exists("/home/server/projects"):
                root_path = "/home/server/projects"
            else:
                root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

        if not os.path.exists(root_path):
            return self.get_projects(db)

        existing_paths = {p.metadata_rel.storage: p for p in self.get_projects(db) if p.metadata_rel and p.metadata_rel.storage}
        existing_names = {p.name for p in self.get_projects(db)}

        for item in os.listdir(root_path):
            full_path = os.path.join(root_path, item)
            if os.path.isdir(full_path) and not item.startswith("."):
                if full_path not in existing_paths and item not in existing_names:
                    desc = f"Auto-registered workspace project: {item}"
                    self.register_project(db, name=item, path=full_path, description=desc)

        return self.get_projects(db)

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
            language=tech.get("language", "Python"),
            framework=tech.get("framework", "FastAPI/Vite"),
            repository=git_details.get("remote_url", "https://github.com/SidddhantJain/HomeLab-OS.git"),
            runtime=tech.get("runtime", "python3"),
            storage=path
        )
        db.add(meta)
        db.commit()
        db.refresh(project)
        return project

    def get_projects(self, db: Session) -> List[Project]:
        """Fetch all registered projects, auto-scanning if DB empty."""
        projects = db.query(Project).filter(Project.status != "DELETED").all()
        if not projects:
            return self.auto_scan_workspace_dir(db)
        return projects

    def get_project(self, db: Session, project_id: str) -> Optional[Project]:
        """Query single project registry detail."""
        return db.query(Project).filter(Project.id == project_id).first()

