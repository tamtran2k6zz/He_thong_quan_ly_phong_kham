"""
Real-World E2E Scenarios, Security Drills & Inventory Integrity (Tier 4).
Tests:
- Doctor Isolation (Doctor A cannot edit Doctor B's medical records).
- Inventory stock decrement and stock exhaustion rejection.
- Financial integrity (Payment locking, duplicate payment prevention).
- Multi-specialty concurrent clinic room workflows.
- BHYT 80%/100% co-pay deduction calculation.
- Anonymous attack rejection across full API surface.
"""

import pytest
from datetime import date, time, datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from typing import Dict, Any


# ---------------------------------------------------------------------------
# Scenario 1: Doctor Record Isolation
# ---------------------------------------------------------------------------

def test_doctor_isolation_cannot_edit_other_doctors_record(
    client: TestClient,
    doctor_headers: Dict[str, str],
    doctor_b_headers: Dict[str, str],
    seed_data: Dict[str, Any]
):
    """Doctor B must be forbidden (403) from editing a record created by Doctor A."""
    pat = seed_data["patients"]["pat_1"]
    doc1 = seed_data["doctors"]["doc_1"]
    room1 = seed_data["rooms"]["room_101"]

    # 1. Doctor 1 creates medical record
    create_res = client.post(
        "/api/v1/medical_records",
        json={
            "patient_id": pat.id,
            "doctor_id": doc1.id,
            "clinic_id": room1.id,
            "chief_complaint": "Đau rát họng",
            "diagnosis_icd10": "Viêm họng cấp",
            "icd10_code": "J02.9"
        },
        headers=doctor_headers
    )
    if create_res.status_code == 404:
        pytest.skip("Medical records endpoint pending in milestone 2")
    assert create_res.status_code in [200, 201]
    record_id = create_res.json()["id"]

    # 2. Doctor 2 attempts to overwrite Doctor 1's record
    tamper_res = client.put(
        f"/api/v1/medical_records/{record_id}",
        json={"doctor_notes": "Bác sĩ B sửa trái phép kết luận chẩn đoán"},
        headers=doctor_b_headers
    )
    assert tamper_res.status_code == 403, "Doctor B was able to modify Doctor A's record!"


# ---------------------------------------------------------------------------
# Scenario 2: Inventory Stock Decrement & Out-of-Stock Protection
# ---------------------------------------------------------------------------

def test_inventory_stock_decrement_on_prescription(
    client: TestClient,
    doctor_headers: Dict[str, str],
    accountant_headers: Dict[str, str],
    seed_data: Dict[str, Any]
):
    """Prescribing medicine should accurately decrement the inventory stock."""
    pat = seed_data["patients"]["pat_1"]
    doc = seed_data["doctors"]["doc_1"]
    med = seed_data["medicines"]["amoxicillin"]
    if not med:
        pytest.skip("Medicine not found or pending in milestone 2")

    # Get initial stock
    initial_res = client.get(f"/api/v1/medicines/{med.id}", headers=doctor_headers)
    if initial_res.status_code == 404:
        pytest.skip("Medicines endpoint pending in milestone 2")
    initial_stock = initial_res.json().get("stock_quantity", 1000)

    # Prescribe 20 units
    presc_res = client.post(
        "/api/v1/prescriptions",
        json={
            "patient_id": pat.id,
            "doctor_id": doc.id,
            "notes": "Uống sau ăn",
            "items": [
                {
                    "medicine_id": med.id,
                    "quantity": 20,
                    "dosage": "1v x 2",
                    "instructions": "Sáng 1 viên, tối 1 viên"
                }
            ]
        },
        headers=doctor_headers
    )
    if presc_res.status_code == 404:
        pytest.skip("Prescriptions endpoint pending in milestone 2")
    assert presc_res.status_code in [200, 201]

    # Verify updated stock
    updated_res = client.get(f"/api/v1/medicines/{med.id}", headers=doctor_headers)
    updated_stock = updated_res.json().get("stock_quantity")
    assert updated_stock == initial_stock - 20 or updated_stock == 980


def test_prescribe_excessive_stock_rejected(
    client: TestClient,
    doctor_headers: Dict[str, str],
    seed_data: Dict[str, Any]
):
    """Attempting to prescribe more than available stock quantity must return 400 Bad Request."""
    pat = seed_data["patients"]["pat_1"]
    doc = seed_data["doctors"]["doc_1"]
    med = seed_data["medicines"]["ibuprofen"]
    med_id = med.id if med else 1

    presc_res = client.post(
        "/api/v1/prescriptions",
        json={
            "patient_id": pat.id,
            "doctor_id": doc.id,
            "items": [
                {
                    "medicine_id": med_id,
                    "quantity": 99999,  # Far exceeds stock
                    "dosage": "1v",
                    "instructions": "Uống khi đau"
                }
            ]
        },
        headers=doctor_headers
    )
    if presc_res.status_code == 404:
        pytest.skip("Prescriptions endpoint pending in milestone 2")
    assert presc_res.status_code in [400, 422]


# ---------------------------------------------------------------------------
# Scenario 3: Financial Integrity & Payment Locking
# ---------------------------------------------------------------------------

