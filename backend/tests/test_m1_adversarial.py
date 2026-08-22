"""
Adversarial Stress Test Suite for Milestone 1:
- JWT Security: Tampered signatures, forged roles, expired tokens, invalid algorithms, deactivated accounts.
- RBAC Cross-Role Privilege Escalation: Comprehensive matrix testing unauthorized access for Doctor, Receptionist, Accountant.
- Patient Data & Search Boundaries: SQL injection vectors, XSS payloads, Unicode, fuzzing, pagination limits, CCCD duplicate detection.
- Doctor, Clinic, Specialty, Shift & Conflict Checker Boundaries: Non-existent foreign keys, unique constraint violations, time interval collision matrix.
"""

from datetime import date, time, datetime, timedelta, timezone
from typing import Dict, Any
import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.config import settings
from backend.app.core.security import create_access_token
from backend.app.core.conflict_checker import check_appointment_conflict
from backend.app.models.user import User, RoleEnum
from backend.app.models.clinic import Specialty, Clinic, Doctor, Shift
from backend.app.models.patient import Patient
from backend.app.models.appointment import Appointment, AppointmentStatus


# ============================================================================
# PART 1: JWT & AUTHENTICATION ADVERSARIAL CHALLENGES
# ============================================================================

def test_jwt_tampered_signature(client: TestClient, admin_headers: Dict[str, str]):
    """Altering signature bytes in a valid JWT must result in 401 Unauthorized."""
    token = admin_headers["Authorization"].split(" ")[1]
    header, payload, signature = token.split(".")
    # Tamper the signature by appending characters
    tampered_token = f"{header}.{payload}.{signature[:-4]}xxxx"
    
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {tampered_token}"})
    assert response.status_code == 401
    assert "detail" in response.json()


def test_jwt_tampered_payload(client: TestClient, admin_headers: Dict[str, str]):
    """Modifying base64 payload without updating signature must fail verification."""
    token = admin_headers["Authorization"].split(" ")[1]
    header, payload, signature = token.split(".")
    # Tamper payload
    tampered_payload = payload[:-4] + "AAAA"
    tampered_token = f"{header}.{tampered_payload}.{signature}"

    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {tampered_token}"})
    assert response.status_code == 401


def test_jwt_none_algorithm(client: TestClient):
    """Tokens crafted with alg='none' must be rejected."""
    payload = {
        "sub": "1",
        "username": "admin",
        "role": "ADMIN",
        "exp": (datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()
    }
    # Create an unsigned token
    token_none = jwt.encode(payload, key="", algorithm="none")
    
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token_none}"})
    assert response.status_code == 401


def test_jwt_wrong_secret_key(client: TestClient):
    """Tokens signed with an attacker's private/different secret key must be rejected."""
    payload = {
        "sub": "1",
        "username": "admin",
        "role": "ADMIN",
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    forged_token = jwt.encode(payload, "malicious-secret-key-123456", algorithm="HS256")
    
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {forged_token}"})
    assert response.status_code == 401


def test_jwt_expired_token(client: TestClient):
    """Tokens with past expiration timestamp must be rejected immediately."""
    payload = {
        "sub": "1",
        "username": "admin",
        "role": "ADMIN",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=10)
    }
    expired_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401
    assert "detail" in response.json()


