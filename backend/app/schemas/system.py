from pydantic import BaseModel
from typing import Optional


class RootResponse(BaseModel):
    name: str = "HomeLab OS"
    version: str = "v1.0"
    status: str = "running"


class SystemStatusResponse(BaseModel):
    status: str = "running"
    server_name: str = "Universal HomeLab Server"
    operating_system: Optional[str] = "Linux / Windows Platform"
    cpu_model: Optional[str] = "Universal Processor"
    memory_total_gb: Optional[float] = 16.0
    cpu: float = 12.5
    ram: float = 42.0
    temperature: Optional[float] = 45.0
    uptime: str = "2 days, 4 hours"
