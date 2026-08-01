from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.docker.service import DockerService

router = APIRouter(prefix="/docker", tags=["Docker Management"])


def get_docker_service() -> DockerService:
    return HomelabCore.instance().get_service("docker")


@router.get("/containers")
def list_docker_containers(
    db: Session = Depends(get_db),
    service: DockerService = Depends(get_docker_service)
):
    return service.list_containers(db)


@router.post("/restart/{id}")
def restart_docker_container(
    id: str,
    db: Session = Depends(get_db),
    service: DockerService = Depends(get_docker_service)
):
    return service.restart_container(db, id)


@router.get("/logs/{id}")
def get_docker_container_logs(
    id: str,
    service: DockerService = Depends(get_docker_service)
):
    return {"id": id, "logs": service.get_logs(id)}
