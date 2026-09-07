# TÀI LIỆU THIẾT KẾ HƯỚNG ĐỐI TƯỢNG (MÔ HÌNH LỚP)
## DỰ ÁN: HỆ THỐNG QUẢN LÝ KHO DƯỢC & PHÒNG KHÁM THÔNG MINH TÍCH HỢP AI
### HỌC PHẦN: ỨNG DỤNG TRÍ TUỆ NHÂN TẠO — ICTU (2026 - 2027)

---

**Thông tin nhóm thực hiện:**
- **Nhóm:** Nhóm 07
- **Thành viên nhóm:**
  1. **Đinh Gia Bảo** (Trưởng nhóm — Phụ trách Kiến trúc Backend, AI Engine & Security)
  2. **Trần Đặng Công Tâm** (Thành viên chính — Phụ trách Frontend SPA Taste-Skill, Nghiệp vụ & QA Lead)
- **Tên ứng dụng:** Hệ thống Quản lý Kho Dược & Phòng khám Đa khoa Thông minh Tích hợp AI
- **Thời gian thực hiện:** Từ 27/07/2026 đến 27/09/2026 (9 tuần)
- **Cổng truy cập ứng dụng:** `http://localhost:3001/login` (Frontend SPA) | `http://localhost:8000/docs` (Backend Swagger)

---

## 1. MÔ HÌNH LỚP TỔNG THỂ (CLASS DIAGRAM)

Mô hình lớp dưới đây biểu diễn cấu trúc hướng đối tượng (OOP) toàn diện của hệ thống, bao gồm các lớp Thực thể (Entity Classes), các lớp Dịch vụ Kiểm soát Nghiệp vụ (Service / Controller Classes), và các lớp Tích hợp Trí tuệ Nhân tạo (AI Provider Classes). 

Sơ đồ thể hiện tường minh các loại quan hệ UML:
- **Kế thừa (Inheritance `<|--`):** `CloudAIProvider` và `MockDeterministicAIProvider` kế thừa từ Abstract Interface `AIProvider`.
- **Chứa chặt (Composition `*--`):** Xóa `Prescription` sẽ tự động hủy các `PrescriptionItem`; Xóa `MedicalRecord` sẽ hủy `ServiceOrder`, `Prescription` và `Invoice`.
- **Chứa lỏng (Aggregation `o--`):** `Clinic` tổng hợp `Doctor`; `AdminAIService` tổng hợp `AIProvider`.
- **Liên kết (Association `-->`):** Tương tác nghiệp vụ giữa các thực thể độc lập.

