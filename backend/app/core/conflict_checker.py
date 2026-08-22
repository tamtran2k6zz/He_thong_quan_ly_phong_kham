from datetime import date, time
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, not_
from backend.app.models.appointment import Appointment, AppointmentStatus
from backend.app.models.clinic import Shift


def check_appointment_conflict(
    db: Session,
    doctor_id: int,
    clinic_id: Optional[int],
    appointment_date: date,
    start_time: time,
    end_time: time,
    exclude_appointment_id: Optional[int] = None
) -> Tuple[bool, Optional[str]]:
    """
    Checks for scheduling conflicts for doctor and consultation room.
    
    Returns:
        (True, None) if slot is valid and free of conflict.
        (False, error_message) if doctor or clinic is already booked.
    """
    if start_time >= end_time:
        return False, "Giờ bắt đầu phải sớm hơn giờ kết thúc"

    # 1. Check doctor time overlap
    doctor_query = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.appointment_date == appointment_date,
        Appointment.status != AppointmentStatus.CANCELLED.value,
        Appointment.start_time < end_time,
        Appointment.end_time > start_time
    )
    if exclude_appointment_id is not None:
        doctor_query = doctor_query.filter(Appointment.id != exclude_appointment_id)
        
    conflicting_doctor_appt = doctor_query.first()
    if conflicting_doctor_appt:
        return False, (
            f"Bác sĩ đã có lịch hẹn mã {conflicting_doctor_appt.appointment_code} "
            f"trong khung giờ {conflicting_doctor_appt.start_time.strftime('%H:%M')} - "
            f"{conflicting_doctor_appt.end_time.strftime('%H:%M')}"
        )

    # 2. Check clinic room time overlap (if clinic_id provided)
    if clinic_id:
        clinic_query = db.query(Appointment).filter(
            Appointment.clinic_id == clinic_id,
            Appointment.appointment_date == appointment_date,
            Appointment.status != AppointmentStatus.CANCELLED.value,
            Appointment.start_time < end_time,
            Appointment.end_time > start_time
        )
        if exclude_appointment_id is not None:
            clinic_query = clinic_query.filter(Appointment.id != exclude_appointment_id)
            
        conflicting_clinic_appt = clinic_query.first()
        if conflicting_clinic_appt:
            return False, (
                f"Phòng khám đã có lịch hẹn mã {conflicting_clinic_appt.appointment_code} "
                f"trong khung giờ {conflicting_clinic_appt.start_time.strftime('%H:%M')} - "
                f"{conflicting_clinic_appt.end_time.strftime('%H:%M')}"
            )

    return True, None
