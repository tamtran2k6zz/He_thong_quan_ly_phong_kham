from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, ConfigDict
from backend.app.models.invoice import PaymentStatus, PaymentMethod
from backend.app.schemas.patient import PatientResponse
from backend.app.schemas.user import UserResponse


class InvoiceBase(BaseModel):
    medical_record_id: Optional[int] = None
    patient_id: int
    consultation_fee: float = 150000.0
    service_fee: float = 0.0
    medicine_fee: float = 0.0
    total_amount: float = 0.0
    insurance_discount: float = 0.0
    patient_pay_amount: float = 0.0
    payment_status: str = PaymentStatus.PENDING.value
    payment_method: Optional[str] = None
    transaction_code: Optional[str] = None
    cashier_id: Optional[int] = None
    notes: Optional[str] = None


class InvoiceCreate(BaseModel):
    medical_record_id: Optional[int] = None
    patient_id: Optional[int] = None
    consultation_fee: Optional[float] = None
    service_fee: Optional[float] = None
    medicine_fee: Optional[float] = None
    discount_amount: Optional[float] = None
    insurance_discount: Optional[float] = None
    total_amount: Optional[float] = None
    patient_pay_amount: Optional[float] = None
    payment_status: Optional[str] = PaymentStatus.PENDING.value
    notes: Optional[str] = None


class InvoiceUpdate(BaseModel):
    consultation_fee: Optional[float] = None
    service_fee: Optional[float] = None
    medicine_fee: Optional[float] = None
    insurance_discount: Optional[float] = None
    payment_status: Optional[str] = None
    payment_method: Optional[str] = None
    transaction_code: Optional[str] = None
    notes: Optional[str] = None


class InvoicePayRequest(BaseModel):
    payment_method: Union[PaymentMethod, str]  # CASH, BANK_TRANSFER, INSURANCE
    transaction_code: Optional[str] = None
    amount_paid: Optional[float] = None
    notes: Optional[str] = None


class InvoiceItemDetail(BaseModel):
    item_type: str  # CONSULTATION, SERVICE, MEDICINE
    item_name: str
    item_code: Optional[str] = None
    quantity: int = 1
    unit: Optional[str] = None
    unit_price: float = 0.0
    total_price: float = 0.0


class InvoiceResponse(InvoiceBase):
    id: int
    invoice_code: str
    paid_at: Optional[datetime] = None
    created_at: datetime
    patient: Optional[PatientResponse] = None
    cashier: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)


class InvoiceDetailResponse(InvoiceResponse):
    items: List[InvoiceItemDetail] = []
    doctor_name: Optional[str] = None
    diagnosis: Optional[str] = None
    clinic_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class InvoicePrintReceiptResponse(BaseModel):
    clinic_header: Dict[str, str]
    invoice_code: str
    created_at: str
    paid_at: Optional[str] = None
    patient_info: Dict[str, Any]
    doctor_info: Optional[Dict[str, Any]] = None
    items: List[Dict[str, Any]] = []
    consultation_fee: float
    service_fee: float
    medicine_fee: float
    total_amount: float
    insurance_discount: float
    patient_pay_amount: float
    payment_status: str
    payment_method: Optional[str] = None
    transaction_code: Optional[str] = None
    cashier_name: Optional[str] = None
    patient_signature_title: str = "Người nộp tiền (Ký, ghi rõ họ tên)"
    cashier_signature_title: str = "Thu ngân / Kế toán (Ký, đóng dấu)"
    print_time: str
    notes: Optional[str] = None
