from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.app.database import get_db
from backend.app.models.user import User, RoleEnum
from backend.app.schemas.user import UserCreate, UserUpdate, UserResponse
from backend.app.core.security import get_password_hash
from backend.app.api.deps import require_admin

router = APIRouter(prefix="/users", tags=["Users Management (Admin Only)"])


@router.get("", response_model=List[UserResponse])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    role: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """
    Get all users with filtering by role and keyword search. (Admin only)
    """
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                User.username.ilike(search_filter),
                User.full_name.ilike(search_filter),
                User.email.ilike(search_filter)
            )
        )
    return query.offset(skip).limit(limit).all()


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """
    Create a new user account. (Admin only)
    """
    existing_user = db.query(User).filter(User.username == user_in.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tên đăng nhập '{user_in.username}' đã tồn tại trong hệ thống"
        )
    
    if user_in.email:
        existing_email = db.query(User).filter(User.email == user_in.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{user_in.email}' đã được sử dụng"
            )

    new_user = User(
        username=user_in.username,
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role.value if hasattr(user_in.role, 'value') else str(user_in.role),
        is_active=user_in.is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """
    Get user details by ID. (Admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy người dùng"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """
    Update user information and roles. (Admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy người dùng"
        )

    if user_in.email is not None and user_in.email != user.email:
        existing_email = db.query(User).filter(User.email == user_in.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{user_in.email}' đã được sử dụng bởi tài khoản khác"
            )
        user.email = user_in.email

    if user_in.full_name is not None:
        user.full_name = user_in.full_name
    if user_in.role is not None:
        user.role = user_in.role.value if hasattr(user_in.role, 'value') else str(user_in.role)
    if user_in.is_active is not None:
        user.is_active = user_in.is_active
    if user_in.password:
        user.hashed_password = get_password_hash(user_in.password)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """
    Deactivate or remove a user account. (Admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy người dùng"
        )
    if user.id == admin_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không thể tự xóa tài khoản quản trị viên đang đăng nhập"
        )
    
    # Soft delete / deactivation preferred or hard delete
    user.is_active = False
    db.commit()
    return {"message": f"Người dùng {user.username} đã được vô hiệu hóa thành công"}
