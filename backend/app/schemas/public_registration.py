from datetime import date, time
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class PublicShift(BaseModel):
    day_of_week: int
    start_time: time
    end_time: time


class PublicDoctor(BaseModel):
    id: int
    full_name: str
    title: Optional[str] = None
    specialty: str
    shifts: List[PublicShift]


class PublicBookingRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    date_of_birth: date
    gender: str = Field(pattern=r"^(Nam|Nữ|Khác)$")
    phone: str = Field(pattern=r"^(?:0\d{9}|\+84\d{9})$")
    identity_card: Optional[str] = Field(default=None, pattern=r"^\d{12}$")
    doctor_id: int = Field(gt=0)
    appointment_date: date
    start_time: time
    reason: Optional[str] = Field(default=None, max_length=255)

    @field_validator("full_name")
    @classmethod
    def clean_full_name(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Họ tên phải có ít nhất 2 ký tự")
        return value


class PublicBookingResponse(BaseModel):
    appointment_code: str
    appointment_date: date
    start_time: time
    status: str
