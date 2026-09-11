from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.hardware.gpu_transcode import gpu_balancer

router = APIRouter(prefix="/gpu", tags=["GPU Transcode Balancer"])


@router.get("/status", response_model=Dict[str, Any])
def get_gpu_transcode_status():
    """Retrieve Intel QuickSync and NVIDIA NVENC GPU hardware metrics."""
    return gpu_balancer.get_gpu_status()


@router.post("/transcode/route")
def route_transcode_job(video_file: str, target_codec: str = "h264"):
    """Route a media transcoding job to the optimal GPU accelerator."""
    if not video_file:
        raise HTTPException(status_code=400, detail="video_file parameter is required.")
    return gpu_balancer.route_transcode_task(video_file, target_codec)
