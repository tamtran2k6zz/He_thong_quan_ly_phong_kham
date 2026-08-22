# TÀI LIỆU ĐẶC TẢ SDLC - GIAI ĐOẠN 1 (KT1)
## KHẢO SÁT BÀI TOÁN, PHÂN TÍCH YÊU CẦU & THIẾT KẾ KIẾN TRÚC HỆ THỐNG
### DỰ ÁN: HỆ THỐNG QUẢN LÝ PHÒNG KHÁM ĐA KHOA THÔNG MINH TÍCH HỢP TRỢ LÝ AI HÀNH CHÍNH
*(Clinic Management System with Administrative AI Assistant - CMS-AI)*

---

## 1. KHẢO SÁT BÀI TOÁN & MỤC TIÊU DỰ ÁN

### 1.1. Bối cảnh & Thực trạng Quản lý Phòng khám Đa khoa
Tại các phòng khám đa khoa quy mô vừa và lớn tại Việt Nam hiện nay, công tác vận hành thường gặp phải các điểm nghẽn nghiêm trọng sau:
1. **Ùn tắc khâu tiếp đón & Đặt lịch trùng lặp:** Việc ghi nhận lịch hẹn qua sổ sách hoặc bảng tính phân tán dẫn đến xung đột khung giờ của bác sĩ, chồng chéo phòng khám và kéo dài thời gian chờ đợi của người bệnh.
2. **Quá tải tài liệu & Đọc bệnh sử thủ công:** Bác sĩ mất từ 3 - 5 phút cho mỗi lượt khám chỉ để lật giở và tra cứu tiền sử bệnh, dị ứng thuốc từ các hồ sơ cũ, làm giảm thời lượng tư vấn chuyên môn trực tiếp.
3. **Sai sót trong kê đơn & Hướng dẫn sau khám:** Việc truyền đạt hướng dẫn uống thuốc, kiêng cữ dinh dưỡng sau khám bằng lời nói hoặc chữ viết tay dễ gây hiểu nhầm, bệnh nhân không tuân thủ phác đồ điều trị.
4. **Thất thoát viện phí & Chậm trễ thanh toán:** Sự thiếu đồng bộ dữ liệu giữa phòng khám và quầy thu ngân gây chậm trễ trong việc tổng hợp chi phí khám, xét nghiệm và tiền thuốc, tính toán sai tỷ lệ chi trả BHYT.
5. **Rủi ro rò rỉ dữ liệu nhạy cảm:** Thông tin định danh cá nhân (PII - Personally Identifiable Information) và bệnh án chưa được bảo vệ theo các tiêu chuẩn bảo mật y tế nghiêm ngặt.

### 1.2. Mục tiêu của Hệ thống CMS-AI
Hệ thống **CMS-AI** được xây dựng nhằm giải quyết triệt để các vấn đề trên thông qua:
- **Chuẩn hóa quy trình nghiệp vụ y tế khép kín:** Vận hành mạch lạc theo luồng: Đặt lịch -> Tiếp đón/Phát số -> Khám bệnh & Cận lâm sàng -> Kê đơn thuốc điện tử -> Trợ lý AI hỗ trợ -> Thu ngân & Xuất hóa đơn/VietQR.
- **Kiểm soát phân quyền nghiêm ngặt (RBAC):** Thiết lập 4 nhóm vai trò (*Quản trị viên, Lễ tân, Bác sĩ, Kế toán*) đảm bảo nguyên tắc đặc quyền tối thiểu (Least Privilege).
- **Tích hợp Trợ lý AI Hành chính phân tầng bảo mật:** Tự động hóa tóm tắt bệnh án (*Pre-visit Briefing*), giải đáp quy trình thủ tục (*FAQ Chatbot*) và sinh hướng dẫn sau khám (*Discharge Instructions*) mà **hoàn toàn không can thiệp vào chẩn đoán chuyên môn** của bác sĩ.
- **Bảo mật dữ liệu y tế & Khử định danh PII (De-identification):** Loại bỏ 100% thông tin cá nhân trước khi truyền dữ liệu qua lớp AI.

---

## 2. PHÂN TÍCH CÁC ACTOR & YÊU CẦU HỆ THỐNG

