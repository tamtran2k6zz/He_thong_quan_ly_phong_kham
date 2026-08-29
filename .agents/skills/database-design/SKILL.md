---
name: database-design
description: Quy chuẩn thiết kế Cơ sở dữ liệu quan hệ y tế (Relational Database Design) chuẩn hóa 3NF gồm 14 bảng quan hệ, tối ưu hóa chỉ mục tìm kiếm và kiểm tra xung đột lịch cho CMS-AI.
objective: Cung cấp phương pháp luận và chuẩn mực thiết kế cơ sở dữ liệu quan hệ y tế chất lượng cao, đảm bảo toàn vẹn dữ liệu (ACID), khóa ngoại, ràng buộc duy nhất, ghi vết kiểm toán và tối ưu hóa hiệu năng truy vấn.
inputs:
  - Tài liệu phân tích yêu cầu nghiệp vụ (docs/requirements.md)
  - Mô hình dữ liệu và các thực thể y tế (Bệnh nhân, Lịch hẹn, Khám bệnh, Đơn thuốc, Viện phí, Logs)
  - Quy định về lưu trữ và bảo vệ dữ liệu y tế (Audit Logging, PII storage)
  - Hệ quản trị cơ sở dữ liệu mục tiêu: SQLite (Dev/Test) & PostgreSQL 16 (Production)
process:
  - 1. Trích xuất thực thể, thuộc tính và mối quan hệ trong quy trình khám chữa bệnh
  - 2. Thiết kế cấu trúc 14 bảng quan hệ và chuẩn hóa đạt mức 3NF (Third Normal Form)
  - 3. Thiết lập các ràng buộc toàn vẹn: Primary Keys, Foreign Keys, Unique Keys và Check Constraints
  - 4. Quy chuẩn định dạng mã định danh nghiệp vụ (Mã bệnh nhân, Mã phiếu khám, Mã hóa đơn)
  - 5. Thiết kế chiến lược chỉ mục (Indexing Strategy) tối ưu hóa xung đột lịch và tìm kiếm hồ sơ
  - 6. Thiết kế bảng ghi nhật ký kiểm toán (AuditLog) và nhật ký gọi AI (AIInvocationLog)
  - 7. Xây dựng tài liệu Từ điển dữ liệu (Data Dictionary) và sơ đồ ERD chi tiết
rules:
  - Mọi bảng bắt buộc phải có Khóa chính (Primary Key `id` kiểu Integer Auto-increment)
  - Khóa ngoại (Foreign Key) phải có quy tắc OnDelete rõ ràng (RESTRICT hoặc CASCADE theo ngữ cảnh)
  - Bảng patients bắt buộc có trường `medical_code` với ràng buộc UNIQUE
  - Trường mật khẩu người dùng `hashed_password` không bao giờ lưu trữ dạng plaintext
  - Mọi thao tác ghi/sửa dữ liệu bệnh nhân và gọi AI phải được phản ánh vào bảng nhật ký tương ứng
outputs:
  - docs/database-design.md (Đặc tả chi tiết 14 bảng CSDL, Sơ đồ ERD, Chỉ mục và Data Dictionary)
verification:
  - Kiểm tra tính tuân thủ chuẩn 3NF: Không có thuộc tính lặp, không có phụ thuộc bắc cầu
  - Kiểm tra tính toàn vẹn tham chiếu của toàn bộ 14 bảng quan hệ
  - Xác nhận sự tồn tại của các Composite Index hỗ trợ Conflict Detection Engine
  - Đảm bảo script migration và seed data thực thi thành công 100% trên cả SQLite và PostgreSQL
---

# Kỹ năng Thiết kế Cơ sở Dữ liệu Quan hệ Y tế (Database Design Skill)

## 1. Objective (Mục tiêu Kỹ năng)

Kỹ năng này định hình các tiêu chuẩn thiết kế và tài liệu hóa cấu trúc Cơ sở Dữ liệu quan hệ y tế cho **Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp Trợ lý AI Hành chính (CMS-AI)**.

