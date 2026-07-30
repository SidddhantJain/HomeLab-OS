from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any
from app.core.homelab_core import HomelabCore
from app.services.documentation.service import DocumentationService

router = APIRouter(prefix="/documentation", tags=["Documentation Server"])


def get_doc_service() -> DocumentationService:
    return HomelabCore.instance().get_service("documentation")


@router.get("/render")
def render_doc(
    path: str = Query(..., description="Absolute or relative path to target markdown file"),
    service: DocumentationService = Depends(get_doc_service)
):
    try:
        content = service.render_markdown(path)
        return {"content": content}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
def search_docs(
    query: str = Query(..., min_length=1),
    service: DocumentationService = Depends(get_doc_service)
):
    return service.search_docs(query)
