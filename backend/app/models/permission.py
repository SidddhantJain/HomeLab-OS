import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from app.core.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    role_id = Column(String(36), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    resource = Column(String(100), nullable=False)  # storage, vault, workspace, projects
    action = Column(String(50), nullable=False)  # READ, WRITE, DELETE, MOUNT, UNMOUNT, BACKUP, RESTORE
    is_allowed = Column(Boolean, default=True, nullable=False)
