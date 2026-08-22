"""
Invoices & Payment Processing Router.
Provides:
- GET /api/v1/invoices: List invoices with filters (payment_status, patient_id, date range).
- POST /api/v1/invoices: Generate invoice from MedicalRecord or direct financial items.
- GET /api/v1/invoices/{id}: Invoice details with full itemized breakdown.
- POST /api/v1/invoices/{id}/pay: Process payment (CASH, BANK_TRANSFER, INSURANCE) with audit log.
- POST /api/v1/invoices/{id}/cancel: Cancel unpaid invoice.
- GET /api/v1/invoices/{id}/print: Printable receipt payload.
"""

from datetime import datetime, date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.database import get_db
from backend.app.models.user import User, RoleEnum
from backend.app.models.invoice import Invoice, PaymentStatus, PaymentMethod
from backend.app.models.medical_record import MedicalRecord
from backend.app.models.patient import Patient
from backend.app.models.prescription import Prescription, PrescriptionItem
from backend.app.models.audit import AuditLog
from backend.app.schemas.invoice import (
    InvoiceCreate,
    InvoiceUpdate,
    InvoicePayRequest,
    InvoiceResponse,
    InvoiceItemDetail,
    InvoiceDetailResponse,
    InvoicePrintReceiptResponse
)
from backend.app.api.deps import require_accountant, require_all_staff
from backend.app.api.v1.audit import log_audit

router = APIRouter(prefix="/invoices", tags=["Invoicing & Billing"])


def generate_invoice_code(db: Session) -> str:
    """
    Generates sequential unique invoice code: HD-YYYYMMDD-XXXX
    """
    today_str = datetime.utcnow().strftime("%Y%m%d")
    prefix = f"HD-{today_str}-"
    count = db.query(Invoice).filter(Invoice.invoice_code.like(f"{prefix}%")).count()
    candidate = f"{prefix}{count + 1:04d}"
    while db.query(Invoice).filter(Invoice.invoice_code == candidate).first():
        count += 1
        candidate = f"{prefix}{count + 1:04d}"
    return candidate


