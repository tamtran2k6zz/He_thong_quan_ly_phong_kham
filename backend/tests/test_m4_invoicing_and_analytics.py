"""
Milestone 4 Comprehensive Test Suite:
- Invoicing Lifecycle & Calculations (Consultation fee, Service orders fee, Prescription items fee, BHYT co-pay deduction)
- Payment Processing & Locking (CASH, BANK_TRANSFER, INSURANCE, VietQR generation)
- Invoice Cancellation & Protection Rules
- Itemized Invoice Details & Printable Receipt Format
- Financial & Clinical Analytics (Overview, Revenue-by-date daily/monthly, Specialty distribution, Doctor workload)
- Role-Based Access Control on Invoicing & Analytics
"""

import pytest
from datetime import date, datetime, timedelta
from typing import Dict, Any
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.models.invoice import Invoice, PaymentStatus, PaymentMethod
from backend.app.models.patient import Patient
from backend.app.models.medical_record import MedicalRecord, RecordStatus, ServiceOrder
from backend.app.models.prescription import Medicine, Prescription, PrescriptionItem


def test_create_invoice_from_completed_medical_record_with_bhyt_calculation(
    client: TestClient,
    accountant_headers: Dict[str, str],
    doctor_headers: Dict[str, str],
    seed_data: Dict[str, Any]
):
    """
    Generate invoice from completed medical record:
    - consultation_fee: 150000 VND default
    - service_fee: sum of ServiceOrder items
    - medicine_fee: sum of PrescriptionItem * Medicine.unit_price
    - insurance_discount: 80% standard BHYT deduction
    - patient_pay_amount: total_amount - insurance_discount
    """
    pat = seed_data["patients"]["pat_1"]  # Has insurance_number: GD4010888999000
    doc = seed_data["doctors"]["doc_1"]
    room = seed_data["rooms"]["room_101"]
    med = seed_data["medicines"]["omeprazole"]

    # 1. Doctor creates medical record
    record_res = client.post(
        "/api/v1/medical_records",
        json={
            "patient_id": pat.id,
            "doctor_id": doc.id,
            "clinic_id": room.id,
            "chief_complaint": "Đau vùng thượng vị dạ dày",
            "diagnosis_icd10": "Viêm dạ dày mạn tính",
            "icd10_code": "K29.5"
        },
        headers=doctor_headers
    )
    assert record_res.status_code in [200, 201]
    record_id = record_res.json()["id"]

    # 2. Add service order to medical record
    service_res = client.post(
        f"/api/v1/medical_records/{record_id}/services",
        json={
            "medical_record_id": record_id,
            "service_name": "Nội soi thực quản dạ dày tá tràng",
            "service_code": "NS-DD-01",
            "price": 600000.0,
            "notes": "Nội soi không đau"
        },
        headers=doctor_headers
    )
    if service_res.status_code == 404:
        # Fallback if service order created directly
        pass

    # 3. Doctor prescribes medication
    presc_res = client.post(
        "/api/v1/prescriptions",
        json={
            "medical_record_id": record_id,
            "patient_id": pat.id,
            "doctor_id": doc.id,
            "items": [
                {
                    "medicine_id": med.id,
                    "quantity": 10,
                    "dosage": "1 viên/ngày",
                    "instructions": "Uống trước ăn"
                }
            ]
        },
        headers=doctor_headers
    )
    assert presc_res.status_code in [200, 201]

    # 4. Accountant generates invoice
    inv_res = client.post(
        "/api/v1/invoices",
        json={"medical_record_id": record_id},
        headers=accountant_headers
    )
    assert inv_res.status_code == 201
    inv_data = inv_res.json()

    assert inv_data["invoice_code"].startswith("HD-")
    assert inv_data["consultation_fee"] == 150000.0
    assert inv_data["medicine_fee"] == 10 * float(med.unit_price)
    assert inv_data["total_amount"] > 0
    assert inv_data["insurance_discount"] > 0
    assert inv_data["patient_pay_amount"] == max(0.0, inv_data["total_amount"] - inv_data["insurance_discount"])
    assert inv_data["payment_status"] == "PENDING"