```
                             +--------------------------------------------------+
                             |           ACTORS IN CMS-AI SYSTEM                |
                             +--------------------------------------------------+
                               /              |               \              \
                              /               |                \              \
                             v                v                 v              v
                     +---------------+ +---------------+ +---------------+ +---------------+
                     | Quản trị viên | |     Lễ tân    | |     Bác sĩ    | |    Kế toán    |
                     |    (Admin)    | | (Receptionist)| |    (Doctor)   | |  (Accountant) |
                     +---------------+ +---------------+ +---------------+ +---------------+
```

### 2.1. Phân tích 4 Nhóm Vai trò (Actors)

| STT | Actor | Vai trò & Trách nhiệm chính trong hệ thống | Phạm vi quyền hạn nghiệp vụ |
|:---:|:---|:---|:---|
| **1** | **Quản trị viên (Admin)** | Quản trị toàn bộ hạ tầng phần mềm, phân quyền tài khoản, cấu hình danh mục y tế, giám sát bảo mật và theo dõi thống kê toàn viện. | - Quản lý tài khoản người dùng (CRUD, Reset pass, Phân quyền).<br>- Quản lý danh mục chuyên khoa, phòng khám, hồ sơ bác sĩ, ca làm việc.<br>- Quản lý danh mục thuốc và kho dược.<br>- Xem nhật ký kiểm toán (Audit Log) & Nhật ký gọi AI (AI Log).<br>- Xem báo cáo doanh thu, lưu lượng khám toàn diện. |
| **2** | **Lễ tân (Receptionist)** | Tiếp nhận người bệnh, điều phối luồng vào, quản lý lịch hẹn, cấp phát số thứ tự và giải đáp thắc mắc hành chính. | - Đăng ký hồ sơ bệnh nhân mới, tra cứu mã định danh y tế.<br>- Đặt lịch hẹn, đổi lịch, hủy lịch khám.<br>- Tiếp đón bệnh nhân, kiểm tra bảo hiểm y tế, phát số vào hàng đợi khám.<br>- Sử dụng Chatbot AI để tra cứu thủ tục, bảng giá, quy định phòng khám. |
| **3** | **Bác sĩ (Doctor)** | Tiếp nhận bệnh nhân theo hàng đợi, thăm khám lâm sàng, chỉ định cận lâm sàng, chẩn đoán ICD-10, kê đơn thuốc và dặn dò sau khám. | - Tiếp nhận danh sách chờ khám tại phòng của mình.<br>- Xem tóm tắt bệnh án do AI sinh (*Pre-visit Briefing*).<br>- Ghi nhận sinh hiệu, triệu chứng, chẩn đoán bệnh theo mã ICD-10.<br>- Chỉ định dịch vụ cận lâm sàng (xét nghiệm, siêu âm, X-quang).<br>- Kê đơn thuốc điện tử và sinh hướng dẫn điều trị xuất viện bằng AI. |
| **4** | **Kế toán / Thu ngân (Accountant)** | Tiếp nhận chỉ định thanh toán từ bác sĩ, tổng hợp chi phí, áp dụng chính sách BHYT, thực hiện thu viện phí và xuất biên lai. | - Tiếp nhận danh sách chờ thanh toán theo thời gian thực.<br>- Tính toán tổng chi phí (Khám + Cận lâm sàng + Đơn thuốc).<br>- Khấu trừ tỷ lệ chi trả của BHYT (80%, 100%).<br>- Xác nhận thanh toán qua Tiền mặt hoặc Mã VietQR tự động.<br>- In hóa đơn/phiếu thu viện phí chuẩn hóa. |

---

## 3. BIỂU ĐỒ USE CASE & LUỒNG NGHIỆP VỤ Y TẾ

### 3.1. Sơ đồ Use Case Tổng quát

