from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.core.conflict_checker import check_appointment_conflict
from backend.app.database import get_db
from backend.app.models.appointment import Appointment, AppointmentStatus
from backend.app.models.audit import AuditLog
from backend.app.models.clinic import Doctor, Shift
from backend.app.models.patient import Patient
from backend.app.models.user import User
from backend.app.api.v1.appointments import generate_appointment_code
from backend.app.api.v1.patients import generate_medical_code
from backend.app.schemas.public_registration import (
    PublicBookingRequest,
    PublicBookingResponse,
    PublicDoctor,
)

router = APIRouter(prefix="/public", tags=["Public Registration"])


def available_doctor(db: Session, doctor_id: int) -> Doctor:
    doctor = (
        db.query(Doctor)
        .join(User, Doctor.user_id == User.id)
        .filter(Doctor.id == doctor_id, User.is_active.is_(True))
        .first()
    )
    if not doctor:
        raise HTTPException(status_code=404, detail="Không tìm thấy bác sĩ")
    return doctor


@router.get("/doctors", response_model=list[PublicDoctor])
def list_public_doctors(db: Session = Depends(get_db)):
    doctors = db.query(Doctor).join(User).filter(User.is_active.is_(True)).all()
    return [
        PublicDoctor(
            id=doctor.id,
            full_name=doctor.user.full_name,
            title=doctor.title,
            specialty=doctor.specialty.name,
            shifts=[
                {
                    "day_of_week": shift.day_of_week,
                    "start_time": shift.start_time,
                    "end_time": shift.end_time,
                }
                for shift in doctor.shifts
            ],
        )
        for doctor in doctors
    ]


@router.post(
    "/appointments",
    response_model=PublicBookingResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_appointment(
    booking: PublicBookingRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """Register a new patient and pending appointment without exposing records."""
    if booking.appointment_date < date.today():
        raise HTTPException(status_code=422, detail="Ngày khám không được ở trong quá khứ")
    if booking.date_of_birth > date.today():
        raise HTTPException(status_code=422, detail="Ngày sinh không hợp lệ")
    if booking.identity_card and db.query(Patient).filter(
        Patient.identity_card == booking.identity_card
    ).first():
        raise HTTPException(
            status_code=409,
            detail="Thông tin đã được đăng ký. Vui lòng liên hệ lễ tân để đặt lịch.",
        )
    if db.query(Patient).filter(
        Patient.full_name == booking.full_name,
        Patient.date_of_birth == booking.date_of_birth,
        Patient.phone == booking.phone,
    ).first():
        raise HTTPException(
            status_code=409,
            detail="Thông tin đã được đăng ký. Vui lòng liên hệ lễ tân để đặt lịch.",
        )

    doctor = available_doctor(db, booking.doctor_id)
    start = datetime.combine(booking.appointment_date, booking.start_time)
    if start <= datetime.now():
        raise HTTPException(status_code=422, detail="Giờ khám phải ở trong tương lai")
    end_time = (start + timedelta(minutes=30)).time()
    if end_time <= booking.start_time:
        raise HTTPException(status_code=422, detail="Giờ khám không hợp lệ")

    shift = db.query(Shift).filter(
        Shift.doctor_id == doctor.id,
        Shift.day_of_week == booking.appointment_date.weekday(),
        Shift.start_time <= booking.start_time,
        Shift.end_time >= end_time,
    ).first()
    if not shift:
        raise HTTPException(status_code=409, detail="Bác sĩ không có ca làm việc trong giờ đã chọn")

    is_available, _ = check_appointment_conflict(
        db=db,
        doctor_id=doctor.id,
        clinic_id=doctor.clinic_id,
        appointment_date=booking.appointment_date,
        start_time=booking.start_time,
        end_time=end_time,
    )
    if not is_available:
        raise HTTPException(status_code=409, detail="Khung giờ đã có lịch hẹn. Vui lòng chọn giờ khác.")

    patient = Patient(
        medical_code=generate_medical_code(db),
        full_name=booking.full_name,
        date_of_birth=booking.date_of_birth,
        gender=booking.gender,
        phone=booking.phone,
        identity_card=booking.identity_card,
    )
    appointment = Appointment(
        appointment_code=generate_appointment_code(db),
        patient=patient,
        doctor_id=doctor.id,
        clinic_id=doctor.clinic_id,
        appointment_date=booking.appointment_date,
        start_time=booking.start_time,
        end_time=end_time,
        status=AppointmentStatus.PENDING.value,
        reason=booking.reason,
    )
    db.add(appointment)
    try:
        db.flush()
        db.add(AuditLog(
            user_id=None,
            action="PUBLIC_BOOK_APPOINTMENT",
            resource_type="Appointment",
            resource_id=str(appointment.id),
            details=f"Public booking {appointment.appointment_code}",
            ip_address=request.client.host if request.client else "unknown",
        ))
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Không thể hoàn tất đăng ký. Vui lòng thử lại.")
    return appointment
