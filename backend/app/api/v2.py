from fastapi import APIRouter

router = APIRouter(prefix="/v2", tags=["API v2 Gateway"])


@router.get("/status")
def get_v2_status():
    return {
        "version": "2.0.0-alpha",
        "compatibility": "v1_forward_compatible",
        "status": "active"
    }