```
+---------------------------------------------------------------------------------------------------+
|                               HỆ THỐNG QUẢN LÝ PHÒNG KHÁM (CMS-AI)                                 |
|                                                                                                   |
|  [Admin] ---------> (Đăng nhập JWT & Phân quyền RBAC)                                             |
|          ---------> (Quản lý Tài khoản & Danh mục Bác sĩ/Phòng/Thuốc)                             |
|          ---------> (Giám sát Audit Logs & AI Invocation Logs)                                    |
|          ---------> (Xem Báo cáo Thống kê & Doanh thu Quản trị)                                   |
|                                                                                                   |
|  [Lễ tân] --------> (Đăng ký Hồ sơ Bệnh nhân & Cấp mã BN-YYYYMMDD-XXXX)                           |
|           --------> (Đặt lịch hẹn & Kiểm tra Xung đột Lịch khám)                                  |
|           --------> (Tiếp đón & Đưa vào Hàng đợi Khám của Bác sĩ)                                 |
|           --------> (Tra cứu Thủ tục qua AI Workflow Chatbot)                                     |
|                                                                                                   |
|  [Bác sĩ] --------> (Xem Hàng đợi Bệnh nhân & Tóm tắt AI Pre-visit Briefing)                      |
|           --------> (Lập Phiếu khám: Sinh hiệu, Triệu chứng, ICD-10)                              |
|           --------> (Chỉ định Dịch vụ / Cận lâm sàng)                                             |
|           --------> (Kê đơn thuốc điện tử & Trừ tồn kho tự động)                                  |
|           --------> (Sinh Hướng dẫn sau khám AI Discharge Instructions)                           |
|                                                                                                   |
|  [Kế toán] -------> (Tổng hợp Viện phí & Tính khấu trừ BHYT)                                      |
|            -------> (Thực hiện Thu tiền: Tiền mặt / VietQR Chuyển khoản)                          |
|            -------> (In Biên lai / Hóa đơn Dịch vụ Y tế)                                          |
+---------------------------------------------------------------------------------------------------+
```

### 3.2. Luồng Nghiệp vụ Y tế Khép kín (End-to-End Clinical Flow)

```
[Bệnh nhân đến / Đặt lịch trước]
               |
               v
 [BƯỚC 1: LỄ TÂN] ----------------> Tạo/Tra cứu Hồ sơ bệnh nhân -> Đặt lịch (Kiểm tra xung đột)
                                    -> Tiếp đón, gán vào Hàng đợi phòng khám chuyên khoa
               |
               v
 [BƯỚC 2: BÁC SĨ] -----------------> Mở Hàng đợi -> Xem AI Pre-visit Summary (Lịch sử, dị ứng)
                                    -> Khám lâm sàng, đo sinh hiệu, chẩn đoán mã ICD-10
                                    -> Chỉ định cận lâm sàng (nếu có)
                                    -> Kê đơn thuốc điện tử
                                    -> Sinh dặn dò sau khám AI Discharge Instructions
               |
               v
 [BƯỚC 3: KẾ TOÁN] ----------------> Tiếp nhận hồ sơ khám hoàn tất -> Kiểm tra bảo hiểm BHYT
                                    -> Tổng hợp chi phí viện phí & khấu trừ bảo hiểm
                                    -> Thu tiền (Tiền mặt / Quét mã VietQR)
                                    -> In Phiếu thu / Hóa đơn viện phí
               |
               v
 [BƯỚC 4: HOÀN TẤT] ---------------> Bệnh nhân nhận thuốc, hóa đơn và hướng dẫn chăm sóc xuất viện
```

---

## 4. THIẾT KẾ CƠ SỞ DỮ LIỆU QUAN HỆ (RELATIONAL DATABASE DESIGN)

Hệ thống được thiết kế chuẩn hóa bậc 3 (3NF) với **14 bảng quan hệ** quản lý toàn diện mọi mặt hoạt động của phòng khám.

### 4.1. Sơ đồ Quan hệ Thực thể (Entity Relationship Diagram - ERD)

