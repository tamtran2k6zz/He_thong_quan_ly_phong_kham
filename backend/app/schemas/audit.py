from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from backend.app.schemas.user import UserResponse


class AuditLogBase(BaseModel):
    user_id: Optional[int] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    details: Optional[str] = None
    ip_address: Optional[str] = None


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogResponse(AuditLogBase):
    id: int
    created_at: datetime
    user: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)


class AIInvocationLogBase(BaseModel):
    user_id: Optional[int] = None
    feature_name: str
    anonymized_prompt: str
    response_text: str
    model_used: str
    latency_ms: int = 0
    disclaimer_included: bool = True


class AIInvocationLogCreate(AIInvocationLogBase):
    pass


class AIInvocationLogResponse(AIInvocationLogBase):
    id: int
    created_at: datetime
    user: Optional[UserResponse] = None
    prompt_raw_redacted: Optional[str] = None
    prompt: Optional[str] = None
    response: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
