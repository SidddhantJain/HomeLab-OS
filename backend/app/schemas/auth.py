from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None
    role: Optional[str] = "admin"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    role: str


class UserResponse(BaseModel):
    id: str
    username: str
    email: Optional[str] = None
    role: str
    status: str
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True
