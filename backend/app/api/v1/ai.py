"""
AI Router for Administrative AI Assistant.
Endpoints:
- POST /api/v1/ai/pre-visit-summary (and /pre-visit-summary/{patient_id})
- POST /api/v1/ai/faq
- POST /api/v1/ai/discharge-instructions (and /discharge-instructions/{medical_record_id})
"""

from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.api.deps import require_clinical_staff, require_doctor
from backend.app.core.rbac import get_current_user, oauth2_scheme
from backend.app.core.security import decode_access_token
from backend.app.models.user import User
from backend.app.schemas.ai import (
    PreVisitSummaryRequest,
    PreVisitSummaryResponse,
    FAQRequest,
    FAQResponse,
    DischargeInstructionRequest,
    DischargeInstructionResponse,
)
from backend.app.ai_engine.service import admin_ai_service

router = APIRouter(prefix="/ai", tags=["Administrative AI Assistant"])


def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Helper to extract user if token is provided, without raising 401 for public/guest FAQ access."""
    if not token:
        return None
    try:
        payload = decode_access_token(token)
        if not payload:
            return None
        user_id_str = payload.get("sub")
        if not user_id_str:
            return None
        user_id = int(user_id_str)
        return db.query(User).filter(User.id == user_id).first()
    except Exception:
        return None


# ---------------------------------------------------------------------------
# 1. Pre-visit Briefing Tool
# ---------------------------------------------------------------------------

@router.post(
    "/pre-visit-summary",
    response_model=PreVisitSummaryResponse,
    summary="Generate Pre-visit Patient History Briefing for Doctors"
)
def generate_pre_visit_summary(
    payload: PreVisitSummaryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinical_staff)
):
    patient_id = payload.patient_id
    patient_dict = payload.model_dump()
    result = admin_ai_service.generate_pre_visit_summary(
        patient_id=patient_id,
        patient_data=patient_dict,
        db=db,
        user_id=current_user.id
    )
    return result


@router.post(
    "/pre-visit-summary/{patient_id}",
    response_model=PreVisitSummaryResponse,
    summary="Generate Pre-visit Summary by Patient ID"
)
def generate_pre_visit_summary_by_id(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinical_staff)
):
    result = admin_ai_service.generate_pre_visit_summary(
        patient_id=patient_id,
        patient_data=None,
        db=db,
        user_id=current_user.id
    )
    return result


# ---------------------------------------------------------------------------
# 2. Clinic Workflow FAQ Chatbot
# ---------------------------------------------------------------------------

@router.post(
    "/faq",
    response_model=FAQResponse,
    summary="Clinic Workflow & Procedures FAQ Chatbot"
)
def answer_clinic_faq(
    payload: FAQRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    user_id = current_user.id if current_user else None
    result = admin_ai_service.answer_faq(
        question=payload.question,
        db=db,
        user_id=user_id,
        conversation_id=payload.conversation_id
    )
    return result


# ---------------------------------------------------------------------------
# 3. Post-visit Discharge Instructions Tool
# ---------------------------------------------------------------------------

@router.post(
    "/discharge-instructions",
    response_model=DischargeInstructionResponse,
    summary="Generate Post-visit Discharge Instructions & Medication Schedule"
)
def generate_discharge_instructions(
    payload: DischargeInstructionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_doctor)
):
    record_id = payload.medical_record_id
    discharge_dict = payload.model_dump()
    result = admin_ai_service.generate_discharge_instructions(
        medical_record_id=record_id,
        discharge_data=discharge_dict,
        db=db,
        user_id=current_user.id
    )
    return result


@router.post(
    "/discharge-instructions/{medical_record_id}",
    response_model=DischargeInstructionResponse,
    summary="Generate Post-visit Discharge Instructions by Medical Record ID"
)
def generate_discharge_instructions_by_id(
    medical_record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_doctor)
):
    result = admin_ai_service.generate_discharge_instructions(
        medical_record_id=medical_record_id,
        discharge_data=None,
        db=db,
        user_id=current_user.id
    )
    return result