@router.get("", response_model=List[InvoiceResponse])
def get_invoices(
    payment_status: Optional[str] = Query(None, description="Filter by status: PENDING, PAID, CANCELLED"),
    patient_id: Optional[int] = Query(None, description="Filter by patient ID"),
    from_date: Optional[date] = Query(None, description="Filter from created date"),
    to_date: Optional[date] = Query(None, description="Filter to created date"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_all_staff)
):
    """
    List invoices with filtering by payment status, patient ID, and date range.
    """
    query = db.query(Invoice)

    if payment_status:
        query = query.filter(Invoice.payment_status == payment_status.upper())
    if patient_id is not None:
        query = query.filter(Invoice.patient_id == patient_id)
    if from_date:
        query = query.filter(Invoice.created_at >= datetime.combine(from_date, datetime.min.time()))
    if to_date:
        query = query.filter(Invoice.created_at <= datetime.combine(to_date, datetime.max.time()))

    return query.order_by(Invoice.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_invoice(
    invoice_in: InvoiceCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_accountant)
):
    """
    Generate an invoice from a completed MedicalRecord or manual itemization (Accountant / Admin).
    Calculates consultation_fee (default 150,000 VND), service_fee, medicine_fee, and applies BHYT discount.
    """
    medical_record = None
    patient = None

    if invoice_in.medical_record_id:
        medical_record = db.query(MedicalRecord).filter(MedicalRecord.id == invoice_in.medical_record_id).first()
        if not medical_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy thông tin phiếu khám bệnh"
            )
        
        # Check if invoice already exists for this medical record
        existing = db.query(Invoice).filter(Invoice.medical_record_id == invoice_in.medical_record_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Phiếu khám bệnh đã có hóa đơn ({existing.invoice_code})"
            )
        
        patient_id = invoice_in.patient_id or medical_record.patient_id
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy thông tin bệnh nhân"
            )

        # 1. Consultation Fee
        if invoice_in.consultation_fee is not None:
            consultation_fee = float(invoice_in.consultation_fee)
        else:
            consultation_fee = 150000.0

        # 2. Service Orders Fee
        if invoice_in.service_fee is not None:
            service_fee = float(invoice_in.service_fee)
        else:
            service_fee = sum(float(s.price) for s in medical_record.service_orders)

        # 3. Medicine Fee
        if invoice_in.medicine_fee is not None:
            medicine_fee = float(invoice_in.medicine_fee)
        else:
            medicine_fee = 0.0
            if medical_record.prescription and medical_record.prescription.items:
                for p_item in medical_record.prescription.items:
                    if p_item.medicine:
                        medicine_fee += float(p_item.quantity) * float(p_item.medicine.unit_price)

        gross_total = consultation_fee + service_fee + medicine_fee

        # 4. BHYT Insurance Discount
        if invoice_in.insurance_discount is not None and invoice_in.insurance_discount > 0:
            insurance_discount = float(invoice_in.insurance_discount)
        elif invoice_in.discount_amount is not None and invoice_in.discount_amount > 0:
            insurance_discount = float(invoice_in.discount_amount)
        elif invoice_in.insurance_discount == 0.0 or invoice_in.discount_amount == 0.0:
            insurance_discount = 0.0
        else:
            if patient.insurance_number and len(patient.insurance_number.strip()) >= 5:
                ins_num = patient.insurance_number.strip().upper()
                if ins_num.startswith(("TE", "CC", "BT", "CA", "QN", "100")):
                    rate = 1.00
                else:
                    rate = 0.80
                insurance_discount = gross_total * rate
            else:
                insurance_discount = 0.0

        # 5. Total amount & Patient pay amount
        if invoice_in.total_amount is not None and invoice_in.total_amount > 0:
            total_amount = float(invoice_in.total_amount)
        else:
            total_amount = gross_total

        if invoice_in.patient_pay_amount is not None:
            patient_pay_amount = float(invoice_in.patient_pay_amount)
        else:
            patient_pay_amount = max(0.0, total_amount - insurance_discount)

    else:
        # Standalone / Manual Invoice
        if not invoice_in.patient_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Thiếu thông tin bệnh nhân (patient_id) để tạo hóa đơn"
            )
        patient = db.query(Patient).filter(Patient.id == invoice_in.patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy thông tin bệnh nhân"
            )
        patient_id = patient.id

        consultation_fee = float(invoice_in.consultation_fee) if invoice_in.consultation_fee is not None else 150000.0
        service_fee = float(invoice_in.service_fee) if invoice_in.service_fee is not None else 0.0
        medicine_fee = float(invoice_in.medicine_fee) if invoice_in.medicine_fee is not None else 0.0
        gross_total = consultation_fee + service_fee + medicine_fee

        if invoice_in.insurance_discount is not None:
            insurance_discount = float(invoice_in.insurance_discount)
        elif invoice_in.discount_amount is not None:
            insurance_discount = float(invoice_in.discount_amount)
        else:
            insurance_discount = 0.0

        if invoice_in.total_amount is not None and invoice_in.total_amount > 0:
            total_amount = float(invoice_in.total_amount)
        else:
            total_amount = gross_total

        if invoice_in.patient_pay_amount is not None:
            patient_pay_amount = float(invoice_in.patient_pay_amount)
        else:
            patient_pay_amount = max(0.0, total_amount - insurance_discount)

    invoice_code = generate_invoice_code(db)

    status_val = invoice_in.payment_status or PaymentStatus.PENDING.value
    if isinstance(status_val, PaymentStatus):
        status_val = status_val.value

    new_invoice = Invoice(
        invoice_code=invoice_code,
        medical_record_id=invoice_in.medical_record_id,
        patient_id=patient_id,
        consultation_fee=consultation_fee,
        service_fee=service_fee,
        medicine_fee=medicine_fee,
        total_amount=total_amount,
        insurance_discount=insurance_discount,
        patient_pay_amount=patient_pay_amount,
        payment_status=status_val.upper(),
        notes=invoice_in.notes,
        created_at=datetime.utcnow()
    )

    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    client_ip = request.client.host if request.client else None
    log_audit(
        db=db,
        user_id=current_user.id,
        action="CREATE_INVOICE",
        resource_type="Invoice",
        resource_id=str(new_invoice.id),
        details=f"Created invoice {new_invoice.invoice_code} for patient ID {patient_id}, total {new_invoice.patient_pay_amount} VND",
        ip_address=client_ip
    )

    return new_invoice


