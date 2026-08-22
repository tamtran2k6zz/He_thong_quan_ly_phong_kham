from sqlalchemy import Column, Integer, String, Boolean, Text, Time, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Specialty(Base):
    __tablename__ = "specialties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Relationships
    clinics = relationship("Clinic", back_populates="specialty")
    doctors = relationship("Doctor", back_populates="specialty")


class Clinic(Base):
    """Consultation Room / Clinic department"""
    __tablename__ = "clinics"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    specialty_id = Column(Integer, ForeignKey("specialties.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    specialty = relationship("Specialty", back_populates="clinics")
    doctors = relationship("Doctor", back_populates="clinic")
    appointments = relationship("Appointment", back_populates="clinic")


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    specialty_id = Column(Integer, ForeignKey("specialties.id"), nullable=False)
    clinic_id = Column(Integer, ForeignKey("clinics.id"), nullable=True)
    title = Column(String(50), nullable=True)  # e.g., "BS.CKI", "ThS.BS", "PGS.TS"
    bio = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)

    # Relationships
    user = relationship("User", back_populates="doctor_profile")
    specialty = relationship("Specialty", back_populates="doctors")
    clinic = relationship("Clinic", back_populates="doctors")
    shifts = relationship("Shift", back_populates="doctor", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="doctor")
    medical_records = relationship("MedicalRecord", back_populates="doctor")


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 0=Monday, ..., 6=Sunday
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    max_patients = Column(Integer, default=20, nullable=False)

    # Relationships
    doctor = relationship("Doctor", back_populates="shifts")
