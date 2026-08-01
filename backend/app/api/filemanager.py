from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.filemanager.service import FileManagerService

router = APIRouter(prefix="/filemanager", tags=["Remote File Manager"])


class FileOpReq(BaseModel):
    operation_type: str
    file_path: str


def get_filemanager_service() -> FileManagerService:
    return HomelabCore.instance().get_service("filemanager")


@router.get("/browse")
def browse_files(
    path: str = Query("/projects", description="Path to browse"),
    service: FileManagerService = Depends(get_filemanager_service)
):
    try:
        return service.browse_directory(path)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/operation")
def perform_file_op(
    req: FileOpReq,
    db: Session = Depends(get_db),
    service: FileManagerService = Depends(get_filemanager_service)
):
    try:
        op = service.perform_operation(db, req.operation_type, req.file_path)
        return {
            "id": op.id,
            "operation_type": op.operation_type,
            "file_path": op.file_path,
            "status": op.status
        }
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