Mục tiêu cốt lõi:
1. Xây dựng lược đồ cơ sở dữ liệu quan hệ gồm **14 bảng chuẩn hóa đạt mức 3NF (Third Normal Form)**, phản ánh chính xác chu trình nghiệp vụ khép kín từ Đón tiếp -> Khám bệnh -> Kê đơn -> Viện phí -> Kiểm toán.
2. Thiết lập hệ thống ràng buộc toàn vẹn dữ liệu nghiêm ngặt (PK, FK, Unique constraints, Not Null) bảo vệ dữ liệu y tế khỏi tình trạng mồ côi hoặc mâu thuẫn.
3. Thiết kế chiến lược đánh chỉ mục (Indexing Strategy) chuyên sâu, tối ưu hóa thời gian thực thi của thuật toán phát hiện xung đột lịch khám (`check_appointment_conflict`) và tra cứu hồ sơ bệnh nhân dưới 10ms.
4. Tích hợp sẵn cơ chế lưu vết kiểm toán (Audit Trail) và nhật ký gọi AI (AI Invocation Logs) ngay trong tầng CSDL.

---

## 2. Terminology & Conceptual Model (Mô hình Khái niệm)

Trong không gian Thiết kế Cơ sở dữ liệu:

```
+-----------------------------------------------------------------------------------------------+
|                                     MÔ HÌNH KHÁI NIỆM CƠ SỞ DỮ LIỆU                           |
+-----------------------------------------------------------------------------------------------+
|  1. CODEX (AI Agent)         : Kỹ sư Cơ sở Dữ liệu (Database Architect Agent). Đề xuất lược đồ|
|                                bảng, chuẩn hóa quan hệ, viết migration và định nghĩa models.  |
|  2. SKILL (Procedural Standard): Quy chuẩn thiết kế CSDL y tế 3NF, từ điển dữ liệu 14 bảng,   |
|                                chiến lược index và quy tắc toàn vẹn tham chiếu (Skill này).   |
|  3. TOOL (Environment Action): Công cụ chạy migration Alembic/SQLAlchemy, công cụ dump schema, |
|                                công cụ đo benchmark truy vấn SQLite/PostgreSQL.               |
|  4. MCP (Model Context Protocol): Giao thức truy xuất schema metadata và cấu trúc bảng an toàn.|
+-----------------------------------------------------------------------------------------------+
```

---

## 3. Inputs & Prerequisites (Đầu vào & Điều kiện Tiên quyết)

1. **Yêu cầu Nghiệp vụ Y tế**: `docs/requirements.md` (FR-001..FR-038).
2. **Quy định Pháp lý & Định danh Y tế**:
   - Quy tắc sinh mã bệnh nhân: `BN-YYYYMMDD-XXXX` (VD: `BN-20260829-0001`).
   - Quy tắc sinh mã số thẻ BHYT: 15 ký tự (2 chữ cái đầu + 13 chữ số).
   - Số Căn cước công dân: 12 chữ số.
3. **Môi trường Cơ sở Dữ liệu**:
   - SQLAlchemy 2.0 ORM Declarative Models.
   - SQLite cho môi trường Dev/Test (In-memory / File local).
   - PostgreSQL 16 cho môi trường Production (Docker Container).

---

## 4. Execution Process (Quy trình Thực thi Từng bước)

```
[Bước 1: Trích xuất 14 Thực thể] ---> [Bước 2: Chuẩn hóa 3NF] ---> [Bước 3: Ràng buộc PK/FK]
                                                                                |
[Bước 6: Thiết kế Bảng Logs]     <--- [Bước 5: Chiến lược Index] <--- [Bước 4: Chuẩn hóa Mã Y tế]
           |
           v
[Bước 7: Lập Từ điển Dữ liệu & Sơ đồ ERD Hoàn chỉnh]
```

### Bước 1: Trích xuất 14 Thực thể Cốt lõi của Phòng khám
Hệ thống quản lý 14 thực thể được phân loại theo 6 nhóm nghiệp vụ:

| Nhóm Nghiệp vụ | Danh sách Bảng CSDL | Mục đích & Trách nhiệm |
|---|---|---|
| **1. Quản trị & Xác thực** | `users` | Lưu tài khoản, email, mật khẩu băm (Bcrypt), vai trò RBAC (admin, receptionist, doctor, accountant), trạng thái kích hoạt. |
| **2. Cơ sở & Bác sĩ** | `specialties`<br>`clinics`<br>`doctors`<br>`doctor_shifts` | Quản lý chuyên khoa (Nội, Ngoại, Nhi...), danh sách phòng khám, hồ sơ bác sĩ (học vị, CCHN), và lịch phân ca làm việc theo tuần. |
| **3. Bệnh nhân & Lịch hẹn** | `patients`<br>`appointments` | Quản lý hồ sơ nhân khẩu học bệnh nhân, BHYT, tiền sử dị ứng; Quản lý lịch hẹn khám, khung giờ và trạng thái lịch. |
| **4. Lâm sàng & Kê đơn** | `medical_records`<br>`prescriptions`<br>`prescription_items`<br>`medicines` | Quản lý hồ sơ phiếu khám (sinh hiệu, triệu chứng, mã ICD-10), đơn thuốc điện tử, chi tiết từng loại thuốc kê, và danh mục kho dược. |
| **5. Viện phí & Thanh toán** | `invoices` | Quản lý hóa đơn viện phí, chi phí khám, xét nghiệm, tiền thuốc, khấu trừ bảo hiểm BHYT và hình thức thanh toán (Tiền mặt/VietQR). |
| **6. Nhật ký & Kiểm toán** | `audit_logs`<br>`ai_invocation_logs` | Ghi vết mọi hành vi đọc/sửa hồ sơ bệnh nhân và ghi lại lịch sử gọi Trợ lý AI (Prompt ẩn danh, Response, Model, Độ trễ). |

### Bước 2: Chuẩn hóa Lược đồ Dữ liệu đạt Mức 3NF
1. **Chuẩn hóa 1NF (Atomic Values)**: Tất cả các cột dữ liệu đều là nguyên tử. Danh sách thuốc trong đơn thuốc được tách riêng thành bảng `prescription_items` thay vì lưu chuỗi JSON gộp.
2. **Chuẩn hóa 2NF (Full Functional Dependency)**: Mọi thuộc tính không khóa đều phụ thuộc toàn phần vào khóa chính. Bảng `prescription_items` có khóa ngoại trỏ tới `prescription_id` và `medicine_id`.
3. **Chuẩn hóa 3NF (No Transitive Dependency)**: Không có sự phụ thuộc bắc cầu. Bác sĩ liên kết với chuyên khoa qua `specialty_id` thay vì lưu trực tiếp tên chuyên khoa trong bảng `doctors`.

### Bước 3: Thiết lập Ràng buộc Khóa Ngoại và Toàn vẹn Dữ liệu
Sơ đồ quan hệ thực thể (ERD) với các ràng buộc khóa ngoại:

```
  +------------------+          +------------------+          +------------------+
  |   specialties    | 1      N |     clinics      | 1      N |  doctor_shifts   |
  |------------------|<---------|------------------|<---------|------------------|
  | id (PK)          |          | id (PK)          |          | id (PK)          |
  | code (UQ)        |          | specialty_id(FK) |          | doctor_id (FK)   |
  | name             |          | room_number(UQ)  |          | clinic_id (FK)   |
  +------------------+          +------------------+          | day_of_week      |
          ^                             ^                     | start_time, end  |
          | 1                           | 1                   +------------------+
          | N                           | N
  +------------------+          +------------------+          +------------------+
  |     doctors      | 1      N |   appointments   | 1      1 | medical_records  |
  |------------------|<---------|------------------|<---------|------------------|
  | id (PK)          |          | id (PK)          |          | id (PK)          |
  | user_id (FK, UQ) |          | patient_id (FK)  |          | appointment_idFK |
  | specialty_id(FK) |          | doctor_id (FK)   |          | patient_id (FK)  |
  | license_number   |          | clinic_id (FK)   |          | doctor_id (FK)   |
  +------------------+          | appointment_time |          | vitals, icd10    |
          ^                     | status           |          +------------------+
          | 1                   +------------------+                   | 1
          |                              ^                             |
  +------------------+                   | 1                           v 1
  |      users       |                   | N                  +------------------+
  |------------------|          +------------------+          |  prescriptions   |
  | id (PK)          |          |     patients     |          |------------------|
  | username (UQ)    |          |------------------|          | id (PK)          |
  | hashed_password  |          | id (PK)          |          | record_id(FK,UQ) |
  | role             |          | medical_code(UQ) |          | patient_id (FK)  |
  +------------------+          | full_name, cccd  |          | doctor_id (FK)   |
                                | phone, bhyt      |          +------------------+
                                +------------------+                   | 1
                                         | 1                           | N
                                         | N                           v
                                +------------------+          +--------------------+
                                |     invoices     |          | prescription_items |
                                |------------------|          |--------------------|
                                | id (PK)          |          | id (PK)            |
                                | patient_id (FK)  |          | prescription_id(FK)|
                                | record_id(FK,UQ) |          | medicine_id (FK)   |
                                | total_amount     |          | quantity, dosage   |
                                | status           |          +--------------------+
                                +------------------+                   | N
                                                                       | 1
                                                              +------------------+
                                                              |    medicines     |
                                                              |------------------|
                                                              | id (PK)          |
                                                              | code(UQ), name   |
                                                              | stock, unit_price|
                                                              +------------------+
```

### Bước 4: Chuẩn hóa Quy tắc Sinh Mã Định danh Nghiệp vụ
1. **Mã Bệnh nhân (`patients.medical_code`)**:
   - Định dạng: `BN-YYYYMMDD-XXXX` (VD: `BN-20260829-0001`).
   - Ràng buộc: `UNIQUE`, `NOT NULL`, `INDEXED`.
2. **Mã Phiếu khám (`medical_records.record_number`)**:
   - Định dạng: `PK-YYYYMMDD-XXXX`.
3. **Mã Hóa đơn (`invoices.invoice_number`)**:
   - Định dạng: `HD-YYYYMMDD-XXXX`.
4. **Mã Thuốc (`medicines.code`)**:
   - Định dạng: `TH-XXXX` (VD: `TH-PARA500`, `TH-AMOX500`).

### Bước 5: Thiết kế Chiến lược Đánh Chỉ mục (Indexing Strategy)
Chỉ mục được tối ưu hóa đặc thù cho các truy vấn thời gian thực của phòng khám:

1. **Composite Index phục vụ Conflict Detection**:
   ```sql
   CREATE INDEX idx_appointments_conflict_doctor 
   ON appointments (doctor_id, appointment_time, end_time, status);

   CREATE INDEX idx_appointments_conflict_clinic 
   ON appointments (clinic_id, appointment_time, end_time, status);
   ```
2. **Index phục vụ Tra cứu Bệnh nhân & Tiếp đón**:
   ```sql
   CREATE INDEX idx_patients_medical_code ON patients (medical_code);
   CREATE INDEX idx_patients_cccd ON patients (cccd);
   CREATE INDEX idx_patients_phone ON patients (phone);
   CREATE INDEX idx_patients_bhyt ON patients (bhyt);
   ```
3. **Index phục vụ Hàng đợi Bác sĩ & Kế toán**:
   ```sql
   CREATE INDEX idx_appointments_date_status ON appointments (appointment_time, status);
   CREATE INDEX idx_invoices_status_created ON invoices (status, created_at);
   ```

### Bước 6: Thiết kế Bảng Nhật ký Kiểm toán & Nhật ký AI
1. **Bảng `audit_logs`**:
   - Cột: `id`, `user_id` (FK `users.id`), `action` (READ, CREATE, UPDATE, DELETE), `target_table`, `target_id`, `details` (JSON), `ip_address`, `timestamp`.
