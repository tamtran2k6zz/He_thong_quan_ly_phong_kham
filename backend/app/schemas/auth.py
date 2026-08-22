from typing import Optional
from pydantic import BaseModel, ConfigDict
from backend.app.models.user import RoleEnum


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: int
    username: str
    full_name: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    username: Optional[str] = None
    role: Optional[str] = None
    exp: Optional[int] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class UserInfo(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    full_name: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
