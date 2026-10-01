from fastapi import APIRouter
from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.users import router as users_router
from backend.app.api.v1.clinics import router as clinics_router
from backend.app.api.v1.patients import router as patients_router
from backend.app.api.v1.appointments import router as appointments_router
from backend.app.api.v1.medical_records import router as medical_records_router
from backend.app.api.v1.prescriptions import router as prescriptions_router
from backend.app.api.v1.medicines import router as medicines_router
from backend.app.api.v1.invoices import router as invoices_router
from backend.app.api.v1.ai import router as ai_router
from backend.app.api.v1.audit import router as audit_router
from backend.app.api.v1.stats import router as stats_router
from backend.app.api.v1.public_registration import router as public_registration_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(clinics_router)
api_router.include_router(patients_router)
api_router.include_router(appointments_router)
api_router.include_router(medical_records_router)
api_router.include_router(prescriptions_router)
api_router.include_router(medicines_router)
api_router.include_router(invoices_router)
api_router.include_router(ai_router)
api_router.include_router(audit_router)
api_router.include_router(stats_router)
api_router.include_router(public_registration_router)

__all__ = ["api_router"]