@router.get("/{invoice_id}", response_model=InvoiceDetailResponse)
def get_invoice_detail(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_all_staff)
):
    """
    Get full itemized invoice details.
    """
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hóa đơn"
        )

    # Build items breakdown
    items: List[InvoiceItemDetail] = []
    
    # 1. Consultation item
    if invoice.consultation_fee > 0:
        items.append(
            InvoiceItemDetail(
                item_type="CONSULTATION",
                item_name="Phí khám chuyên khoa",
                quantity=1,
                unit="Lượt",
                unit_price=invoice.consultation_fee,
                total_price=invoice.consultation_fee
            )
        )

    doctor_name = None
    diagnosis = None
    clinic_name = None

    # 2. Services and Medicines from Medical Record
    if invoice.medical_record:
        mr = invoice.medical_record
        if mr.doctor and mr.doctor.user:
            doctor_name = mr.doctor.user.full_name
        if mr.doctor and mr.doctor.clinic:
            clinic_name = mr.doctor.clinic.name
        diagnosis = mr.diagnosis_icd10

        for s in mr.service_orders:
            items.append(
                InvoiceItemDetail(
                    item_type="SERVICE",
                    item_name=s.service_name,
                    item_code=s.service_code,
                    quantity=1,
                    unit="Lần",
                    unit_price=s.price,
                    total_price=s.price
                )
            )

        if mr.prescription and mr.prescription.items:
            for p_item in mr.prescription.items:
                med = p_item.medicine
                med_name = med.name if med else "Thuốc điều trị"
                med_unit = med.unit if med else "Viên"
                unit_price = med.unit_price if med else 0.0
                items.append(
                    InvoiceItemDetail(
                        item_type="MEDICINE",
                        item_name=med_name,
                        item_code=med.code if med else None,
                        quantity=p_item.quantity,
                        unit=med_unit,
                        unit_price=unit_price,
                        total_price=p_item.quantity * unit_price
                    )
                )

    detail_res = InvoiceDetailResponse.model_validate(invoice)
    detail_res.items = items
    detail_res.doctor_name = doctor_name
    detail_res.diagnosis = diagnosis
    detail_res.clinic_name = clinic_name

    return detail_res


@router.post("/{invoice_id}/pay", response_model=InvoiceResponse)
def process_invoice_payment(
    invoice_id: int,
    pay_in: InvoicePayRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_accountant)
):
    """
    Process payment for invoice (Accountant / Admin only).
    Locks already PAID invoices to prevent duplicate payments.
    """
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hóa đơn"
        )

    # Prevent duplicate payment on already paid invoices
    if invoice.payment_status == PaymentStatus.PAID.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hóa đơn đã được thanh toán trước đó (Duplicate payment rejected)"
        )

    # Reject payment on cancelled invoices
    if invoice.payment_status == PaymentStatus.CANCELLED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hóa đơn đã bị hủy, không thể thực hiện thanh toán"
        )

    # Normalize payment method
    if hasattr(pay_in.payment_method, "value"):
        payment_method_str = pay_in.payment_method.value
    else:
        payment_method_str = str(pay_in.payment_method).upper()

    tx_code = pay_in.transaction_code
    if payment_method_str == PaymentMethod.BANK_TRANSFER.value and not tx_code:
        today_str = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        tx_code = f"VQR-{today_str}-{invoice.id:04d}"

    invoice.payment_status = PaymentStatus.PAID.value
    invoice.payment_method = payment_method_str
    invoice.transaction_code = tx_code
    invoice.cashier_id = current_user.id
    invoice.paid_at = datetime.utcnow()

    if pay_in.notes:
        if invoice.notes:
            invoice.notes += f"\n[Thanh toán]: {pay_in.notes}"
        else:
            invoice.notes = pay_in.notes

    db.commit()
    db.refresh(invoice)

    client_ip = request.client.host if request.client else None
    log_audit(
        db=db,
        user_id=current_user.id,
        action="PAY_INVOICE",
        resource_type="Invoice",
        resource_id=str(invoice.id),
        details=f"Processed payment of {invoice.patient_pay_amount} VND for invoice {invoice.invoice_code} via {payment_method_str} by {current_user.username}",
        ip_address=client_ip
    )

    return invoice


@router.post("/{invoice_id}/cancel", response_model=InvoiceResponse)
def cancel_invoice(
    invoice_id: int,
    request: Request,
    notes: Optional[str] = Query(None, description="Lý do hủy"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_accountant)
):
    """
    Cancel an unpaid invoice (Accountant / Admin only).
    """
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hóa đơn"
        )

    if invoice.payment_status == PaymentStatus.PAID.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không thể hủy hóa đơn đã thanh toán"
        )

    if invoice.payment_status == PaymentStatus.CANCELLED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hóa đơn đã bị hủy trước đó"
        )

    invoice.payment_status = PaymentStatus.CANCELLED.value
    if notes:
        invoice.notes = f"[HỦY]: {notes}" if not invoice.notes else f"{invoice.notes}\n[HỦY]: {notes}"

    db.commit()
    db.refresh(invoice)

    client_ip = request.client.host if request.client else None
    log_audit(
        db=db,
        user_id=current_user.id,
        action="CANCEL_INVOICE",
        resource_type="Invoice",
        resource_id=str(invoice.id),
        details=f"Cancelled invoice {invoice.invoice_code} by {current_user.username}",
        ip_address=client_ip
    )

    return invoice