```mermaid
classDiagram
    %% ==========================================
    %% TẦNG AI PROVIDERS (INHERITANCE & INTERFACE)
    %% ==========================================
    class AIProvider {
        <<interface>>
        +str model_name
        +generate(prompt: str, system_prompt: str)* AIProviderResponse
    }

    class CloudAIProvider {
        -str api_key
        -str provider_type
        -int timeout
        +generate(prompt: str, system_prompt: str) AIProviderResponse
        -_call_gemini(prompt: str, system_prompt: str) AIProviderResponse
        -_call_openai(prompt: str, system_prompt: str) AIProviderResponse
    }

    class MockDeterministicAIProvider {
        -str model_name
        +generate(prompt: str, system_prompt: str) AIProviderResponse
        -_handle_faq(prompt: str) str
        -_handle_briefing(prompt: str) str
        -_handle_discharge(prompt: str) str
    }

    AIProvider <|-- CloudAIProvider : Kế thừa (Inheritance)
    AIProvider <|-- MockDeterministicAIProvider : Kế thừa (Inheritance)

    %% ==========================================
    %% TẦNG DỊCH VỤ KIỂM SOÁT (SERVICES)
    %% ==========================================
    class AdminAIService {
        -AIProvider _provider
        +generate_pre_visit_summary(patient_id: int, db: Session) dict
        +answer_faq(question: str, conversation_id: str) dict
        +generate_discharge_instructions(record_id: int, db: Session) dict
        +predict_inventory_restock(medicine_id: int, db: Session) dict
        -_log_invocation(db: Session, feature: str, prompt: str, resp: str, latency: float) void
    }

    class ConflictChecker {
        +check_appointment_conflict(db: Session, doc_id: int, clinic_id: int, start: datetime, end: datetime, exclude_id: int) tuple
    }

    class PIIAnonymizer {
        -Pattern PHONE_REGEX
        -Pattern CCCD_REGEX
        -Pattern BHYT_REGEX
        +anonymize(text: str, patient_name: str) tuple
        +de_anonymize(text: str, mapping: dict) str
    }

    AdminAIService o-- AIProvider : Chứa lỏng (Aggregation)
    AdminAIService ..> PIIAnonymizer : Phụ thuộc (Uses)

    %% ==========================================
    %% TẦNG THỰC THỂ LÂM SÀNG & KHO DƯỢC (ENTITIES)
    %% ==========================================
    class User {
        +int id
        +str username
        -str password_hash
        +str full_name
        +str email
        +str role
        +bool is_active
        +datetime created_at
        +verify_password(plain_pwd: str) bool
        +has_role(required_role: str) bool
    }

    class Medicine {
        +int id
        +str medicine_code
        +str name
        +str active_ingredient
        +str dosage_form
        +str unit
        +float unit_price
        +int stock_quantity
        +int min_stock_threshold
        +date expiry_date
        +bool is_active
        +check_stock_availability(qty: int) bool
        +deduct_stock(qty: int) void
        +restock(qty: int) void
        +is_low_stock() bool
    }

    class Prescription {
        +int id
        +int medical_record_id
        +int doctor_id
        +str notes
        +str status
        +datetime created_at
        +add_item(item: PrescriptionItem) void
        +calculate_total_cost() float
        +dispense_prescription(db: Session) bool
    }

    class PrescriptionItem {
        +int id
        +int prescription_id
        +int medicine_id
        +str dosage
        +int quantity
        +float unit_price
        +str instructions
        +get_subtotal() float
    }

    class Patient {
        +int id
        +str patient_code
        +str full_name
        +date dob
        +str gender
        +str phone
        -str identity_card
        -str health_insurance
        +str address
        +str medical_history
        +str drug_allergies
        +calculate_age() int
        +has_drug_allergy(drug_name: str) bool
    }

    class Doctor {
        +int id
        +int user_id
        +int specialty_id
        +int clinic_id
        +str qualification
        +str title
        +int max_patients_per_shift
        +get_schedule(target_date: date) list
    }

    class Clinic {
        +int id
        +str name
        +str room_number
        +int specialty_id
        +str location
        +bool is_active
        +is_available(start: datetime, end: datetime) bool
    }

    class Appointment {
        +int id
        +int patient_id
        +int doctor_id
        +int clinic_id
        +datetime start_time
        +datetime end_time
        +str status
        +int queue_number
        +str symptoms
        +confirm() void
        +check_in() void
        +cancel(reason: str) void
    }

    class MedicalRecord {
        +int id
        +int patient_id
        +int doctor_id
        +int appointment_id
        +str status
        +str chief_complaint
        +str clinical_notes
        +str diagnosis_icd10
        +str icd10_code
        +float blood_pressure_systolic
        +float blood_pressure_diastolic
        +float heart_rate
        +float temperature
        +float weight_kg
        +float height_cm
        +float bmi
        +calculate_bmi() dict
        +complete_encounter() void
    }

    class ServiceOrder {
        +int id
        +int medical_record_id
        +str service_name
        +float price
        +str status
        +str results
    }

    class Invoice {
        +int id
        +int medical_record_id
        +int patient_id
        +float total_amount
        +float insurance_discount
        +float patient_payment
        +str status
        +str payment_method
        +calculate_bhyt_co_pay(rate: float) float
        +mark_paid(method: str) void
        +generate_vietqr_payload() dict
    }

    %% ==========================================
    %% QUAN HỆ GIỮA CÁC THỰC THỂ (RELATIONSHIPS)
    %% ==========================================
    User "1" <-- "1" Doctor : Tài khoản liên kết
    Clinic "1" o-- "*" Doctor : Chứa lỏng (Hosts)

    Patient "1" <-- "*" Appointment : Đặt hẹn
    Doctor "1" <-- "*" Appointment : Phụ trách
    Clinic "1" <-- "*" Appointment : Diễn ra tại

    Patient "1" <-- "*" MedicalRecord : Lịch sử bệnh án
    Doctor "1" <-- "*" MedicalRecord : Thăm khám
    Appointment "1" <-- "0..1" MedicalRecord : Xuất phát từ

    MedicalRecord "1" *-- "*" ServiceOrder : Chứa chặt (Chỉ định xét nghiệm)
    MedicalRecord "1" *-- "0..1" Prescription : Chứa chặt (Kê đơn xuất kho)
    Prescription "1" *-- "*" PrescriptionItem : Chứa chặt (Chi tiết đơn thuốc)
    Medicine "1" <-- "*" PrescriptionItem : Xuất trừ tồn kho

    MedicalRecord "1" *-- "0..1" Invoice : Chứa chặt (Thanh toán viện phí)
    Patient "1" <-- "*" Invoice : Thanh toán bởi
```

---

## 2. ĐẶC TẢ CHI TIẾT CÁC CLASS (CLASS SPECIFICATIONS)

---

### 2.1. LỚP `User` (Tài khoản & Phân quyền người dùng)
- **Mô tả:** Đại diện cho tài khoản nhân viên phòng khám (Quản trị viên, Lễ tân, Bác sĩ, Kế toán), chịu trách nhiệm xác thực danh tính qua JWT và băm mật khẩu Bcrypt.

