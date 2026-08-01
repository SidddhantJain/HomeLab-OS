from fastapi import APIRouter, Depends
from typing import Dict, Any
from app.core.homelab_core import HomelabCore
from app.services.health.service import HealthService

router = APIRouter(prefix="/health", tags=["Health Center & Health Score"])


def get_health_service() -> HealthService:
    return HomelabCore.instance().get_service("health")


@router.get("/summary")
def get_health_summary(
    service: HealthService = Depends(get_health_service)
):
    return service.calculate_health_summary()
