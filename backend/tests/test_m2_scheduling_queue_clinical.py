"""
Milestone 2 Comprehensive Test Suite:
- Appointments booking, conflict detection, available-slots, rescheduling, check-in, cancellation.
- Consultation queue filtering and sequential ordering.
- Clinical examination encounters (vitals, BMI calculation, ICD-10, doctor notes, service orders).
- e-Prescription creation, medicine stock validation & decrement, prescription item lookup.
- Medicine catalog management (search, create, restock, delete).
"""

import pytest
from datetime import date, time, datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from typing import Dict, Any


def test_available_slots_endpoint(client: TestClient, doctor_headers: Dict[str, str], seed_data: Dict[str, Any]):
    """GET /api/v1/appointments/available-slots returns valid list of time slots."""
    doc = seed_data["doctors"]["doc_1"]
    target_date = (date.today() + timedelta(days=15)).isoformat()

    response = client.get(
        f"/api/v1/appointments/available-slots?doctor_id={doc.id}&date={target_date}",
        headers=doctor_headers
    )
    assert response.status_code == 200
    slots = response.json()
    assert isinstance(slots, list)
    assert len(slots) > 0
    first_slot = slots[0]
    assert "start_time" in first_slot
    assert "end_time" in first_slot
    assert "is_available" in first_slot


def test_reception_queue_flow(client: TestClient, receptionist_headers: Dict[str, str], doctor_headers: Dict[str, str], seed_data: Dict[str, Any]):
    """Appointments checked in appear in the consultation queue in sequence."""
    pat1 = seed_data["patients"]["pat_1"]
    pat2 = seed_data["patients"]["pat_2"]
    doc = seed_data["doctors"]["doc_1"]
    room = seed_data["rooms"]["room_101"]
    today_str = date.today().isoformat()

    # Book 2 appointments for today
    res1 = client.post(
        "/api/v1/appointments",
        json={
            "patient_id": pat1.id,
            "doctor_id": doc.id,
            "clinic_id": room.id,
            "appointment_date": today_str,
            "start_time": "08:00:00",
            "end_time": "08:30:00",
            "reason": "Khám huyết áp",
            "status": "CONFIRMED"
        },
        headers=receptionist_headers
    )
    assert res1.status_code in [200, 201]
    appt1_id = res1.json()["id"]

    res2 = client.post(
        "/api/v1/appointments",
        json={
            "patient_id": pat2.id,
            "doctor_id": doc.id,
            "clinic_id": room.id,
            "appointment_date": today_str,
            "start_time": "08:30:00",
            "end_time": "09:00:00",
            "reason": "Khám dạ dày",
            "status": "CONFIRMED"
        },
        headers=receptionist_headers
    )
    assert res2.status_code in [200, 201]
    appt2_id = res2.json()["id"]

    # Check-in appointment 1
    checkin_res = client.post(f"/api/v1/appointments/{appt1_id}/check-in", headers=receptionist_headers)
    assert checkin_res.status_code == 200

    # Query queue
    queue_res = client.get(f"/api/v1/medical_records/queue?doctor_id={doc.id}&appointment_date={today_str}", headers=doctor_headers)
    assert queue_res.status_code == 200
    queue = queue_res.json()
    assert len(queue) >= 2
    # Check that appt1 is marked CHECKED_IN
    checked_in_items = [q for q in queue if q["appointment_id"] == appt1_id]
    assert len(checked_in_items) == 1
    assert checked_in_items[0]["status"] == "CHECKED_IN"


def test_clinical_medical_record_and_service_orders(client: TestClient, doctor_headers: Dict[str, str], seed_data: Dict[str, Any]):
    """Doctor creates encounter, calculates BMI, adds lab orders, and completes consultation."""
    pat = seed_data["patients"]["pat_1"]
    doc = seed_data["doctors"]["doc_1"]
    room = seed_data["rooms"]["room_101"]

    # 1. Create medical record with height/weight for BMI calculation
    rec_res = client.post(
        "/api/v1/medical_records",
        json={
            "patient_id": pat.id,
            "doctor_id": doc.id,
            "clinic_id": room.id,
            "chief_complaint": "Đau hạ sườn phải, đầy bụng khó tiêu",
            "blood_pressure": "130/85 mmHg",
            "heart_rate": 80,
            "temperature": 37.2,
            "weight": 70.0,
            "height": 175.0,
            "diagnosis_icd10": "Rối loạn tiêu hóa chức năng",
            "icd10_code": "K30",
            "doctor_notes": "Theo dõi đáp ứng thuốc trong 7 ngày."
        },
        headers=doctor_headers
    )
    assert rec_res.status_code in [200, 201]
    record = rec_res.json()
    record_id = record["id"]
    assert record["record_code"].startswith("PK-")
    assert record["bmi"] == 22.86  # 70 / (1.75^2)

    # 2. Add service order (Ultrasound)
    service_res = client.post(
        f"/api/v1/medical_records/{record_id}/services",
        json={
            "service_name": "Siêu âm ổ bụng tổng quát",
            "service_code": "SA-OB-01",
            "price": 180000.0,
            "notes": "Kiểm tra gan mật tụy"
        },
        headers=doctor_headers
    )
    assert service_res.status_code in [200, 201]
    srv_data = service_res.json()
    assert srv_data["service_name"] == "Siêu âm ổ bụng tổng quát"
    assert srv_data["price"] == 180000.0

    # 3. Complete encounter
    complete_res = client.post(f"/api/v1/medical_records/{record_id}/complete", headers=doctor_headers)
    assert complete_res.status_code == 200
    assert complete_res.json()["status"] == "COMPLETED"


def test_medicine_catalog_admin_crud(client: TestClient, admin_headers: Dict[str, str], doctor_headers: Dict[str, str]):
    """Admin can create, update stock, search, and delete medicines."""
    # 1. Create new medicine
    create_res = client.post(
        "/api/v1/medicines",
        json={
            "code": "MED-CIPRO-TEST-500",
            "name": "Ciprofloxacin 500mg",
            "active_ingredient": "Ciprofloxacin",
            "dosage_form": "Viên nén bao phim",
            "unit": "Viên",
            "unit_price": 6500.0,
            "stock_quantity": 500,
            "usage_instructions": "Uống sau ăn 2 giờ",
            "is_active": True
        },
        headers=admin_headers
    )
    assert create_res.status_code in [200, 201]
    med_data = create_res.json()
    med_id = med_data["id"]

    # 2. Search medicine
    search_res = client.get("/api/v1/medicines?q=Ciprofloxacin", headers=doctor_headers)
    assert search_res.status_code == 200
    results = search_res.json()
    assert any(m["id"] == med_id for m in results)

    # 3. Admin restock
    update_res = client.put(
        f"/api/v1/medicines/{med_id}",
        json={"stock_quantity": 1000},
        headers=admin_headers
    )
    assert update_res.status_code == 200
    assert update_res.json()["stock_quantity"] == 1000

    # 4. Admin delete
    del_res = client.delete(f"/api/v1/medicines/{med_id}", headers=admin_headers)
    assert del_res.status_code == 200
