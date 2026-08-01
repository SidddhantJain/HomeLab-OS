import hashlib
import secrets
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.token import ApiToken

router = APIRouter(prefix="/tokens", tags=["Public Platform APIs & Token Auth"])


class TokenCreateReq(BaseModel):
    name: str
    scopes: Optional[List[str]] = None


@router.get("")
def list_api_tokens(db: Session = Depends(get_db)):
    tokens = db.query(ApiToken).all()
    return [
        {
            "id": t.id,
            "name": t.name,
            "scopes": t.scopes,
            "created_at": t.created_at
        } for t in tokens
    ]


@router.post("")
def generate_api_token(req: TokenCreateReq, db: Session = Depends(get_db)):
    raw_token = f"hl_{secrets.token_hex(24)}"
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

    token_obj = ApiToken(
        name=req.name,
        token_hash=token_hash,
        scopes=req.scopes or ["read", "write"]
    )
    db.add(token_obj)
    db.commit()
    db.refresh(token_obj)

    return {
        "id": token_obj.id,
        "name": token_obj.name,
        "raw_token": raw_token,
        "warning": "Store this token securely. It will not be shown again."
    }