@router.get("/{invoice_id}/print", response_model=InvoicePrintReceiptResponse)
def get_printable_receipt(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_all_staff)
):
    """
    Printable receipt payload with clinic header, tax ID, patient info, itemized table, total, BHYT coverage, and cashier signature line.
    """
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hóa đơn"
        )

    patient = invoice.patient
    medical_record = invoice.medical_record

    # Item table
    items_list = []
    stt = 1

    if invoice.consultation_fee > 0:
        items_list.append({
            "stt": stt,
            "category": "Khám bệnh",
            "name": "Khám chuyên khoa",
            "unit": "Lượt",
            "quantity": 1,
            "unit_price": invoice.consultation_fee,
            "total_price": invoice.consultation_fee
        })
        stt += 1

    if medical_record:
        for s in medical_record.service_orders:
            items_list.append({
                "stt": stt,
                "category": "Cận lâm sàng",
                "name": s.service_name,
                "unit": "Lần",
                "quantity": 1,
                "unit_price": s.price,
                "total_price": s.price
            })
            stt += 1

        if medical_record.prescription and medical_record.prescription.items:
            for p_item in medical_record.prescription.items:
                med = p_item.medicine
                med_name = med.name if med else "Thuốc kê đơn"
                med_unit = med.unit if med else "Viên"
                unit_price = med.unit_price if med else 0.0
                total_p = float(p_item.quantity) * float(unit_price)
                items_list.append({
                    "stt": stt,
                    "category": "Thuốc & Dược phẩm",
                    "name": med_name,
                    "unit": med_unit,
                    "quantity": p_item.quantity,
                    "unit_price": unit_price,
                    "total_price": total_p
                })
                stt += 1

    doctor_info = None
    if medical_record and medical_record.doctor:
        doc = medical_record.doctor
        doctor_info = {
            "full_name": doc.user.full_name if doc.user else "Bác sĩ điều trị",
            "title": doc.title or "Bác sĩ",
            "specialty": doc.specialty.name if doc.specialty else "Đa khoa",
            "diagnosis": medical_record.diagnosis_icd10,
            "icd10_code": medical_record.icd10_code
        }

    patient_info = {
        "id": patient.id,
        "medical_code": patient.medical_code,
        "full_name": patient.full_name,
        "date_of_birth": patient.date_of_birth.strftime("%d/%m/%Y") if patient.date_of_birth else None,
        "gender": patient.gender,
        "phone": patient.phone,
        "address": patient.address,
        "insurance_number": patient.insurance_number
    }

    clinic_header = {
        "name": "PHÒNG KHÁM ĐA KHOA QUỐC TẾ HÀ NỘI",
        "address": "123 Phố Huế, Hai Bà Trưng, Hà Nội",
        "phone": "1900 6868",
        "tax_id": "0109887766",
        "email": "contact@phongkham.vn",
        "website": "https://phongkham.vn"
    }

    cashier_name = invoice.cashier.full_name if invoice.cashier else current_user.full_name

    return InvoicePrintReceiptResponse(
        clinic_header=clinic_header,
        invoice_code=invoice.invoice_code,
        created_at=invoice.created_at.strftime("%d/%m/%Y %H:%M:%S"),
        paid_at=invoice.paid_at.strftime("%d/%m/%Y %H:%M:%S") if invoice.paid_at else None,
        patient_info=patient_info,
        doctor_info=doctor_info,
        items=items_list,
        consultation_fee=invoice.consultation_fee,
        service_fee=invoice.service_fee,
        medicine_fee=invoice.medicine_fee,
        total_amount=invoice.total_amount,
        insurance_discount=invoice.insurance_discount,
        patient_pay_amount=invoice.patient_pay_amount,
        payment_status=invoice.payment_status,
        payment_method=invoice.payment_method,
        transaction_code=invoice.transaction_code,
        cashier_name=cashier_name,
        patient_signature_title="Người nộp tiền (Ký, ghi rõ họ tên)",
        cashier_signature_title="Thu ngân / Kế toán (Ký, đóng dấu)",
        print_time=datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S"),
        notes=invoice.notes
    )