```
  +------------------+          +------------------+          +------------------+
  |   specialties    | 1      N |     clinics      | 1      N |  doctor_shifts   |
  |------------------|<---------|------------------|<---------|------------------|
  | id (PK)          |          | id (PK)          |          | id (PK)          |
  | code, name, desc |          | specialty_id(FK) |          | doctor_id (FK)   |
  +------------------+          | room_number, name|          | clinic_id (FK)   |
          ^                     +------------------+          | day_of_week, time|
          | 1                            ^                    +------------------+
          |                              | 1                           |
          | N                            | N                           |
  +------------------+          +------------------+                   |
  |     doctors      | 1      N |   appointments   |                   |
  |------------------|<---------|------------------|                   |
  | id (PK)          |          | id (PK)          |                   |
  | user_id (FK)     |          | patient_id (FK)  |                   |
  | specialty_id(FK) |          | doctor_id (FK)   |                   |
  | license_number   |          | clinic_id (FK)   |                   |
  +------------------+          | appointment_time |                   |
          | 1                   | status           |                   |
          |                     +------------------+                   |
          | 1                            ^                             |
  +------------------+                   | 1                           |
  |      users       |                   |                             |
  |------------------|                   |                             |
  | id (PK)          |                   | N                           |
  | username, email  |          +------------------+                   |
  | hashed_password  |          |     patients     |                   |
  | role, is_active  |          |------------------|                   |
  +------------------+          | id (PK)          |                   |
          | 1                   | medical_code(UQ) |                   |
          |                     | full_name, dob   |                   |
          | N                   | phone, cccd, bhyt|                   |
  +------------------+          | allergies, history|                  |
  |    audit_logs    |          +------------------+                   |
  |------------------|                   ^                             |
  | id (PK)          |                   | 1                           |
  | user_id (FK)     |                   |                             |
  | action, entity   |                   | N                           |
  | ip_address, time |          +------------------+                   |
  +------------------+          | medical_records  | 1       N         |
                                |------------------|-------------------+
                                | id (PK)          |
                                | patient_id (FK)  |
                                | doctor_id (FK)   |
                                | appointment_id   |
                                | icd10_code, diag |
                                | pulse, bp, temp  |
                                | ai_summary, note |
                                +------------------+
                                    | 1         | 1
                                    |           +----------------------+
                                    | N                                | 1
                          +--------------------+             +--------------------+
                          |   service_orders   |             |   prescriptions    |
                          |--------------------|             |--------------------|
                          | id (PK)            |             | id (PK)            |
                          | record_id (FK)     |             | record_id (FK)     |
                          | service_name, price|             | doctor_id (FK)     |
                          +--------------------+             | patient_id (FK)    |
                                    |                        | ai_instructions    |
                                    |                        +--------------------+
                                    |                                  | 1
                                    |                                  | N
                                    |                        +--------------------+
                                    |                        | prescription_items |
                                    |                        |--------------------|
                                    |                        | id (PK)            |
                                    |                        | prescription_id(FK)|
                                    |                        | medicine_id (FK)   |
                                    |                        | quantity, dosage   |
                                    |                        +--------------------+
                                    |                                  | N
                                    |                                  | 1
                                    |                        +--------------------+
                                    |                        |     medicines      |
                                    |                        |--------------------|
                                    |                        | id (PK)            |
                                    |                        | code, name, unit   |
                                    |                        | stock_quantity     |
                                    |                        | unit_price         |
                                    |                        +--------------------+
                                    |                                  |
                                    v N                                v N
                                +------------------------------------------+
                                |                 invoices                 |
                                |------------------------------------------|
                                | id (PK)                                  |
                                | record_id (FK, UQ)                       |
                                | patient_id (FK)                          |
                                | total_amount, bhyt_discount              |
                                | final_amount, status, payment_method     |
                                +------------------------------------------+
```

---

### 4.2. Từ điển Dữ liệu Chi tiết (Data Dictionary)

#### 1. Bảng `users` (Tài khoản người dùng hệ thống)
| Tên trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| `id` | INTEGER | PK, Auto Increment | Khóa chính |
| `username` | VARCHAR(50) | UNIQUE, NOT NULL | Tên đăng nhập |
| `email` | VARCHAR(100) | UNIQUE, NOT NULL | Email liên lạc |
| `hashed_password` | VARCHAR(255) | NOT NULL | Mật khẩu băm (Bcrypt) |
| `full_name` | VARCHAR(100) | NOT NULL | Họ và tên nhân viên |
| `role` | VARCHAR(20) | NOT NULL | Vai trò: `admin`, `receptionist`, `doctor`, `accountant` |
| `is_active` | BOOLEAN | DEFAULT TRUE | Trạng thái hoạt động |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Thời gian tạo tài khoản |