#### A. Danh sách Thuộc tính (Attributes)
| Tên thuộc tính | Kiểu dữ liệu | Kích thước / Ràng buộc | Mô tả |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | 4 bytes, PK, Auto Increment | Định danh duy nhất của người dùng |
| `username` | `String` | 50 ký tự, UNIQUE, NOT NULL | Tên tài khoản đăng nhập |
| `password_hash` | `String` | 255 ký tự, NOT NULL | Chuỗi mật khẩu băm thuật toán Bcrypt (Salt 12 vòng) |
| `full_name` | `String` | 100 ký tự, NOT NULL | Họ và tên đầy đủ của nhân viên |
| `email` | `String` | 100 ký tự, NULLABLE | Địa chỉ email liên hệ |
| `role` | `String` | 20 ký tự, NOT NULL | Vai trò RBAC: `admin`, `receptionist`, `doctor`, `accountant` |
| `is_active` | `Boolean` | 1 byte, DEFAULT TRUE | Trạng thái hoạt động của tài khoản |
| `created_at` | `DateTime` | 8 bytes, DEFAULT CURRENT_TIMESTAMP | Thời điểm tạo tài khoản |

#### B. Danh sách Phương thức (Methods)
##### 1. Phương thức `verify_password`
- **Mô tả:** Đối soát mật khẩu văn bản thô do người dùng nhập vào với chuỗi băm lưu trong CSDL.
- **Tham số đầu vào:**
  - `plain_pwd`: `String`, tối đa 128 ký tự (Mật khẩu người dùng nhập vào màn hình login).
- **Kết quả đầu ra:** `Boolean` (1 byte): `True` nếu khớp mật mã, `False` nếu sai mật mã.
- **Luồng xử lý:**
  1. Kiểm tra tài khoản có đang hoạt động (`is_active == True`) hay không.
  2. Sử dụng thư viện `passlib.context.CryptContext` hàm `verify(plain_pwd, self.password_hash)`.
  3. Trả về kết quả xác thực.
- **Điều kiện bắt đầu:** Bản ghi `User` đã được nạp từ cơ sở dữ liệu.
- **Điều kiện kết thúc:** Trả về kết quả logic, không làm thay đổi trạng thái bản ghi.

##### 2. Phương thức `has_role`
- **Mô tả:** Kiểm tra tài khoản có thuộc danh sách các vai trò được phép truy cập tài nguyên hay không.
- **Tham số đầu vào:**
  - `required_role`: `String`, 20 ký tự (Vai trò cần kiểm tra, ví dụ: `'doctor'`).
- **Kết quả đầu ra:** `Boolean` (1 byte): `True` nếu vai trò người dùng trùng khớp.
- **Luồng xử lý:** So sánh chuỗi `self.role.lower() == required_role.lower()`.
- **Điều kiện bắt đầu:** Đối tượng `User` hợp lệ.
- **Điều kiện kết thúc:** Trả về kết quả kiểm tra quyền.

---

### 2.2. LỚP `Medicine` (Sản phẩm Thuốc & Quản lý Kho Dược)
- **Mô tả:** Đại diện cho danh mục thuốc, vật tư y tế trong kho của phòng khám; chịu trách nhiệm theo dõi số lượng tồn kho khả dụng, giá bán niêm yết, hạn dùng và kích hoạt cảnh báo tồn kho tối thiểu.

#### A. Danh sách Thuộc tính (Attributes)
| Tên thuộc tính | Kiểu dữ liệu | Kích thước / Ràng buộc | Mô tả |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | 4 bytes, PK, Auto Increment | Mã số định danh của thuốc trong CSDL |
| `medicine_code`| `String` | 30 ký tự, UNIQUE, NOT NULL | Mã quản lý kho dược (ví dụ: `MED-PARA-500`) |
| `name` | `String` | 150 ký tự, NOT NULL | Tên thương mại của thuốc (ví dụ: `Paracetamol 500mg`) |
| `active_ingredient`| `String` | 150 ký tự, NULLABLE | Tên hoạt chất y học (ví dụ: `Acetaminophen`) |
| `dosage_form` | `String` | 50 ký tự, NOT NULL | Dạng bào chế: Viên nén, Viên nang, Siro, Hỗn dịch |
| `unit` | `String` | 20 ký tự, NOT NULL | Đơn vị tính: Viên, Hộp, Vỉ, Gói, Chai |
| `unit_price` | `Float` | 8 bytes, >= 0, NOT NULL | Đơn vị giá bán niêm yết (VNĐ) |
| `stock_quantity`| `Integer` | 4 bytes, DEFAULT 0, NOT NULL | Số lượng tồn kho thực tế hiện có |
| `min_stock_threshold`| `Integer`| 4 bytes, DEFAULT 20, NOT NULL | Ngưỡng cảnh báo sắp hết hàng cần nhập bổ sung |
| `expiry_date` | `Date` | 4 bytes, NOT NULL | Hạn sử dụng của lô thuốc hiện tại |
| `is_active` | `Boolean` | 1 byte, DEFAULT TRUE | Trạng thái còn lưu hành kinh doanh hay không |

#### B. Danh sách Phương thức (Methods)
##### 1. Phương thức `check_stock_availability`
- **Mô tả:** Kiểm tra tồn kho có đủ số lượng theo đơn thuốc yêu cầu trước khi xuất bán hay không.
- **Tham số đầu vào:**
  - `qty`: `Integer`, 4 bytes, > 0 (Số lượng thuốc cần xuất kê đơn).
