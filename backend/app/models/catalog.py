import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, JSON
from app.core.database import Base


class AppCatalogItem(Base):
    __tablename__ = "app_catalog_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    template_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    icon_url = Column(String(255), nullable=True)
    description = Column(String(500), nullable=True)
    default_ports = Column(JSON, nullable=True)
    env_defaults = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
