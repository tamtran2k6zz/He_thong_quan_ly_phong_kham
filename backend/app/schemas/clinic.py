from datetime import time
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from backend.app.schemas.user import UserResponse


# Specialty Schemas
class SpecialtyBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class SpecialtyCreate(SpecialtyBase):
    pass


class SpecialtyUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None


class SpecialtyResponse(SpecialtyBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Clinic / Room Schemas
class ClinicBase(BaseModel):
    room_number: str
    name: str
    specialty_id: int
    is_active: bool = True


class ClinicCreate(ClinicBase):
    pass


class ClinicUpdate(BaseModel):
    room_number: Optional[str] = None
    name: Optional[str] = None
    specialty_id: Optional[int] = None
    is_active: Optional[bool] = None


class ClinicResponse(ClinicBase):
    id: int
    specialty: Optional[SpecialtyResponse] = None

    model_config = ConfigDict(from_attributes=True)


# Shift Schemas
class ShiftBase(BaseModel):
    doctor_id: int
    day_of_week: int  # 0=Mon, ..., 6=Sun
    start_time: time
    end_time: time
    max_patients: int = 20


class ShiftCreate(ShiftBase):
    pass


class ShiftUpdate(BaseModel):
    day_of_week: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    max_patients: Optional[int] = None


class ShiftResponse(ShiftBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Doctor Schemas
class DoctorBase(BaseModel):
    user_id: int
    specialty_id: int
    clinic_id: Optional[int] = None
    title: Optional[str] = "BS"
    bio: Optional[str] = None
    phone: Optional[str] = None


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    specialty_id: Optional[int] = None
    clinic_id: Optional[int] = None
    title: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None


class DoctorResponse(DoctorBase):
    id: int
    user: Optional[UserResponse] = None
    specialty: Optional[SpecialtyResponse] = None
    clinic: Optional[ClinicResponse] = None
    shifts: List[ShiftResponse] = []

    model_config = ConfigDict(from_attributes=True)