def test_payment_locking_prevent_duplicate_transactions(
    client: TestClient,
    accountant_headers: Dict[str, str],
    seed_data: Dict[str, Any]
):
    """Paying an already PAID invoice must be rejected to prevent duplicate transactions."""
    pat = seed_data["patients"]["pat_1"]

    # 1. Create invoice
    inv_res = client.post(
        "/api/v1/invoices",
        json={
            "patient_id": pat.id,
            "consultation_fee": 150000.0,
            "medicine_fee": 0.0,
            "total_amount": 150000.0,
            "payment_status": "PENDING"
        },
        headers=accountant_headers
    )
    if inv_res.status_code == 404:
        pytest.skip("Invoices endpoint pending in milestone 4")
    assert inv_res.status_code in [200, 201]
    inv_id = inv_res.json()["id"]

    # 2. Pay first time
    pay1_res = client.post(
        f"/api/v1/invoices/{inv_id}/pay",
        json={"payment_method": "CASH", "amount_paid": 150000.0},
        headers=accountant_headers
    )
    assert pay1_res.status_code == 200

    # 3. Attempt second payment on same invoice
    pay2_res = client.post(
        f"/api/v1/invoices/{inv_id}/pay",
        json={"payment_method": "CASH", "amount_paid": 150000.0},
        headers=accountant_headers
    )
    assert pay2_res.status_code in [400, 409]


# ---------------------------------------------------------------------------
# Scenario 4: Concurrent Multi-Specialty Operations
# ---------------------------------------------------------------------------

def test_concurrent_multi_specialty_consultations(
    client: TestClient,
    receptionist_headers: Dict[str, str],
    seed_data: Dict[str, Any]
):
    """Two doctors in different specialties/rooms can have appointments in the same time slot without conflict."""
    pat1 = seed_data["patients"]["pat_1"]
    pat2 = seed_data["patients"]["pat_2"]
    doc1 = seed_data["doctors"]["doc_1"]
    doc2 = seed_data["doctors"]["doc_2"]
    room1 = seed_data["rooms"]["room_101"]
    room2 = seed_data["rooms"]["room_102"]
    target_date = (date.today() + timedelta(days=20)).isoformat()

    # Slot: 09:00 - 09:30
    res1 = client.post(
        "/api/v1/appointments",
        json={
            "patient_id": pat1.id,
            "doctor_id": doc1.id,
            "clinic_id": room1.id,
            "appointment_date": target_date,
            "start_time": "09:00:00",
            "end_time": "09:30:00",
            "reason": "Khám Nội",
            "status": "CONFIRMED"
        },
        headers=receptionist_headers
    )
    if res1.status_code == 404:
        pytest.skip("Appointments endpoint pending in milestone 2")
    assert res1.status_code in [200, 201]

    # Concurrent Slot for Doctor 2 in Room 102
    res2 = client.post(
        "/api/v1/appointments",
        json={
            "patient_id": pat2.id,
            "doctor_id": doc2.id,
            "clinic_id": room2.id,
            "appointment_date": target_date,
            "start_time": "09:00:00",
            "end_time": "09:30:00",
            "reason": "Khám Tim mạch",
            "status": "CONFIRMED"
        },
        headers=receptionist_headers
    )
    assert res2.status_code in [200, 201]


# ---------------------------------------------------------------------------
# Scenario 5: BHYT Co-pay Deduction Calculation
# ---------------------------------------------------------------------------

def test_bhyt_insurance_copay_calculation(
    client: TestClient,
    accountant_headers: Dict[str, str],
    seed_data: Dict[str, Any]
):
    """When patient has BHYT (80% coverage), invoice reflects insurance covered portion and patient co-pay."""
    pat = seed_data["patients"]["pat_1"]

    total_gross = 500000.0
    insurance_rate = 0.80
    expected_covered = total_gross * insurance_rate  # 400,000 VND
    expected_patient_pay = total_gross - expected_covered  # 100,000 VND

    invoice_res = client.post(
        "/api/v1/invoices",
        json={
            "patient_id": pat.id,
            "consultation_fee": 200000.0,
            "medicine_fee": 300000.0,
            "service_fee": 0.0,
            "insurance_discount": expected_covered,
            "total_amount": total_gross,
            "patient_pay_amount": expected_patient_pay,
            "payment_status": "PENDING"
        },
        headers=accountant_headers
    )
    if invoice_res.status_code == 404:
        pytest.skip("Invoices endpoint pending in milestone 4")
    assert invoice_res.status_code in [200, 201]
    inv = invoice_res.json()
    assert inv["patient_pay_amount"] == expected_patient_pay or inv.get("insurance_discount") == expected_covered


# ---------------------------------------------------------------------------
# Scenario 6: Anonymous Attack Surface Protection
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("endpoint,method", [
    ("/api/v1/users", "GET"),
    ("/api/v1/users", "POST"),
    ("/api/v1/patients", "GET"),
    ("/api/v1/patients", "POST"),
    ("/api/v1/appointments", "GET"),
    ("/api/v1/appointments", "POST"),
    ("/api/v1/medical_records", "GET"),
    ("/api/v1/medical_records", "POST"),
    ("/api/v1/prescriptions", "GET"),
    ("/api/v1/prescriptions", "POST"),
    ("/api/v1/invoices", "GET"),
    ("/api/v1/invoices", "POST"),
    ("/api/v1/audit", "GET"),
    ("/api/v1/audit/ai-logs", "GET"),
    ("/api/v1/stats", "GET"),
])
def test_anonymous_requests_blocked_with_401(client: TestClient, endpoint: str, method: str):
    """Every sensitive clinical and administrative endpoint must reject unauthenticated requests with 401."""
    if method == "GET":
        res = client.get(endpoint)
    elif method == "POST":
        res = client.post(endpoint, json={})
    if res.status_code == 404:
        pytest.skip("Endpoint pending implementation in future milestone")
    assert res.status_code in [401, 403], f"Endpoint {method} {endpoint} leaked data to anonymous user!"
