from datetime import date, datetime
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, model_validator


class PatientBase(BaseModel):
    full_name: str
    date_of_birth: Optional[date] = None
    dob: Optional[date] = None
    gender: str = "Nam"  # "Nam", "Nữ", "Khác", "MALE", "FEMALE"
    phone: str
    identity_card: Optional[str] = None  # CCCD 12 digits
    address: Optional[str] = None
    insurance_number: Optional[str] = None  # BHYT 15 chars
    medical_history: Optional[str] = None
    drug_allergies: Optional[str] = None
    emergency_contact: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def normalize_fields(cls, data: Any):
        if isinstance(data, dict):
            if "dob" in data and not data.get("date_of_birth"):
                data["date_of_birth"] = data["dob"]
            elif "date_of_birth" in data and not data.get("dob"):
                data["dob"] = data["date_of_birth"]
        return data


class PatientCreate(PatientBase):
    medical_code: Optional[str] = None  # Auto-generated if not provided


class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    identity_card: Optional[str] = None
    address: Optional[str] = None
    insurance_number: Optional[str] = None
    medical_history: Optional[str] = None
    drug_allergies: Optional[str] = None
    emergency_contact: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def normalize_fields(cls, data: Any):
        if isinstance(data, dict):
            if "dob" in data and not data.get("date_of_birth"):
                data["date_of_birth"] = data["dob"]
            elif "date_of_birth" in data and not data.get("dob"):
                data["dob"] = data["date_of_birth"]
        return data


class PatientResponse(PatientBase):
    id: int
    medical_code: str
    date_of_birth: date
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
