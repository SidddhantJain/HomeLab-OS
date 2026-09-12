"""
HAL — Smart NVR Camera Video Analytics Pipeline (Frigate AI).

Manages security camera stream feeds and local AI object detection (person, car, motion)
with real-time alert dispatching.
"""

from __future__ import annotations
import time
from typing import Dict, Any, List


class FrigateNVRAnalyticsEngine:
    """Smart NVR Video Analytics HAL."""

    def __init__(self):
        self._cameras = [
            {"camera_id": "cam-front-door", "name": "Front Porch 4K", "resolution": "3840x2160", "fps": 25, "status": "RECORDING 🟢"},
            {"camera_id": "cam-driveway", "name": "Driveway Wide", "resolution": "1920x1080", "fps": 30, "status": "RECORDING 🟢"},
            {"camera_id": "cam-backyard", "name": "Backyard Garden", "resolution": "1920x1080", "fps": 30, "status": "RECORDING 🟢"}
        ]

    def list_cameras(self) -> List[Dict[str, Any]]:
        """Return connected security camera inventory."""
        return self._cameras

    def get_ai_events(self) -> List[Dict[str, Any]]:
        """Return recent AI object detection events."""
        return [
            {
                "event_id": "evt-ai-991",
                "camera_id": "cam-front-door",
                "camera_name": "Front Porch 4K",
                "label": "person",
                "confidence": 0.96,
                "timestamp": "12 mins ago",
                "snapshot_url": "/api/v1/nvr/snapshots/evt-ai-991.jpg"
            },
            {
                "event_id": "evt-ai-988",
                "camera_id": "cam-driveway",
                "camera_name": "Driveway Wide",
                "label": "car",
                "confidence": 0.92,
                "timestamp": "45 mins ago",
                "snapshot_url": "/api/v1/nvr/snapshots/evt-ai-988.jpg"
            }
        ]


nvr_engine = FrigateNVRAnalyticsEngine()