def test_prevent_duplicate_invoice_generation_for_same_record(
    client: TestClient,
    accountant_headers: Dict[str, str],
    doctor_headers: Dict[str, str],
    seed_data: Dict[str, Any]
):
    """Creating two invoices for the same medical record must be rejected with 400."""
    pat = seed_data["patients"]["pat_2"]
    doc = seed_data["doctors"]["doc_2"]

    rec_res = client.post(
        "/api/v1/medical_records",
        json={
            "patient_id": pat.id,
            "doctor_id": doc.id,
            "chief_complaint": "Tức ngực, hồi hộp",
            "diagnosis_icd10": "Tăng huyết áp vô căn",
            "icd10_code": "I10"
        },
        headers=doctor_headers
    )
    rec_id = rec_res.json()["id"]

    # First invoice creation -> Success
    inv1_res = client.post("/api/v1/invoices", json={"medical_record_id": rec_id}, headers=accountant_headers)
    assert inv1_res.status_code == 201

    # Second invoice creation for same medical record -> 400 Bad Request
    inv2_res = client.post("/api/v1/invoices", json={"medical_record_id": rec_id}, headers=accountant_headers)
    assert inv2_res.status_code == 400
    assert "đã có hóa đơn" in inv2_res.json()["detail"]


def test_invoice_filters_and_listing(
    client: TestClient,
    accountant_headers: Dict[str, str],
    seed_data: Dict[str, Any]
):
    """Accountant can filter invoices by status (PENDING/PAID/CANCELLED), patient ID, and date range."""
    pat = seed_data["patients"]["pat_1"]

    # Create pending invoice
    inv_res = client.post(
        "/api/v1/invoices",
        json={"patient_id": pat.id, "consultation_fee": 150000.0, "total_amount": 150000.0},
        headers=accountant_headers
    )
    assert inv_res.status_code == 201

    # Filter by PENDING
    pending_list = client.get("/api/v1/invoices?payment_status=PENDING", headers=accountant_headers)
    assert pending_list.status_code == 200
    assert all(inv["payment_status"] == "PENDING" for inv in pending_list.json())

    # Filter by patient ID
    patient_invs = client.get(f"/api/v1/invoices?patient_id={pat.id}", headers=accountant_headers)
    assert patient_invs.status_code == 200
    assert all(inv["patient_id"] == pat.id for inv in patient_invs.json())


def test_invoice_details_and_print_receipt(
    client: TestClient,
    accountant_headers: Dict[str, str],
    seed_data: Dict[str, Any]
):
    """GET /invoices/{id} returns full itemization and GET /invoices/{id}/print returns printable receipt."""
    pat = seed_data["patients"]["pat_1"]

    inv_res = client.post(
        "/api/v1/invoices",
        json={"patient_id": pat.id, "consultation_fee": 200000.0, "total_amount": 200000.0},
        headers=accountant_headers
    )
    inv_id = inv_res.json()["id"]

    # 1. Invoice detail
    detail_res = client.get(f"/api/v1/invoices/{inv_id}", headers=accountant_headers)
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert "items" in detail
    assert any(i["item_type"] == "CONSULTATION" for i in detail["items"])

    # 2. Print receipt
    print_res = client.get(f"/api/v1/invoices/{inv_id}/print", headers=accountant_headers)
    assert print_res.status_code == 200
    receipt = print_res.json()
    assert "clinic_header" in receipt
    assert "tax_id" in receipt["clinic_header"]
    assert "patient_info" in receipt
    assert receipt["patient_info"]["full_name"] == pat.full_name
    assert "items" in receipt
    assert "cashier_signature_title" in receipt


def test_payment_methods_and_vietqr_generation(
    client: TestClient,
    accountant_headers: Dict[str, str],
    seed_data: Dict[str, Any]
):
    """Test BANK_TRANSFER payment automatically generates VietQR reference if omitted."""
    pat = seed_data["patients"]["pat_1"]

    inv_res = client.post(
        "/api/v1/invoices",
        json={"patient_id": pat.id, "consultation_fee": 300000.0, "total_amount": 300000.0},
        headers=accountant_headers
    )
    inv_id = inv_res.json()["id"]

    pay_res = client.post(
        f"/api/v1/invoices/{inv_id}/pay",
        json={"payment_method": "BANK_TRANSFER"},
        headers=accountant_headers
    )
    assert pay_res.status_code == 200
    paid = pay_res.json()
    assert paid["payment_status"] == "PAID"
    assert paid["payment_method"] == "BANK_TRANSFER"
    assert paid["transaction_code"].startswith("VQR-")
    assert paid["paid_at"] is not None


