"""
Clinical & Financial Analytics Router.
Provides:
- GET /api/v1/stats: Overview dashboard counters (alias to /overview).
- GET /api/v1/stats/overview: Overview counters (total patients, today's appointments, completed exams, total revenue, pending invoice count).
- GET /api/v1/stats/revenue-by-date: Revenue trend (daily/monthly).
- GET /api/v1/stats/patients-by-specialty: Patient distribution across specialties.
- GET /api/v1/stats/doctor-workload: Doctor consultation volume and revenue.
"""

from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct, cast, Date

from backend.app.database import get_db
from backend.app.models.user import User, RoleEnum
from backend.app.models.patient import Patient
from backend.app.models.appointment import Appointment, AppointmentStatus
from backend.app.models.medical_record import MedicalRecord, RecordStatus
from backend.app.models.prescription import Prescription
from backend.app.models.invoice import Invoice, PaymentStatus
from backend.app.models.clinic import Specialty, Clinic, Doctor
from backend.app.schemas.stats import (
    StatsOverviewResponse,
    RevenueTrendItem,
    SpecialtyStatsResponse,
    DoctorWorkloadResponse
)
from backend.app.api.deps import require_all_staff

router = APIRouter(prefix="/stats", tags=["Clinical & Financial Analytics"])


def compute_overview_stats(db: Session) -> StatsOverviewResponse:
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())

    # 1. Total Patients
    total_patients = db.query(Patient).count()

    # 2. Today's Appointments
    today_appointments = db.query(Appointment).filter(
        Appointment.appointment_date == today
    ).count()

    # 3. Completed Exams (Today and Total)
    completed_exams = db.query(MedicalRecord).filter(
        MedicalRecord.status == RecordStatus.COMPLETED.value
    ).count()
    if completed_exams == 0:
        # Fallback to count all medical records
        completed_exams = db.query(MedicalRecord).count()

    today_completed = db.query(MedicalRecord).filter(
        MedicalRecord.exam_date >= today_start,
        MedicalRecord.exam_date <= today_end
    ).count()

    # 4. Revenues
    total_revenue_val = db.query(
        func.coalesce(func.sum(Invoice.patient_pay_amount), 0.0)
    ).filter(
        Invoice.payment_status == PaymentStatus.PAID.value
    ).scalar() or 0.0

    today_revenue_val = db.query(
        func.coalesce(func.sum(Invoice.patient_pay_amount), 0.0)
    ).filter(
        Invoice.payment_status == PaymentStatus.PAID.value,
        Invoice.paid_at >= today_start,
        Invoice.paid_at <= today_end
    ).scalar() or 0.0

    # 5. Pending Invoices
    pending_count = db.query(Invoice).filter(
        Invoice.payment_status == PaymentStatus.PENDING.value
    ).count()

    # 6. Doctors & Clinics
    total_doctors = db.query(Doctor).count()
    active_clinics = db.query(Clinic).filter(Clinic.is_active == True).count()

    # 7. Specialty breakdown
    specialties = db.query(Specialty).all()
    specialty_stats: List[SpecialtyStatsResponse] = []
    
    for sp in specialties:
        # Doctor IDs in this specialty
        doc_ids = [d.id for d in sp.doctors]
        p_count = 0
        sp_revenue = 0.0
        if doc_ids:
            # Count distinct patients
            p_count = db.query(distinct(MedicalRecord.patient_id)).filter(
                MedicalRecord.doctor_id.in_(doc_ids)
            ).count()

            # Sum revenue
            rev = db.query(
                func.coalesce(func.sum(Invoice.patient_pay_amount), 0.0)
            ).join(
                MedicalRecord, Invoice.medical_record_id == MedicalRecord.id
            ).filter(
                MedicalRecord.doctor_id.in_(doc_ids),
                Invoice.payment_status == PaymentStatus.PAID.value
            ).scalar()
            sp_revenue = float(rev) if rev else 0.0

        specialty_stats.append(
            SpecialtyStatsResponse(
                specialty_id=sp.id,
                specialty_code=sp.code,
                specialty_name=sp.name,
                patient_count=p_count,
                appointment_count=0,
                revenue=sp_revenue,
                percentage=round((p_count / total_patients * 100), 1) if total_patients > 0 else 0.0
            )
        )

    return StatsOverviewResponse(
        total_patients=total_patients,
        today_appointments=today_appointments,
        completed_exams=completed_exams,
        today_completed=today_completed,
        total_revenue=float(total_revenue_val),
        today_revenue=float(today_revenue_val),
        pending_invoice_count=pending_count,
        pending_invoices_count=pending_count,
        total_doctors=total_doctors,
        active_clinics=active_clinics,
        revenue_by_specialty=specialty_stats
    )


@router.get("", response_model=StatsOverviewResponse)
def get_stats_root(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_all_staff)
):
    """
    Overview statistics and counters (Root alias).
    """
    return compute_overview_stats(db)


@router.get("/overview", response_model=StatsOverviewResponse)
def get_stats_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_all_staff)
):
    """
    Overview statistics and counters for administrative and clinical dashboards.
    """
    return compute_overview_stats(db)