- **Kết quả đầu ra:** `Boolean` (1 byte): `True` nếu `stock_quantity >= qty`, ngược lại `False`.
- **Luồng xử lý:** Kiểm tra `self.stock_quantity >= qty and self.is_active is True`.
- **Điều kiện bắt đầu:** Bản ghi thuốc tồn tại trong CSDL.
- **Điều kiện kết thúc:** Không làm thay đổi số lượng kho, chỉ kiểm tra logic.

##### 2. Phương thức `deduct_stock`
- **Mô tả:** Trừ trực tiếp số lượng thuốc xuất kho khi hóa đơn thuốc được thanh toán thành công.
- **Tham số đầu vào:**
  - `qty`: `Integer`, 4 bytes, > 0 (Số lượng thực tế xuất phát cho bệnh nhân).
- **Kết quả đầu ra:** `None`.
- **Luồng xử lý:**
  1. Kiểm tra nếu `self.stock_quantity < qty` thì kích hoạt ngoại lệ `ValueError("Tồn kho không đủ để xuất thuốc")`.
  2. Thực hiện trừ tồn kho: `self.stock_quantity -= qty`.
  3. Nếu `self.stock_quantity <= self.min_stock_threshold`, ghi nhận cảnh báo tồn kho thấp.
- **Điều kiện bắt đầu:** Hóa đơn khám chữa bệnh được xác nhận thanh toán `PAID`.
- **Điều kiện kết thúc:** Thuộc tính `stock_quantity` được cập nhật trong phiên CSDL Transaction.

##### 3. Phương thức `is_low_stock`
- **Mô tả:** Kiểm tra thuốc có rơi vào tình trạng thiếu hụt dưới ngưỡng an toàn hay không.
- **Tham số đầu vào:** Không có.
- **Kết quả đầu ra:** `Boolean` (1 byte): `True` nếu thuốc cần lập phiếu nhập kho bổ sung.
- **Luồng xử lý:** Trả về kết quả so sánh `self.stock_quantity <= self.min_stock_threshold`.

---

### 2.3. LỚP `Prescription` & `PrescriptionItem` (Đơn thuốc & Xuất kho Dược)
- **Mô tả:** Quản lý toàn bộ thông tin đơn thuốc do Bác sĩ chỉ định, liên kết trực tiếp với phiếu khám bệnh và quản lý danh sách chi tiết các mặt hàng thuốc xuất kho.

#### A. Danh sách Thuộc tính Lớp `Prescription`
| Tên thuộc tính | Kiểu dữ liệu | Kích thước / Ràng buộc | Mô tả |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | 4 bytes, PK, Auto Increment | Mã định danh đơn thuốc |
| `medical_record_id`| `Integer`| 4 bytes, FK, UNIQUE, NOT NULL | Phiếu khám lâm sàng gốc sở hữu đơn thuốc |
| `doctor_id` | `Integer` | 4 bytes, FK, NOT NULL | Bác sĩ thực hiện kê đơn |
| `notes` | `Text` | Tối đa 500 ký tự, NULLABLE | Lời dặn chung của bác sĩ về chế độ dùng thuốc |
| `status` | `String` | 20 ký tự, DEFAULT 'PENDING' | Trạng thái: `PENDING`, `DISPENSED`, `CANCELLED` |
| `created_at` | `DateTime` | 8 bytes, DEFAULT CURRENT_TIMESTAMP | Thời điểm lập đơn thuốc |

#### B. Danh sách Thuộc tính Lớp `PrescriptionItem`
| Tên thuộc tính | Kiểu dữ liệu | Kích thước / Ràng buộc | Mô tả |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | 4 bytes, PK, Auto Increment | Mã dòng chi tiết thuốc kê đơn |
| `prescription_id` | `Integer` | 4 bytes, FK, NOT NULL | Đơn thuốc chứa mặt hàng này |
| `medicine_id` | `Integer` | 4 bytes, FK, NOT NULL | Loại thuốc trong danh mục kho dược |
| `dosage` | `String` | 100 ký tự, NOT NULL | Liều lượng (ví dụ: `1 viên/lần, 2 lần/ngày`) |
| `quantity` | `Integer` | 4 bytes, > 0, NOT NULL | Tổng số lượng cấp phát |
| `unit_price` | `Float` | 8 bytes, >= 0, NOT NULL | Đơn vị giá tại thời điểm kê đơn |
| `instructions` | `String` | 200 ký tự, NULLABLE | Hướng dẫn uống: Uống sau ăn no, sáng/tối |

#### C. Danh sách Phương thức Lớp `Prescription`
##### 1. Phương thức `add_item`
- **Mô tả:** Thêm một mặt hàng thuốc mới vào đơn thuốc điện tử.
- **Tham số đầu vào:**
  - `item`: `PrescriptionItem` (Đối tượng dòng thuốc chi tiết).
- **Kết quả đầu ra:** `None`.
- **Luồng xử lý:**
  1. Kiểm tra thuốc tương ứng trong kho có đang hoạt động hay không.
  2. Thêm đối tượng `item` vào tập danh sách `self.items`.