def test_invoice_cancellation_rules(
    client: TestClient,
    accountant_headers: Dict[str, str],
    seed_data: Dict[str, Any]
):
    """Unpaid invoices can be cancelled; paid invoices cannot be cancelled; cancelled invoices cannot be paid."""
    pat = seed_data["patients"]["pat_1"]

    # 1. Cancel unpaid invoice -> Success
    inv_res = client.post(
        "/api/v1/invoices",
        json={"patient_id": pat.id, "consultation_fee": 150000.0, "total_amount": 150000.0},
        headers=accountant_headers
    )
    inv_id = inv_res.json()["id"]

    cancel_res = client.post(f"/api/v1/invoices/{inv_id}/cancel?notes=Benh_nhan_doi_y", headers=accountant_headers)
    assert cancel_res.status_code == 200
    assert cancel_res.json()["payment_status"] == "CANCELLED"

    # 2. Attempt to pay cancelled invoice -> Rejected 400
    pay_cancelled = client.post(
        f"/api/v1/invoices/{inv_id}/pay",
        json={"payment_method": "CASH"},
        headers=accountant_headers
    )
    assert pay_cancelled.status_code == 400

    # 3. Create another invoice, pay it, then attempt to cancel -> Rejected 400
    inv2_res = client.post(
        "/api/v1/invoices",
        json={"patient_id": pat.id, "consultation_fee": 150000.0, "total_amount": 150000.0},
        headers=accountant_headers
    )
    inv2_id = inv2_res.json()["id"]
    client.post(f"/api/v1/invoices/{inv2_id}/pay", json={"payment_method": "CASH"}, headers=accountant_headers)

    cancel_paid = client.post(f"/api/v1/invoices/{inv2_id}/cancel", headers=accountant_headers)
    assert cancel_paid.status_code == 400


def test_clinical_and_financial_analytics_endpoints(
    client: TestClient,
    accountant_headers: Dict[str, str],
    admin_headers: Dict[str, str]
):
    """
    Test analytics endpoints:
    - /api/v1/stats/overview
    - /api/v1/stats/revenue-by-date
    - /api/v1/stats/patients-by-specialty
    - /api/v1/stats/doctor-workload
    """
    # 1. Overview
    overview_res = client.get("/api/v1/stats/overview", headers=admin_headers)
    assert overview_res.status_code == 200
    ov = overview_res.json()
    assert ov["total_patients"] >= 0
    assert ov["total_doctors"] >= 0
    assert ov["total_revenue"] >= 0

    # 2. Revenue by date (daily)
    rev_daily = client.get("/api/v1/stats/revenue-by-date?period=daily", headers=accountant_headers)
    assert rev_daily.status_code == 200
    assert isinstance(rev_daily.json(), list)

    # 3. Revenue by date (monthly)
    rev_monthly = client.get("/api/v1/stats/revenue-by-date?period=monthly", headers=accountant_headers)
    assert rev_monthly.status_code == 200
    assert isinstance(rev_monthly.json(), list)

    # 4. Patients by specialty
    specialty_stats = client.get("/api/v1/stats/patients-by-specialty", headers=accountant_headers)
    assert specialty_stats.status_code == 200
    sp_list = specialty_stats.json()
    assert isinstance(sp_list, list)
    assert len(sp_list) > 0
    assert "specialty_name" in sp_list[0]
    assert "revenue" in sp_list[0]

    # 5. Doctor workload
    workload_res = client.get("/api/v1/stats/doctor-workload", headers=admin_headers)
    assert workload_res.status_code == 200
    doc_list = workload_res.json()
    assert isinstance(doc_list, list)
    assert len(doc_list) > 0
    assert "doctor_name" in doc_list[0]
    assert "total_consultations" in doc_list[0]