2. **Bảng `ai_invocation_logs`**:
   - Cột: `id`, `user_id` (FK `users.id`), `feature` (pre_visit_summary, faq_chatbot, discharge_instructions), `anonymized_prompt` (Text), `response` (Text), `model` (String), `latency_ms` (Integer), `created_at` (DateTime).

### Bước 7: Lập Từ điển Dữ liệu (Data Dictionary) Hoàn chỉnh
Đặc tả chi tiết từng cột của 14 bảng trong tài liệu `docs/database-design.md` gồm: Tên cột, Kiểu dữ liệu, Nullable, Default, Khóa ngoại, Ràng buộc nghiệp vụ và Diễn giải ý nghĩa y tế.

---

## 5. Human-in-the-loop Governance (Cơ chế Kiểm soát Con người)

### 5.1. Thẩm định Schema
- Quản trị viên CSDL (DBA) và Kỹ sư Trưởng (Lead Backend Engineer) thẩm định bản thiết kế trước khi tiến hành viết mã ORM Models.

### 5.2. Danh mục Kiểm tra Thẩm định
- [ ] 1. Toàn bộ 14 bảng đều có khóa chính `id` và tuân thủ chuẩn 3NF.
- [ ] 2. Các ràng buộc UNIQUE trên `medical_code`, `username`, `email`, `cccd` được thiết lập chính xác.
- [ ] 3. Composite Indexes cho giải thuật xung đột lịch khám được cấu hình đầy đủ.
- [ ] 4. Bảng `audit_logs` và `ai_invocation_logs` sẵn sàng ghi nhận đầy đủ mọi tương tác nhạy cảm.

---

## 6. Business & Compliance Rules (Quy tắc Nghiệp vụ & Tuân thủ)

1. **Ràng buộc Tồn kho Thuốc**: Bảng `medicines` có ràng buộc kiểm tra `stock >= 0`. Không bao giờ cho phép số lượng tồn kho âm khi kê đơn thuốc.
2. **Ràng buộc Trạng thái Hóa đơn**: Trạng thái thanh toán của bảng `invoices` chỉ được nhận 1 trong 3 giá trị: `PENDING` (Chờ thanh toán), `PAID` (Đã thanh toán), `CANCELLED` (Đã hủy).
3. **Nguyên tắc Bất biến Bệnh án**: Sau khi phiếu khám (`medical_records`) được bác sĩ ký hoàn tất, dữ liệu chẩn đoán và sinh hiệu không được phép chỉnh sửa tùy tiện mà phải qua quy trình hiệu chỉnh có ghi log.

---

## 7. Expected Outputs & Deliverables (Tài liệu Đầu ra Bắt buộc)

1. `docs/database-design.md`: Tài liệu đặc tả CSDL toàn diện gồm Sơ đồ ERD, Data Dictionary 14 bảng, Chiến lược Index và Kịch bản Seed Data.
2. Tệp mã nguồn SQLAlchemy Models trong `backend/app/models/` phản ánh chính xác 100% bản thiết kế.

---

## 8. Verification & Quality Acceptance Criteria (Tiêu chí Nghiệm thu Chất lượng)

- **Tính Đúng đắn Toàn vẹn (Integrity Correctness)**: Chạy script khởi tạo bảng và chèn 1,000 bản ghi mẫu thành công không phát sinh lỗi ràng buộc khóa ngoại.
- **Hiệu năng Truy vấn (Query Performance)**: Thời gian thực thi câu truy vấn kiểm tra xung đột lịch khám trung bình < 5ms trên tập dữ liệu 50,000 lịch hẹn mẫu.
- **Tính Tương thích Đa CSDL (DB Portability)**: Mã nguồn ORM hoạt động tương thích 100% trên cả SQLite và PostgreSQL mà không cần sửa đổi câu lệnh truy vấn.