#### 2. Bảng `specialties` (Chuyên khoa khám bệnh)
| Tên trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| `id` | INTEGER | PK, Auto Increment | Khóa chính |
| `code` | VARCHAR(20) | UNIQUE, NOT NULL | Mã chuyên khoa (ví dụ: `NOI`, `TIM`, `NHI`) |
| `name` | VARCHAR(100) | NOT NULL | Tên chuyên khoa (Tim mạch, Nhi khoa, v.v.) |
| `description` | TEXT | NULL | Mô tả chi tiết chuyên khoa |

#### 3. Bảng `clinics` (Phòng khám / Buồng khám)
| Tên trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| `id` | INTEGER | PK, Auto Increment | Khóa chính |
| `room_number` | VARCHAR(20) | UNIQUE, NOT NULL | Số phòng khám (ví dụ: `P.101`, `P.202`) |
| `name` | VARCHAR(100) | NOT NULL | Tên buồng khám |
| `specialty_id` | INTEGER | FK -> `specialties.id` | Thuộc chuyên khoa nào |
| `is_active` | BOOLEAN | DEFAULT TRUE | Trạng thái phòng khả dụng |

#### 4. Bảng `doctors` (Thông tin hồ sơ bác sĩ)
| Tên trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| `id` | INTEGER | PK, Auto Increment | Khóa chính |
| `user_id` | INTEGER | FK -> `users.id`, UNIQUE | Liên kết tài khoản đăng nhập |
| `specialty_id` | INTEGER | FK -> `specialties.id` | Chuyên khoa chuyên trách |
| `license_number` | VARCHAR(50) | UNIQUE, NOT NULL | Số chứng chỉ hành nghề y |
| `title` | VARCHAR(50) | NOT NULL | Học hàm/học vị (BS, ThS.BS, BS.CKII) |
| `consultation_fee` | NUMERIC(12,2)| NOT NULL | Giá khám niêm yết của bác sĩ (VNĐ) |

#### 5. Bảng `doctor_shifts` (Ca làm việc & Lịch trực)
| Tên trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| `id` | INTEGER | PK, Auto Increment | Khóa chính |
| `doctor_id` | INTEGER | FK -> `doctors.id` | Bác sĩ trực |
| `clinic_id` | INTEGER | FK -> `clinics.id` | Buồng khám trực |
| `day_of_week` | INTEGER | NOT NULL (0-6) | Thứ trong tuần (0: Thứ 2 ... 6: Chủ nhật) |
| `start_time` | TIME | NOT NULL | Giờ bắt đầu ca trực |
| `end_time` | TIME | NOT NULL | Giờ kết thúc ca trực |

#### 6. Bảng `patients` (Hồ sơ bệnh nhân)
| Tên trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| `id` | INTEGER | PK, Auto Increment | Khóa chính |
| `medical_code` | VARCHAR(30) | UNIQUE, NOT NULL | Mã y tế định danh (`BN-YYYYMMDD-XXXX`) |
| `full_name` | VARCHAR(100) | NOT NULL | Họ và tên bệnh nhân |
| `date_of_birth` | DATE | NOT NULL | Ngày tháng năm sinh |
| `gender` | VARCHAR(10) | NOT NULL | Giới tính (`Nam`, `Nữ`, `Khác`) |
| `phone_number` | VARCHAR(20) | NOT NULL | Số điện thoại liên lạc |
| `cccd_number` | VARCHAR(20) | NULL | Số CCCD/CMND 12 chữ số |
| `bhyt_number` | VARCHAR(25) | NULL | Mã thẻ BHYT (15 ký tự) |
| `address` | VARCHAR(255) | NULL | Địa chỉ cư trú |
| `drug_allergies` | TEXT | NULL | Tiền sử dị ứng thuốc nghiêm trọng |
| `medical_history`| TEXT | NULL | Bệnh sử gia đình & bệnh mạn tính |