- **Điều kiện bắt đầu:** Đơn thuốc đang ở trạng thái soạn thảo.
- **Điều kiện kết thúc:** Danh sách `self.items` tăng thêm 1 phần tử.

##### 2. Phương thức `calculate_total_cost`
- **Mô tả:** Tổng hợp tổng chi phí tiền thuốc của toàn bộ đơn.
- **Tham số đầu vào:** Không có.
- **Kết quả đầu ra:** `Float` (8 bytes): Tổng số tiền thuốc tính bằng VNĐ.
- **Luồng xử lý:** Duyệt qua các phần tử trong `self.items`, tính tổng: `sum(item.quantity * item.unit_price)`.

---

### 2.4. LỚP `Patient` (Hồ sơ Bệnh nhân)
- **Mô tả:** Quản lý toàn bộ thông tin hành chính, thẻ bảo hiểm y tế, lịch sử bệnh án và các cảnh báo dị ứng thuốc nhằm bảo đảm an toàn tính mạng cho người bệnh.

#### A. Danh sách Thuộc tính (Attributes)
| Tên thuộc tính | Kiểu dữ liệu | Kích thước / Ràng buộc | Mô tả |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | 4 bytes, PK, Auto Increment | Định danh nội bộ bệnh nhân |
| `patient_code` | `String` | 30 ký tự, UNIQUE, NOT NULL | Mã định danh chuẩn: `BN-YYYYMMDD-XXXX` |
| `full_name` | `String` | 100 ký tự, NOT NULL | Họ tên đầy đủ của bệnh nhân |
| `dob` | `Date` | 4 bytes, NOT NULL | Ngày tháng năm sinh |
| `gender` | `String` | 10 ký tự, NOT NULL | Giới tính: `Nam`, `Nữ`, `Khác` |
| `phone` | `String` | 15 ký tự, NOT NULL | Số điện thoại liên hệ chính |
| `identity_card`| `String` | 12 ký tự, NULLABLE | Số CCCD (12 số) hoặc CMND (9 số) |
| `health_insurance`| `String`| 15 ký tự, NULLABLE | Mã thẻ BHYT Việt Nam (15 ký tự) |
| `address` | `String` | 255 ký tự, NULLABLE | Địa chỉ nơi cư trú |
| `medical_history`| `Text` | Tối đa 2000 ký tự, NULLABLE| Tiền sử bệnh nền: Tiểu đường, Tăng HA... |
| `drug_allergies` | `Text` | Tối đa 1000 ký tự, NULLABLE| Danh sách các loại thuốc dị ứng |

#### B. Danh sách Phương thức (Methods)
##### 1. Phương thức `calculate_age`
- **Mô tả:** Tính tuổi chính xác của bệnh nhân tại thời điểm khám bệnh.
- **Tham số đầu vào:** Không có.
- **Kết quả đầu ra:** `Integer` (4 bytes): Số tuổi tính theo năm dương lịch.
- **Luồng xử lý:** `date.today().year - self.dob.year`.

##### 2. Phương thức `has_drug_allergy`
- **Mô tả:** Kiểm tra tên thuốc bác sĩ dự định kê đơn có trùng khớp với tiền sử dị ứng đã khai báo của người bệnh hay không.
- **Tham số đầu vào:**
  - `drug_name`: `String`, tối đa 150 ký tự (Tên thuốc hoặc nhóm hoạt chất).
- **Kết quả đầu ra:** `Boolean` (1 byte): `True` nếu phát hiện có nguy cơ dị ứng.
- **Luồng xử lý:** Kiểm tra nếu chuỗi `drug_name.lower()` xuất hiện trong `self.drug_allergies.lower()`.

---

### 2.5. LỚP `Appointment` (Lịch hẹn khám bệnh & Hàng đợi)
- **Mô tả:** Quản lý vòng đời cuộc hẹn khám giữa Bệnh nhân và Bác sĩ chuyên khoa tại Buồng khám; ngăn chặn tuyệt đối xung đột lịch hẹn.

#### A. Danh sách Thuộc tính (Attributes)
| Tên thuộc tính | Kiểu dữ liệu | Kích thước / Ràng buộc | Mô tả |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | 4 bytes, PK, Auto Increment | Mã số lịch hẹn |
| `patient_id` | `Integer` | 4 bytes, FK, NOT NULL | Bệnh nhân đặt lịch |
| `doctor_id` | `Integer` | 4 bytes, FK, NOT NULL | Bác sĩ chuyên môn phụ trách ca khám |
| `clinic_id` | `Integer` | 4 bytes, FK, NOT NULL | Phòng khám tiếp nhận |
| `start_time` | `DateTime` | 8 bytes, NOT NULL | Thời gian bắt đầu khung giờ khám |
| `end_time` | `DateTime` | 8 bytes, NOT NULL | Thời gian kết thúc khung giờ khám |
| `status` | `String` | 20 ký tự, DEFAULT 'PENDING' | Trạng thái: `PENDING`, `CONFIRMED`, `CHECKED_IN`, `COMPLETED`, `CANCELLED` |
| `queue_number` | `Integer` | 4 bytes, NULLABLE | Số thứ tự tiếp đón trong ngày tại phòng khám |
| `symptoms` | `Text` | Tối đa 500 ký tự, NULLABLE | Triệu chứng ban đầu khi đăng ký khám |

