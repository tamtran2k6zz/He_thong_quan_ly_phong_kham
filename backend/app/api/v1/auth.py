from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.audit import AuditLog
from backend.app.schemas.auth import Token, LoginRequest, RegisterRequest
from backend.app.schemas.user import UserResponse
from backend.app.core.security import verify_password, create_access_token, get_password_hash
from backend.app.core.rbac import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(register_data: RegisterRequest, db: Session = Depends(get_db)):
    """Receive a staff account request for administrator approval."""
    username = register_data.username.lower()
    email = register_data.email.lower()
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=409, detail="Tên đăng nhập đã được sử dụng")
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=409, detail="Email đã được sử dụng")

    user = User(
        username=username,
        email=email,
        full_name=register_data.full_name,
        hashed_password=get_password_hash(register_data.password),
        role=register_data.role,
        is_active=False,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Tên đăng nhập hoặc email đã được sử dụng")
    db.refresh(user)
    return user


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