#### 7. Bảng `appointments` (Lịch hẹn khám bệnh)
| Tên trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| `id` | INTEGER | PK, Auto Increment | Khóa chính |
| `patient_id` | INTEGER | FK -> `patients.id` | Bệnh nhân đặt khám |
| `doctor_id` | INTEGER | FK -> `doctors.id` | Bác sĩ được chỉ định khám |
| `clinic_id` | INTEGER | FK -> `clinics.id` | Phòng khám tiếp nhận |
| `appointment_time`| TIMESTAMP | NOT NULL | Thời điểm khám |
| `duration_minutes`| INTEGER | DEFAULT 30 | Thời lượng dự kiến ca khám |
| `symptoms` | TEXT | NULL | Triệu chứng ban đầu khi đăng ký |
| `status` | VARCHAR(20) | NOT NULL | `PENDING`, `CONFIRMED`, `CHECKED_IN`, `COMPLETED`, `CANCELLED` |
| `queue_number` | INTEGER | NULL | Số thứ tự phát trong ngày |

#### 8. Bảng `medical_records` (Phiếu khám bệnh / Lượt khám)
| Tên trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| `id` | INTEGER | PK, Auto Increment | Khóa chính |
| `patient_id` | INTEGER | FK -> `patients.id` | Bệnh nhân |
| `doctor_id` | INTEGER | FK -> `doctors.id` | Bác sĩ phụ trách |
| `appointment_id` | INTEGER | FK -> `appointments.id`, NULL | Lịch hẹn liên quan (nếu có) |
| `pulse` | INTEGER | NULL | Mạch (lần/phút) |
| `blood_pressure` | VARCHAR(20) | NULL | Huyết áp (mmHg, ví dụ `120/80`) |
| `temperature` | NUMERIC(4,1) | NULL | Thân nhiệt (°C) |
| `respiratory_rate`| INTEGER | NULL | Nhịp thở (lần/phút) |
| `weight` | NUMERIC(5,2) | NULL | Cân nặng (kg) |
| `height` | NUMERIC(5,2) | NULL | Chiều cao (cm) |
| `symptoms` | TEXT | NOT NULL | Triệu chứng thực thể |
| `icd10_code` | VARCHAR(10) | NOT NULL | Mã bệnh theo chuẩn ICD-10 (ví dụ `I10`) |
| `diagnosis` | TEXT | NOT NULL | Chẩn đoán xác định của bác sĩ |
| `doctor_notes` | TEXT | NULL | Ghi chú dặn dò của bác sĩ |
| `ai_pre_summary` | TEXT | NULL | Tóm tắt hồ sơ do AI sinh trước khám |
| `status` | VARCHAR(20) | NOT NULL | `IN_PROGRESS`, `WAITING_TESTS`, `COMPLETED`, `CANCELLED` |

#### 9. Bảng `service_orders` (Chỉ định dịch vụ / Cận lâm sàng)
| Tên trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| `id` | INTEGER | PK, Auto Increment | Khóa chính |
| `record_id` | INTEGER | FK -> `medical_records.id` | Thuộc phiếu khám nào |
| `service_name` | VARCHAR(100) | NOT NULL | Tên dịch vụ (Xét nghiệm máu, Siêu âm, v.v.) |
| `price` | NUMERIC(12,2)| NOT NULL | Đơn giá niêm yết (VNĐ) |
| `results` | TEXT | NULL | Kết quả cận lâm sàng trả về |
| `status` | VARCHAR(20) | NOT NULL | `PENDING`, `COMPLETED`, `CANCELLED` |

#### 10. Bảng `medicines` (Danh mục thuốc & Kho dược)
| Tên trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| `id` | INTEGER | PK, Auto Increment | Khóa chính |
| `code` | VARCHAR(30) | UNIQUE, NOT NULL | Mã thuốc quốc gia |
| `name` | VARCHAR(100) | NOT NULL | Tên thương mại / Hoạt chất |
| `active_ingredient`| VARCHAR(100)| NULL | Hoạt chất chính |
| `dosage_form` | VARCHAR(50) | NOT NULL | Dạng bào chế (Viên nén, Dung dịch, v.v.) |
| `unit` | VARCHAR(20) | NOT NULL | Đơn vị tính (Viên, Hộp, Chai, Vỉ) |
| `unit_price` | NUMERIC(12,2)| NOT NULL | Đơn giá bán lẻ (VNĐ) |
| `stock_quantity` | INTEGER | NOT NULL, >= 0 | Số lượng khả dụng trong kho |