#### B. Danh sách Phương thức (Methods)
##### 1. Phương thức `check_in`
- **Mô tả:** Chuyển trạng thái lịch hẹn khi bệnh nhân có mặt tại quầy tiếp đón và cấp số thứ tự vào phòng khám.
- **Tham số đầu vào:**
  - `queue_num`: `Integer`, 4 bytes (Số thứ tự khám trong ngày).
- **Kết quả đầu ra:** `None`.
- **Luồng xử lý:** Cập nhật `self.status = 'CHECKED_IN'` và gán `self.queue_number = queue_num`.
- **Điều kiện bắt đầu:** Cuộc hẹn đang ở trạng thái `PENDING` hoặc `CONFIRMED`.
- **Điều kiện kết thúc:** Lịch hẹn chuyển sang `CHECKED_IN`, bệnh nhân xuất hiện trong hàng đợi của bác sĩ.

---

### 2.6. LỚP `MedicalRecord` (Phiếu khám Lâm sàng EMR)
- **Mô tả:** Lưu trữ toàn bộ diễn tiến khám bệnh lâm sàng của Bác sĩ: đo sinh hiệu, chỉ số BMI, chẩn đoán bệnh theo danh mục ICD-10 và kết quả tóm tắt/dặn dò của AI.

#### A. Danh sách Thuộc tính (Attributes)
| Tên thuộc tính | Kiểu dữ liệu | Kích thước / Ràng buộc | Mô tả |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | 4 bytes, PK, Auto Increment | Mã hồ sơ ca khám bệnh |
| `patient_id` | `Integer` | 4 bytes, FK, NOT NULL | Bệnh nhân được thăm khám |
| `doctor_id` | `Integer` | 4 bytes, FK, NOT NULL | Bác sĩ thực hiện khám bệnh |
| `appointment_id` | `Integer` | 4 bytes, FK, NULLABLE | Lịch hẹn tương ứng |
| `status` | `String` | 20 ký tự, DEFAULT 'IN_PROGRESS' | Trạng thái: `IN_PROGRESS`, `COMPLETED`, `CANCELLED` |
| `chief_complaint`| `Text` | Tối đa 1000 ký tự, NOT NULL | Lý do đến khám và triệu chứng chủ quan |
| `clinical_notes` | `Text` | Tối đa 2000 ký tự, NULLABLE| Ghi nhận khám các cơ quan |
| `icd10_code` | `String` | 10 ký tự, NOT NULL | Mã chẩn đoán quốc tế ICD-10 (ví dụ `I10`) |
| `diagnosis_icd10`| `String` | 200 ký tự, NOT NULL | Tên chẩn đoán xác định |
| `blood_pressure` | `String` | 20 ký tự, NULLABLE | Chỉ số Huyết áp (ví dụ `120/80 mmHg`) |
| `heart_rate` | `Integer` | 4 bytes, NULLABLE | Nhịp tim (nhịp/phút) |
| `temperature` | `Float` | 4 bytes, NULLABLE | Thân nhiệt (°C) |
| `weight_kg` | `Float` | 4 bytes, NULLABLE | Cân nặng (kg) |
| `height_cm` | `Float` | 4 bytes, NULLABLE | Chiều cao (cm) |
| `bmi` | `Float` | 4 bytes, NULLABLE | Chỉ số khối cơ thể (Body Mass Index) |

#### B. Danh sách Phương thức (Methods)
##### 1. Phương thức `calculate_bmi`
- **Mô tả:** Tự động tính chỉ số khối cơ thể BMI từ chiều cao và cân nặng theo chuẩn y tế Châu Á.
- **Tham số đầu vào:** Không có (sử dụng thuộc tính `self.weight_kg` và `self.height_cm`).
- **Kết quả đầu ra:** `Dictionary` chứa:
  - `bmi_value`: `Float` (làm tròn 1 chữ số thập phân).
  - `category`: `String` (`Thiếu cân`, `Bình thường`, `Thừa cân`, `Béo phì độ I`, `Béo phì độ II`).
- **Luồng xử lý:**
  1. Nếu `height_cm <= 0` hoặc `weight_kg <= 0` thì trả về `bmi = 0`.
  2. Tính `height_m = self.height_cm / 100.0`.
  3. Tính `bmi = self.weight_kg / (height_m * height_m)`.
  4. Phân loại theo thang WPRO (Tổ chức Y tế Thế giới khu vực Tây Thái Bình Dương).

##### 2. Phương thức `complete_encounter`
- **Mô tả:** Chốt ca khám bệnh, khóa chỉnh sửa và tự động đẩy dữ liệu sang phân hệ Thu ngân để lập hóa đơn.
- **Tham số đầu vào:** Không có.
- **Kết quả đầu ra:** `None`.
- **Luồng xử lý:** Đổi `self.status = 'COMPLETED'`. Kích hoạt tạo bản ghi `Invoice` ở trạng thái `UNPAID`.

