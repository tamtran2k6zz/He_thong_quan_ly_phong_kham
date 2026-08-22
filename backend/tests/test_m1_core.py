from datetime import date, time
import pytest
from backend.app.core.conflict_checker import check_appointment_conflict
from backend.app.models.user import User
from backend.app.models.clinic import Doctor, Specialty, Clinic
from backend.app.models.patient import Patient
from backend.app.models.prescription import Medicine


def test_specialties_and_clinics(client, receptionist_headers, admin_headers):
    # Receptionist can read specialties
    r_spec = client.get("/api/v1/specialties", headers=receptionist_headers)
    assert r_spec.status_code == 200
    assert len(r_spec.json()) >= 6

    # Receptionist cannot create specialty
    r_create_spec_rec = client.post(
        "/api/v1/specialties",
        json={"code": "UNG", "name": "Ung bướu", "description": "Khoa Ung bướu"},
        headers=receptionist_headers
    )
    assert r_create_spec_rec.status_code == 403

    # Admin can create specialty
    r_create_spec_admin = client.post(
        "/api/v1/specialties",
        json={"code": "UNG", "name": "Ung bướu", "description": "Khoa Ung bướu"},
        headers=admin_headers
    )
    assert r_create_spec_admin.status_code == 201
    assert r_create_spec_admin.json()["code"] == "UNG"


def test_doctors_and_shifts(client, receptionist_headers):
    r_docs = client.get("/api/v1/doctors", headers=receptionist_headers)
    assert r_docs.status_code == 200
    docs = r_docs.json()
    assert len(docs) >= 4
    
    # Check doctor has shifts and specialty loaded
    first_doc = docs[0]
    assert "user" in first_doc
    assert "specialty" in first_doc
    assert "shifts" in first_doc
    assert len(first_doc["shifts"]) > 0


def test_patients_crud_and_search(client, receptionist_headers, accountant_headers):
    # Accountant cannot create/read patients
    r_acc = client.get("/api/v1/patients", headers=accountant_headers)
    assert r_acc.status_code == 403

    # Receptionist can list patients
    r_pat = client.get("/api/v1/patients", headers=receptionist_headers)
    assert r_pat.status_code == 200
    patients = r_pat.json()
    assert len(patients) >= 10

    # Search by Name
    r_search_name = client.get("/api/v1/patients?q=Hùng", headers=receptionist_headers)
    assert r_search_name.status_code == 200
    assert any("Hùng" in p["full_name"] for p in r_search_name.json())

    # Search by Phone
    r_search_phone = client.get("/api/v1/patients?q=0913884521", headers=receptionist_headers)
    assert r_search_phone.status_code == 200
    assert len(r_search_phone.json()) >= 1
    assert r_search_phone.json()[0]["phone"] == "0913884521"

    # Search by CCCD
    r_search_cccd = client.get("/api/v1/patients?q=001085012345", headers=receptionist_headers)
    assert r_search_cccd.status_code == 200
    assert len(r_search_cccd.json()) >= 1

    # Search by BHYT
    r_search_bhyt = client.get("/api/v1/patients?q=GD4010123456789", headers=receptionist_headers)
    assert r_search_bhyt.status_code == 200
    assert len(r_search_bhyt.json()) >= 1

    # Create Patient with auto medical_code
    new_patient = {
        "full_name": "Nguyễn Hoàng Nam",
        "date_of_birth": "1995-05-20",
        "gender": "Nam",
        "phone": "0988776655",
        "identity_card": "038095009988",
        "address": "100 Cầu Giấy, Hà Nội",
        "insurance_number": "DN4380123456789",
        "medical_history": "Không có",
        "drug_allergies": "Không có",
        "emergency_contact": "Nguyễn Văn Cường (Anh) - 0988776654"
    }
    r_create = client.post("/api/v1/patients", json=new_patient, headers=receptionist_headers)
    assert r_create.status_code == 201
    created_data = r_create.json()
    assert created_data["medical_code"].startswith("BN-")
    assert created_data["full_name"] == "Nguyễn Hoàng Nam"

    # Duplicate CCCD should fail
    r_dup_cccd = client.post("/api/v1/patients", json=new_patient, headers=receptionist_headers)
    assert r_dup_cccd.status_code == 400


def test_conflict_checker(db_session):
    doctor = db_session.query(Doctor).first()
    clinic = db_session.query(Clinic).first()
    assert doctor is not None
    assert clinic is not None

    test_date = date(2026, 9, 1)
    
    # 1. Invalid time: start >= end
    ok, err = check_appointment_conflict(
        db=db_session,
        doctor_id=doctor.id,
        clinic_id=clinic.id,
        appointment_date=test_date,
        start_time=time(10, 0),
        end_time=time(9, 0)
    )
    assert ok is False
    assert "Giờ bắt đầu phải sớm hơn" in err

    # 2. Valid slot with no existing appointment
    ok, err = check_appointment_conflict(
        db=db_session,
        doctor_id=doctor.id,
        clinic_id=clinic.id,
        appointment_date=test_date,
        start_time=time(9, 0),
        end_time=time(9, 30)
    )
    assert ok is True
    assert err is None


def test_seed_medicines_dataset(db_session):
    med_count = db_session.query(Medicine).count()
    assert med_count >= 25
    # Spot check essential medicines
    augmentin = db_session.query(Medicine).filter(Medicine.code == "MED-AUG-1G").first()
    assert augmentin is not None
    assert augmentin.stock_quantity > 0

    paracetamol = db_session.query(Medicine).filter(Medicine.code == "MED-PARA-500").first()
    assert paracetamol is not None
    assert paracetamol.unit_price == 1500.0
