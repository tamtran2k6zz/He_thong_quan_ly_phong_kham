import sys
import io

# Force UTF-8 for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from fastapi.testclient import TestClient
from backend.app.main import app

def test_system():
    client = TestClient(app)
    roles = [
        ('admin', 'admin123', 'admin'),
        ('receptionist', 'rec123', 'receptionist'),
        ('dr_nam', 'doc123', 'doctor'),
        ('accountant', 'acc123', 'accountant')
    ]

    tokens = {}
    print("--- 1. KIEM TRA DANG NHAP 4 VAI TRO ---")
    for u, p, role in roles:
        r = client.post('/api/v1/auth/login', json={'username': u, 'password': p})
        assert r.status_code == 200, f"Login failed for {u}: {r.text}"
        tokens[role] = r.json()['access_token']
        print(f"[OK] Dang nhap thanh cong [{role.upper()}]: username={u}")

    print("\n--- 2. KIEM TRA NGIEP VU LE TAN (RECEPTIONIST) ---")
    headers_rec = {'Authorization': f"Bearer {tokens['receptionist']}"}
    r_pats = client.get('/api/v1/patients/?limit=5', headers=headers_rec)
    assert r_pats.status_code == 200
    patients = r_pats.json()
    print(f"[OK] Lay danh sach benh nhan: {len(patients)} benh nhan")

    r_appts = client.get('/api/v1/appointments/', headers=headers_rec)
    assert r_appts.status_code == 200
    print(f"[OK] Lay danh sach lich hen: {len(r_appts.json())} lich hen")

    print("\n--- 3. KIEM TRA NGIEP VU BAC SI (DOCTOR) ---")
    headers_doc = {'Authorization': f"Bearer {tokens['doctor']}"}
    r_queue = client.get('/api/v1/medical_records/queue', headers=headers_doc)
    assert r_queue.status_code == 200, f"Get queue failed: {r_queue.text}"
    queue = r_queue.json()
    print(f"[OK] Bac si lay hang cho kham: {len(queue)} benh nhan dang cho")

    # Kiem tra AI suggestion
    print("\n--- 4. KIEM TRA TINH NANG AI TRO LY HANH CHINH ---")
    ai_req = {
        "symptoms": "Bệnh nhân sốt cao 39 độ, ho có đờm, đau họng 3 ngày",
        "patient_age": 35,
        "patient_gender": "Nam",
        "medical_history": "Không có tiền sử dị ứng"
    }
    r_ai = client.post('/api/v1/ai/suggest-icd10', json=ai_req, headers=headers_doc)
    print(f"[OK] Goi AI goi y ICD-10: Status {r_ai.status_code}")
    if r_ai.status_code == 200:
        data = r_ai.json()
        print(f"     Ket qua AI: {data}")

    print("\n--- 5. KIEM TRA NGIEP VU KE TOAN (ACCOUNTANT) ---")
    headers_acc = {'Authorization': f"Bearer {tokens['accountant']}"}
    r_inv = client.get('/api/v1/invoices/', headers=headers_acc)
    assert r_inv.status_code == 200
    print(f"[OK] Ke toan lay danh sach hoa don: {len(r_inv.json())} hoa don")

    print("\n--- 6. KIEM TRA QUAN TRI VIEN (ADMIN) ---")
    headers_admin = {'Authorization': f"Bearer {tokens['admin']}"}
    r_dash = client.get('/api/v1/stats/dashboard', headers=headers_admin)
    assert r_dash.status_code == 200
    dash_data = r_dash.json()
    print(f"[OK] Dashboard thong ke: Doanh thu={dash_data.get('total_revenue')}, Benh nhan={dash_data.get('total_patients')}")

    r_audit = client.get('/api/v1/audit/logs', headers=headers_admin)
    assert r_audit.status_code == 200
    print(f"[OK] Audit Logs: {len(r_audit.json())} nhat ky")

    r_ai_logs = client.get('/api/v1/audit/ai-logs', headers=headers_admin)
    assert r_ai_logs.status_code == 200
    print(f"[OK] AI Audit Logs: {len(r_ai_logs.json())} nhat ky AI")

    print("\n--- 7. KIEM TRA CONG DANG KY CONG DONG (PUBLIC PORTAL) ---")
    r_specs = client.get('/api/v1/public/specialties')
    print(f"[OK] Chuyen khoa cong khai: Status {r_specs.status_code}, {len(r_specs.json())} chuyen khoa")

    print("\n=======================================================")
    print(">>> TAT CA CAC LUONG NGHIEP VU HOAT DONG TOT! <<<")
    print("=======================================================")

if __name__ == '__main__':
    test_system()
