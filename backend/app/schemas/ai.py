from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class PreVisitSummaryRequest(BaseModel):
    patient_id: Optional[int] = None
    patient_code: Optional[str] = None
    full_name: Optional[str] = None
    medical_history: Optional[str] = None
    drug_allergies: Optional[str] = None
    recent_visits_summary: Optional[str] = None


class PreVisitSummaryResponse(BaseModel):
    patient_id: int
    patient_name: str
    medical_code: str
    age: int
    gender: str
    allergies: Optional[str] = None
    medical_history: Optional[str] = None
    recent_visits_summary: str
    chronic_conditions: List[str] = []
    clinical_alerts: List[str] = []
    summary: Optional[str] = None
    content: Optional[str] = None
    disclaimer: str
    disclaimer_included: bool = True


class FAQRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None


class FAQResponse(BaseModel):
    question: str
    answer: str
    response: Optional[str] = None
    category: Optional[str] = None
    related_links: List[str] = []
    is_medical_advice_refused: bool = False
    disclaimer: str
    disclaimer_included: bool = True


class DischargeInstructionRequest(BaseModel):
    medical_record_id: Optional[int] = None
    patient_id: Optional[int] = None
    patient_name: Optional[str] = None
    diagnosis_icd10: Optional[str] = None
    diagnosis_text: Optional[str] = None
    prescriptions: Optional[List[Dict[str, Any]]] = None
    follow_up_days: Optional[int] = 7
    doctor_advice: Optional[str] = None


class DischargeInstructionResponse(BaseModel):
    medical_record_id: int
    diagnosis: str
    medication_schedule: List[Dict[str, Any]] = []
    dietary_guidelines: str
    activity_recommendations: str
    warning_signs: List[str] = []
    follow_up_advice: str
    instructions: Optional[str] = None
    content: Optional[str] = None
    disclaimer: str
    disclaimer_included: bool = True