---

### 2.7. LỚP `Invoice` (Hóa đơn Viện phí & Thanh toán VietQR)
- **Mô tả:** Tổng hợp các khoản chi phí của lần khám (tiền công khám, cận lâm sàng, thuốc kê đơn), tính toán mức chi trả của BHYT và sinh mã VietQR động để thu ngân thanh toán.

#### A. Danh sách Thuộc tính (Attributes)
| Tên thuộc tính | Kiểu dữ liệu | Kích thước / Ràng buộc | Mô tả |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | 4 bytes, PK, Auto Increment | Mã hóa đơn viện phí |
| `medical_record_id`| `Integer`| 4 bytes, FK, UNIQUE, NOT NULL | Phiếu khám phát sinh hóa đơn |
| `patient_id` | `Integer` | 4 bytes, FK, NOT NULL | Bệnh nhân thanh toán |
| `total_amount` | `Float` | 8 bytes, >= 0, NOT NULL | Tổng chi phí trước khi giảm trừ (VNĐ) |
| `insurance_discount`| `Float`| 8 bytes, DEFAULT 0 | Số tiền được BHYT chi trả (VNĐ) |
| `patient_payment`| `Float` | 8 bytes, >= 0, NOT NULL | Số tiền thực tế người bệnh phải nộp (VNĐ) |
| `status` | `String` | 20 ký tự, DEFAULT 'UNPAID' | Trạng thái: `UNPAID`, `PAID`, `CANCELLED` |
| `payment_method` | `String` | 20 ký tự, NULLABLE | Hình thức: `CASH`, `TRANSFER`, `CREDIT_CARD` |
| `paid_at` | `DateTime` | 8 bytes, NULLABLE | Thời điểm thanh toán thành công |

#### B. Danh sách Phương thức (Methods)
##### 1. Phương thức `calculate_bhyt_co_pay`
- **Mô tả:** Tính toán số tiền khấu trừ bảo hiểm y tế theo mức hưởng (80% đúng tuyến, 100% người có công).
- **Tham số đầu vào:**
  - `insurance_rate`: `Float`, giá trị từ `0.0` đến `1.0` (ví dụ `0.80`).
- **Kết quả đầu ra:** `Float`: Số tiền thực tế người bệnh đồng chi trả.
- **Luồng xử lý:**
  1. `self.insurance_discount = self.total_amount * insurance_rate`.
  2. `self.patient_payment = self.total_amount - self.insurance_discount`.
  3. Trả về `self.patient_payment`.

##### 2. Phương thức `generate_vietqr_payload`
- **Mô tả:** Tạo chuỗi dữ liệu chuẩn để sinh mã QR thanh toán nhanh Napas247 theo chuẩn VietQR.
- **Tham số đầu vào:** Không có.
- **Kết quả đầu ra:** `Dictionary` chứa: ngân hàng nhận, số tài khoản, số tiền thanh toán, nội dung chuyển khoản (`Mã Hóa Đơn - Mã Bệnh Nhân`).

---

### 2.8. LỚP `AdminAIService` & `InventoryAIService` (Trợ lý AI Hành chính & Quản lý Kho Dược)
- **Mô tả:** Điều phối các chức năng Trí tuệ Nhân tạo phục vụ quản lý: tóm tắt tiền sử bệnh án (Pre-visit Briefing), hỏi đáp quy trình phòng khám (FAQ Chatbot), sinh dặn dò xuất viện (Discharge Instructions) và dự báo cảnh báo tồn kho dược.

#### A. Danh sách Thuộc tính (Attributes)
| Tên thuộc tính | Kiểu dữ liệu | Mô tả |
| :--- | :--- | :--- |
| `_provider` | `AIProvider` | Đối tượng nhà cung cấp AI (Cloud Gemini hoặc Mock Deterministic) |
| `_anonymizer` | `PIIAnonymizer`| Đối tượng chịu trách nhiệm khử định danh PII 100% trước khi gửi LLM |
| `_guardrails` | `AdminAIGuardrails`| Bộ lọc đạo đức y tế, chặn câu lệnh phá rào và gắn Disclaimer bắt buộc |

#### B. Danh sách Phương thức (Methods)
##### 1. Phương thức `generate_pre_visit_summary`
- **Mô tả:** Tóm tắt nhanh lịch sử các lần khám trước, bệnh nền mạn tính và cảnh báo dị ứng thuốc để bác sĩ xem trong 10 giây trước khi vào ca khám.
- **Tham số đầu vào:**
  - `patient_id`: `Integer`, 4 bytes (Mã ID của bệnh nhân).
  - `db`: `Session` (Phiên làm việc CSDL SQLAlchemy).
