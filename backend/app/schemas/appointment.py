from datetime import date, time, datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from backend.app.models.appointment import AppointmentStatus
from backend.app.schemas.patient import PatientResponse
from backend.app.schemas.clinic import DoctorResponse, ClinicResponse


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    clinic_id: Optional[int] = None
    appointment_date: date
    start_time: time
    end_time: time
    reason: Optional[str] = None
    notes: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    appointment_code: Optional[str] = None
    status: Optional[str] = AppointmentStatus.PENDING.value


class AppointmentUpdate(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    clinic_id: Optional[int] = None
    appointment_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    status: Optional[str] = None
    reason: Optional[str] = None
    notes: Optional[str] = None


class AppointmentStatusUpdate(BaseModel):
    status: str


class AppointmentResponse(AppointmentBase):
    id: int
    appointment_code: str
    status: str
    created_at: datetime
    patient: Optional[PatientResponse] = None
    doctor: Optional[DoctorResponse] = None
    clinic: Optional[ClinicResponse] = None

    model_config = ConfigDict(from_attributes=True)


class AvailableSlotResponse(BaseModel):
    start_time: str
    end_time: str
    is_available: bool
    conflict_reason: Optional[str] = None
