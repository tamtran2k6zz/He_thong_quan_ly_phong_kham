"""
Audit & AI Invocation Logging Router and Utilities.
Provides:
- Helper function `log_audit()` for tracking data access & modifications.
- GET /api/v1/audit/logs (Admin only): System audit trail.
- GET /api/v1/audit/ai-logs (Admin only): AI request & response logs with anonymized prompts.
"""

from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException, status, Request
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.api.deps import require_admin
from backend.app.models.user import User
from backend.app.models.audit import AuditLog, AIInvocationLog
from backend.app.schemas.audit import AuditLogResponse, AIInvocationLogResponse

router = APIRouter(prefix="/audit", tags=["Audit & Governance"])


def log_audit(
    db: Session,
    user_id: Optional[int],
    action: str,
    resource_type: str,
    resource_id: Optional[str] = None,
    details: Optional[str] = None,
    ip_address: Optional[str] = None
) -> Optional[AuditLog]:
    """
    Standard audit logger to record data access, modification, or security actions.
    """
    try:
        audit_entry = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=str(resource_id) if resource_id is not None else None,
            details=details,
            ip_address=ip_address,
            created_at=datetime.utcnow()
        )
        db.add(audit_entry)
        db.commit()
        db.refresh(audit_entry)
        return audit_entry
    except Exception:
        db.rollback()
        return None


@router.get(
    "",
    response_model=List[AuditLogResponse],
    summary="Retrieve System Audit Logs (Admin only)"
)
@router.get(
    "/logs",
    response_model=List[AuditLogResponse],
    summary="Retrieve System Audit Logs (Admin only)"
)
def get_audit_logs(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    action: Optional[str] = Query(None, description="Filter by action type (e.g. VIEW_PATIENT, LOGIN)"),
    resource_type: Optional[str] = Query(None, description="Filter by resource type"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    query = db.query(AuditLog)
    if user_id is not None:
        query = query.filter(AuditLog.user_id == user_id)
    if action:
        query = query.filter(AuditLog.action == action)
    if resource_type:
        query = query.filter(AuditLog.resource_type == resource_type)

    logs = query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
    return logs


@router.get(
    "/ai-logs",
    response_model=List[AIInvocationLogResponse],
    summary="Retrieve AI Invocation & Request Logs (Admin only)"
)
def get_ai_invocation_logs(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    feature_name: Optional[str] = Query(None, description="Filter by AI feature name"),
    model_used: Optional[str] = Query(None, description="Filter by AI model"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    query = db.query(AIInvocationLog)
    if user_id is not None:
        query = query.filter(AIInvocationLog.user_id == user_id)
    if feature_name:
        query = query.filter(AIInvocationLog.feature_name == feature_name)
    if model_used:
        query = query.filter(AIInvocationLog.model_used == model_used)

    raw_logs = query.order_by(AIInvocationLog.created_at.desc()).offset(skip).limit(limit).all()

    # Map alias fields to support multiple client consumer conventions
    response_list = []
    for log in raw_logs:
        response_list.append(
            AIInvocationLogResponse(
                id=log.id,
                user_id=log.user_id,
                feature_name=log.feature_name,
                anonymized_prompt=log.anonymized_prompt,
                prompt_raw_redacted=log.anonymized_prompt,
                prompt=log.anonymized_prompt,
                response_text=log.response_text,
                response=log.response_text,
                model_used=log.model_used,
                latency_ms=log.latency_ms,
                disclaimer_included=log.disclaimer_included,
                created_at=log.created_at,
                user=log.user
            )
        )
    return response_list
