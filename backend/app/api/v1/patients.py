from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.app.database import get_db
from backend.app.models.patient import Patient
from backend.app.models.audit import AuditLog
from backend.app.models.user import User, RoleEnum
from backend.app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from backend.app.api.deps import require_clinical_staff, require_admin

router = APIRouter(prefix="/patients", tags=["Patients Management"])


def generate_medical_code(db: Session) -> str:
    """Generates unique medical code in format BN-YYYYMMDD-XXXX."""
    today_str = datetime.utcnow().strftime("%Y%m%d")
    prefix = f"BN-{today_str}-"
    count = db.query(Patient).filter(Patient.medical_code.like(f"{prefix}%")).count()
    candidate = f"{prefix}{count + 1:04d}"
    # Double check collision
    while db.query(Patient).filter(Patient.medical_code == candidate).first():
        count += 1
        candidate = f"{prefix}{count + 1:04d}"
    return candidate


@router.get("", response_model=List[PatientResponse])
def get_patients(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    q: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinical_staff)
):
    """
    Search and list patients.
    Supports searching by Name, Phone, CCCD, BHYT, or Medical Code.
    """
    query = db.query(Patient)
    if q:
        search_filter = f"%{q.strip()}%"
        query = query.filter(
            or_(
                Patient.full_name.ilike(search_filter),
                Patient.phone.ilike(search_filter),
                Patient.identity_card.ilike(search_filter),
                Patient.insurance_number.ilike(search_filter),
                Patient.medical_code.ilike(search_filter)
            )
        )
    return query.order_by(Patient.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(
    patient_in: PatientCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinical_staff)
):
    """
    Register a new patient. Auto-generates medical code BN-YYYYMMDD-XXXX if omitted.
    """
    # Check CCCD duplication if provided
    if patient_in.identity_card:
        existing_cccd = db.query(Patient).filter(Patient.identity_card == patient_in.identity_card).first()
        if existing_cccd:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Số CCCD/CMND '{patient_in.identity_card}' đã tồn tại trong hệ thống (Mã BN: {existing_cccd.medical_code})"
            )
    
    # Generate medical code
    medical_code = patient_in.medical_code
    if not medical_code:
        medical_code = generate_medical_code(db)
    else:
        if db.query(Patient).filter(Patient.medical_code == medical_code).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Mã bệnh nhân '{medical_code}' đã tồn tại"
            )

    patient_data = patient_in.model_dump(exclude_unset=False)
    dob_val = patient_data.pop("dob", None)
    if not patient_data.get("date_of_birth") and dob_val:
        patient_data["date_of_birth"] = dob_val
    if not patient_data.get("date_of_birth"):
        patient_data["date_of_birth"] = date(1990, 1, 1)
    patient_data["medical_code"] = medical_code
    
    patient = Patient(**patient_data)
    db.add(patient)
    db.commit()
    db.refresh(patient)

    # Log audit
    client_ip = request.client.host if request.client else "unknown"
    audit = AuditLog(
        user_id=current_user.id,
        action="CREATE_PATIENT",
        resource_type="Patient",
        resource_id=str(patient.id),
        details=f"Created patient {patient.full_name} ({patient.medical_code}) by {current_user.username}",
        ip_address=client_ip
    )
    db.add(audit)
    db.commit()

    return patient


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinical_staff)
):
    """
    Get patient detailed information.
    """
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hồ sơ bệnh nhân"
        )

    # Log audit
    client_ip = request.client.host if request.client else "unknown"
    audit = AuditLog(
        user_id=current_user.id,
        action="VIEW_PATIENT",
        resource_type="Patient",
        resource_id=str(patient.id),
        details=f"Viewed patient {patient.full_name} ({patient.medical_code}) by {current_user.username}",
        ip_address=client_ip
    )
    db.add(audit)
    db.commit()

    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient_in: PatientUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinical_staff)
):
    """
    Update patient information.
    """
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hồ sơ bệnh nhân"
        )

    if patient_in.identity_card and patient_in.identity_card != patient.identity_card:
        existing_cccd = db.query(Patient).filter(
            Patient.identity_card == patient_in.identity_card,
            Patient.id != patient_id
        ).first()
        if existing_cccd:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Số CCCD '{patient_in.identity_card}' đã trùng với bệnh nhân khác"
            )

    update_data = patient_in.model_dump(exclude_unset=True)
    dob_val = update_data.pop("dob", None)
    if "date_of_birth" not in update_data and dob_val:
        update_data["date_of_birth"] = dob_val
    for field, value in update_data.items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)

    # Log audit
    client_ip = request.client.host if request.client else "unknown"
    audit = AuditLog(
        user_id=current_user.id,
        action="UPDATE_PATIENT",
        resource_type="Patient",
        resource_id=str(patient.id),
        details=f"Updated patient {patient.full_name} ({patient.medical_code}) by {current_user.username}",
        ip_address=client_ip
    )
    db.add(audit)
    db.commit()

    return patient


@router.delete("/{patient_id}", status_code=status.HTTP_200_OK)
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """
    Delete patient record (Admin only).
    """
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hồ sơ bệnh nhân"
        )
    db.delete(patient)
    db.commit()
    return {"message": f"Đã xóa hồ sơ bệnh nhân {patient.full_name} thành công"}
