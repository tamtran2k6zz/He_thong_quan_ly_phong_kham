from datetime import datetime, date, time
from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict
from backend.app.models.medical_record import RecordStatus
from backend.app.schemas.patient import PatientResponse
from backend.app.schemas.clinic import DoctorResponse


# Service Order Schemas
class ServiceOrderBase(BaseModel):
    service_name: str
    service_code: Optional[str] = None
    price: float = 0.0
    notes: Optional[str] = None
    result: Optional[str] = None


class ServiceOrderCreate(ServiceOrderBase):
    pass


class ServiceOrderUpdate(BaseModel):
    service_name: Optional[str] = None
    service_code: Optional[str] = None
    price: Optional[float] = None
    notes: Optional[str] = None
    result: Optional[str] = None


class ServiceOrderResponse(BaseModel):
    id: int
    medical_record_id: int
    service_name: str
    service_code: str
    price: float
    notes: Optional[str] = None
    result: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Medical Record Schemas
class MedicalRecordBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int] = None
    chief_complaint: Optional[str] = None
    symptoms: Optional[str] = None
    blood_pressure: Optional[str] = None
    heart_rate: Optional[int] = None
    temperature: Optional[float] = None
    respiratory_rate: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    bmi: Optional[float] = None
    physical_exam: Optional[str] = None
    diagnosis_icd10: Optional[str] = None
    icd10_code: Optional[str] = None
    doctor_notes: Optional[str] = None
    status: Optional[str] = RecordStatus.IN_EXAM.value


class MedicalRecordCreate(MedicalRecordBase):
    record_code: Optional[str] = None
    clinic_id: Optional[int] = None
    service_orders: Optional[List[ServiceOrderCreate]] = []


class MedicalRecordUpdate(BaseModel):
    chief_complaint: Optional[str] = None
    symptoms: Optional[str] = None
    blood_pressure: Optional[str] = None
    heart_rate: Optional[int] = None
    temperature: Optional[float] = None
    respiratory_rate: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    bmi: Optional[float] = None
    physical_exam: Optional[str] = None
    diagnosis_icd10: Optional[str] = None
    icd10_code: Optional[str] = None
    doctor_notes: Optional[str] = None
    status: Optional[str] = None


class QueueItemResponse(BaseModel):
    queue_number: int
    appointment_id: Optional[int] = None
    appointment_code: Optional[str] = None
    patient_id: int
    patient_name: str
    medical_code: str
    doctor_id: int
    doctor_name: str
    clinic_room: Optional[str] = None
    status: str
    start_time: Optional[time] = None
    appointment_date: Optional[date] = None
    reason: Optional[str] = None
    medical_record_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class MedicalRecordResponse(BaseModel):
    id: int
    record_code: str
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int] = None
    chief_complaint: Optional[str] = None
    blood_pressure: Optional[str] = None
    heart_rate: Optional[int] = None
    temperature: Optional[float] = None
    respiratory_rate: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    bmi: Optional[float] = None
    physical_exam: Optional[str] = None
    diagnosis_icd10: Optional[str] = None
    icd10_code: Optional[str] = None
    doctor_notes: Optional[str] = None
    status: str
    exam_date: datetime
    created_at: datetime
    patient: Optional[PatientResponse] = None
    doctor: Optional[DoctorResponse] = None
    service_orders: List[ServiceOrderResponse] = []

    model_config = ConfigDict(from_attributes=True)