#### 11. Bảng `prescriptions` (Đơn thuốc điện tử)
| Tên trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| `id` | INTEGER | PK, Auto Increment | Khóa chính |
| `record_id` | INTEGER | FK -> `medical_records.id`, UNIQUE | Thuộc phiếu khám nào |
| `doctor_id` | INTEGER | FK -> `doctors.id` | Bác sĩ kê đơn |
| `patient_id` | INTEGER | FK -> `patients.id` | Bệnh nhân nhận đơn |
| `notes` | TEXT | NULL | Lời dặn tổng quát của bác sĩ |
| `ai_discharge_instructions`| TEXT | NULL | Hướng dẫn xuất viện do AI tự động sinh |

#### 12. Bảng `prescription_items` (Chi tiết thuốc trong đơn)
| Tên trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| `id` | INTEGER | PK, Auto Increment | Khóa chính |
| `prescription_id`| INTEGER | FK -> `prescriptions.id` | Thuộc đơn thuốc nào |
| `medicine_id` | INTEGER | FK -> `medicines.id` | Thuốc được kê |
| `quantity` | INTEGER | NOT NULL, > 0 | Số lượng cấp |
| `dosage` | VARCHAR(100) | NOT NULL | Liều dùng (ví dụ: `1 viên/lần, 2 lần/ngày`) |
| `instructions` | VARCHAR(255) | NOT NULL | Cách dùng (Uống sau ăn sáng/tối) |

#### 13. Bảng `invoices` (Hóa đơn & Viện phí)
| Tên trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| `id` | INTEGER | PK, Auto Increment | Khóa chính |
| `record_id` | INTEGER | FK -> `medical_records.id`, UNIQUE | Thuộc lượt khám nào |
| `patient_id` | INTEGER | FK -> `patients.id` | Người thanh toán |
| `consultation_amount`| NUMERIC(12,2)| NOT NULL | Tiền công khám bác sĩ |
| `services_amount`| NUMERIC(12,2)| NOT NULL | Tổng tiền xét nghiệm / cận lâm sàng |
| `medicines_amount`| NUMERIC(12,2)| NOT NULL | Tổng tiền thuốc |
| `total_amount` | NUMERIC(12,2)| NOT NULL | Tổng chi phí trước bảo hiểm |
| `bhyt_discount` | NUMERIC(12,2)| DEFAULT 0.00 | Số tiền BHYT chi trả |
| `final_amount` | NUMERIC(12,2)| NOT NULL | Số tiền bệnh nhân thực tế thanh toán |
| `status` | VARCHAR(20) | NOT NULL | `UNPAID`, `PAID`, `CANCELLED` |
| `payment_method`| VARCHAR(20) | NULL | `CASH`, `BANK_TRANSFER`, `CREDIT_CARD` |
| `paid_at` | TIMESTAMP | NULL | Thời điểm thanh toán thành công |

#### 14. Bảng `audit_logs` & `ai_invocation_logs` (Nhật ký kiểm toán & Giám sát AI)
| Tên trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| `id` | INTEGER | PK, Auto Increment | Khóa chính |
| `user_id` | INTEGER | FK -> `users.id`, NULL | Người thực hiện hành động |
| `action` | VARCHAR(50) | NOT NULL | Loại hành động: `CREATE_RECORD`, `VIEW_PATIENT`, `CALL_AI` |
| `entity_type` | VARCHAR(50) | NOT NULL | Thực thể bị tác động (`Patient`, `Prescription`, v.v.) |
| `entity_id` | INTEGER | NULL | ID thực thể |
| `ip_address` | VARCHAR(45) | NULL | Địa chỉ IP của client |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Thời điểm ghi log |
| `prompt_redacted`| TEXT | NULL (AI log) | Nội dung prompt sau khi đã khử định danh PII |
| `ai_response` | TEXT | NULL (AI log) | Phản hồi từ mô hình AI |
| `model_used` | VARCHAR(50) | NULL (AI log) | Tên mô hình (`mock`, `llama3`, `gemini-1.5-flash`) |
| `latency_ms` | INTEGER | NULL (AI log) | Thời gian phản hồi tính bằng mili-giây |

---

## 5. RANH GIỚI ĐẠO ĐỨC AI & QUẢN TRỊ DỮ LIỆU Y TẾ

