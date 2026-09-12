from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.hardware.power_optimizer import power_optimizer

router = APIRouter(prefix="/power/optimizer", tags=["Autonomous Power Optimizer"])


@router.get("/metrics", response_model=Dict[str, Any])
def get_power_optimizer_metrics():
    """Retrieve thermal state, power draw, and active governor policy."""
    return power_optimizer.get_power_metrics()


@router.post("/policy/set")
def set_power_policy(policy_name: str = "SMART_DYNAMIC_SAVER"):
    """Set active power management policy (MAX_PERFORMANCE, SMART_DYNAMIC_SAVER, ECO_SOLAR_MODE)."""
    if not policy_name:
        raise HTTPException(status_code=400, detail="policy_name parameter is required.")
    return power_optimizer.set_power_policy(policy_name)
