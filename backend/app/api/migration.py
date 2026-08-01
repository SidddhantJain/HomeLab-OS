from fastapi import APIRouter, Depends
from typing import Dict, Any
from app.core.homelab_core import HomelabCore
from app.services.migration.service import MigrationService

router = APIRouter(prefix="/migration", tags=["Server Migration Assistant"])


def get_migration_service() -> MigrationService:
    return HomelabCore.instance().get_service("migration")


@router.get("/export")
def export_platform_config(
    service: MigrationService = Depends(get_migration_service)
):
    return service.export_platform_config()
