from typing import List, Optional
from pydantic import BaseModel


class DailyStatsResponse(BaseModel):
    date: str
    total_appointments: int = 0
    completed_visits: int = 0
    new_patients: int = 0
    daily_revenue: float = 0.0


class RevenueStatsResponse(BaseModel):
    total_revenue: float = 0.0
    consultation_revenue: float = 0.0
    service_revenue: float = 0.0
    medicine_revenue: float = 0.0
    insurance_covered_amount: float = 0.0
    patient_paid_amount: float = 0.0
    pending_amount: float = 0.0


class SpecialtyStatsResponse(BaseModel):
    specialty_id: int
    specialty_code: Optional[str] = None
    specialty_name: str
    patient_count: int = 0
    appointment_count: int = 0
    revenue: float = 0.0
    percentage: float = 0.0


class DoctorWorkloadResponse(BaseModel):
    doctor_id: int
    doctor_name: str
    specialty_name: str
    title: Optional[str] = None
    total_consultations: int = 0
    total_appointments: int = 0
    total_revenue_generated: float = 0.0
    total_prescriptions: int = 0


class RevenueTrendItem(BaseModel):
    date: str
    total_revenue: float = 0.0
    consultation_revenue: float = 0.0
    service_revenue: float = 0.0
    medicine_revenue: float = 0.0
    insurance_covered_amount: float = 0.0
    patient_paid_amount: float = 0.0
    paid_invoices_count: int = 0


class StatsOverviewResponse(BaseModel):
    total_patients: int = 0
    today_appointments: int = 0
    completed_exams: int = 0
    today_completed: int = 0
    total_revenue: float = 0.0
    today_revenue: float = 0.0
    pending_invoice_count: int = 0
    pending_invoices_count: int = 0
    total_doctors: int = 0
    active_clinics: int = 0
    revenue_by_specialty: List[SpecialtyStatsResponse] = []


class DashboardStatsResponse(StatsOverviewResponse):
    pass