### 5.1. Phân tích Rủi ro Đạo đức Trí tuệ Nhân tạo trong Y tế
Việc tích hợp Trí tuệ nhân tạo (AI) vào môi trường chăm sóc sức khỏe mang lại hiệu quả vượt bậc nhưng cũng tiềm ẩn các rủi ro nguy hiểm:
1. **Rủi ro Ảo giác Y khoa (Medical Hallucination):** Mô hình ngôn ngữ lớn (LLM) có thể tự suy diễn ra các chẩn đoán sai lệch hoặc phác đồ điều trị nguy hiểm không có căn cứ y học thực nghiệm.
2. **Xâm phạm Quyền riêng tư & Rò rỉ Thông tin Cá nhân:** Dữ liệu bệnh án chứa thông tin định danh cá nhân nhạy cảm (CCCD, SĐT, Địa chỉ, Bệnh sử) có nguy cơ bị rò rỉ nếu truyền tải trực tiếp tới các máy chủ AI đám mây bên thứ ba.
3. **Đùn đẩy Trách nhiệm Pháp lý:** Nguy cơ nhân viên y tế phụ thuộc hoàn toàn vào gợi ý tự động của AI dẫn đến sai sót chuyên môn nghiêm trọng.

### 5.2. Các Nguyên tắc Quản trị & Hàng rào Bảo vệ (Guardrails) của CMS-AI
Nhằm đảm bảo an toàn tuyệt đối, hệ thống CMS-AI tuân thủ 4 nguyên tắc bất di bất dịch:

```
[DỮ LIỆU BỆNH NHÂN GỐC]
         |
         v
[LỚP 1: PII DE-IDENTIFICATION] --------> Loại bỏ Họ tên, CCCD, SĐT, Địa chỉ, BHYT bằng Regex/Token
         |
         v
[LỚP 2: SYSTEM GUARDRAILS] -----------> Chặn Prompt Injection, Chặn yêu cầu chẩn đoán bệnh học
         |
         v
[LỚP 3: AI PROVIDER] -----------------> Xử lý tóm tắt / dặn dò (Mock, Ollama, Gemini)
         |
         v
[LỚP 4: MEDICAL DISCLAIMER] ----------> Bắt buộc đính kèm Tuyên bố miễn trừ trách nhiệm y tế
```

1. **Khử định danh PII Tuyệt đối (Zero PII to AI):**
   Mọi thông tin định danh cá nhân đều được thay thế bằng các token ẩn danh (`[PATIENT_NAME_REDACTED]`, `[CCCD_REDACTED]`, `[PHONE_REDACTED]`) trước khi payload được chuyển tới bất kỳ mô hình AI nào.
2. **Ranh giới Phi chẩn đoán (Non-Diagnostic Guardrail):**
   AI chỉ đóng vai trò **Trợ lý Hành chính** (Tóm tắt bệnh sử có sẵn, Dặn dò chế độ ăn uống/uống thuốc theo y lệnh bác sĩ, Giải đáp quy trình đặt lịch). AI bị **nghiêm cấm tuyệt đối** việc đưa ra kết luận chẩn đoán bệnh học mới hoặc tự ý kê đơn thuốc.
3. **Bắt buộc Tuyên bố Miễn trừ Trách nhiệm Y tế (Mandatory Medical Disclaimer):**
   Mọi kết quả do AI sinh ra trên giao diện người dùng và phiếu in đều đính kèm thông báo pháp lý bắt buộc:
   > *"TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y TẾ: Nội dung này được tạo tự động bởi Trợ lý AI Hành chính chỉ nhằm mục đích tham khảo và hỗ trợ thông tin. AI không có chức năng chẩn đoán, điều trị hay thay thế quyết định chuyên môn của Bác sĩ điều trị."*
4. **Trách nhiệm Quyết định Cuối cùng thuộc về Bác sĩ (Human-in-the-Loop):**
   Toàn bộ nội dung dặn dò sau khám do AI gợi ý đều phải được Bác sĩ trực tiếp đọc duyệt, chỉnh sửa (nếu cần) và ký xác nhận trước khi lưu vào hệ thống hoặc gửi cho bệnh nhân.
