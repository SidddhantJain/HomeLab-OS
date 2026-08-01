from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.catalog.service import CatalogService

router = APIRouter(prefix="/catalog", tags=["Docker Application Catalog"])


def get_catalog_service() -> CatalogService:
    return HomelabCore.instance().get_service("catalog")


@router.get("")
def list_app_catalog(
    db: Session = Depends(get_db),
    service: CatalogService = Depends(get_catalog_service)
):
    return service.list_catalog_templates(db)
