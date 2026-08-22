from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(50), nullable=False)  # LOGIN, VIEW_PATIENT, UPDATE_RECORD, etc.
    resource_type = Column(String(50), nullable=False)  # Patient, MedicalRecord, Prescription, Invoice, User
    resource_id = Column(String(50), nullable=True)
    details = Column(Text, nullable=True)
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="audit_logs")


class AIInvocationLog(Base):
    __tablename__ = "ai_invocation_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    feature_name = Column(String(50), nullable=False)  # PRE_VISIT_SUMMARY, CLINIC_FAQ, DISCHARGE_INSTRUCTIONS
    anonymized_prompt = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    model_used = Column(String(50), nullable=False)
    latency_ms = Column(Integer, default=0, nullable=False)
    disclaimer_included = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="ai_logs")
