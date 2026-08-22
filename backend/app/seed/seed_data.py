from datetime import datetime, date, time, timedelta
from sqlalchemy.orm import Session
from backend.app.database import engine, Base, SessionLocal
from backend.app.models.user import User, RoleEnum
from backend.app.models.clinic import Specialty, Clinic, Doctor, Shift
from backend.app.models.patient import Patient
from backend.app.models.appointment import Appointment, AppointmentStatus
from backend.app.models.medical_record import MedicalRecord, RecordStatus, ServiceOrder
from backend.app.models.prescription import Medicine, Prescription, PrescriptionItem
from backend.app.models.invoice import Invoice, PaymentStatus, PaymentMethod
from backend.app.models.audit import AuditLog, AIInvocationLog
from backend.app.core.security import get_password_hash


def seed_database(db: Session = None):
    close_session = False
    if db is None:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        close_session = True

    try:
        print("--- [SEED DATA] Clearing old data if any ---")
        # Check if already seeded
        if db.query(User).filter(User.username == "admin").first():
            print("Database already contains seed data. Refreshing / Ensuring complete dataset...")
        
        # ====================================================================
        # 1. USERS & STAFF ACCOUNTS
        # ====================================================================
        print("1. Seeding Staff Accounts (Admin, Receptionist, Doctors, Accountant)...")
        
        users_data = [
            {
                "username": "admin",
                "email": "admin@phongkham.vn",
                "full_name": "Quản trị viên Hệ thống",
                "role": RoleEnum.ADMIN.value,
                "password": "admin123"
            },
            {
                "username": "receptionist",
                "email": "letan@phongkham.vn",
                "full_name": "Nguyễn Thị Thu Hà",
                "role": RoleEnum.RECEPTIONIST.value,
                "password": "rec123"
            },
            {
                "username": "accountant",
                "email": "ketoan@phongkham.vn",
                "full_name": "Trần Bích Phương",
                "role": RoleEnum.ACCOUNTANT.value,
                "password": "acc123"
            },
            {
                "username": "dr_nam",
                "email": "dr.nam@phongkham.vn",
                "full_name": "BS.CKII Nguyễn Văn Nam",
                "role": RoleEnum.DOCTOR.value,
                "password": "doc123"
            },
            {
                "username": "dr_huong",
                "email": "dr.huong@phongkham.vn",
                "full_name": "ThS.BS Lê Thu Hương",
                "role": RoleEnum.DOCTOR.value,
                "password": "doc123"
            },
            {
                "username": "dr_minh",
                "email": "dr.minh@phongkham.vn",
                "full_name": "BS.CKI Phạm Hoàng Minh",
                "role": RoleEnum.DOCTOR.value,
                "password": "doc123"
            },
            {
                "username": "dr_lan",
                "email": "dr.lan@phongkham.vn",
                "full_name": "BS Vũ Mai Lan",
                "role": RoleEnum.DOCTOR.value,
                "password": "doc123"
            }
        ]

        user_map = {}
        for u in users_data:
            existing = db.query(User).filter(User.username == u["username"]).first()
            if not existing:
                user_obj = User(
                    username=u["username"],
                    email=u["email"],
                    full_name=u["full_name"],
                    role=u["role"],
                    hashed_password=get_password_hash(u["password"]),
                    is_active=True
                )
                db.add(user_obj)
                db.flush()
                user_map[u["username"]] = user_obj
            else:
                user_map[u["username"]] = existing

        # ====================================================================
        # 2. SPECIALTIES
        # ====================================================================
        print("2. Seeding 6 Medical Specialties...")
        specialties_data = [
            {
                "code": "NOI",
                "name": "Nội tổng quát",
                "description": "Khám và điều trị các bệnh nội khoa tổng quát, tiêu hóa, hô hấp, đái tháo đường và nội tiết."
            },
            {
                "code": "TIM",
                "name": "Tim mạch",
                "description": "Khám, chẩn đoán và điều trị tăng huyết áp, bệnh mạch vành, rối loạn nhịp tim và suy tim."
            },
            {
                "code": "NHI",
                "name": "Nhi khoa",
                "description": "Khám, tư vấn dinh dưỡng và điều trị bệnh lý cho trẻ sơ sinh, trẻ nhỏ và trẻ vị thành niên."
            },
            {
                "code": "TMH",
                "name": "Tai Mũi Họng",
                "description": "Nội soi chẩn đoán và điều trị viêm xoang, viêm họng hạt, viêm amidan, viêm tai giữa."
            },
            {
                "code": "RHM",
                "name": "Răng Hàm Mặt",
                "description": "Khám, chữa tủy, nhổ răng không đau, cạo vôi răng và chỉnh nha thẩm mỹ."
            },
            {
                "code": "DL",
                "name": "Da liễu",
                "description": "Khám và điều trị các bệnh lý ngoài da, dị ứng thời tiết, viêm da cơ địa, mụn trứng cá."
            }
        ]

        specialty_map = {}
        for s in specialties_data:
            spec = db.query(Specialty).filter(Specialty.code == s["code"]).first()
            if not spec:
                spec = Specialty(**s)
                db.add(spec)
                db.flush()
            specialty_map[s["code"]] = spec

        # ====================================================================
        # 3. CLINIC CONSULTATION ROOMS
        # ====================================================================
        print("3. Seeding 6 Consultation Rooms...")
        clinics_data = [
            {"room_number": "P101", "name": "Phòng khám Nội tổng quát 1", "specialty_id": specialty_map["NOI"].id},
            {"room_number": "P102", "name": "Phòng khám Chuyên khoa Tim mạch", "specialty_id": specialty_map["TIM"].id},
            {"room_number": "P103", "name": "Phòng khám Nhi khoa 1", "specialty_id": specialty_map["NHI"].id},
            {"room_number": "P201", "name": "Phòng khám Tai Mũi Họng", "specialty_id": specialty_map["TMH"].id},
            {"room_number": "P202", "name": "Phòng khám Nha khoa Răng Hàm Mặt", "specialty_id": specialty_map["RHM"].id},
            {"room_number": "P203", "name": "Phòng khám Chuyên khoa Da liễu", "specialty_id": specialty_map["DL"].id}
        ]

        clinic_map = {}
        for c in clinics_data:
            cl = db.query(Clinic).filter(Clinic.room_number == c["room_number"]).first()
            if not cl:
                cl = Clinic(**c)
                db.add(cl)
                db.flush()
            clinic_map[c["room_number"]] = cl

        # ====================================================================
        # 4. DOCTOR PROFILES & SHIFTS
        # ====================================================================
        print("4. Seeding Doctor Profiles & Weekly Shifts...")
        doctors_data = [
            {
                "user_id": user_map["dr_nam"].id,
                "specialty_id": specialty_map["NOI"].id,
                "clinic_id": clinic_map["P101"].id,
                "title": "BS.CKII",
                "bio": "Hơn 15 năm kinh nghiệm điều trị Nội khoa và Tiêu hóa tại các bệnh viện tuyến đầu.",
                "phone": "0912345601"
            },
            {
                "user_id": user_map["dr_huong"].id,
                "specialty_id": specialty_map["TIM"].id,
                "clinic_id": clinic_map["P102"].id,
                "title": "ThS.BS",
                "bio": "Chuyên gia Viện Tim mạch - Chuyên sâu Tăng huyết áp, Bệnh mạch vành và Siêu âm tim.",
                "phone": "0912345602"
            },
            {
                "user_id": user_map["dr_minh"].id,
                "specialty_id": specialty_map["NHI"].id,
                "clinic_id": clinic_map["P103"].id,
                "title": "BS.CKI",
                "bio": "Bác sĩ chuyên khoa Nhi - Hơn 10 năm kinh nghiệm khám chữa bệnh hô hấp và dinh dưỡng trẻ em.",
                "phone": "0912345603"
            },
            {
                "user_id": user_map["dr_lan"].id,
                "specialty_id": specialty_map["TMH"].id,
                "clinic_id": clinic_map["P201"].id,
                "title": "BS.CKI",
                "bio": "Bác sĩ Tai Mũi Họng - Giỏi nội soi chẩn đoán và điều trị viêm xoang, viêm thanh quản.",
                "phone": "0912345604"
            }
        ]

        doctor_map = {}
        for d in doctors_data:
            doc = db.query(Doctor).filter(Doctor.user_id == d["user_id"]).first()
            if not doc:
                doc = Doctor(**d)
                db.add(doc)
                db.flush()
            doctor_map[d["user_id"]] = doc

        # Shifts
        shifts_data = [
            # Dr Nam: Mon to Fri (0-4), morning 07:30-11:30, afternoon 13:30-17:00
            * [{"doctor_id": doctor_map[user_map["dr_nam"].id].id, "day_of_week": day, "start_time": time(7, 30), "end_time": time(11, 30), "max_patients": 20} for day in range(5)],
            * [{"doctor_id": doctor_map[user_map["dr_nam"].id].id, "day_of_week": day, "start_time": time(13, 30), "end_time": time(17, 0), "max_patients": 20} for day in range(5)],
            # Dr Huong: Mon(0), Wed(2), Fri(4), morning 08:00-12:00, afternoon 13:30-17:30
            * [{"doctor_id": doctor_map[user_map["dr_huong"].id].id, "day_of_week": day, "start_time": time(8, 0), "end_time": time(12, 0), "max_patients": 15} for day in [0, 2, 4]],
            * [{"doctor_id": doctor_map[user_map["dr_huong"].id].id, "day_of_week": day, "start_time": time(13, 30), "end_time": time(17, 30), "max_patients": 15} for day in [0, 2, 4]],
            # Dr Minh: Mon-Sat (0-5), morning 07:30-11:30
            * [{"doctor_id": doctor_map[user_map["dr_minh"].id].id, "day_of_week": day, "start_time": time(7, 30), "end_time": time(11, 30), "max_patients": 25} for day in range(6)],
            # Dr Lan: Tue(1), Thu(3), Sat(5), morning 08:00-12:00, afternoon 13:30-17:00
            * [{"doctor_id": doctor_map[user_map["dr_lan"].id].id, "day_of_week": day, "start_time": time(8, 0), "end_time": time(12, 0), "max_patients": 20} for day in [1, 3, 5]],
            * [{"doctor_id": doctor_map[user_map["dr_lan"].id].id, "day_of_week": day, "start_time": time(13, 30), "end_time": time(17, 0), "max_patients": 20} for day in [1, 3, 5]]
        ]

        for s in shifts_data:
            existing_shift = db.query(Shift).filter(
                Shift.doctor_id == s["doctor_id"],
                Shift.day_of_week == s["day_of_week"],
                Shift.start_time == s["start_time"]
            ).first()
            if not existing_shift:
                shift_obj = Shift(**s)
                db.add(shift_obj)
        db.flush()

        # ====================================================================
        # 5. MEDICINES CATALOG (25+ standard Vietnamese medicines)
        # ====================================================================
        print("5. Seeding 28 Standard Vietnamese Medicines & Stock...")
        medicines_data = [
            # Antibiotics
            {"code": "MED-AUG-1G", "name": "Augmentin 1g", "active_ingredient": "Amoxicillin + Clavulanic acid", "dosage_form": "Viên nén", "unit": "Viên", "unit_price": 18500.0, "stock_quantity": 500, "usage_instructions": "Uống ngay trước bữa ăn"},
            {"code": "MED-AMOX-500", "name": "Amoxicillin 500mg", "active_ingredient": "Amoxicillin", "dosage_form": "Viên nang", "unit": "Viên", "unit_price": 2500.0, "stock_quantity": 1000, "usage_instructions": "Uống sau ăn no"},
            {"code": "MED-CEF-200", "name": "Cefixime 200mg", "active_ingredient": "Cefixime", "dosage_form": "Viên nén", "unit": "Viên", "unit_price": 12000.0, "stock_quantity": 400, "usage_instructions": "Uống sau bữa ăn, cách 12 giờ"},
            {"code": "MED-AZI-500", "name": "Azithromycin 500mg", "active_ingredient": "Azithromycin", "dosage_form": "Viên nén", "unit": "Viên", "unit_price": 22000.0, "stock_quantity": 300, "usage_instructions": "Uống 1 lần/ngày trước ăn 1h hoặc sau ăn 2h"},
            {"code": "MED-CIPRO-500", "name": "Ciprofloxacin 500mg", "active_ingredient": "Ciprofloxacin", "dosage_form": "Viên nén", "unit": "Viên", "unit_price": 6500.0, "stock_quantity": 350, "usage_instructions": "Uống với nhiều nước sau ăn"},
            
            # Pain & Fever
            {"code": "MED-PARA-500", "name": "Paracetamol 500mg", "active_ingredient": "Paracetamol", "dosage_form": "Viên nén", "unit": "Viên", "unit_price": 1500.0, "stock_quantity": 2500, "usage_instructions": "Uống khi sốt trên 38.5 độ C hoặc đau nhức, cách mỗi 4-6 giờ"},
            {"code": "MED-PANADOL-EXTRA", "name": "Panadol Extra", "active_ingredient": "Paracetamol 500mg + Caffeine 65mg", "dosage_form": "Viên nén", "unit": "Viên", "unit_price": 2800.0, "stock_quantity": 1500, "usage_instructions": "Uống sau ăn khi đau đầu hoặc sốt"},
            {"code": "MED-EFFER-500", "name": "Efferalgan 500mg", "active_ingredient": "Paracetamol", "dosage_form": "Viên sủi", "unit": "Viên", "unit_price": 4500.0, "stock_quantity": 800, "usage_instructions": "Hòa tan trong 1 ly nước lọc rồi uống"},
            {"code": "MED-IBU-400", "name": "Ibuprofen 400mg", "active_ingredient": "Ibuprofen", "dosage_form": "Viên nén", "unit": "Viên", "unit_price": 3000.0, "stock_quantity": 600, "usage_instructions": "Uống ngay sau khi ăn no, không dùng cho bệnh nhân loét dạ dày"},
            {"code": "MED-CELE-200", "name": "Celecoxib 200mg", "active_ingredient": "Celecoxib", "dosage_form": "Viên nang", "unit": "Viên", "unit_price": 11000.0, "stock_quantity": 400, "usage_instructions": "Uống sau ăn no"},
            {"code": "MED-ALPHA-CHYMO", "name": "Alphachoay", "active_ingredient": "Chymotrypsin 4.2mg", "dosage_form": "Viên nén", "unit": "Viên", "unit_price": 3200.0, "stock_quantity": 1200, "usage_instructions": "Ngậm dưới lưỡi hoặc uống sau ăn để giảm phù nề, sưng viêm"},
            
            # Cardiovascular & Hypertension
            {"code": "MED-AMLO-5", "name": "Amlodipine 5mg", "active_ingredient": "Amlodipine", "dosage_form": "Viên nén", "unit": "Viên", "unit_price": 3500.0, "stock_quantity": 900, "usage_instructions": "Uống 1 viên vào buổi sáng mỗi ngày"},
            {"code": "MED-LOSAR-50", "name": "Losartan 50mg", "active_ingredient": "Losartan potassium", "dosage_form": "Viên nén", "unit": "Viên", "unit_price": 5500.0, "stock_quantity": 700, "usage_instructions": "Uống 1 viên mỗi ngày cố định một giờ"},
            {"code": "MED-TELMI-40", "name": "Telmisartan 40mg", "active_ingredient": "Telmisartan", "dosage_form": "Viên nén", "unit": "Viên", "unit_price": 8500.0, "stock_quantity": 600, "usage_instructions": "Uống 1 viên vào buổi sáng"},
            {"code": "MED-CONCOR-5", "name": "Concor 5mg", "active_ingredient": "Bisoprolol", "dosage_form": "Viên nén", "unit": "Viên", "unit_price": 7200.0, "stock_quantity": 500, "usage_instructions": "Uống 1 viên buổi sáng trước hoặc sau ăn"},
            {"code": "MED-ATOR-20", "name": "Atorvastatin 20mg", "active_ingredient": "Atorvastatin", "dosage_form": "Viên nén", "unit": "Viên", "unit_price": 9000.0, "stock_quantity": 800, "usage_instructions": "Uống 1 viên vào buổi tối trước khi đi ngủ"},
            
            # Gastrointestinal
            {"code": "MED-NEXIUM-40", "name": "Nexium Mups 40mg", "active_ingredient": "Esomeprazole", "dosage_form": "Viên nén", "unit": "Viên", "unit_price": 24500.0, "stock_quantity": 400, "usage_instructions": "Uống trước bữa ăn sáng 30-60 phút"},
            {"code": "MED-OMEP-20", "name": "Omeprazole 20mg", "active_ingredient": "Omeprazole", "dosage_form": "Viên nang", "unit": "Viên", "unit_price": 3000.0, "stock_quantity": 1000, "usage_instructions": "Uống trước bữa ăn sáng 30 phút"},
            {"code": "MED-BERB-100", "name": "Berberin 100mg", "active_ingredient": "Berberin Clorid", "dosage_form": "Viên nén", "unit": "Viên", "unit_price": 1200.0, "stock_quantity": 1000, "usage_instructions": "Uống khi đau bụng, tiêu chảy"},
            {"code": "MED-PHOSPHALUGEL", "name": "Phosphalugel (Gel chữ P)", "active_ingredient": "Aluminium phosphate 20%", "dosage_form": "Gói hỗn dịch", "unit": "Gói", "unit_price": 5000.0, "stock_quantity": 1200, "usage_instructions": "Uống 1 gói khi đau rát dạ dày hoặc sau ăn 1-2 giờ"},
            {"code": "MED-SMECTA", "name": "Smecta", "active_ingredient": "Diosmectite 3g", "dosage_form": "Gói bột", "unit": "Gói", "unit_price": 4200.0, "stock_quantity": 700, "usage_instructions": "Hòa với 50ml nước ấm uống khi tiêu chảy"},
            {"code": "MED-DOMP-10", "name": "Domperidone 10mg", "active_ingredient": "Domperidone", "dosage_form": "Viên nén", "unit": "Viên", "unit_price": 2000.0, "stock_quantity": 600, "usage_instructions": "Uống trước bữa ăn 15-30 phút để chống buồn nôn"},

            # Respiratory & Allergy
            {"code": "MED-DESLOR-5", "name": "Desloratadine 5mg", "active_ingredient": "Desloratadine", "dosage_form": "Viên nén", "unit": "Viên", "unit_price": 4800.0, "stock_quantity": 800, "usage_instructions": "Uống 1 viên vào buổi tối"},
            {"code": "MED-CETI-10", "name": "Cetirizine 10mg", "active_ingredient": "Cetirizine dihydrochloride", "dosage_form": "Viên nén", "unit": "Viên", "unit_price": 2200.0, "stock_quantity": 900, "usage_instructions": "Uống 1 viên mỗi ngày khi có triệu chứng dị ứng"},
            {"code": "MED-ACETYL-200", "name": "Acetylcysteine 200mg", "active_ingredient": "Acetylcysteine", "dosage_form": "Gói bột sủi", "unit": "Gói", "unit_price": 3500.0, "stock_quantity": 1100, "usage_instructions": "Hòa vào nước uống sau bữa ăn để làm loãng đờm"},
            {"code": "MED-XISAT-75", "name": "Nước muối xịt mũi Xisat 75ml", "active_ingredient": "Nước biển sâu nguyên chất", "dosage_form": "Chai xịt", "unit": "Chai", "unit_price": 32000.0, "stock_quantity": 300, "usage_instructions": "Xịt vào mỗi bên mũi 2-3 lần/ngày để vệ sinh đường thở"},
            {"code": "MED-OTRIVIN-005", "name": "Otrivin 0.05% nhỏ mũi", "active_ingredient": "Xylometazoline hydrochloride", "dosage_form": "Chai nhỏ", "unit": "Chai", "unit_price": 45000.0, "stock_quantity": 150, "usage_instructions": "Nhỏ 1-2 giọt vào mỗi bên mũi, dùng không quá 5 ngày liên tục"},

            # Vitamins & Supplements
            {"code": "MED-VIT-C-500", "name": "Vitamin C 500mg", "active_ingredient": "Acid Ascorbic", "dosage_form": "Viên nén", "unit": "Viên", "unit_price": 1800.0, "stock_quantity": 1200, "usage_instructions": "Uống sau bữa ăn sáng để tăng đề kháng"},
            {"code": "MED-BEROCCA", "name": "Berocca Performance", "active_ingredient": "Vitamin nhóm B + C + Magie + Kẽm", "dosage_form": "Viên sủi", "unit": "Viên", "unit_price": 9500.0, "stock_quantity": 500, "usage_instructions": "Hòa tan 1 viên trong ly nước uống vào buổi sáng"}
        ]

        medicine_map = {}
        for m in medicines_data:
            med = db.query(Medicine).filter(Medicine.code == m["code"]).first()
            if not med:
                med = Medicine(**m)
                db.add(med)
                db.flush()
            medicine_map[m["code"]] = med

        # ====================================================================
        # 6. PATIENT RECORDS (10 Realistic Vietnamese Patient Profiles)
        # ====================================================================
        print("6. Seeding 10 Realistic Vietnamese Patients...")
        patients_data = [
            {
                "medical_code": "BN-20260105-0001",
                "full_name": "Trần Văn Hùng",
                "date_of_birth": date(1975, 4, 12),
                "gender": "Nam",
                "phone": "0913884521",
                "identity_card": "001085012345",
                "address": "Số 45 ngõ 198 Thái Hà, Đống Đa, Hà Nội",
                "insurance_number": "GD4010123456789",
                "medical_history": "Tăng huyết áp 5 năm, đái tháo đường type 2 đang điều trị ngoại trú.",
                "drug_allergies": "Dị ứng Penicillin (nổi mề đay, khó thở nhẹ)",
                "emergency_contact": "Trần Thị Mai (Vợ) - 0913884522"
            },
            {
                "medical_code": "BN-20260110-0002",
                "full_name": "Lê Thị Kim Ngân",
                "date_of_birth": date(1992, 8, 24),
                "gender": "Nữ",
                "phone": "0982345678",
                "identity_card": "079192004567",
                "address": "128 Nguyễn Đình Chiểu, Quận 3, TP. Hồ Chí Minh",
                "insurance_number": "HS4790123456789",
                "medical_history": "Hen phế quản mãn tính từ nhỏ, viêm mũi dị ứng thời tiết.",
                "drug_allergies": "Dị ứng Aspirin và nhóm NSAIDs (co thắt phế quản)",
                "emergency_contact": "Lê Văn Tuấn (Anh trai) - 0982345679"
            },
            {
                "medical_code": "BN-20260115-0003",
                "full_name": "Hoàng Đức Thắng",
                "date_of_birth": date(1988, 11, 3),
                "gender": "Nam",
                "phone": "0904567890",
                "identity_card": "031078009876",
                "address": "Số 12 Lạch Tray, Ngô Quyền, Hải Phòng",
                "insurance_number": "DN4310123456789",
                "medical_history": "Viêm loét dạ dày tá tràng Hp (+), đau thượng vị tái diễn.",
                "drug_allergies": "Chưa ghi nhận dị ứng thuốc",
                "emergency_contact": "Nguyễn Thu Thủy (Vợ) - 0904567891"
            },
            {
                "medical_code": "BN-20260201-0004",
                "full_name": "Phạm Quỳnh Trang",
                "date_of_birth": date(1998, 6, 17),
                "gender": "Nữ",
                "phone": "0971239876",
                "identity_card": "001198007654",
                "address": "22 Tôn Thất Tùng, Đống Đa, Hà Nội",
                "insurance_number": "SV4010123456789",
                "medical_history": "Viêm xoang hàm mạn tính, rối loạn tiền đình nhẹ.",
                "drug_allergies": "Dị ứng Hải sản tôm cua",
                "emergency_contact": "Phạm Văn Quang (Bố) - 0971239870"
            },
            {
                "medical_code": "BN-20260210-0005",
                "full_name": "Nguyễn Văn Bảo",
                "date_of_birth": date(2020, 3, 15),
                "gender": "Nam",
                "phone": "0934567123",
                "identity_card": None,
                "address": "56 Giải Phóng, Phương Mai, Đống Đa, Hà Nội",
                "insurance_number": "TE1010123456789",
                "medical_history": "Viêm phế quản co thắt tái phát nhiều lần.",
                "drug_allergies": "Dị ứng phấn hoa và lông mèo",
                "emergency_contact": "Nguyễn Văn Hùng (Bố) - 0934567123"
            },
            {
                "medical_code": "BN-20260215-0006",
                "full_name": "Đỗ Thị Minh Châu",
                "date_of_birth": date(1968, 9, 30),
                "gender": "Nữ",
                "phone": "0945678123",
                "identity_card": "040180003421",
                "address": "88 Trần Phú, Hà Đông, Hà Nội",
                "insurance_number": "CB4400123456789",
                "medical_history": "Rối loạn lipid máu, thiếu máu cơ tim cục bộ.",
                "drug_allergies": "Dị ứng Amoxicillin (phát ban mẩn đỏ)",
                "emergency_contact": "Đỗ Minh Đức (Con trai) - 0945678124"
            },
            {
                "medical_code": "BN-20260220-0007",
                "full_name": "Vũ Hải Long",
                "date_of_birth": date(1983, 1, 14),
                "gender": "Nam",
                "phone": "0967890123",
                "identity_card": "036092001122",
                "address": "15 Lê Lợi, TP. Nam Định",
                "insurance_number": "CN4360123456789",
                "medical_history": "Gút mạn tính có tophi nhỏ, sỏi thận 4mm.",
                "drug_allergies": "Không có",
                "emergency_contact": "Vũ Thị Sen (Vợ) - 0967890125"
            },
            {
                "medical_code": "BN-20260301-0008",
                "full_name": "Bùi Thị Bích Liên",
                "date_of_birth": date(1955, 12, 5),
                "gender": "Nữ",
                "phone": "0918765432",
                "identity_card": "001175008899",
                "address": "40 Phan Chu Trinh, Hoàn Kiếm, Hà Nội",
                "insurance_number": "HT4010123456789",
                "medical_history": "Thoái hóa khớp gối hai bên, loãng xương sau mãn kinh.",
                "drug_allergies": "Dị ứng Cephalosporin thế hệ 1",
                "emergency_contact": "Bùi Tuấn Anh (Con trai) - 0918765430"
            },
            {
                "medical_code": "BN-20260305-0009",
                "full_name": "Đặng Quang Huy",
                "date_of_birth": date(1995, 7, 20),
                "gender": "Nam",
                "phone": "0923456789",
                "identity_card": "079090005544",
                "address": "250 Lê Văn Sỹ, Phường 14, Quận 3, TP. Hồ Chí Minh",
                "insurance_number": "DN4790123456789",
                "medical_history": "Viêm gan B mạn tính đang theo dõi định kỳ.",
                "drug_allergies": "Không có",
                "emergency_contact": "Đặng Thị Hoa (Mẹ) - 0923456780"
            },
            {
                "medical_code": "BN-20260310-0010",
                "full_name": "Ngô Phương Thảo",
                "date_of_birth": date(2001, 10, 8),
                "gender": "Nữ",
                "phone": "0938991122",
                "identity_card": "025199006677",
                "address": "78 Quang Trung, TP. Thái Nguyên",
                "insurance_number": "GD4250123456789",
                "medical_history": "Đau nửa đầu Migraine, mất ngủ kéo dài.",
                "drug_allergies": "Dị ứng Paracetamol (hiếm gặp - ngứa nổi ban)",
                "emergency_contact": "Ngô Văn Kiên (Bố) - 0938991120"
            }
        ]

        patient_map = {}
        for p in patients_data:
            pat = db.query(Patient).filter(Patient.medical_code == p["medical_code"]).first()
            if not pat:
                pat = Patient(**p)
                db.add(pat)
                db.flush()
            patient_map[p["medical_code"]] = pat

        # ====================================================================
        # 7. SAMPLE APPOINTMENTS, MEDICAL RECORDS, PRESCRIPTIONS & INVOICES
        # ====================================================================
        print("7. Seeding Sample Encounters, Prescriptions & Invoices...")
        
        # Encounter 1: Patient Tran Van Hung (dr_huong - Tim mach)
        today = date.today()
        p1 = patient_map["BN-20260105-0001"]
        d_huong = doctor_map[user_map["dr_huong"].id]
        c_tim = clinic_map["P102"]

        appt1 = db.query(Appointment).filter(Appointment.appointment_code == "LH-20260822-0001").first()
        if not appt1:
            appt1 = Appointment(
                appointment_code="LH-20260822-0001",
                patient_id=p1.id,
                doctor_id=d_huong.id,
                clinic_id=c_tim.id,
                appointment_date=today,
                start_time=time(8, 30),
                end_time=time(9, 0),
                status=AppointmentStatus.COMPLETED.value,
                reason="Tái khám định kỳ tăng huyết áp và đau ngực nhẹ khi gắng sức",
                notes="Bệnh nhân có tiền sử dị ứng Penicillin"
            )
            db.add(appt1)
            db.flush()

        mr1 = db.query(MedicalRecord).filter(MedicalRecord.record_code == "KB-20260822-0001").first()
        if not mr1:
            mr1 = MedicalRecord(
                record_code="KB-20260822-0001",
                patient_id=p1.id,
                doctor_id=d_huong.id,
                appointment_id=appt1.id,
                exam_date=datetime.now(),
                chief_complaint="Hồi hộp, nặng ngực khi leo cầu thang, huyết áp đo tại nhà dao động 145/90 mmHg",
                blood_pressure="140/90 mmHg",
                heart_rate=82,
                temperature=36.7,
                respiratory_rate=18,
                weight=72.0,
                height=168.0,
                bmi=25.5,
                physical_exam="Tim đều, T1 T2 rõ, không nghe tiếng thổi bệnh lý. Phổi thông khí tốt, không rale. Bụng mềm.",
                diagnosis_icd10="Bệnh tăng huyết áp vô căn (nguyên phát)",
                icd10_code="I10",
                doctor_notes="Ăn giảm muối, hạn chế mỡ động vật, tập thể dục nhẹ nhàng 30p mỗi ngày, không tự ý ngưng thuốc.",
                status=RecordStatus.COMPLETED.value
            )
            db.add(mr1)
            db.flush()

            # Service order
            so1 = ServiceOrder(
                medical_record_id=mr1.id,
                service_name="Điện tâm đồ ECG 12 chuyển đạo",
                service_code="ECG-12",
                price=100000.0,
                result="Nhịp xoang đều tần số 80ck/p, trục trung gian, không thấy biến đổi ST-T cấp."
            )
            so2 = ServiceOrder(
                medical_record_id=mr1.id,
                service_name="Siêu âm tim Dopler màu",
                service_code="SA-TIM-DOPLER",
                price=350000.0,
                result="Chức năng tâm thu thất trái EF 62%, thất trái dày nhẹ đồng tâm, không hở van tim nặng."
            )
            db.add_all([so1, so2])
            db.flush()

            # Prescription
            presc1 = Prescription(
                prescription_code="DT-20260822-0001",
                medical_record_id=mr1.id,
                doctor_id=d_huong.id,
                patient_id=p1.id,
                diagnosis="Tăng huyết áp vô căn (I10) / Rối loạn lipid máu",
                advice="Uống thuốc đều đặn vào mỗi buổi sáng, tái khám sau 30 ngày hoặc khi có dấu hiệu bất thường."
            )
            db.add(presc1)
            db.flush()

            # Prescription Items (Amlodipine + Atorvastatin)
            pi1 = PrescriptionItem(
                prescription_id=presc1.id,
                medicine_id=medicine_map["MED-AMLO-5"].id,
                quantity=30,
                dosage="1 viên",
                frequency="1 lần/ngày vào buổi sáng",
                duration_days=30,
                instructions="Uống sau bữa ăn sáng 15 phút"
            )
            pi2 = PrescriptionItem(
                prescription_id=presc1.id,
                medicine_id=medicine_map["MED-ATOR-20"].id,
                quantity=30,
                dosage="1 viên",
                frequency="1 lần/ngày vào buổi tối",
                duration_days=30,
                instructions="Uống trước khi đi ngủ"
            )
            db.add_all([pi1, pi2])
            db.flush()

            # Invoice
            inv1 = Invoice(
                invoice_code="HD-20260822-0001",
                medical_record_id=mr1.id,
                patient_id=p1.id,
                consultation_fee=150000.0,
                service_fee=450000.0,  # 100k + 350k
                medicine_fee=375000.0, # 30 * 3500 + 30 * 9000 = 105000 + 270000 = 375000
                total_amount=975000.0,
                insurance_discount=195000.0, # 20% BHYT discount for example
                patient_pay_amount=780000.0,
                payment_status=PaymentStatus.PAID.value,
                payment_method=PaymentMethod.BANK_TRANSFER.value,
                transaction_code="TXN-20260822-0098",
                cashier_id=user_map["accountant"].id,
                paid_at=datetime.now(),
                notes="Thanh toán qua chuyển khoản ngân hàng VietQR"
            )
            db.add(inv1)
            db.flush()

        # Encounter 2: Patient Hoang Duc Thang (dr_nam - Noi tong quat)
        p3 = patient_map["BN-20260115-0003"]
        d_nam = doctor_map[user_map["dr_nam"].id]
        c_noi = clinic_map["P101"]

        appt2 = db.query(Appointment).filter(Appointment.appointment_code == "LH-20260822-0002").first()
        if not appt2:
            appt2 = Appointment(
                appointment_code="LH-20260822-0002",
                patient_id=p3.id,
                doctor_id=d_nam.id,
                clinic_id=c_noi.id,
                appointment_date=today,
                start_time=time(9, 30),
                end_time=time(10, 0),
                status=AppointmentStatus.CONFIRMED.value,
                reason="Đau âm ỉ vùng thượng vị sau ăn, ợ chua, buồn nôn",
                notes="Có tiền sử viêm loét dạ dày"
            )
            db.add(appt2)
            db.flush()

        db.commit()
        print("--- [SEED DATA] Database seeding completed successfully! ---")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        if close_session:
            db.close()


if __name__ == "__main__":
    seed_database()
