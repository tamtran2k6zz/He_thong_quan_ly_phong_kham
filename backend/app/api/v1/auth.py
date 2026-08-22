from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.audit import AuditLog
from backend.app.schemas.auth import Token, LoginRequest, UserInfo
from backend.app.schemas.user import UserResponse
from backend.app.core.security import verify_password, create_access_token
from backend.app.core.rbac import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Authenticate user with username and password, return JWT Bearer token.
    """
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản này đã bị khóa hoặc ngừng kích hoạt"
        )

    # Record login audit log
    client_ip = request.client.host if request.client else "unknown"
    audit = AuditLog(
        user_id=user.id,
        action="LOGIN",
        resource_type="User",
        resource_id=str(user.id),
        details=f"User {user.username} ({user.role}) logged in successfully",
        ip_address=client_ip
    )
    db.add(audit)
    db.commit()

    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role
    }
    access_token = create_access_token(token_data)

    return Token(
        access_token=access_token,
        token_type="bearer",
        role=user.role,
        user_id=user.id,
        username=user.username,
        full_name=user.full_name
    )


@router.post("/token", response_model=Token)
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request = None,
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login for Swagger UI.
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản này đã bị khóa"
        )

    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role
    }
    access_token = create_access_token(token_data)

    return Token(
        access_token=access_token,
        token_type="bearer",
        role=user.role,
        user_id=user.id,
        username=user.username,
        full_name=user.full_name
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Get profile information of currently authenticated user.
    """
    return current_user
