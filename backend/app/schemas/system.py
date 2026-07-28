from pydantic import BaseModel
from typing import Optional


class RootResponse(BaseModel):
    name: str = "HomeLab OS"
    version: str = "v1.0"
    status: str = "running"


class SystemStatusResponse(BaseModel):
    status: str = "running"
    server_name: str = "Dell Inspiron 5558"
    cpu: float = 12.5
    ram: float = 42.0
    temperature: Optional[float] = 45.0
    uptime: str = "2 days, 4 hours"
