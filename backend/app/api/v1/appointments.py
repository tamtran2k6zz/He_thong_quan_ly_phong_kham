from datetime import date, time, datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.app.database import get_db
from backend.app.models.appointment import Appointment, AppointmentStatus
from backend.app.models.clinic import Doctor, Clinic, Shift
from backend.app.models.patient import Patient
from backend.app.models.audit import AuditLog
from backend.app.models.user import User
from backend.app.core.conflict_checker import check_appointment_conflict
from backend.app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
    AvailableSlotResponse
)
from backend.app.api.deps import require_clinical_staff, require_all_staff

router = APIRouter(prefix="/appointments", tags=["Appointments Management"])


def generate_appointment_code(db: Session) -> str:
    """Generates unique appointment code in format LH-YYYYMMDD-XXXX."""
    today_str = datetime.utcnow().strftime("%Y%m%d")
    prefix = f"LH-{today_str}-"
    count = db.query(Appointment).filter(Appointment.appointment_code.like(f"{prefix}%")).count()
    candidate = f"{prefix}{count + 1:04d}"
    while db.query(Appointment).filter(Appointment.appointment_code == candidate).first():
        count += 1
        candidate = f"{prefix}{count + 1:04d}"
    return candidate


@router.get("/available-slots", response_model=List[AvailableSlotResponse])
def get_available_slots(
    doctor_id: int = Query(..., description="ID của bác sĩ"),
    date: Optional[date] = Query(None, description="Ngày khám (YYYY-MM-DD)"),
    appointment_date: Optional[date] = Query(None, description="Ngày khám thay thế"),
    clinic_id: Optional[int] = Query(None, description="ID phòng khám"),
    slot_duration_minutes: int = Query(30, ge=15, le=120),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_all_staff)
):
    """
    Get all available appointment time slots for a given doctor on a specific date.
    Calculates conflict status for each half-hour interval.
    """
    target_date = date or appointment_date or (datetime.utcnow().date() + timedelta(days=1))

    # Standard working day slots: Morning (08:00 - 11:30), Afternoon (13:30 - 17:00)
    slot_windows = [
        (time(8, 0), time(11, 30)),
        (time(13, 30), time(17, 0))
    ]

    slots_result = []
    for start_window, end_window in slot_windows:
        curr = datetime.combine(target_date, start_window)
        end_boundary = datetime.combine(target_date, end_window)

        while curr + timedelta(minutes=slot_duration_minutes) <= end_boundary:
            slot_start = curr.time()
            slot_end = (curr + timedelta(minutes=slot_duration_minutes)).time()

            is_valid, reason = check_appointment_conflict(
                db=db,
                doctor_id=doctor_id,
                clinic_id=clinic_id,
                appointment_date=target_date,
                start_time=slot_start,
                end_time=slot_end
            )

            slots_result.append(
                AvailableSlotResponse(
                    start_time=slot_start.strftime("%H:%M:%S"),
                    end_time=slot_end.strftime("%H:%M:%S"),
                    is_available=is_valid,
                    conflict_reason=reason
                )
            )

            curr += timedelta(minutes=slot_duration_minutes)

    return slots_result


@router.get("", response_model=List[AppointmentResponse])
def get_appointments(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    doctor_id: Optional[int] = None,
    patient_id: Optional[int] = None,
    clinic_id: Optional[int] = None,
    status: Optional[str] = None,
    date: Optional[date] = None,
    appointment_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_all_staff)
):
    """
    List appointments with optional filtering by doctor, patient, room, status, and date.
    """
    query = db.query(Appointment)

    target_date = date or appointment_date
    if target_date:
        query = query.filter(Appointment.appointment_date == target_date)
    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)
    if patient_id:
        query = query.filter(Appointment.patient_id == patient_id)
    if clinic_id:
        query = query.filter(Appointment.clinic_id == clinic_id)
    if status:
        query = query.filter(Appointment.status == status.upper())

    return query.order_by(Appointment.appointment_date.desc(), Appointment.start_time.asc()).offset(skip).limit(limit).all()