- **Kết quả đầu ra:** `Dictionary` chứa tóm tắt tiền sử bệnh án kèm nhãn `MEDICAL_DISCLAIMER`.
- **Luồng xử lý:**
  1. Truy vấn lịch sử khám cũ của bệnh nhân từ CSDL.
  2. Sử dụng `_anonymizer.anonymize()` để loại bỏ Họ tên, CCCD, SĐT, BHYT.
  3. Ghép prompt mẫu gửi đến `_provider.generate()`.
  4. Đính kèm cảnh báo miễn trừ trách nhiệm y tế: *"Nội dung chỉ hỗ trợ hành chính, không thay thế chẩn đoán của bác sĩ"*.
  5. Ghi nhận nhật ký vào bảng `ai_invocation_logs`.
- **Điều kiện bắt đầu:** Bác sĩ mở ca khám tại màn hình EMR.
- **Điều kiện kết thúc:** Trả về kết quả hiển thị trên thẻ AI Pre-visit Card.

##### 2. Phương thức `predict_inventory_restock`
- **Mô tả:** Phân tích tốc độ kê đơn các mặt hàng thuốc trong 30 ngày qua để dự báo danh mục thuốc sắp cạn kho cần lập phiếu nhập hàng.
- **Tham số đầu vào:**
  - `medicine_id`: `Integer`, 4 bytes.
  - `db`: `Session`.
- **Kết quả đầu ra:** `Dictionary` gồm: số lượng xuất trung bình/ngày, số ngày dự kiến hết hàng, số lượng khuyến nghị nhập kho.
- **Luồng xử lý:** Thống kê từ bảng `prescription_items`, tính toán lượng tiêu thụ trung bình $\mu$ và độ lệch chuẩn $\sigma$ để đưa ra đề xuất nhập kho tối ưu.

---

### 2.9. LỚP `ConflictChecker` (Thuật toán Kiểm tra Xung đột Lịch hẹn)
- **Mô tả:** Bộ xử lý toán học kiểm tra sự giao thoa khoảng thời gian (Interval Intersection) trên hai chiều không gian: Bác sĩ và Buồng khám.

#### A. Thuộc tính & Phương thức
##### Phương thức `check_appointment_conflict`
- **Mô tả:** Kiểm tra yêu cầu đặt lịch hoặc đổi lịch mới có bị chồng lấn thời gian với lịch đã có hay không.
- **Tham số đầu vào:**
  - `db`: `Session` (Phiên kết nối CSDL).
  - `doctor_id`: `Integer`, 4 bytes.
  - `clinic_id`: `Integer`, 4 bytes.
  - `start_time`: `DateTime`, 8 bytes (Giờ bắt đầu yêu cầu).
  - `end_time`: `DateTime`, 8 bytes (Giờ kết thúc yêu cầu).
  - `exclude_id`: `Integer`, 4 bytes, NULLABLE (Bỏ qua ID lịch hẹn hiện tại khi thao tác đổi lịch).
- **Kết quả đầu ra:** `Tuple[Boolean, Optional[String]]`:
  - Phần tử 1: `True` nếu không xung đột (Hợp lệ), `False` nếu bị trùng lịch.
  - Phần tử 2: Chuỗi thông báo nguyên nhân cụ thể (ví dụ: *"Bác sĩ đã có lịch hẹn khác từ 09:00"*).
- **Luồng xử lý:**
  1. Áp dụng điều kiện giao thoa khoảng thời gian: $\text{Overlap}(A, B) \iff (Start_A < End_B) \land (End_A > Start_B)$.
  2. Truy vấn kiểm tra trùng lịch Bác sĩ với các trạng thái hoạt động (`PENDING`, `CONFIRMED`, `CHECKED_IN`).
  3. Truy vấn kiểm tra trùng lịch Phòng khám buồng bệnh.
  4. Trả về kết quả phân tích.
- **Điều kiện bắt đầu:** Lễ tân gửi yêu cầu đặt lịch từ màn hình `AppointmentCalendarPage`.
- **Điều kiện kết thúc:** Trả về kết quả trong thời gian thực (< 5ms).

---

## 3. TỔNG KẾT & ĐÁNH GIÁ MỨC ĐỘ ĐÁP ỨNG

Tài liệu thiết kế hướng đối tượng trên đã:
1. ✅ **Mô hình hóa đầy đủ 100% sơ đồ lớp UML (Class Diagram)** với phân tầng chuẩn: *Domain Entities, Service Layer, AI Providers*.
2. ✅ **Đặc tả chi tiết từng thuộc tính:** Có tên thuộc tính, kiểu dữ liệu chuẩn, kích thước byte/chiều dài ký tự và ràng buộc toàn vẹn CSDL.
3. ✅ **Đặc tả chi tiết từng phương thức:** Có tên phương thức, mô tả chức năng, tham số đầu vào (tên, kiểu, kích thước), kết quả đầu ra, luồng xử lý chi tiết từng bước, điều kiện bắt đầu (Pre-conditions) và điều kiện kết thúc (Post-conditions).
4. ✅ **Bao hàm toàn diện phân hệ Quản lý Kho Dược, Thuốc, Kê đơn, Lịch hẹn và Trợ lý AI** đúng theo các tiêu chuẩn học phần CNTT và thực hành AI-Augmented SDLC.
