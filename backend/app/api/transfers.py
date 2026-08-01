from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.transfers.service import TransferService

router = APIRouter(prefix="/transfers", tags=["File Transfer Manager"])


def get_transfer_service() -> TransferService:
    return HomelabCore.instance().get_service("transfers")


@router.get("")
def list_file_transfers(
    db: Session = Depends(get_db),
    service: TransferService = Depends(get_transfer_service)
):
    transfers = service.list_transfers(db)
    return [
        {
            "id": t.id,
            "file_name": t.file_name,
            "source_path": t.source_path,
            "destination_path": t.destination_path,
            "total_bytes": t.total_bytes,
            "transferred_bytes": t.transferred_bytes,
            "status": t.status
        } for t in transfers
    ]
