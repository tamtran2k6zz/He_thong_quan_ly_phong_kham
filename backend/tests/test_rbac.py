"""
RBAC & Authentication Test Suite (Tiers 1 & 2).
Tests JWT token issuance, session verification, and strict 4-role isolation:
- Admin (Full control)
- Receptionist (Patient registration, appointment scheduling, FAQ chatbot)
- Doctor (Medical records, prescriptions, AI briefing, AI discharge)
- Accountant (Invoices, payments, receipts, revenue analytics)
"""

import pytest
from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
from typing import Dict, Any

from backend.app.core.security import create_access_token


# ---------------------------------------------------------------------------
# Tier 1: JWT Authentication & Credential Verification
# ---------------------------------------------------------------------------

def test_login_success_admin(client: TestClient, seed_data: Dict[str, Any]):
    """Valid admin login should return JWT access token and role=admin."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
    data = response.json()
    assert "access_token" in data
    assert data.get("token_type", "").lower() == "bearer"
    role = data.get("role") or data.get("user", {}).get("role")
    assert role.lower() == "admin"


def test_login_success_receptionist(client: TestClient, seed_data: Dict[str, Any]):
    """Valid receptionist login should return role=receptionist."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "receptionist", "password": "rec123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    role = data.get("role") or data.get("user", {}).get("role")
    assert role.lower() == "receptionist"


def test_login_success_doctor(client: TestClient, seed_data: Dict[str, Any]):
    """Valid doctor login should return role=doctor."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "dr_nam", "password": "doc123"}
    )
    assert response.status_code == 200
    data = response.json()
    role = data.get("role") or data.get("user", {}).get("role")
    assert role.lower() == "doctor"


def test_login_success_accountant(client: TestClient, seed_data: Dict[str, Any]):
    """Valid accountant login should return role=accountant."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "accountant", "password": "acc123"}
    )
    assert response.status_code == 200
    data = response.json()
    role = data.get("role") or data.get("user", {}).get("role")
    assert role.lower() == "accountant"


def test_login_invalid_password(client: TestClient, seed_data: Dict[str, Any]):
    """Login with wrong password must return 401 Unauthorized."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "WrongPassword!999"}
    )
    assert response.status_code == 401
    assert "detail" in response.json()


def test_login_nonexistent_user(client: TestClient, seed_data: Dict[str, Any]):
    """Login with non-existent username must return 401 Unauthorized."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "ghost_user_does_not_exist", "password": "Password@123"}
    )
    assert response.status_code == 401


