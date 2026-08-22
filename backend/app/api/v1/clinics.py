from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.clinic import Specialty, Clinic, Doctor, Shift
from backend.app.models.user import User, RoleEnum
from backend.app.schemas.clinic import (
    SpecialtyCreate, SpecialtyUpdate, SpecialtyResponse,
    ClinicCreate, ClinicUpdate, ClinicResponse,
    DoctorCreate, DoctorUpdate, DoctorResponse,
    ShiftCreate, ShiftUpdate, ShiftResponse
)
from backend.app.api.deps import require_admin, require_all_staff

router = APIRouter(tags=["Clinics, Specialties & Doctors"])


# ============================================================================
# Specialties Endpoints
# ============================================================================

@router.get("/specialties", response_model=List[SpecialtyResponse])
def get_specialties(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_all_staff)
):
    """List all medical specialties."""
    return db.query(Specialty).all()


@router.post("/specialties", response_model=SpecialtyResponse, status_code=status.HTTP_201_CREATED)
def create_specialty(
    specialty_in: SpecialtyCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Create a new medical specialty (Admin only)."""
    if db.query(Specialty).filter(Specialty.code == specialty_in.code).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Mã chuyên khoa '{specialty_in.code}' đã tồn tại"
        )
    if db.query(Specialty).filter(Specialty.name == specialty_in.name).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tên chuyên khoa '{specialty_in.name}' đã tồn tại"
        )
    specialty = Specialty(**specialty_in.model_dump())
    db.add(specialty)
    db.commit()
    db.refresh(specialty)
    return specialty


@router.put("/specialties/{specialty_id}", response_model=SpecialtyResponse)
def update_specialty(
    specialty_id: int,
    specialty_in: SpecialtyUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Update medical specialty (Admin only)."""
    specialty = db.query(Specialty).filter(Specialty.id == specialty_id).first()
    if not specialty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy chuyên khoa")
    
    update_data = specialty_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(specialty, field, value)
    
    db.commit()
    db.refresh(specialty)
    return specialty


@router.delete("/specialties/{specialty_id}", status_code=status.HTTP_200_OK)
def delete_specialty(
    specialty_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Delete medical specialty (Admin only)."""
    specialty = db.query(Specialty).filter(Specialty.id == specialty_id).first()
    if not specialty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy chuyên khoa")
    db.delete(specialty)
    db.commit()
    return {"message": "Đã xóa chuyên khoa thành công"}


# ============================================================================
# Clinics (Consultation Rooms) Endpoints
# ============================================================================

@router.get("/clinics", response_model=List[ClinicResponse])
def get_clinics(
    specialty_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_all_staff)
):
    """List all clinic consultation rooms."""
    query = db.query(Clinic)
    if specialty_id:
        query = query.filter(Clinic.specialty_id == specialty_id)
    return query.all()


@router.post("/clinics", response_model=ClinicResponse, status_code=status.HTTP_201_CREATED)
def create_clinic(
    clinic_in: ClinicCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Create a new consultation room (Admin only)."""
    if db.query(Clinic).filter(Clinic.room_number == clinic_in.room_number).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Số phòng '{clinic_in.room_number}' đã tồn tại"
        )
    specialty = db.query(Specialty).filter(Specialty.id == clinic_in.specialty_id).first()
    if not specialty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy chuyên khoa tương ứng")

    clinic = Clinic(**clinic_in.model_dump())
    db.add(clinic)
    db.commit()
    db.refresh(clinic)
    return clinic


@router.put("/clinics/{clinic_id}", response_model=ClinicResponse)
def update_clinic(
    clinic_id: int,
    clinic_in: ClinicUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Update consultation room (Admin only)."""
    clinic = db.query(Clinic).filter(Clinic.id == clinic_id).first()
    if not clinic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy phòng khám")
    
    update_data = clinic_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(clinic, field, value)
    
    db.commit()
    db.refresh(clinic)
    return clinic


@router.delete("/clinics/{clinic_id}", status_code=status.HTTP_200_OK)
def delete_clinic(
    clinic_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Delete consultation room (Admin only)."""
    clinic = db.query(Clinic).filter(Clinic.id == clinic_id).first()
    if not clinic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy phòng khám")
    db.delete(clinic)
    db.commit()
    return {"message": "Đã xóa phòng khám thành công"}


# ============================================================================
# Doctor Profiles & Shifts Endpoints
# ============================================================================

@router.get("/doctors", response_model=List[DoctorResponse])
def get_doctors(
    specialty_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_all_staff)
):
    """List all doctor profiles with specialties, assigned room, and shifts."""
    query = db.query(Doctor)
    if specialty_id:
        query = query.filter(Doctor.specialty_id == specialty_id)
    return query.all()


@router.get("/doctors/{doctor_id}", response_model=DoctorResponse)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_all_staff)
):
    """Get single doctor profile."""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy bác sĩ")
    return doctor


@router.post("/doctors", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def create_doctor(
    doctor_in: DoctorCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Create doctor profile for a user account (Admin only)."""
    user = db.query(User).filter(User.id == doctor_in.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tài khoản người dùng")
    
    if db.query(Doctor).filter(Doctor.user_id == doctor_in.user_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tài khoản này đã được tạo hồ sơ bác sĩ"
        )
    
    # Ensure role is DOCTOR
    user.role = RoleEnum.DOCTOR.value

    doctor = Doctor(**doctor_in.model_dump())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


@router.put("/doctors/{doctor_id}", response_model=DoctorResponse)
def update_doctor(
    doctor_id: int,
    doctor_in: DoctorUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Update doctor profile (Admin only)."""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy bác sĩ")
    
    update_data = doctor_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(doctor, field, value)
    
    db.commit()
    db.refresh(doctor)
    return doctor


# ============================================================================
# Shifts Endpoints
# ============================================================================

@router.get("/shifts", response_model=List[ShiftResponse])
def get_shifts(
    doctor_id: Optional[int] = None,
    day_of_week: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_all_staff)
):
    """List doctor working shifts."""
    query = db.query(Shift)
    if doctor_id:
        query = query.filter(Shift.doctor_id == doctor_id)
    if day_of_week is not None:
        query = query.filter(Shift.day_of_week == day_of_week)
    return query.all()


@router.post("/shifts", response_model=ShiftResponse, status_code=status.HTTP_201_CREATED)
def create_shift(
    shift_in: ShiftCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Add a working shift for a doctor (Admin only)."""
    doctor = db.query(Doctor).filter(Doctor.id == shift_in.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy bác sĩ")
    
    shift = Shift(**shift_in.model_dump())
    db.add(shift)
    db.commit()
    db.refresh(shift)
    return shift


@router.delete("/shifts/{shift_id}", status_code=status.HTTP_200_OK)
def delete_shift(
    shift_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Delete a working shift (Admin only)."""
    shift = db.query(Shift).filter(Shift.id == shift_id).first()
    if not shift:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy ca làm việc")
    db.delete(shift)
    db.commit()
    return {"message": "Đã xóa ca làm việc thành công"}
