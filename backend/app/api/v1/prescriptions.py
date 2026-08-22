from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.prescription import Prescription, PrescriptionItem, Medicine
from backend.app.models.medical_record import MedicalRecord, RecordStatus
from backend.app.models.clinic import Doctor
from backend.app.models.patient import Patient
from backend.app.models.audit import AuditLog
from backend.app.models.user import User, RoleEnum
from backend.app.schemas.prescription import (
    PrescriptionCreate,
    PrescriptionResponse
)
from backend.app.api.deps import require_doctor, require_clinical_staff, require_all_staff

router = APIRouter(prefix="/prescriptions", tags=["e-Prescriptions Management"])


def generate_prescription_code(db: Session) -> str:
    """Generates unique prescription code in format DT-YYYYMMDD-XXXX."""
    today_str = datetime.utcnow().strftime("%Y%m%d")
    prefix = f"DT-{today_str}-"
    count = db.query(Prescription).filter(Prescription.prescription_code.like(f"{prefix}%")).count()
    candidate = f"{prefix}{count + 1:04d}"
    while db.query(Prescription).filter(Prescription.prescription_code == candidate).first():
        count += 1
        candidate = f"{prefix}{count + 1:04d}"
    return candidate


def generate_record_code(db: Session) -> str:
    """Generates unique medical record code in format PK-YYYYMMDD-XXXX."""
    today_str = datetime.utcnow().strftime("%Y%m%d")
    prefix = f"PK-{today_str}-"
    count = db.query(MedicalRecord).filter(MedicalRecord.record_code.like(f"{prefix}%")).count()
    candidate = f"{prefix}{count + 1:04d}"
    while db.query(MedicalRecord).filter(MedicalRecord.record_code == candidate).first():
        count += 1
        candidate = f"{prefix}{count + 1:04d}"
    return candidate


@router.get("", response_model=List[PrescriptionResponse])
def get_prescriptions(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    patient_id: Optional[int] = None,
    doctor_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinical_staff)
):
    """
    List prescriptions with optional filtering by patient or doctor.
    """
    query = db.query(Prescription)
    if patient_id:
        query = query.filter(Prescription.patient_id == patient_id)
    if doctor_id:
        query = query.filter(Prescription.doctor_id == doctor_id)

    return query.order_by(Prescription.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=PrescriptionResponse, status_code=status.HTTP_201_CREATED)
def create_prescription(
    presc_in: PrescriptionCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_doctor)
):
    """
    Create an electronic prescription (e-Prescription).
    Validates medicine stock availability and automatically decrements inventory.
    """
    # 1. Verify patient
    patient = db.query(Patient).filter(Patient.id == presc_in.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy bệnh nhân ID {presc_in.patient_id}"
        )

    # 2. Verify doctor
    doctor = db.query(Doctor).filter(Doctor.id == presc_in.doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy bác sĩ ID {presc_in.doctor_id}"
        )

    # 3. Resolve medical_record_id
    medical_record_id = presc_in.medical_record_id
    if medical_record_id is not None:
        med_rec = db.query(MedicalRecord).filter(MedicalRecord.id == medical_record_id).first()
        if not med_rec:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy hồ sơ bệnh án ID {medical_record_id}"
            )
        # Check if record already has a prescription
        existing_presc = db.query(Prescription).filter(Prescription.medical_record_id == medical_record_id).first()
        if existing_presc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Hồ sơ bệnh án này đã có đơn thuốc được tạo"
            )
    else:
        # Check if there is an active medical record for this patient and doctor
        med_rec = db.query(MedicalRecord).filter(
            MedicalRecord.patient_id == presc_in.patient_id,
            MedicalRecord.doctor_id == presc_in.doctor_id
        ).order_by(MedicalRecord.created_at.desc()).first()

        if med_rec and not db.query(Prescription).filter(Prescription.medical_record_id == med_rec.id).first():
            medical_record_id = med_rec.id
        else:
            # Auto-create a linked medical record encounter to fulfill FK constraint
            new_record_code = generate_record_code(db)
            auto_rec = MedicalRecord(
                record_code=new_record_code,
                patient_id=presc_in.patient_id,
                doctor_id=presc_in.doctor_id,
                chief_complaint=presc_in.diagnosis or "Khám và kê đơn ngoại trú",
                diagnosis_icd10=presc_in.diagnosis or "Kê đơn theo dõi",
                doctor_notes=presc_in.notes or presc_in.advice,
                status=RecordStatus.IN_EXAM.value
            )
            db.add(auto_rec)
            db.flush()
            medical_record_id = auto_rec.id

    # 4. Stock validation & decrement preparation
    items_to_create = []
    medicines_to_update = []

    for item_in in presc_in.items:
        medicine = db.query(Medicine).filter(Medicine.id == item_in.medicine_id).first()
        if not medicine:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy thuốc ID {item_in.medicine_id}"
            )

        if not medicine.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Thuốc '{medicine.name}' hiện không còn lưu hành trong danh mục"
            )

        if medicine.stock_quantity < item_in.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Thuốc '{medicine.name}' không đủ số lượng tồn kho "
                    f"(Hiện còn: {medicine.stock_quantity}, Yêu cầu kê: {item_in.quantity})"
                )
            )

        # Decrement stock
        medicine.stock_quantity -= item_in.quantity
        medicines_to_update.append(medicine)

        items_to_create.append({
            "medicine_id": item_in.medicine_id,
            "quantity": item_in.quantity,
            "dosage": item_in.dosage or "1 viên",
            "frequency": item_in.frequency or "2 lần/ngày",
            "duration_days": item_in.duration_days or 5,
            "instructions": item_in.instructions or medicine.usage_instructions or "Uống sau ăn"
        })

    # 5. Generate Prescription code
    code = presc_in.prescription_code
    if not code:
        code = generate_prescription_code(db)
    else:
        existing = db.query(Prescription).filter(Prescription.prescription_code == code).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Mã đơn thuốc '{code}' đã tồn tại"
            )

    advice_text = presc_in.advice or presc_in.notes

    prescription = Prescription(
        prescription_code=code,
        medical_record_id=medical_record_id,
        doctor_id=presc_in.doctor_id,
        patient_id=presc_in.patient_id,
        diagnosis=presc_in.diagnosis,
        advice=advice_text
    )
    db.add(prescription)
    db.flush()

    for item_data in items_to_create:
        item = PrescriptionItem(
            prescription_id=prescription.id,
            **item_data
        )
        db.add(item)

    db.commit()
    db.refresh(prescription)

    client_ip = request.client.host if request.client else "unknown"
    audit = AuditLog(
        user_id=current_user.id,
        action="CREATE_PRESCRIPTION",
        resource_type="Prescription",
        resource_id=str(prescription.id),
        details=f"Created prescription {prescription.prescription_code} with {len(items_to_create)} items for patient {patient.full_name}",
        ip_address=client_ip
    )
    db.add(audit)
    db.commit()

    return prescription


@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def get_prescription(
    prescription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinical_staff)
):
    """
    Get prescription details with medicine items and dosage instructions.
    """
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy đơn thuốc"
        )
    return prescription


@router.get("/by-record/{record_id}", response_model=PrescriptionResponse)
def get_prescription_by_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinical_staff)
):
    """
    Get prescription linked to a specific medical record encounter.
    """
    prescription = db.query(Prescription).filter(Prescription.medical_record_id == record_id).first()
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hồ sơ bệnh án này chưa có đơn thuốc"
        )
    return prescription
