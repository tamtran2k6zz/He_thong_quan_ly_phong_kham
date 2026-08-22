from datetime import date, time, datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from backend.app.database import get_db
from backend.app.models.medical_record import MedicalRecord, RecordStatus, ServiceOrder
from backend.app.models.appointment import Appointment, AppointmentStatus
from backend.app.models.clinic import Doctor, Clinic
from backend.app.models.patient import Patient
from backend.app.models.audit import AuditLog
from backend.app.models.user import User, RoleEnum
from backend.app.schemas.medical_record import (
    MedicalRecordCreate,
    MedicalRecordUpdate,
    MedicalRecordResponse,
    ServiceOrderCreate,
    ServiceOrderResponse,
    QueueItemResponse
)
from backend.app.api.deps import (
    require_doctor,
    require_clinical_staff,
    require_all_staff
)

router = APIRouter(prefix="/medical_records", tags=["Medical Records & Queue"])


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


def generate_service_code(db: Session) -> str:
    """Generates unique service order code in format CLS-YYYYMMDD-XXXX."""
    today_str = datetime.utcnow().strftime("%Y%m%d")
    prefix = f"CLS-{today_str}-"
    count = db.query(ServiceOrder).filter(ServiceOrder.service_code.like(f"{prefix}%")).count()
    candidate = f"{prefix}{count + 1:04d}"
    while db.query(ServiceOrder).filter(ServiceOrder.service_code == candidate).first():
        count += 1
        candidate = f"{prefix}{count + 1:04d}"
    return candidate


@router.get("/queue", response_model=List[QueueItemResponse])
def get_consultation_queue(
    doctor_id: Optional[int] = None,
    appointment_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_all_staff)
):
    """
    Get the patient queue for consultation.
    Lists appointments in CHECKED_IN or IN_PROGRESS state.
    """
    target_date = appointment_date or datetime.utcnow().date()
    query = db.query(Appointment).filter(
        Appointment.appointment_date == target_date,
        Appointment.status.in_([
            AppointmentStatus.CHECKED_IN.value,
            AppointmentStatus.IN_PROGRESS.value,
            AppointmentStatus.CONFIRMED.value
        ])
    )

    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)

    # Sort checked_in / in_progress first, then by time
    appointments = query.order_by(
        Appointment.status.desc(),
        Appointment.start_time.asc()
    ).all()

    queue_list = []
    for idx, appt in enumerate(appointments, start=1):
        patient = appt.patient
        doctor = appt.doctor
        doc_user_name = doctor.user.full_name if doctor and doctor.user else "Bác sĩ"
        clinic_room = appt.clinic.room_number if appt.clinic else (doctor.clinic.room_number if doctor and doctor.clinic else "P101")
        
        queue_list.append(
            QueueItemResponse(
                queue_number=idx,
                appointment_id=appt.id,
                appointment_code=appt.appointment_code,
                patient_id=appt.patient_id,
                patient_name=patient.full_name if patient else "Không rõ",
                medical_code=patient.medical_code if patient else "N/A",
                doctor_id=appt.doctor_id,
                doctor_name=doc_user_name,
                clinic_room=clinic_room,
                status=appt.status,
                start_time=appt.start_time,
                appointment_date=appt.appointment_date,
                reason=appt.reason,
                medical_record_id=appt.medical_record.id if appt.medical_record else None
            )
        )

    return queue_list


@router.get("", response_model=List[MedicalRecordResponse])
def get_medical_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    patient_id: Optional[int] = None,
    doctor_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinical_staff)
):
    """
    List medical records with optional filters.
    """
    query = db.query(MedicalRecord)
    if patient_id:
        query = query.filter(MedicalRecord.patient_id == patient_id)
    if doctor_id:
        query = query.filter(MedicalRecord.doctor_id == doctor_id)
    if status:
        query = query.filter(MedicalRecord.status == status.upper())

    return query.order_by(MedicalRecord.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=MedicalRecordResponse, status_code=status.HTTP_201_CREATED)
