from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from backend.app.schemas.patient import PatientResponse
from backend.app.schemas.clinic import DoctorResponse


# Medicine Schemas
class MedicineBase(BaseModel):
    code: Optional[str] = None
    name: str
    active_ingredient: str
    dosage_form: str
    unit: str
    unit_price: float = 0.0
    stock_quantity: int = 0
    usage_instructions: Optional[str] = None
    is_active: bool = True


class MedicineCreate(MedicineBase):
    pass


class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    active_ingredient: Optional[str] = None
    dosage_form: Optional[str] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    usage_instructions: Optional[str] = None
    is_active: Optional[bool] = None


class MedicineResponse(BaseModel):
    id: int
    code: str
    name: str
    active_ingredient: str
    dosage_form: str
    unit: str
    unit_price: float
    stock_quantity: int
    usage_instructions: Optional[str] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# Prescription Item Schemas
class PrescriptionItemBase(BaseModel):
    medicine_id: int
    quantity: int = 1
    dosage: Optional[str] = "1 viên"
    frequency: Optional[str] = "2 lần/ngày"
    duration_days: Optional[int] = 5
    instructions: Optional[str] = None


class PrescriptionItemCreate(PrescriptionItemBase):
    pass


class PrescriptionItemResponse(BaseModel):
    id: int
    prescription_id: int
    medicine_id: int
    quantity: int
    dosage: str
    frequency: str
    duration_days: int
    instructions: Optional[str] = None
    medicine: Optional[MedicineResponse] = None

    model_config = ConfigDict(from_attributes=True)


# Prescription Schemas
class PrescriptionBase(BaseModel):
    medical_record_id: Optional[int] = None
    doctor_id: int
    patient_id: int
    diagnosis: Optional[str] = None
    advice: Optional[str] = None
    notes: Optional[str] = None


class PrescriptionCreate(PrescriptionBase):
    prescription_code: Optional[str] = None
    items: List[PrescriptionItemCreate] = []


class PrescriptionResponse(BaseModel):
    id: int
    prescription_code: str
    medical_record_id: int
    doctor_id: int
    patient_id: int
    diagnosis: Optional[str] = None
    advice: Optional[str] = None
    created_at: datetime
    patient: Optional[PatientResponse] = None
    doctor: Optional[DoctorResponse] = None
    items: List[PrescriptionItemResponse] = []

    model_config = ConfigDict(from_attributes=True)
