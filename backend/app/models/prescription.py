from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), unique=True, index=True, nullable=False)  # e.g., "MED-PARA-500"
    name = Column(String(150), nullable=False, index=True)
    active_ingredient = Column(String(150), nullable=False)  # Hoạt chất
    dosage_form = Column(String(50), nullable=False)  # Viên nén, Viên nang, Siro, Gói
    unit = Column(String(30), nullable=False)  # Viên, Chai, Gói, Vỉ
    unit_price = Column(Float, default=0.0, nullable=False)  # Đơn giá VND
    stock_quantity = Column(Integer, default=0, nullable=False)  # Số lượng tồn kho
    usage_instructions = Column(Text, nullable=True)  # Hướng dẫn dùng mặc định
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    prescription_items = relationship("PrescriptionItem", back_populates="medicine")


class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    prescription_code = Column(String(30), unique=True, index=True, nullable=False)  # DT-YYYYMMDD-XXXX
    medical_record_id = Column(Integer, ForeignKey("medical_records.id"), unique=True, nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    diagnosis = Column(String(255), nullable=True)
    advice = Column(Text, nullable=True)  # Lời dặn dùng thuốc
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    medical_record = relationship("MedicalRecord", back_populates="prescription")
    items = relationship("PrescriptionItem", back_populates="prescription", cascade="all, delete-orphan")


class PrescriptionItem(Base):
    __tablename__ = "prescription_items"

    id = Column(Integer, primary_key=True, index=True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id"), nullable=False)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    dosage = Column(String(100), nullable=False)  # e.g., "1 viên"
    frequency = Column(String(100), nullable=False)  # e.g., "2 lần/ngày (sáng 1, tối 1)"
    duration_days = Column(Integer, default=5, nullable=False)
    instructions = Column(String(255), nullable=True)  # e.g., "Uống sau ăn no"

    # Relationships
    prescription = relationship("Prescription", back_populates="items")
    medicine = relationship("Medicine", back_populates="prescription_items")