@router.get("/revenue-by-date", response_model=List[RevenueTrendItem])
def get_revenue_by_date(
    from_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    to_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    period: str = Query("daily", description="'daily' or 'monthly'"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_all_staff)
):
    """
    Revenue trends breakdown (daily or monthly).
    """
    if not to_date:
        to_date = date.today()
    if not from_date:
        from_date = to_date - timedelta(days=30)

    start_dt = datetime.combine(from_date, datetime.min.time())
    end_dt = datetime.combine(to_date, datetime.max.time())

    invoices = db.query(Invoice).filter(
        Invoice.payment_status == PaymentStatus.PAID.value,
        Invoice.paid_at >= start_dt,
        Invoice.paid_at <= end_dt
    ).order_by(Invoice.paid_at.asc()).all()

    # Aggregate by date / month
    trend_dict: Dict[str, RevenueTrendItem] = {}

    for inv in invoices:
        paid_time = inv.paid_at or inv.created_at
        if period == "monthly":
            key_str = paid_time.strftime("%Y-%m")
        else:
            key_str = paid_time.strftime("%Y-%m-%d")

        if key_str not in trend_dict:
            trend_dict[key_str] = RevenueTrendItem(date=key_str)

        item = trend_dict[key_str]
        item.total_revenue += float(inv.total_amount)
        item.consultation_revenue += float(inv.consultation_fee)
        item.service_revenue += float(inv.service_fee)
        item.medicine_revenue += float(inv.medicine_fee)
        item.insurance_covered_amount += float(inv.insurance_discount)
        item.patient_paid_amount += float(inv.patient_pay_amount)
        item.paid_invoices_count += 1

    # If no records, populate dates with zeros for a smooth trend curve
    if not trend_dict:
        curr = from_date
        while curr <= to_date:
            k = curr.strftime("%Y-%m") if period == "monthly" else curr.strftime("%Y-%m-%d")
            if k not in trend_dict:
                trend_dict[k] = RevenueTrendItem(date=k)
            curr += timedelta(days=1) if period != "monthly" else timedelta(days=30)

    return sorted(trend_dict.values(), key=lambda x: x.date)


@router.get("/patients-by-specialty", response_model=List[SpecialtyStatsResponse])
def get_patients_by_specialty(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_all_staff)
):
    """
    Patient and revenue distribution across all medical specialties.
    """
    total_patients = db.query(Patient).count()
    specialties = db.query(Specialty).all()
    results: List[SpecialtyStatsResponse] = []

    for sp in specialties:
        doc_ids = [d.id for d in sp.doctors]
        patient_count = 0
        appointment_count = 0
        sp_revenue = 0.0

        if doc_ids:
            patient_count = db.query(distinct(MedicalRecord.patient_id)).filter(
                MedicalRecord.doctor_id.in_(doc_ids)
            ).count()

            appointment_count = db.query(Appointment).filter(
                Appointment.doctor_id.in_(doc_ids)
            ).count()

            rev = db.query(
                func.coalesce(func.sum(Invoice.patient_pay_amount), 0.0)
            ).join(
                MedicalRecord, Invoice.medical_record_id == MedicalRecord.id
            ).filter(
                MedicalRecord.doctor_id.in_(doc_ids),
                Invoice.payment_status == PaymentStatus.PAID.value
            ).scalar()
            sp_revenue = float(rev) if rev else 0.0

        percentage = round((patient_count / total_patients * 100), 1) if total_patients > 0 else 0.0

        results.append(
            SpecialtyStatsResponse(
                specialty_id=sp.id,
                specialty_code=sp.code,
                specialty_name=sp.name,
                patient_count=patient_count,
                appointment_count=appointment_count,
                revenue=sp_revenue,
                percentage=percentage
            )
        )

    return results


@router.get("/doctor-workload", response_model=List[DoctorWorkloadResponse])
def get_doctor_workload(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_all_staff)
):
    """
    Doctor clinical consultation volume, prescriptions written, and revenue generation.
    """
    doctors = db.query(Doctor).all()
    results: List[DoctorWorkloadResponse] = []

    for doc in doctors:
        doc_name = doc.user.full_name if doc.user else f"Bác sĩ ID {doc.id}"
        specialty_name = doc.specialty.name if doc.specialty else "Đa khoa"

        total_consultations = db.query(MedicalRecord).filter(
            MedicalRecord.doctor_id == doc.id
        ).count()

        total_appointments = db.query(Appointment).filter(
            Appointment.doctor_id == doc.id
        ).count()

        total_prescriptions = db.query(Prescription).filter(
            Prescription.doctor_id == doc.id
        ).count()

        rev = db.query(
            func.coalesce(func.sum(Invoice.patient_pay_amount), 0.0)
        ).join(
            MedicalRecord, Invoice.medical_record_id == MedicalRecord.id
        ).filter(
            MedicalRecord.doctor_id == doc.id,
            Invoice.payment_status == PaymentStatus.PAID.value
        ).scalar()
        total_revenue = float(rev) if rev else 0.0

        results.append(
            DoctorWorkloadResponse(
                doctor_id=doc.id,
                doctor_name=doc_name,
                specialty_name=specialty_name,
                title=doc.title,
                total_consultations=total_consultations,
                total_appointments=total_appointments,
                total_revenue_generated=total_revenue,
                total_prescriptions=total_prescriptions
            )
        )

    return results
