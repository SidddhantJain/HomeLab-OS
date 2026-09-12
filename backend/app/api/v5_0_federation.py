from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from app.hardware.federation import federation_hal

router = APIRouter(prefix="/v5/federation", tags=["v5_0-federation"])

class PairNodeRequest(BaseModel):
    name: str
    owner: str
    ip_address: str
    shared_quota_tb: float = 5.0

class TriggerAgentTaskRequest(BaseModel):
    agent_id: str
    task_name: str

@router.get("/status")
def get_federation_status() -> Dict[str, Any]:
    """Returns status of Sovereign P2P Federation & Quantum Cryptography engine."""
    return federation_hal.get_federation_status()

@router.get("/nodes")
def list_nodes() -> List[Dict[str, Any]]:
    """Returns list of federated P2P cluster nodes."""
    return federation_hal.list_nodes()

@router.post("/nodes/pair")
def pair_node(req: PairNodeRequest) -> Dict[str, Any]:
    """Pairs a new P2P federated server node with Kyber quantum encryption."""
    return federation_hal.pair_node(
        name=req.name,
        owner=req.owner,
        ip_address=req.ip_address,
        shared_quota_tb=req.shared_quota_tb
    )

@router.get("/quantum-crypto")
def get_quantum_crypto_info() -> Dict[str, Any]:
    """Returns status of Kyber-1024 / Dilithium-5 Post-Quantum Cryptography."""
    return federation_hal.get_quantum_crypto_info()

@router.get("/ai-agents")
def list_ai_agents() -> List[Dict[str, Any]]:
    """Returns list of local AI multi-agent orchestration workers."""
    return federation_hal.list_ai_agents()

@router.post("/ai-agents/trigger")
def trigger_agent_task(req: TriggerAgentTaskRequest) -> Dict[str, Any]:
    """Triggers an autonomous task on an AI sub-agent."""
    try:
        return federation_hal.trigger_agent_task(agent_id=req.agent_id, task_name=req.task_name)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
