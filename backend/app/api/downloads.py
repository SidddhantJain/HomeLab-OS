from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.downloads.service import DownloadService

router = APIRouter(prefix="/downloads", tags=["Download Manager"])


class DownloadCreate(BaseModel):
    url: str
    destination: Optional[str] = None


def get_download_service() -> DownloadService:
    return HomelabCore.instance().get_service("downloads")


@router.get("")
def list_downloads(
    db: Session = Depends(get_db),
    service: DownloadService = Depends(get_download_service)
):
    tasks = service.get_downloads(db)
    return [
        {
            "id": t.id,
            "url": t.url,
            "file_path": t.file_path,
            "status": t.status,
            "progress": t.progress,
            "total_size": t.total_size,
            "downloaded_size": t.downloaded_size,
            "created_at": t.created_at
        } for t in tasks
    ]


@router.post("")
def start_download(
    req: DownloadCreate,
    db: Session = Depends(get_db),
    service: DownloadService = Depends(get_download_service)
):
    try:
        return service.enqueue_download(db, req.url, req.destination)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
