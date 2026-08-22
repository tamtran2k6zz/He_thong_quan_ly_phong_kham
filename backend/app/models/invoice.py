import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base


class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


class PaymentMethod(str, enum.Enum):
    CASH = "CASH"
    BANK_TRANSFER = "BANK_TRANSFER"
    INSURANCE = "INSURANCE"


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_code = Column(String(30), unique=True, index=True, nullable=False)  # HD-YYYYMMDD-XXXX
    medical_record_id = Column(Integer, ForeignKey("medical_records.id"), unique=False, nullable=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # Financial breakdown
    consultation_fee = Column(Float, default=150000.0, nullable=False)
    service_fee = Column(Float, default=0.0, nullable=False)
    medicine_fee = Column(Float, default=0.0, nullable=False)
    total_amount = Column(Float, default=0.0, nullable=False)
    insurance_discount = Column(Float, default=0.0, nullable=False)  # BHYT giảm trừ
    patient_pay_amount = Column(Float, default=0.0, nullable=False)  # Bệnh nhân thực trả
    
    # Payment status & details
    payment_status = Column(String(20), default=PaymentStatus.PENDING.value, nullable=False)
    payment_method = Column(String(20), nullable=True)  # CASH, BANK_TRANSFER, INSURANCE
    transaction_code = Column(String(50), nullable=True)  # Mã giao dịch / VietQR ref
    cashier_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    paid_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    medical_record = relationship("MedicalRecord", back_populates="invoice")
    patient = relationship("Patient", back_populates="invoices")
    cashier = relationship("User", foreign_keys=[cashier_id])