def create_medical_record(
    record_in: MedicalRecordCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_doctor)
):
    """
    Create a new clinical consultation record (Doctor / Admin only).
    """
    # 1. Verify patient
    patient = db.query(Patient).filter(Patient.id == record_in.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy bệnh nhân ID {record_in.patient_id}"
        )

    # 2. Verify doctor
    doctor = db.query(Doctor).filter(Doctor.id == record_in.doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy bác sĩ ID {record_in.doctor_id}"
        )

    # 3. Chief complaint handling (fallback to symptoms or default)
    chief_complaint = record_in.chief_complaint or record_in.symptoms or "Khám lâm sàng tổng quát"

    # 4. Generate code
    code = record_in.record_code
    if not code:
        code = generate_record_code(db)
    else:
        existing = db.query(MedicalRecord).filter(MedicalRecord.record_code == code).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Mã hồ sơ bệnh án '{code}' đã tồn tại"
            )

    # 5. BMI calculation if missing
    bmi = record_in.bmi
    if bmi is None and record_in.weight and record_in.height and record_in.height > 0:
        height_m = record_in.height / 100.0
        bmi = round(record_in.weight / (height_m * height_m), 2)

    rec_data = record_in.model_dump(exclude={"service_orders", "clinic_id", "symptoms"}, exclude_unset=False)
    rec_data["record_code"] = code
    rec_data["chief_complaint"] = chief_complaint
    rec_data["bmi"] = bmi
    if not rec_data.get("status"):
        rec_data["status"] = RecordStatus.IN_EXAM.value
    else:
        rec_data["status"] = rec_data["status"].upper()

    medical_record = MedicalRecord(**rec_data)
    db.add(medical_record)
    db.flush()

    # 6. Add service orders if any
    if record_in.service_orders:
        for order_in in record_in.service_orders:
            srv_code = order_in.service_code or generate_service_code(db)
            srv = ServiceOrder(
                medical_record_id=medical_record.id,
                service_name=order_in.service_name,
                service_code=srv_code,
                price=order_in.price,
                notes=order_in.notes,
                result=order_in.result
            )
            db.add(srv)

    # 7. If linked to an appointment, transition appointment status to IN_PROGRESS
    if record_in.appointment_id:
        appt = db.query(Appointment).filter(Appointment.id == record_in.appointment_id).first()
        if appt and appt.status != AppointmentStatus.COMPLETED.value:
            appt.status = AppointmentStatus.IN_PROGRESS.value

    db.commit()
    db.refresh(medical_record)

    client_ip = request.client.host if request.client else "unknown"
    audit = AuditLog(
        user_id=current_user.id,
        action="CREATE_MEDICAL_RECORD",
        resource_type="MedicalRecord",
        resource_id=str(medical_record.id),
        details=f"Created medical record {medical_record.record_code} for patient {patient.full_name} by Dr. {current_user.username}",
        ip_address=client_ip
    )
    db.add(audit)
    db.commit()

    return medical_record


@router.get("/{record_id}", response_model=MedicalRecordResponse)
def get_medical_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinical_staff)
):
    """
    Get full clinical medical record by ID including vitals, diagnosis, and service orders.
    """
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hồ sơ bệnh án"
        )
    return record


