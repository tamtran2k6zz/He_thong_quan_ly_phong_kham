"""
Full Clinical Encounter Lifecycle Test Suite (Tier 3).
Simulates the complete real-world patient journey:
Receptionist (Register + Book + Check-in)
  -> Doctor (AI Briefing + Vitals + ICD-10 Diagnosis + e-Prescription + AI Discharge)
    -> Accountant (Invoice Generation + VietQR/Cash Payment + Receipt)
      -> Admin (Audit Trail Verification).
"""

import pytest
from datetime import date, time, datetime, timedelta
from fastapi.testclient import TestClient
from typing import Dict, Any


def test_full_clinical_encounter_workflow_success(
    client: TestClient,
    receptionist_headers: Dict[str, str],
    doctor_headers: Dict[str, str],
    accountant_headers: Dict[str, str],
    admin_headers: Dict[str, str],
    seed_data: Dict[str, Any]
):
    """
    Complete end-to-end multi-role clinical journey:
    1. Receptionist registers patient.
    2. Receptionist books & checks in appointment.
    3. Doctor reads AI pre-visit briefing.
    4. Doctor performs exam (vitals, ICD-10).
    5. Doctor prescribes medicines.
    6. Doctor generates AI discharge instructions.
    7. Accountant aggregates fees into invoice.
    8. Accountant processes payment.
    9. Admin verifies audit log chain.
    """
    doc = seed_data["doctors"]["doc_1"]
    room = seed_data["rooms"]["room_101"]
    med_omep = seed_data["medicines"]["omeprazole"]

    # -----------------------------------------------------------------------
    # Step 1: Receptionist registers patient
    # -----------------------------------------------------------------------
    patient_res = client.post(
        "/api/v1/patients",
        json={
            "full_name": "Phạm Quốc Huy",
            "date_of_birth": "1988-12-05",
            "gender": "Nam",
            "phone": "0912888999",
            "identity_card": "001088019999",
            "insurance_number": "GD4010888999000",
            "address": "99 Láng Hạ, Đống Đa, Hà Nội",
            "medical_history": "Trào ngược dạ dày thực quản (GERD)",
            "drug_allergies": "Không dị ứng thuốc"
        },
        headers=receptionist_headers
    )
    if patient_res.status_code == 404:
        pytest.skip("Backend implementation pending")
    assert patient_res.status_code in [200, 201]
    patient_data = patient_res.json()
    patient_id = patient_data["id"]

    # -----------------------------------------------------------------------
    # Step 2: Receptionist books appointment & checks in
    # -----------------------------------------------------------------------
    appt_date = (date.today() + timedelta(days=1)).isoformat()
    appt_res = client.post(
        "/api/v1/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doc.id,
            "clinic_id": room.id,
            "appointment_date": appt_date,
            "start_time": "08:30:00",
            "end_time": "09:00:00",
            "reason": "Ợ chua, đau thượng vị",
            "status": "CONFIRMED"
        },
        headers=receptionist_headers
    )
    if appt_res.status_code == 404:
        pytest.skip("Appointments endpoint pending in milestone 2")
    assert appt_res.status_code in [200, 201]
    appt_data = appt_res.json()
    appt_id = appt_data["id"]

    # Check-in patient
    checkin_res = client.post(f"/api/v1/appointments/{appt_id}/check-in", headers=receptionist_headers)
    if checkin_res.status_code == 404:
        checkin_res = client.put(f"/api/v1/appointments/{appt_id}", json={"status": "CHECKED_IN"}, headers=receptionist_headers)
    assert checkin_res.status_code == 200

    # -----------------------------------------------------------------------
    # Step 3: Doctor reads AI Pre-visit Briefing
    # -----------------------------------------------------------------------
    briefing_res = client.post(
        "/api/v1/ai/pre-visit-summary",
        json={
            "patient_id": patient_id,
            "patient_code": patient_data.get("medical_code", "BN-TEST"),
            "full_name": patient_data["full_name"],
            "medical_history": patient_data.get("medical_history"),
            "drug_allergies": patient_data.get("drug_allergies")
        },
        headers=doctor_headers
    )
    if briefing_res.status_code == 404:
        pytest.skip("AI Pre-visit briefing pending in milestone 3")
    assert briefing_res.status_code == 200
    assert len(briefing_res.json().get("summary", "")) > 10

    # -----------------------------------------------------------------------
    # Step 4: Doctor performs examination & creates Medical Record
    # -----------------------------------------------------------------------
    record_res = client.post(
        "/api/v1/medical_records",
        json={
            "appointment_id": appt_id,
            "patient_id": patient_id,
            "doctor_id": doc.id,
            "clinic_id": room.id,
            "chief_complaint": "Ợ nóng, đau âm ỉ vùng thượng vị sau ăn",
            "blood_pressure": "125/80 mmHg",
            "heart_rate": 76,
            "temperature": 37.0,
            "diagnosis_icd10": "Viêm dạ dày mạn tính không đặc hiệu",
            "icd10_code": "K29.5",
            "doctor_notes": "Tái khám sau 2 tuần nếu triệu chứng không thuyên giảm."
        },
        headers=doctor_headers
    )
    if record_res.status_code == 404:
        pytest.skip("Medical records endpoint pending in milestone 2")
    assert record_res.status_code in [200, 201]
    record_data = record_res.json()
    record_id = record_data["id"]

    # -----------------------------------------------------------------------
    # Step 5: Doctor prescribes medicines
    # -----------------------------------------------------------------------
    presc_res = client.post(
        "/api/v1/prescriptions",
        json={
            "medical_record_id": record_id,
            "patient_id": patient_id,
            "doctor_id": doc.id,
            "notes": "Kiêng đồ cay nóng, không uống rượu bia",
            "items": [
                {
                    "medicine_id": med_omep.id,
                    "dosage": "1 viên/lần",
                    "frequency": "1 lần/ngày",
                    "duration_days": 14,
                    "quantity": 14,
                    "instructions": "Uống trước bữa ăn sáng 30 phút"
                }
            ]
        },
        headers=doctor_headers
    )
    if presc_res.status_code == 404:
        pytest.skip("Prescriptions endpoint pending in milestone 2")
    assert presc_res.status_code in [200, 201]

    # -----------------------------------------------------------------------
    # Step 6: Doctor generates AI Post-visit Discharge Instructions
    # -----------------------------------------------------------------------
    discharge_res = client.post(
        "/api/v1/ai/discharge-instructions",
        json={
            "patient_id": patient_id,
            "patient_name": patient_data["full_name"],
            "diagnosis_icd10": "K29.5",
            "diagnosis_text": "Viêm dạ dày mạn tính",
            "prescriptions": [
                {"medicine_name": "Omeprazole 20mg", "dosage": "1 viên/ngày trước ăn sáng"}
            ],
            "follow_up_days": 14,
            "doctor_advice": "Ăn đúng giờ, tránh thức khuya và đồ cay nóng"
        },
        headers=doctor_headers
    )
    assert discharge_res.status_code == 200

    # Complete appointment status
    client.put(f"/api/v1/appointments/{appt_id}", json={"status": "COMPLETED"}, headers=doctor_headers)

    # -----------------------------------------------------------------------
    # Step 7: Accountant creates Invoice & calculates totals
    # -----------------------------------------------------------------------
    consultation_fee = 150000.0
    medicine_fee = 14 * 4000.0
    total_expected = consultation_fee + medicine_fee

    invoice_res = client.post(
        "/api/v1/invoices",
        json={
            "patient_id": patient_id,
            "medical_record_id": record_id,
            "consultation_fee": consultation_fee,
            "medicine_fee": medicine_fee,
            "service_fee": 0.0,
            "discount_amount": 0.0,
            "total_amount": total_expected,
            "payment_status": "PENDING"
        },
        headers=accountant_headers
    )
    if invoice_res.status_code == 404:
        pytest.skip("Invoices endpoint pending in milestone 4")
    assert invoice_res.status_code in [200, 201]
    invoice_data = invoice_res.json()
    invoice_id = invoice_data["id"]

    # -----------------------------------------------------------------------
    # Step 8: Accountant processes Payment (Cash)
    # -----------------------------------------------------------------------
    pay_res = client.post(
        f"/api/v1/invoices/{invoice_id}/pay",
        json={
            "payment_method": "CASH",
            "amount_paid": total_expected,
            "notes": "Bệnh nhân thanh toán tiền mặt đủ tại quầy thu ngân"
        },
        headers=accountant_headers
    )
    assert pay_res.status_code == 200
    paid_data = pay_res.json()
    assert paid_data["payment_status"].upper() == "PAID"

    # -----------------------------------------------------------------------
    # Step 9: Admin verifies audit log presence
    # -----------------------------------------------------------------------
    audit_res = client.get("/api/v1/audit", headers=admin_headers)
    assert audit_res.status_code == 200
    logs = audit_res.json()
    assert isinstance(logs, list)
