from fastapi import APIRouter, Depends, Query
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.homelab_core import HomelabCore
from app.services.search.service import SearchService

router = APIRouter(prefix="/search", tags=["Global Search"])


def get_search_service() -> SearchService:
    return HomelabCore.instance().get_service("search")


@router.get("")
def execute_global_search(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    service: SearchService = Depends(get_search_service)
):
    return service.global_search(db, q)