def test_jwt_forged_role_in_payload(client: TestClient, db_session: Session):
    """
    CRITICAL RBAC CHECK:
    If an attacker takes a low-privilege account (Receptionist, ID=2), signs a token with
    'role': 'ADMIN' in the payload, the backend MUST query the database or enforce true
    role and REJECT access to Admin endpoints with 403 Forbidden.
    """
    rec_user = db_session.query(User).filter(User.role == RoleEnum.RECEPTIONIST.value).first()
    assert rec_user is not None
    
    # Craft token with Receptionist ID as sub, but claiming role=ADMIN
    forged_payload = {
        "sub": str(rec_user.id),
        "username": rec_user.username,
        "role": "ADMIN",  # Forged claim in token body
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(forged_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    headers = {"Authorization": f"Bearer {token}"}

    # Attempt admin-only endpoint: GET /api/v1/users
    response = client.get("/api/v1/users", headers=headers)
    assert response.status_code == 403, f"Privilege escalation succeeded! Status: {response.status_code}"


def test_jwt_nonexistent_user_id(client: TestClient):
    """Token with valid signature but non-existent sub (user ID) must return 401."""
    payload = {
        "sub": "99999999",
        "username": "ghost_user",
        "role": "ADMIN",
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_jwt_malformed_sub(client: TestClient):
    """Token with non-integer sub must return 401."""
    payload = {
        "sub": "not_an_int_id",
        "username": "admin",
        "role": "ADMIN",
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_jwt_missing_sub(client: TestClient):
    """Token payload missing 'sub' claim must return 401."""
    payload = {
        "username": "admin",
        "role": "ADMIN",
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_jwt_deactivated_user(client: TestClient, db_session: Session):
    """A user deactivated in DB after token issuance must be denied with 403."""
    user = db_session.query(User).filter(User.username == "receptionist").first()
    assert user is not None
    
    token = create_access_token({"sub": str(user.id), "username": user.username, "role": user.role})
    
    # Deactivate the user
    user.is_active = False
    db_session.commit()
    
    response = client.get("/api/v1/patients", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    assert "vô hiệu hóa" in response.json()["detail"] or "không hoạt động" in response.json()["detail"]


def test_malformed_auth_headers(client: TestClient):
    """Various malformed Authorization header formats must return 401."""
    # Missing Bearer prefix
    res1 = client.get("/api/v1/auth/me", headers={"Authorization": "Basic dXNlcjpwYXNz"})
    assert res1.status_code == 401

    # Empty token
    res2 = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer "})
    assert res2.status_code == 401

    # Random garbage characters
    res3 = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer ??????????$$$$$$$$$$"})
    assert res3.status_code == 401


def test_login_sql_injection_attempt(client: TestClient):
    """SQL injection payloads in login must be treated as literal strings and return 401."""
    payloads = [
        "' OR '1'='1",
        "admin' --",
        "' OR 1=1 --",
        "admin' /*",
        "' UNION SELECT 1, 'admin', 'pwd', 'ADMIN' --"
    ]
    for sqli in payloads:
        res = client.post("/api/v1/auth/login", json={"username": sqli, "password": "password"})
        assert res.status_code == 401


# ============================================================================
# PART 2: CROSS-ROLE RBAC PRIVILEGE ESCALATION MATRIX
# ============================================================================

def test_doctor_cross_role_escalations(client: TestClient, doctor_headers: Dict[str, str]):
    """Doctor role must NOT be able to access Admin or Accounting restricted actions."""
    # 1. User management
    assert client.get("/api/v1/users", headers=doctor_headers).status_code == 403
    assert client.post("/api/v1/users", json={"username": "hack_doc", "password": "123", "full_name": "Hack", "role": "ADMIN"}, headers=doctor_headers).status_code == 403
    assert client.get("/api/v1/users/1", headers=doctor_headers).status_code == 403
    assert client.put("/api/v1/users/1", json={"full_name": "Hack"}, headers=doctor_headers).status_code == 403
    assert client.delete("/api/v1/users/1", headers=doctor_headers).status_code == 403

    # 2. Clinic & Specialty administration
    assert client.post("/api/v1/specialties", json={"code": "HACK", "name": "Hack"}, headers=doctor_headers).status_code == 403
    assert client.put("/api/v1/specialties/1", json={"name": "Hack"}, headers=doctor_headers).status_code == 403
    assert client.delete("/api/v1/specialties/1", headers=doctor_headers).status_code == 403

    assert client.post("/api/v1/clinics", json={"room_number": "P999", "specialty_id": 1}, headers=doctor_headers).status_code == 403
    assert client.put("/api/v1/clinics/1", json={"room_number": "P999"}, headers=doctor_headers).status_code == 403
    assert client.delete("/api/v1/clinics/1", headers=doctor_headers).status_code == 403

    # 3. Doctor profiles and shifts
    assert client.post("/api/v1/doctors", json={"user_id": 1, "specialty_id": 1}, headers=doctor_headers).status_code == 403
    assert client.put("/api/v1/doctors/1", json={"room_id": 1}, headers=doctor_headers).status_code == 403
    assert client.post("/api/v1/shifts", json={"doctor_id": 1, "day_of_week": 1, "start_time": "08:00:00", "end_time": "12:00:00"}, headers=doctor_headers).status_code == 403
    assert client.delete("/api/v1/shifts/1", headers=doctor_headers).status_code == 403

    # 4. Deleting patient records (Admin only)
    assert client.delete("/api/v1/patients/1", headers=doctor_headers).status_code == 403


def test_receptionist_cross_role_escalations(client: TestClient, receptionist_headers: Dict[str, str]):
    """Receptionist role must NOT be able to modify admin catalogs or manage users."""
    # 1. User management
    assert client.get("/api/v1/users", headers=receptionist_headers).status_code == 403
    assert client.post("/api/v1/users", json={"username": "hack_rec", "password": "123", "full_name": "Hack", "role": "ADMIN"}, headers=receptionist_headers).status_code == 403
    assert client.delete("/api/v1/users/1", headers=receptionist_headers).status_code == 403

    # 2. Clinic administration
    assert client.post("/api/v1/clinics", json={"room_number": "P999", "specialty_id": 1}, headers=receptionist_headers).status_code == 403
    assert client.delete("/api/v1/clinics/1", headers=receptionist_headers).status_code == 403
    assert client.post("/api/v1/specialties", json={"code": "HACK", "name": "Hack"}, headers=receptionist_headers).status_code == 403
    assert client.delete("/api/v1/specialties/1", headers=receptionist_headers).status_code == 403

    # 3. Doctor/Shift setup
    assert client.post("/api/v1/doctors", json={"user_id": 1, "specialty_id": 1}, headers=receptionist_headers).status_code == 403
    assert client.post("/api/v1/shifts", json={"doctor_id": 1, "day_of_week": 1, "start_time": "08:00:00", "end_time": "12:00:00"}, headers=receptionist_headers).status_code == 403
    assert client.delete("/api/v1/shifts/1", headers=receptionist_headers).status_code == 403

    # 4. Deleting patient records
    assert client.delete("/api/v1/patients/1", headers=receptionist_headers).status_code == 403


def test_accountant_cross_role_escalations(client: TestClient, accountant_headers: Dict[str, str]):
    """Accountant role must NOT be able to view/edit clinical patients or manage admin catalogs."""
    # 1. Patients access blocked for accountant
    assert client.get("/api/v1/patients", headers=accountant_headers).status_code == 403
    assert client.get("/api/v1/patients/1", headers=accountant_headers).status_code == 403
    assert client.post("/api/v1/patients", json={"full_name": "Test", "phone": "0912345678"}, headers=accountant_headers).status_code == 403
    assert client.put("/api/v1/patients/1", json={"full_name": "Test"}, headers=accountant_headers).status_code == 403
    assert client.delete("/api/v1/patients/1", headers=accountant_headers).status_code == 403

    # 2. User & Clinic administration blocked
    assert client.get("/api/v1/users", headers=accountant_headers).status_code == 403
    assert client.post("/api/v1/users", json={"username": "hack_acc", "password": "123", "full_name": "Hack", "role": "ADMIN"}, headers=accountant_headers).status_code == 403
    assert client.post("/api/v1/specialties", json={"code": "HACK", "name": "Hack"}, headers=accountant_headers).status_code == 403
    assert client.post("/api/v1/clinics", json={"room_number": "P999", "specialty_id": 1}, headers=accountant_headers).status_code == 403
    assert client.post("/api/v1/doctors", json={"user_id": 1, "specialty_id": 1}, headers=accountant_headers).status_code == 403
    assert client.post("/api/v1/shifts", json={"doctor_id": 1, "day_of_week": 1, "start_time": "08:00:00", "end_time": "12:00:00"}, headers=accountant_headers).status_code == 403


def test_admin_cannot_self_delete(client: TestClient, admin_headers: Dict[str, str], db_session: Session):
    """Admin must be prevented from deleting their own active account."""
    admin_user = db_session.query(User).filter(User.username == "admin").first()
    assert admin_user is not None
    
    response = client.delete(f"/api/v1/users/{admin_user.id}", headers=admin_headers)
    assert response.status_code == 400
    assert "Không thể tự xóa" in response.json()["detail"]


# ============================================================================
# PART 3: PATIENT SEARCH & DATA BOUNDARY TESTS
# ============================================================================

@pytest.mark.parametrize("fuzz_query", [
    "",
    "   ",
    "' OR '1'='1",
    "'; DROP TABLE patients; --",
    "UNION SELECT 1,2,3,4,5,6,7,8,9,10,11,12,13 --",
    "<script>alert(1)</script>",
    ".*+?^${}()|[]\\",
    "🏥🩺💉🇻🇳",
    "A" * 2000,
    "__%_%___",
    "\\x00\\x01\\x02"
])
def test_patient_search_adversarial_queries(client: TestClient, receptionist_headers: Dict[str, str], fuzz_query: str):
    """Adversarial and boundary queries in patient search must return 200 and not crash."""
    response = client.get(f"/api/v1/patients", params={"q": fuzz_query}, headers=receptionist_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_patient_pagination_boundaries(client: TestClient, receptionist_headers: Dict[str, str]):
    """Validate pagination query parameter boundaries (skip, limit)."""
    # Negative skip -> 422
    assert client.get("/api/v1/patients?skip=-1", headers=receptionist_headers).status_code == 422
    
    # Zero limit -> 422
    assert client.get("/api/v1/patients?limit=0", headers=receptionist_headers).status_code == 422

    # Limit exceeding max 200 -> 422
    assert client.get("/api/v1/patients?limit=201", headers=receptionist_headers).status_code == 422

    # Max valid limit 200 -> 200
    res_max = client.get("/api/v1/patients?limit=200", headers=receptionist_headers)
    assert res_max.status_code == 200


def test_patient_duplicate_cccd_rejection(client: TestClient, receptionist_headers: Dict[str, str]):
    """Patient creation with already existing CCCD must be rejected with 400."""
    pat_data_1 = {
        "full_name": "Phan Văn A",
        "date_of_birth": "1990-01-01",
        "gender": "Nam",
        "phone": "0911000001",
        "identity_card": "038090001111"
    }
    r1 = client.post("/api/v1/patients", json=pat_data_1, headers=receptionist_headers)
    assert r1.status_code == 201

    pat_data_2 = {
        "full_name": "Phan Văn B",
        "date_of_birth": "1992-02-02",
        "gender": "Nam",
        "phone": "0911000002",
        "identity_card": "038090001111"  # Same CCCD
    }
    r2 = client.post("/api/v1/patients", json=pat_data_2, headers=receptionist_headers)
    assert r2.status_code == 400
    assert "đã tồn tại" in r2.json()["detail"]


def test_patient_duplicate_medical_code_rejection(client: TestClient, receptionist_headers: Dict[str, str]):
    """Explicitly providing an existing medical_code must be rejected with 400."""
    pat_data_1 = {
        "medical_code": "BN-CUSTOM-9999",
        "full_name": "Lê Văn C",
        "date_of_birth": "1988-08-08",
        "gender": "Nam",
        "phone": "0911000003"
    }
    r1 = client.post("/api/v1/patients", json=pat_data_1, headers=receptionist_headers)
    assert r1.status_code == 201

    pat_data_2 = {
        "medical_code": "BN-CUSTOM-9999",
        "full_name": "Lê Văn D",
        "date_of_birth": "1989-09-09",
        "gender": "Nam",
        "phone": "0911000004"
    }
    r2 = client.post("/api/v1/patients", json=pat_data_2, headers=receptionist_headers)
    assert r2.status_code == 400
    assert "đã tồn tại" in r2.json()["detail"]


def test_patient_not_found_endpoints(client: TestClient, receptionist_headers: Dict[str, str], admin_headers: Dict[str, str]):
    """Requesting non-existent patient ID must return 404."""
    assert client.get("/api/v1/patients/999999", headers=receptionist_headers).status_code == 404
    assert client.put("/api/v1/patients/999999", json={"full_name": "Updated"}, headers=receptionist_headers).status_code == 404
    assert client.delete("/api/v1/patients/999999", headers=admin_headers).status_code == 404


# ============================================================================
# PART 4: DOCTOR, CLINIC, SPECIALTY, SHIFT & CONFLICT CHECKER BOUNDARIES
# ============================================================================

def test_specialty_boundaries(client: TestClient, admin_headers: Dict[str, str]):
    """Duplicate specialty code/name and 404 checks."""
    # Duplicate code
    r_dup_code = client.post("/api/v1/specialties", json={"code": "NOI", "name": "Khoa Nội Mới"}, headers=admin_headers)
    assert r_dup_code.status_code == 400
    assert "đã tồn tại" in r_dup_code.json()["detail"]

    # Duplicate name
    r_dup_name = client.post("/api/v1/specialties", json={"code": "NOI_2", "name": "Nội tổng quát"}, headers=admin_headers)
    assert r_dup_name.status_code == 400
    assert "đã tồn tại" in r_dup_name.json()["detail"]

    # 404 updates/deletes
    assert client.put("/api/v1/specialties/99999", json={"name": "Test"}, headers=admin_headers).status_code == 404
    assert client.delete("/api/v1/specialties/99999", headers=admin_headers).status_code == 404


def test_clinic_room_boundaries(client: TestClient, admin_headers: Dict[str, str]):
    """Duplicate room number and non-existent specialty ID checks."""
    # Duplicate room_number
    r_dup_room = client.post(
        "/api/v1/clinics",
        json={"room_number": "P101", "name": "Phòng Khám Trùng", "specialty_id": 1},
        headers=admin_headers
    )
    assert r_dup_room.status_code == 400
    assert "đã tồn tại" in r_dup_room.json()["detail"]

    # Non-existent specialty
    r_invalid_spec = client.post(
        "/api/v1/clinics",
        json={"room_number": "P999", "name": "Phòng Khám Mới", "specialty_id": 99999},
        headers=admin_headers
    )
    assert r_invalid_spec.status_code == 404
    assert "chuyên khoa" in r_invalid_spec.json()["detail"]

    # 404 updates/deletes
    assert client.put("/api/v1/clinics/99999", json={"room_number": "P999"}, headers=admin_headers).status_code == 404
    assert client.delete("/api/v1/clinics/99999", headers=admin_headers).status_code == 404


def test_doctor_profile_boundaries(client: TestClient, admin_headers: Dict[str, str], db_session: Session):
    """Doctor creation for non-existent user or already registered doctor."""
    # Non-existent user
    r_no_user = client.post("/api/v1/doctors", json={"user_id": 99999, "specialty_id": 1}, headers=admin_headers)
    assert r_no_user.status_code == 404

    # User already having doctor profile (dr_nam)
    doc_user = db_session.query(User).filter(User.username == "dr_nam").first()
    assert doc_user is not None
    r_dup_doc = client.post("/api/v1/doctors", json={"user_id": doc_user.id, "specialty_id": 1}, headers=admin_headers)
    assert r_dup_doc.status_code == 400
    assert "đã được tạo hồ sơ bác sĩ" in r_dup_doc.json()["detail"]

    # 404 lookup & update
    assert client.get("/api/v1/doctors/99999", headers=admin_headers).status_code == 404
    assert client.put("/api/v1/doctors/99999", json={"room_id": 1}, headers=admin_headers).status_code == 404


def test_shift_boundaries(client: TestClient, admin_headers: Dict[str, str]):
    """Shift creation for non-existent doctor and 404 deletion."""
    r_no_doc = client.post(
        "/api/v1/shifts",
        json={"doctor_id": 99999, "day_of_week": 1, "start_time": "08:00:00", "end_time": "12:00:00"},
        headers=admin_headers
    )
    assert r_no_doc.status_code == 404

    assert client.delete("/api/v1/shifts/99999", headers=admin_headers).status_code == 404


def test_conflict_checker_interval_matrix(db_session: Session, seed_data: Dict[str, Any]):
    """
    Exhaustive empirical testing of conflict detection algorithm:
    1. Start time >= End time -> Error
    2. Touching boundary (08:00-09:00 vs 09:00-10:00) -> NO CONFLICT
    3. Exact collision (08:00-09:00 vs 08:00-09:00) -> CONFLICT
    4. Partial left collision (08:00-09:00 vs 07:30-08:30) -> CONFLICT
    5. Partial right collision (08:00-09:00 vs 08:30-09:30) -> CONFLICT
    6. Inside subset (08:00-10:00 vs 08:30-09:30) -> CONFLICT
    7. Enclosing superset (08:30-09:30 vs 08:00-10:00) -> CONFLICT
    8. Exclude appointment ID on reschedule -> NO CONFLICT
    9. Cancelled appointment ignored -> NO CONFLICT
    """
    doc = seed_data["doctors"]["doc_1"]
    room = seed_data["rooms"]["room_101"]
    pat = seed_data["patients"]["pat_1"]
    appt_date = date(2026, 9, 1)

    # 1. Start >= End
    ok, err = check_appointment_conflict(db_session, doc.id, room.id, appt_date, time(10, 0), time(9, 0))
    assert not ok
    assert "Giờ bắt đầu phải sớm hơn" in err

    ok, err = check_appointment_conflict(db_session, doc.id, room.id, appt_date, time(10, 0), time(10, 0))
    assert not ok
    assert "Giờ bắt đầu phải sớm hơn" in err

    # Create baseline appointment: 08:00 - 09:00
    base_appt = Appointment(
        appointment_code="LH-TEST-001",
        patient_id=pat.id,
        doctor_id=doc.id,
        clinic_id=room.id,
        appointment_date=appt_date,
        start_time=time(8, 0),
        end_time=time(9, 0),
        status=AppointmentStatus.CONFIRMED.value
    )
    db_session.add(base_appt)
    db_session.commit()

    # 2. Touching boundary: 09:00 - 10:00 -> NO CONFLICT
    ok, err = check_appointment_conflict(db_session, doc.id, room.id, appt_date, time(9, 0), time(10, 0))
    assert ok, f"Touching right boundary should not conflict: {err}"

    # Touching boundary: 07:00 - 08:00 -> NO CONFLICT
    ok, err = check_appointment_conflict(db_session, doc.id, room.id, appt_date, time(7, 0), time(8, 0))
    assert ok, f"Touching left boundary should not conflict: {err}"

    # 3. Exact collision: 08:00 - 09:00 -> CONFLICT
    ok, err = check_appointment_conflict(db_session, doc.id, room.id, appt_date, time(8, 0), time(9, 0))
    assert not ok
    assert "đã có lịch hẹn" in err

    # 4. Partial left collision: 07:30 - 08:30 -> CONFLICT
    ok, err = check_appointment_conflict(db_session, doc.id, room.id, appt_date, time(7, 30), time(8, 30))
    assert not ok
    assert "đã có lịch hẹn" in err

    # 5. Partial right collision: 08:30 - 09:30 -> CONFLICT
    ok, err = check_appointment_conflict(db_session, doc.id, room.id, appt_date, time(8, 30), time(9, 30))
    assert not ok
    assert "đã có lịch hẹn" in err

    # 6. Inside subset: 08:15 - 08:45 -> CONFLICT
    ok, err = check_appointment_conflict(db_session, doc.id, room.id, appt_date, time(8, 15), time(8, 45))
    assert not ok
    assert "đã có lịch hẹn" in err

    # 7. Enclosing superset: 07:30 - 09:30 -> CONFLICT
    ok, err = check_appointment_conflict(db_session, doc.id, room.id, appt_date, time(7, 30), time(9, 30))
    assert not ok
    assert "đã có lịch hẹn" in err

    # 8. Exclude appointment ID on reschedule -> NO CONFLICT
    ok, err = check_appointment_conflict(
        db_session, doc.id, room.id, appt_date, time(8, 0), time(9, 0),
        exclude_appointment_id=base_appt.id
    )
    assert ok, f"Self exclusion failed: {err}"

    # 9. Cancelled appointment ignored -> NO CONFLICT
    base_appt.status = AppointmentStatus.CANCELLED.value
    db_session.commit()

    ok, err = check_appointment_conflict(db_session, doc.id, room.id, appt_date, time(8, 0), time(9, 0))
    assert ok, f"Cancelled appointment caused unexpected conflict: {err}"
