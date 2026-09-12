from fastapi import APIRouter
from typing import List, Dict, Any
from app.hardware.nvr_analytics import nvr_engine

router = APIRouter(prefix="/nvr", tags=["Frigate NVR Video Analytics"])


@router.get("/cameras", response_model=List[Dict[str, Any]])
def list_nvr_cameras():
    """List connected security camera feeds."""
    return nvr_engine.list_cameras()


@router.get("/events", response_model=List[Dict[str, Any]])
def get_nvr_ai_events():
    """Retrieve recent AI object detection events (person, car, motion)."""
    return nvr_engine.get_ai_events()