def test_auth_me_with_valid_token(client: TestClient, receptionist_headers: Dict[str, str]):
    """GET /api/v1/auth/me with valid Bearer token returns current user profile."""
    response = client.get("/api/v1/auth/me", headers=receptionist_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "receptionist"
    assert data["role"].lower() == "receptionist"


def test_auth_me_missing_token(client: TestClient):
    """GET /api/v1/auth/me without token must return 401 Unauthorized."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code in [401, 403]


def test_auth_me_expired_token(client: TestClient):
    """Expired JWT token must be rejected with 401 Unauthorized."""
    past_exp = datetime.now(timezone.utc) - timedelta(minutes=10)
    token = create_access_token(data={"sub": "1", "username": "admin", "role": "admin"}, expires_delta=-timedelta(minutes=10))
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_auth_me_tampered_token(client: TestClient):
    """Tampered or invalid signature JWT must return 401 Unauthorized."""
    fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidXNlcm5hbWUiOiJhZG1pbl90ZXN0In0.invalidsignature12345"
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {fake_token}"})
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# Tier 2: Admin Privilege & Route Protection
# ---------------------------------------------------------------------------

def test_admin_can_access_user_management(client: TestClient, admin_headers: Dict[str, str]):
    """Admin can list and manage system users."""
    response = client.get("/api/v1/users", headers=admin_headers)
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) >= 4


def test_admin_can_create_new_user(client: TestClient, admin_headers: Dict[str, str]):
    """Admin can create new staff account."""
    new_user_payload = {
        "username": "nurse_hoa_test",
        "email": "nurse.hoa@clinic.vn",
        "password": "Password@123",
        "full_name": "Điều Dưỡng Nguyễn Thị Hoa",
        "role": "receptionist",
        "is_active": True
    }
    response = client.post("/api/v1/users", json=new_user_payload, headers=admin_headers)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["username"] == "nurse_hoa_test"
    assert data["role"].lower() == "receptionist"


def test_admin_can_view_audit_logs(client: TestClient, admin_headers: Dict[str, str]):
    """Admin can inspect system audit logs."""
    response = client.get("/api/v1/audit", headers=admin_headers)
    if response.status_code == 404:
        pytest.skip("Audit endpoint pending in milestone 3")
    assert response.status_code == 200


def test_admin_can_view_ai_logs(client: TestClient, admin_headers: Dict[str, str]):
    """Admin can inspect AI request and invocation logs."""
    response = client.get("/api/v1/audit/ai-logs", headers=admin_headers)
    if response.status_code == 404:
        pytest.skip("AI audit logs endpoint pending in milestone 3")
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# Tier 2: Receptionist Isolation & Permission Boundaries
# ---------------------------------------------------------------------------

def test_receptionist_cannot_access_user_management(client: TestClient, receptionist_headers: Dict[str, str]):
    """Receptionist attempting to list users must be blocked with 403 Forbidden."""
    response = client.get("/api/v1/users", headers=receptionist_headers)
    assert response.status_code == 403


def test_receptionist_cannot_create_user(client: TestClient, receptionist_headers: Dict[str, str]):
    """Receptionist attempting to create user must be blocked with 403 Forbidden."""
    response = client.post(
        "/api/v1/users",
        json={"username": "hack_user", "password": "Password@123", "role": "admin", "full_name": "Hacker"},
        headers=receptionist_headers
    )
    assert response.status_code == 403


def test_receptionist_cannot_view_audit_logs(client: TestClient, receptionist_headers: Dict[str, str]):
    """Receptionist attempting to view audit logs must be blocked with 403 Forbidden."""
    response = client.get("/api/v1/audit", headers=receptionist_headers)
    if response.status_code == 404:
        pytest.skip("Audit endpoint pending in milestone 3")
    assert response.status_code == 403


def test_receptionist_can_register_patient(client: TestClient, receptionist_headers: Dict[str, str]):
    """Receptionist can register a new patient profile."""
    patient_payload = {
        "full_name": "Phạm Văn Đông",
        "date_of_birth": "1990-01-01",
        "gender": "Nam",
        "phone": "0912111333",
        "identity_card": "001090123999",
        "insurance_number": "GD4010999888777",
        "address": "12 Bà Triệu, Hà Nội",
        "medical_history": "Không có",
        "drug_allergies": "Không dị ứng"
    }
    response = client.post("/api/v1/patients", json=patient_payload, headers=receptionist_headers)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["full_name"] == "Phạm Văn Đông"
    assert "medical_code" in data or "patient_code" in data


def test_receptionist_cannot_create_medical_record(client: TestClient, receptionist_headers: Dict[str, str], seed_data: Dict[str, Any]):
    """Receptionist cannot create medical examination / diagnosis record (403)."""
    pat = seed_data["patients"]["pat_1"]
    doc = seed_data["doctors"]["doc_1"]
    record_payload = {
        "patient_id": pat.id,
        "doctor_id": doc.id,
        "symptoms": "Đau đầu, chóng mặt",
        "diagnosis_icd10": "R51",
    }
    response = client.post("/api/v1/medical_records", json=record_payload, headers=receptionist_headers)
    if response.status_code == 404:
        pytest.skip("Medical records endpoint pending in milestone 2")
    assert response.status_code == 403


def test_receptionist_cannot_prescribe_medicine(client: TestClient, receptionist_headers: Dict[str, str], seed_data: Dict[str, Any]):
    """Receptionist cannot create prescriptions (403)."""
    pat = seed_data["patients"]["pat_1"]
    doc = seed_data["doctors"]["doc_1"]
    med = seed_data["medicines"]["paracetamol"]
    presc_payload = {
        "patient_id": pat.id,
        "doctor_id": doc.id,
        "items": [{"medicine_id": med.id, "quantity": 10, "dosage": "1v x 2", "instructions": "Sau ăn"}]
    }
    response = client.post("/api/v1/prescriptions", json=presc_payload, headers=receptionist_headers)
    if response.status_code == 404:
        pytest.skip("Prescriptions endpoint pending in milestone 2")
    assert response.status_code == 403


def test_receptionist_cannot_process_payment(client: TestClient, receptionist_headers: Dict[str, str]):
    """Receptionist cannot execute payment transactions (403)."""
    response = client.post(
        "/api/v1/invoices/1/pay",
        json={"payment_method": "CASH", "amount_paid": 150000},
        headers=receptionist_headers
    )
    if response.status_code == 404:
        pytest.skip("Invoices payment endpoint pending in milestone 4")
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# Tier 2: Doctor Isolation & Permission Boundaries
# ---------------------------------------------------------------------------

def test_doctor_cannot_access_user_management(client: TestClient, doctor_headers: Dict[str, str]):
    """Doctor attempting to view or manage users must get 403 Forbidden."""
    response = client.get("/api/v1/users", headers=doctor_headers)
    assert response.status_code == 403


def test_doctor_cannot_view_audit_logs(client: TestClient, doctor_headers: Dict[str, str]):
    """Doctor cannot view system audit logs (403)."""
    response = client.get("/api/v1/audit", headers=doctor_headers)
    if response.status_code == 404:
        pytest.skip("Audit endpoint pending in milestone 3")
    assert response.status_code == 403


def test_doctor_cannot_create_invoice(client: TestClient, doctor_headers: Dict[str, str], seed_data: Dict[str, Any]):
    """Doctor cannot create billing invoices (403)."""
    pat = seed_data["patients"]["pat_1"]
    invoice_payload = {
        "patient_id": pat.id,
        "consultation_fee": 150000,
        "medicine_fee": 50000,
        "total_amount": 200000
    }
    response = client.post("/api/v1/invoices", json=invoice_payload, headers=doctor_headers)
    if response.status_code == 404:
        pytest.skip("Invoices endpoint pending in milestone 4")
    assert response.status_code == 403


def test_doctor_cannot_process_payment(client: TestClient, doctor_headers: Dict[str, str]):
    """Doctor cannot process payments (403)."""
    response = client.post(
        "/api/v1/invoices/1/pay",
        json={"payment_method": "CASH", "amount_paid": 200000},
        headers=doctor_headers
    )
    if response.status_code == 404:
        pytest.skip("Invoices endpoint pending in milestone 4")
    assert response.status_code == 403


def test_doctor_can_create_medical_record(client: TestClient, doctor_headers: Dict[str, str], seed_data: Dict[str, Any]):
    """Doctor can record examination findings and ICD-10 diagnosis."""
    pat = seed_data["patients"]["pat_1"]
    doc = seed_data["doctors"]["doc_1"]
    record_payload = {
        "patient_id": pat.id,
        "doctor_id": doc.id,
        "clinic_id": doc.clinic_id,
        "chief_complaint": "Sốt cao 38.5 độ C, đau rát họng 2 ngày",
        "blood_pressure": "120/80 mmHg",
        "heart_rate": 82,
        "temperature": 38.5,
        "diagnosis_icd10": "Viêm họng cấp tính",
        "icd10_code": "J02.9",
        "doctor_notes": "Bệnh nhân có tiền sử dị ứng Penicillin - không kê nhóm Beta-lactam."
    }
    response = client.post("/api/v1/medical_records", json=record_payload, headers=doctor_headers)
    if response.status_code == 404:
        pytest.skip("Medical records endpoint pending in milestone 2")
    assert response.status_code in [200, 201]


def test_doctor_can_create_prescription(client: TestClient, doctor_headers: Dict[str, str], seed_data: Dict[str, Any]):
    """Doctor can prescribe medication from catalog."""
    pat = seed_data["patients"]["pat_1"]
    doc = seed_data["doctors"]["doc_1"]
    med_para = seed_data["medicines"]["paracetamol"]
    med_omep = seed_data["medicines"]["omeprazole"]

    presc_payload = {
        "patient_id": pat.id,
        "doctor_id": doc.id,
        "notes": "Uống đúng liều sau khi ăn no",
        "items": [
            {
                "medicine_id": med_para.id,
                "dosage": "1 viên/lần",
                "frequency": "2-3 lần/ngày khi sốt > 38.5",
                "duration_days": 3,
                "quantity": 10,
                "instructions": "Uống với nhiều nước"
            },
            {
                "medicine_id": med_omep.id,
                "dosage": "1 viên/lần",
                "frequency": "1 lần/ngày vào buổi sáng",
                "duration_days": 7,
                "quantity": 7,
                "instructions": "Uống trước bữa ăn sáng 30 phút"
            }
        ]
    }
    response = client.post("/api/v1/prescriptions", json=presc_payload, headers=doctor_headers)
    if response.status_code == 404:
        pytest.skip("Prescriptions endpoint pending in milestone 2")
    assert response.status_code in [200, 201]


# ---------------------------------------------------------------------------
# Tier 2: Accountant Isolation & Billing Boundaries
# ---------------------------------------------------------------------------

def test_accountant_cannot_access_user_management(client: TestClient, accountant_headers: Dict[str, str]):
    """Accountant cannot manage system users (403)."""
    response = client.get("/api/v1/users", headers=accountant_headers)
    assert response.status_code == 403


def test_accountant_cannot_create_medical_record(client: TestClient, accountant_headers: Dict[str, str], seed_data: Dict[str, Any]):
    """Accountant cannot create clinical records (403)."""
    pat = seed_data["patients"]["pat_1"]
    doc = seed_data["doctors"]["doc_1"]
    record_payload = {
        "patient_id": pat.id,
        "doctor_id": doc.id,
        "symptoms": "Đau bụng",
        "diagnosis_icd10": "K29",
    }
    response = client.post("/api/v1/medical_records", json=record_payload, headers=accountant_headers)
    if response.status_code == 404:
        pytest.skip("Medical records endpoint pending in milestone 2")
    assert response.status_code == 403


def test_accountant_cannot_prescribe_medicine(client: TestClient, accountant_headers: Dict[str, str], seed_data: Dict[str, Any]):
    """Accountant cannot prescribe medicines (403)."""
    pat = seed_data["patients"]["pat_1"]
    doc = seed_data["doctors"]["doc_1"]
    med = seed_data["medicines"]["paracetamol"]
    response = client.post(
        "/api/v1/prescriptions",
        json={"patient_id": pat.id, "doctor_id": doc.id, "items": [{"medicine_id": med.id, "quantity": 5}]},
        headers=accountant_headers
    )
    if response.status_code == 404:
        pytest.skip("Prescriptions endpoint pending in milestone 2")
    assert response.status_code == 403


def test_accountant_can_access_invoices_and_revenue(client: TestClient, accountant_headers: Dict[str, str]):
    """Accountant can view invoices and billing reports."""
    response = client.get("/api/v1/invoices", headers=accountant_headers)
    if response.status_code == 404:
        pytest.skip("Invoices endpoint pending in milestone 4")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
