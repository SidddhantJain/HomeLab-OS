from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User, UserRole, UserStatus
from app.models.audit import AuditLog
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_in.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    hashed_pwd = hash_password(user_in.password)
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hashed_pwd,
        role=user_in.role or UserRole.ADMIN.value,
        status=UserStatus.ACTIVE.value
    )
    db.add(new_user)

    # Add audit log entry
    audit = AuditLog(
        action="USER_REGISTERED",
        user=user_in.username,
        metadata_json={"role": new_user.role}
    )
    db.add(audit)
    
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    if user.status != UserStatus.ACTIVE.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    # Update last login time
    user.last_login = datetime.utcnow()
    
    # Audit log entry
    audit = AuditLog(
        action="USER_LOGIN_SUCCESS",
        user=user.username,
        metadata_json={"login_time": str(user.last_login)}
    )
    db.add(audit)
    db.commit()

    token = create_access_token(subject=user.username)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        username=user.username,
        role=user.role
    )
