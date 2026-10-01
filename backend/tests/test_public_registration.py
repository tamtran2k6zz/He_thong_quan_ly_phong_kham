from datetime import date, timedelta

from backend.app.models.patient import Patient
from backend.app.models.user import User


def next_weekday():
    candidate = date.today() + timedelta(days=1)
    while candidate.weekday() != 0:
        candidate += timedelta(days=1)
    return candidate.isoformat()


def test_staff_registration_requires_admin_activation(client, db_session, admin_headers):
    payload = {
        "username": "new_staff",
        "full_name": "Nguyễn Văn Mới",
        "email": "new.staff@example.com",
        "password": "StrongPass123",
        "role": "doctor",
        "is_active": True,
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    assert response.json()["role"] == "doctor"
    assert response.json()["is_active"] is False
    assert "hashed_password" not in response.json()
    assert db_session.query(User).filter_by(username="new_staff").one().is_active is False

    login = client.post(
        "/api/v1/auth/login",
        json={"username": "new_staff", "password": "StrongPass123"},
    )
    assert login.status_code == 403
    assert client.post("/api/v1/auth/register", json=payload).status_code == 409

    admin_attempt = client.post("/api/v1/auth/register", json={
        **payload, "username": "fake_admin", "email": "fake.admin@example.com", "role": "admin",
    })
    assert admin_attempt.status_code == 422

    activation = client.put(
        f"/api/v1/users/{response.json()['id']}",
        json={"is_active": True},
        headers=admin_headers,
    )
    assert activation.status_code == 200
    assert client.post(
        "/api/v1/auth/login",
        json={"username": "new_staff", "password": "StrongPass123"},
    ).status_code == 200


def test_staff_registration_rejects_short_password(client):
    response = client.post("/api/v1/auth/register", json={
        "username": "short_staff",
        "full_name": "Nguyễn Văn Mới",
        "email": "short@example.com",
        "password": "short",
    })
    assert response.status_code == 422


def test_public_booking_creates_pending_appointment_without_exposing_patient(client, db_session):
    doctors = client.get("/api/v1/public/doctors")
    assert doctors.status_code == 200
    assert doctors.json()
    assert "email" not in doctors.json()[0]
    doctor = next(
        item for item in doctors.json()
        if any(
            shift["day_of_week"] == 0
            and shift["start_time"] <= "08:00:00"
            and shift["end_time"] >= "08:30:00"
            for shift in item["shifts"]
        )
    )
    date_value = next_weekday()
    payload = {
        "full_name": "Trần Thị Khách",
        "date_of_birth": "1992-04-15",
        "gender": "Nữ",
        "phone": "0912345678",
        "identity_card": "001092000123",
        "doctor_id": doctor["id"],
        "appointment_date": date_value,
        "start_time": "08:00",
        "reason": "Khám tổng quát",
    }
    response = client.post("/api/v1/public/appointments", json=payload)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["status"] == "PENDING"
    assert data["appointment_code"].startswith("LH-")
    assert "patient" not in data
    assert db_session.query(Patient).filter_by(identity_card="001092000123").one()
    assert client.post("/api/v1/public/appointments", json=payload).status_code == 409

    duplicate_slot = client.post("/api/v1/public/appointments", json={
        **payload,
        "identity_card": "001092000124",
        "phone": "0912345679",
    })
    assert duplicate_slot.status_code == 409


def test_public_booking_rejects_invalid_shift(client):
    doctors = client.get("/api/v1/public/doctors").json()
    doctor = next(item for item in doctors if item["shifts"])
    response = client.post("/api/v1/public/appointments", json={
        "full_name": "Trần Thị Khách",
        "date_of_birth": "1992-04-15",
        "gender": "Nữ",
        "phone": "0912345680",
        "doctor_id": doctor["id"],
        "appointment_date": next_weekday(),
        "start_time": "02:00",
    })
    assert response.status_code == 409
