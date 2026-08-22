from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from backend.app.models.user import RoleEnum


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: str
    role: RoleEnum = RoleEnum.RECEPTIONIST
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
