from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


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


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_]+$")
    full_name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=100, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    password: str = Field(min_length=8)
    role: Literal["receptionist", "doctor", "accountant"] = "receptionist"

    @field_validator("full_name")
    @classmethod
    def clean_full_name(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Họ tên phải có ít nhất 2 ký tự")
        return value

    @field_validator("password")
    @classmethod
    def check_password_length(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Mật khẩu không được vượt quá 72 byte")
        return value


class UserInfo(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    full_name: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