@router.put("/{record_id}", response_model=MedicalRecordResponse)
def update_medical_record(
    record_id: int,
    record_in: MedicalRecordUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_doctor)
):
    """
    Update medical record vitals, notes, and ICD-10 diagnosis.
    Enforces Doctor Isolation: A doctor can only edit records they are assigned to.
    """
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hồ sơ bệnh án"
        )

    # Doctor Isolation Check
    if current_user.role == RoleEnum.DOCTOR.value:
        doc_profile = db.query(Doctor).filter(Doctor.user_id == current_user.id).first()
        if not doc_profile or record.doctor_id != doc_profile.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bác sĩ chỉ có quyền chỉnh sửa hồ sơ bệnh án do chính mình phụ trách"
            )

    update_data = record_in.model_dump(exclude_unset=True)
    if "symptoms" in update_data and not update_data.get("chief_complaint"):
        update_data["chief_complaint"] = update_data.pop("symptoms")
    elif "symptoms" in update_data:
        update_data.pop("symptoms")

    if "status" in update_data and update_data["status"]:
        update_data["status"] = update_data["status"].upper()

    for field, value in update_data.items():
        setattr(record, field, value)

    # Recalculate BMI if weight and height updated
    if record.weight and record.height and record.height > 0:
        height_m = record.height / 100.0
        record.bmi = round(record.weight / (height_m * height_m), 2)

    db.commit()
    db.refresh(record)

    client_ip = request.client.host if request.client else "unknown"
    audit = AuditLog(
        user_id=current_user.id,
        action="UPDATE_MEDICAL_RECORD",
        resource_type="MedicalRecord",
        resource_id=str(record.id),
        details=f"Updated medical record {record.record_code} by {current_user.username}",
        ip_address=client_ip
    )
    db.add(audit)
    db.commit()

    return record


@router.post("/{record_id}/services", response_model=ServiceOrderResponse, status_code=status.HTTP_201_CREATED)
def add_service_order(
    record_id: int,
    order_in: ServiceOrderCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_doctor)
):
    """
    Order a lab test or imaging service for an active medical record.
    """
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hồ sơ bệnh án"
        )

    # Doctor Isolation Check
    if current_user.role == RoleEnum.DOCTOR.value:
        doc_profile = db.query(Doctor).filter(Doctor.user_id == current_user.id).first()
        if not doc_profile or record.doctor_id != doc_profile.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bác sĩ chỉ có quyền chỉ định dịch vụ cho hồ sơ của mình"
            )

    srv_code = order_in.service_code or generate_service_code(db)
    srv = ServiceOrder(
        medical_record_id=record.id,
        service_name=order_in.service_name,
        service_code=srv_code,
        price=order_in.price,
        notes=order_in.notes,
        result=order_in.result
    )
    db.add(srv)
    db.commit()
    db.refresh(srv)

    client_ip = request.client.host if request.client else "unknown"
    audit = AuditLog(
        user_id=current_user.id,
        action="ADD_SERVICE_ORDER",
        resource_type="ServiceOrder",
        resource_id=str(srv.id),
        details=f"Added service order {srv.service_name} ({srv.service_code}) to record {record.record_code}",
        ip_address=client_ip
    )
    db.add(audit)
    db.commit()

    return srv


@router.post("/{record_id}/complete", response_model=MedicalRecordResponse)
def complete_medical_record(
    record_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_doctor)
):
    """
    Complete clinical consultation encounter.
    Transitions status to COMPLETED and completes linked appointment.
    """
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hồ sơ bệnh án"
        )

    # Doctor Isolation Check
    if current_user.role == RoleEnum.DOCTOR.value:
        doc_profile = db.query(Doctor).filter(Doctor.user_id == current_user.id).first()
        if not doc_profile or record.doctor_id != doc_profile.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bác sĩ chỉ có quyền hoàn tất hồ sơ do chính mình phụ trách"
            )

    record.status = RecordStatus.COMPLETED.value
    if record.appointment:
        record.appointment.status = AppointmentStatus.COMPLETED.value

    db.commit()
    db.refresh(record)

    client_ip = request.client.host if request.client else "unknown"
    audit = AuditLog(
        user_id=current_user.id,
        action="COMPLETE_MEDICAL_RECORD",
        resource_type="MedicalRecord",
        resource_id=str(record.id),
        details=f"Completed consultation for medical record {record.record_code}",
        ip_address=client_ip
    )
    db.add(audit)
    db.commit()

    return record
