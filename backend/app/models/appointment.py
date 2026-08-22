import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Time, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base


class AppointmentStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CHECKED_IN = "CHECKED_IN"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    appointment_code = Column(String(30), unique=True, index=True, nullable=False)  # LH-YYYYMMDD-XXXX
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    clinic_id = Column(Integer, ForeignKey("clinics.id"), nullable=True)
    appointment_date = Column(Date, index=True, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(String(20), default=AppointmentStatus.PENDING.value, nullable=False)
    reason = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    clinic = relationship("Clinic", back_populates="appointments")
    medical_record = relationship("MedicalRecord", back_populates="appointment", uselist=False)
