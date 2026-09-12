from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from app.hardware.tariff_compiler import tariff_compiler_hal
from app.hardware.build_farm import build_farm_hal
from app.hardware.ai_self_fix import ai_self_fix_hal
from app.hardware.shamir_backup import shamir_backup_hal

router = APIRouter(prefix="/v3_5/compiler", tags=["v3_5-compiler"])

class ScheduleBuildRequest(BaseModel):
    name: str
    language: str = "Rust"
    estimated_time_mins: int = 30

class AISelfFixRequest(BaseModel):
    log_snippet: str
    file_path: str = "src/main.rs"

class SplitSecretRequest(BaseModel):
    secret_name: str
    threshold: int = 3
    total_shares: int = 5

class ReconstructSecretRequest(BaseModel):
    shares: List[str]

@router.get("/tariff/status")
def get_tariff_compiler_status() -> Dict[str, Any]:
    """Returns tariff-aware compiler and build cache telemetry."""
    return tariff_compiler_hal.get_compiler_status()

@router.get("/tariff/prices")
def get_energy_tariffs() -> List[Dict[str, Any]]:
    """Returns 24h spot electricity price schedule."""
    return tariff_compiler_hal.get_energy_tariffs()

@router.post("/tariff/schedule")
def schedule_deferred_build(req: ScheduleBuildRequest) -> Dict[str, Any]:
    """Schedules a compilation job during off-peak low-cost energy windows."""
    return tariff_compiler_hal.schedule_deferred_build(
        name=req.name,
        language=req.language,
        estimated_time_mins=req.estimated_time_mins
    )

@router.get("/build-farm/status")
def get_build_farm_status() -> Dict[str, Any]:
    """Returns multi-node build farm mesh telemetry."""
    return build_farm_hal.get_build_farm_status()

@router.post("/ai-self-fix/analyze")
def analyze_compiler_error(req: AISelfFixRequest) -> Dict[str, Any]:
    """Analyzes a compiler failure log and generates an AI fix patch diff."""
    return ai_self_fix_hal.analyze_compiler_error(log_snippet=req.log_snippet, file_path=req.file_path)

@router.post("/shamir/split")
def split_secret(req: SplitSecretRequest) -> Dict[str, Any]:
    """Splits a secret into k-of-n threshold Shamir shares."""
    return shamir_backup_hal.split_secret(secret_name=req.secret_name, threshold=req.threshold, total_shares=req.total_shares)

@router.post("/shamir/reconstruct")
def reconstruct_secret(req: ReconstructSecretRequest) -> Dict[str, Any]:
    """Reconstructs master secret from threshold Shamir shares."""
    try:
        return shamir_backup_hal.reconstruct_secret(shares=req.shares)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