@router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(
    appointment_in: AppointmentCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinical_staff)
):
    """
    Book a new appointment.
    Validates patient, doctor, and clinic existence, and runs conflict detection engine.
    """
    # 1. Verify patient exists
    patient = db.query(Patient).filter(Patient.id == appointment_in.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy bệnh nhân ID {appointment_in.patient_id}"
        )

    # 2. Verify doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == appointment_in.doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy bác sĩ ID {appointment_in.doctor_id}"
        )

    # 3. If clinic_id not specified, fallback to doctor's assigned clinic room
    clinic_id = appointment_in.clinic_id or doctor.clinic_id

    # 4. Check for scheduling conflicts (Doctor overlap, Room overlap)
    is_valid, conflict_reason = check_appointment_conflict(
        db=db,
        doctor_id=appointment_in.doctor_id,
        clinic_id=clinic_id,
        appointment_date=appointment_in.appointment_date,
        start_time=appointment_in.start_time,
        end_time=appointment_in.end_time
    )
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Trùng lịch khám: {conflict_reason}"
        )

    # 5. Generate code
    code = appointment_in.appointment_code
    if not code:
        code = generate_appointment_code(db)
    else:
        existing = db.query(Appointment).filter(Appointment.appointment_code == code).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Mã lịch hẹn '{code}' đã tồn tại"
            )

    appt_data = appointment_in.model_dump(exclude_unset=False)
    appt_data["appointment_code"] = code
    appt_data["clinic_id"] = clinic_id
    if not appt_data.get("status"):
        appt_data["status"] = AppointmentStatus.PENDING.value
    else:
        appt_data["status"] = appt_data["status"].upper()

    appointment = Appointment(**appt_data)
    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    # Log audit
    client_ip = request.client.host if request.client else "unknown"
    audit = AuditLog(
        user_id=current_user.id,
        action="BOOK_APPOINTMENT",
        resource_type="Appointment",
        resource_id=str(appointment.id),
        details=f"Booked appointment {appointment.appointment_code} for patient {patient.full_name} with Dr. ID {doctor.id}",
        ip_address=client_ip
    )
    db.add(audit)
    db.commit()

    return appointment


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_all_staff)
):
    """
    Get appointment details by ID.
    """
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy lịch hẹn"
        )
    return appointment


@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    appointment_in: AppointmentUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinical_staff)
):
    """
    Update appointment details, reschedule, or transition status.
    Re-runs conflict detection if time, date, doctor, or clinic is altered.
    """
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy lịch hẹn"
        )

    target_doctor_id = appointment_in.doctor_id or appointment.doctor_id
    target_clinic_id = appointment_in.clinic_id if appointment_in.clinic_id is not None else appointment.clinic_id
    target_date = appointment_in.appointment_date or appointment.appointment_date
    target_start = appointment_in.start_time or appointment.start_time
    target_end = appointment_in.end_time or appointment.end_time

    # If rescheduling or changing doctor/room, run conflict check excluding current appointment
    if (
        appointment_in.appointment_date is not None
        or appointment_in.start_time is not None
        or appointment_in.end_time is not None
        or appointment_in.doctor_id is not None
        or appointment_in.clinic_id is not None
    ):
        is_valid, conflict_reason = check_appointment_conflict(
            db=db,
            doctor_id=target_doctor_id,
            clinic_id=target_clinic_id,
            appointment_date=target_date,
            start_time=target_start,
            end_time=target_end,
            exclude_appointment_id=appointment.id
        )
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Trùng lịch hẹn khi đổi giờ: {conflict_reason}"
            )

    update_data = appointment_in.model_dump(exclude_unset=True)
    if "status" in update_data and update_data["status"]:
        update_data["status"] = update_data["status"].upper()

    for field, value in update_data.items():
        setattr(appointment, field, value)

    db.commit()
    db.refresh(appointment)

    client_ip = request.client.host if request.client else "unknown"
    audit = AuditLog(
        user_id=current_user.id,
        action="UPDATE_APPOINTMENT",
        resource_type="Appointment",
        resource_id=str(appointment.id),
        details=f"Updated appointment {appointment.appointment_code} (Status: {appointment.status})",
        ip_address=client_ip
    )
    db.add(audit)
    db.commit()

    return appointment


@router.post("/{appointment_id}/check-in", response_model=AppointmentResponse)
def check_in_appointment(
    appointment_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinical_staff)
):
    """
    Receptionist check-in when patient arrives at clinic.
    Transitions appointment status to CHECKED_IN.
    """
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy lịch hẹn"
        )

    appointment.status = AppointmentStatus.CHECKED_IN.value
    db.commit()
    db.refresh(appointment)

    client_ip = request.client.host if request.client else "unknown"
    audit = AuditLog(
        user_id=current_user.id,
        action="CHECKIN_APPOINTMENT",
        resource_type="Appointment",
        resource_id=str(appointment.id),
        details=f"Checked in appointment {appointment.appointment_code}",
        ip_address=client_ip
    )
    db.add(audit)
    db.commit()

    return appointment


@router.post("/{appointment_id}/cancel", response_model=AppointmentResponse)
def cancel_appointment(
    appointment_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinical_staff)
):
    """
    Cancel appointment and free up doctor/room slot.
    """
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy lịch hẹn"
        )

    appointment.status = AppointmentStatus.CANCELLED.value
    db.commit()
    db.refresh(appointment)

    client_ip = request.client.host if request.client else "unknown"
    audit = AuditLog(
        user_id=current_user.id,
        action="CANCEL_APPOINTMENT",
        resource_type="Appointment",
        resource_id=str(appointment.id),
        details=f"Cancelled appointment {appointment.appointment_code}",
        ip_address=client_ip
    )
    db.add(audit)
    db.commit()

    return appointment
