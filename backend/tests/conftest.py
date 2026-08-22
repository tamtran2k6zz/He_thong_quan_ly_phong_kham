"""
Pytest Test Infrastructure & Configuration for Clinic Management System.
Provides high-performance in-memory SQLite test database with StaticPool,
FastAPI TestClient with transactional isolation, complete seed dataset,
and authenticated header fixtures for 4 RBAC roles.
"""

import os
import sys
import pytest
from datetime import date, time, datetime, timedelta
from typing import Generator, Dict, Any

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

# Ensure workspace root is in sys.path
WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# Set test environment flags
os.environ["ENVIRONMENT"] = "testing"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["AI_PROVIDER"] = "MOCK"
os.environ["JWT_SECRET"] = "test-jwt-secret-key-super-secure-clinic-2026"
os.environ["SECRET_KEY"] = "test-jwt-secret-key-super-secure-clinic-2026"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "60"

from backend.app.main import app
from backend.app.database import Base, get_db
from backend.app.seed.seed_data import seed_database
from backend.app.models.user import User, RoleEnum
from backend.app.models.clinic import Specialty, Clinic, Doctor, Shift
from backend.app.models.patient import Patient
from backend.app.models.appointment import Appointment, AppointmentStatus
from backend.app.models.medical_record import MedicalRecord, RecordStatus, ServiceOrder
from backend.app.models.prescription import Medicine, Prescription, PrescriptionItem
from backend.app.models.invoice import Invoice, PaymentStatus, PaymentMethod
from backend.app.models.audit import AuditLog, AIInvocationLog
from backend.app.core.security import create_access_token, get_password_hash

# Ultra-fast in-memory SQLite engine with StaticPool
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if hasattr(dbapi_connection, "cursor"):
        try:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()
        except Exception:
            pass

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create all database tables and seed initial catalog data once in memory."""
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    seed_database(db)
    db.close()
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Provides a transactional database session for each test function.
    Rolls back any changes made during the test to guarantee 100% isolation.
    """
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    FastAPI TestClient with overridden get_db dependency.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def seed_data(db_session: Session) -> Dict[str, Any]:
    """
    Convenience lookup dictionary for pre-seeded database entities.
    """
    admin_user = db_session.query(User).filter(User.username == "admin").first()
    receptionist_user = db_session.query(User).filter(User.username == "receptionist").first()
    doctor_user_1 = db_session.query(User).filter(User.username == "dr_nam").first()
    doctor_user_2 = db_session.query(User).filter(User.username == "dr_huong").first()
    accountant_user = db_session.query(User).filter(User.username == "accountant").first()

    spec_noi = db_session.query(Specialty).filter(Specialty.code == "NOI").first()
    spec_tim = db_session.query(Specialty).filter(Specialty.code == "TIM").first()
    spec_nhi = db_session.query(Specialty).filter(Specialty.code == "NHI").first()
    spec_tmh = db_session.query(Specialty).filter(Specialty.code == "TMH").first()

    room_101 = db_session.query(Clinic).filter(Clinic.room_number == "P101").first()
    room_102 = db_session.query(Clinic).filter(Clinic.room_number == "P102").first()

    doc_profile_1 = db_session.query(Doctor).filter(Doctor.user_id == doctor_user_1.id).first() if doctor_user_1 else None
    doc_profile_2 = db_session.query(Doctor).filter(Doctor.user_id == doctor_user_2.id).first() if doctor_user_2 else None

    med_para = db_session.query(Medicine).filter(Medicine.code == "MED-PARA-500").first()
    med_amox = db_session.query(Medicine).filter(Medicine.code == "MED-AMOX-500").first()
    med_ibu = db_session.query(Medicine).filter(Medicine.code == "MED-IBU-400").first()
    med_omep = db_session.query(Medicine).filter(Medicine.code == "MED-OMEP-20").first()
    med_aug = db_session.query(Medicine).filter(Medicine.code == "MED-AUG-1G").first()

    pat1 = db_session.query(Patient).filter(Patient.medical_code == "BN-20260105-0001").first()
    pat2 = db_session.query(Patient).filter(Patient.medical_code == "BN-20260110-0002").first()
    pat3 = db_session.query(Patient).filter(Patient.medical_code == "BN-20260115-0003").first()

    return {
        "users": {
            "admin": admin_user,
            "receptionist": receptionist_user,
            "doctor_1": doctor_user_1,
            "doctor_2": doctor_user_2,
            "accountant": accountant_user,
        },
        "specialties": {
            "noi": spec_noi,
            "tim": spec_tim,
            "nhi": spec_nhi,
            "tmh": spec_tmh,
        },
        "rooms": {
            "room_101": room_101,
            "room_102": room_102,
        },
        "doctors": {
            "doc_1": doc_profile_1,
            "doc_2": doc_profile_2,
        },
        "medicines": {
            "paracetamol": med_para,
            "amoxicillin": med_amox,
            "ibuprofen": med_ibu,
            "omeprazole": med_omep,
            "augmentin": med_aug,
        },
        "patients": {
            "pat_1": pat1,
            "pat_2": pat2,
            "pat_3": pat3,
        }
    }


def get_token_headers_for_user(db_session: Session, username: str) -> Dict[str, str]:
    user = db_session.query(User).filter(User.username == username).first()
    if not user:
        raise ValueError(f"User {username} not found in test db")
    token = create_access_token({
        "sub": str(user.id),
        "username": user.username,
        "role": user.role
    })
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def admin_headers(db_session: Session) -> Dict[str, str]:
    return get_token_headers_for_user(db_session, "admin")


@pytest.fixture(scope="function")
def receptionist_headers(db_session: Session) -> Dict[str, str]:
    return get_token_headers_for_user(db_session, "receptionist")


@pytest.fixture(scope="function")
def doctor_headers(db_session: Session) -> Dict[str, str]:
    return get_token_headers_for_user(db_session, "dr_nam")


@pytest.fixture(scope="function")
def doctor_b_headers(db_session: Session) -> Dict[str, str]:
    return get_token_headers_for_user(db_session, "dr_huong")


@pytest.fixture(scope="function")
def accountant_headers(db_session: Session) -> Dict[str, str]:
    return get_token_headers_for_user(db_session, "accountant")
