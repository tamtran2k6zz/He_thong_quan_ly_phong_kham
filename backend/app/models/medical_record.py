import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base


class RecordStatus(str, enum.Enum):
    IN_EXAM = "IN_EXAM"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class MedicalRecord(Base):
    """Medical Record / Clinical Examination Record (Phiếu khám bệnh)"""
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    record_code = Column(String(30), unique=True, index=True, nullable=False)  # KB-YYYYMMDD-XXXX
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True)
    exam_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Clinical Vitals & Examination
    chief_complaint = Column(Text, nullable=False)  # Triệu chứng chính / Lý do khám
    blood_pressure = Column(String(20), nullable=True)  # Huyết áp (e.g. "120/80 mmHg")
    heart_rate = Column(Integer, nullable=True)  # Nhịp tim bpm
    temperature = Column(Float, nullable=True)  # Nhiệt độ C
    respiratory_rate = Column(Integer, nullable=True)  # Nhịp thở
    weight = Column(Float, nullable=True)  # Cân nặng kg
    height = Column(Float, nullable=True)  # Chiều cao cm
    bmi = Column(Float, nullable=True)  # BMI
    physical_exam = Column(Text, nullable=True)  # Khám lâm sàng
    
    # Diagnosis
    diagnosis_icd10 = Column(String(255), nullable=True)  # Tên bệnh
    icd10_code = Column(String(20), nullable=True)  # Mã ICD-10 (e.g. "I10", "E11")
    doctor_notes = Column(Text, nullable=True)  # Lời dặn
    
    status = Column(String(20), default=RecordStatus.IN_EXAM.value, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    patient = relationship("Patient", back_populates="medical_records")
    doctor = relationship("Doctor", back_populates="medical_records")
    appointment = relationship("Appointment", back_populates="medical_record")
    service_orders = relationship("ServiceOrder", back_populates="medical_record", cascade="all, delete-orphan")
    prescription = relationship("Prescription", back_populates="medical_record", uselist=False, cascade="all, delete-orphan")
    invoice = relationship("Invoice", back_populates="medical_record", uselist=False)


class ServiceOrder(Base):
    """Lab order or diagnostic imaging service order (Chỉ định cận lâm sàng)"""
    __tablename__ = "service_orders"

    id = Column(Integer, primary_key=True, index=True)
    medical_record_id = Column(Integer, ForeignKey("medical_records.id"), nullable=False)
    service_name = Column(String(150), nullable=False)  # e.g., "Siêu âm bụng tổng quát"
    service_code = Column(String(30), nullable=False)  # e.g., "SA-BUNG-01"
    price = Column(Float, default=0.0, nullable=False)
    notes = Column(Text, nullable=True)
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    medical_record = relationship("MedicalRecord", back_populates="service_orders")
