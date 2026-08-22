from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, Text
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    medical_code = Column(String(30), unique=True, index=True, nullable=False)  # BN-YYYYMMDD-XXXX
    full_name = Column(String(100), nullable=False, index=True)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)  # "Nam", "Nữ", "Khác"
    phone = Column(String(20), nullable=False, index=True)
    identity_card = Column(String(20), unique=True, nullable=True, index=True)  # CCCD 12 digits
    address = Column(String(255), nullable=True)
    insurance_number = Column(String(25), nullable=True, index=True)  # BHYT 15 chars
    medical_history = Column(Text, nullable=True)  # Tiền sử bệnh
    drug_allergies = Column(Text, nullable=True)  # Tiền sử dị ứng thuốc/thực phẩm
    emergency_contact = Column(String(150), nullable=True)  # Tên và SĐT người thân
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    appointments = relationship("Appointment", back_populates="patient")
    medical_records = relationship("MedicalRecord", back_populates="patient")
    invoices = relationship("Invoice", back_populates="patient")
