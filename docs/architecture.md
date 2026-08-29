# ĐẶC TẢ KIẾN TRÚC KỸ THUẬT TOÀN DIỆN (SYSTEM ARCHITECTURE SPECIFICATION)
## DỰ ÁN: HỆ THỐNG QUẢN LÝ PHÒNG KHÁM ĐA KHOA THÔNG MINH TÍCH HỢP TRỢ LÝ AI HÀNH CHÍNH
### (Clinic Management System with Administrative AI Assistant - CMS-AI)

---

## 1. TỔNG QUAN KIẾN TRÚC TỔNG THỂ (SYSTEM OVERVIEW)

Hệ thống **CMS-AI** được xây dựng theo mô hình **Kiến trúc Phân tầng Hướng Dịch vụ (Service-Oriented Layered Architecture)** hiện đại, phân tách rõ ràng giữa Tầng Giao diện Người dùng (Presentation Layer), Tầng Dịch vụ API & Nghiệp vụ (Application & Business Logic Layer), Tầng Trợ lý AI Phân tầng Bảo mật (Administrative AI Engine), và Tầng Dữ liệu Quan hệ (Data Persistence Layer).

```mermaid
graph TD
    subgraph CLIENT_LAYER [TẦNG GIAO DIỆN CLIENT - React 18 SPA]
        UI1[Receptionist Dashboard]
        UI2[Doctor Consultation Workspace]
        UI3[Accountant Cashier Portal]
        UI4[Admin Governance & Analytics]
        AUTH_CTX[AuthContext & Axios Interceptors]
    end

    subgraph API_GATEWAY [TẦNG API BACKEND - FastAPI Python 3.10+]
        CORS[CORS Middleware]
        SEC[Security & JWT Validator]
        RBAC[RBAC RoleChecker Engine]
        ROUTER[FastAPI v1 REST Routers]
    end

    subgraph CORE_BUSINESS [TẦNG LOGIC NGHIỆP VỤ Y TẾ]
        SCHED[Conflict Detection Engine]
        CLINICAL[Clinical Record & ICD-10]
        RX[e-Prescription & Stock Manager]
        BILL[BHYT & VietQR Billing Engine]
    end

    subgraph AI_ENGINE [TẦNG TRỢ LÝ AI HÀNH CHÍNH 4 LỚP]
        L1[Lớp 1: PII De-identification Regex]
        L2[Lớp 2: Guardrails & Disclaimer]
        L3[Lớp 3: Multi-Provider Mock/Ollama/Cloud]
        L4[Lớp 4: AI Invocation Logger]
    end

    subgraph DATA_PERSISTENCE [TẦNG DỮ LIỆU CSDL]
        ORM[SQLAlchemy 2.0 ORM]
        DB[(PostgreSQL 16 / SQLite)]
    end

    CLIENT_LAYER -->|HTTPS / JSON / JWT| API_GATEWAY
    API_GATEWAY --> SEC
    SEC --> RBAC
    RBAC --> ROUTER
    ROUTER --> CORE_BUSINESS
    CORE_BUSINESS --> AI_ENGINE
    CORE_BUSINESS --> ORM
    AI_ENGINE --> ORM
    ORM --> DB
```

---

## 2. ĐẶC TẢ TẦNG BACKEND (FASTAPI + SQLALCHEMY 2.0 + PYDANTIC V2)

### 2.1. Thành phần Công nghệ Cốt lõi
- **Framework:** FastAPI (Python 3.10+) với kiến trúc bất đồng bộ (Asynchronous ASGI via Uvicorn), mang lại hiệu năng cao (> 20,000 req/sec) và tài liệu API tương tác tự động OpenAPI (Swagger UI tại `/docs`).
- **ORM & Database Toolkit:** SQLAlchemy 2.0 sử dụng cú pháp `select()` hiện đại, quản lý session an toàn qua `SessionLocal` theo từng request và hỗ trợ quản lý transaction nghiêm ngặt (`commit()`, `rollback()`).
- **Data Validation & Serializer:** Pydantic v2 với cơ chế kiểm tra kiểu dữ liệu tĩnh mạnh mẽ (Strict schema validation), chuẩn hóa định dạng ngày giờ ISO 8601, biểu thức chính quy cho CCCD (12 số), SĐT (10 số), BHYT (15 ký tự).
- **Authentication & Cryptography:** 
  - Mã hóa mật khẩu: `passlib[bcrypt]` với salt 12 vòng.
  - Cấp phát & giải mã Token: `PyJWT` (chuẩn RFC 7519, thuật toán ký mật mã `HS256`, thời hạn hết hạn 60 phút).

### 2.2. Cấu trúc Thư mục Backend Chuẩn Clean Architecture
```
backend/
├── app/
│   ├── main.py                  # Điểm khởi động ứng dụng, CORS middleware, gộp routers
│   ├── config.py                # Cấu hình Pydantic BaseSettings (.env loader)
│   ├── database.py              # Khởi tạo engine, SessionLocal, Base model
│   ├── models/                  # 14 SQLAlchemy ORM models (Entity definitions)
│   ├── schemas/                 # Pydantic v2 Request/Response Data Transfer Objects
│   ├── core/                    # Security, JWT handler, RBAC RoleChecker, Conflict Checker
│   ├── ai_engine/               # Module AI 4 lớp: Anonymizer, Guardrails, Providers, Services
│   ├── api/v1/                  # REST API Endpoints theo từng phân hệ nghiệp vụ
│   └── seed/                    # Script nạp dữ liệu mẫu y tế Việt Nam
└── tests/                       # 14 tệp test suite tự động với 223+ test cases
```

---

## 3. ĐẶC TẢ TẦNG FRONTEND (REACT 18 + VITE + TAILWIND CSS)

### 3.1. Thiết kế Giao diện Công thái học Y tế (Taste-Skill UI Standard)
- **Framework & Build Tool:** React 18 SPA đóng gói bằng Vite, đảm bảo thời gian Hot Module Replacement (HMR) < 50ms và kích thước bundle tối ưu.
- **Styling & Design System:** Tailwind CSS tuân thủ triết lý Taste-Skill chống "AI Slop":
  - Bảng màu lâm sàng chuẩn mực: Slate (Nền tảng & Văn bản), Emerald (Thành công & Khám bệnh), Sky Blue (Thông tin & Điều phối), Rose (Cảnh báo dị ứng & Khẩn cấp).
  - Phông chữ 3 tầng: *Plus Jakarta Sans* (Tiêu đề lớn), *Inter* (Giao diện & Văn bản), *JetBrains Mono* (Mã ICD-10, Sinh hiệu, Số tiền VNĐ với `tabular-nums font-mono`).
  - Viền xúc giác 1px (`border-slate-200/80`) thay thế bóng mờ lem nhem.
- **Biểu tượng:** `lucide-react` trực quan, nhất quán ngữ nghĩa y tế.

### 3.2. Quản lý Trạng thái & Bảo mật Định tuyến (Routing & State)
- **AuthContext & Token Storage:** Quản lý thông tin phiên làm việc của người dùng hiện tại, tự động phục hồi phiên từ `localStorage` khi F5 trang.
- **Axios HTTP Client Interceptor:** Tự động chèn header `Authorization: Bearer <token>` vào 100% request; tự động chuyển hướng về trang `/login` khi nhận mã lỗi `401 Unauthorized`.
- **RoleGate & ProtectedRoute:** Chặn hiển thị và ngăn truy cập trái phép các trang chức năng không thuộc quyền hạn của vai trò người dùng.

---

## 4. ĐẶC TẢ KIẾN TRÚC PHÂN TẦNG TRỢ LÝ AI HÀNH CHÍNH (4-LAYER AI ENGINE)

```mermaid
graph TD
    subgraph LAYER_1 [LỚP 1: KHỬ ĐỊNH DANH DỮ LIỆU - PII ANONYMIZATION]
        RAW_DATA[Dữ liệu Y tế Thô] --> REGEX_PHONE[Regex Số điện thoại VN]
        RAW_DATA --> REGEX_CCCD[Regex CCCD/CMND 12 số]
        RAW_DATA --> REGEX_BHYT[Regex Thẻ BHYT 15 ký tự]
        RAW_DATA --> TOKEN_NAME[Tokenize Họ tên Bệnh nhân]
        REGEX_PHONE --> ANON_PROMPT[Prompt đã Ẩn danh Hoàn toàn]
        REGEX_CCCD --> ANON_PROMPT
        REGEX_BHYT --> ANON_PROMPT
        TOKEN_NAME --> ANON_PROMPT
    end

    subgraph LAYER_2 [LỚP 2: HÀNG RÀO ĐẠO ĐỨC & MIỄN TRỪ Y TẾ - GUARDRAILS]
        ANON_PROMPT --> INJECTION_CHECK{Kiểm tra Prompt Injection?}
        INJECTION_CHECK -->|Phát hiện Tấn công| SANITIZE[Làm sạch & Vô hiệu hóa]
        INJECTION_CHECK -->|Hợp lệ| PROMPT_SAFE[Prompt An toàn]
        PROMPT_SAFE --> SYSTEM_RULES[Quy tắc: Cấm Tự Chẩn đoán Bệnh học]
        SYSTEM_RULES --> INJECT_DISCLAIMER[Đính kèm TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM]
    end

    subgraph LAYER_3 [LỚP 3: ĐA NHÀ CUNG CẤP & DỰ PHÒNG NGOẠI TUYẾN - MULTI-PROVIDER]
        INJECT_DISCLAIMER --> ROUTER_AI{Kiểm tra Cấu hình & Mạng}
        ROUTER_AI -->|Môi trường Test / Mất mạng| MOCK_ENGINE[Deterministic Mock Engine]
        ROUTER_AI -->|Cài đặt Local LLM| OLLAMA_LOCAL[Ollama Local LLM]
        ROUTER_AI -->|Có Internet & API Key| CLOUD_API[Gemini / OpenAI Cloud API]
        OLLAMA_LOCAL -->|Lỗi / Timeout| FALLBACK[Tự động Fallback sang Mock]
        CLOUD_API -->|Lỗi / Hết Quota| FALLBACK
        FALLBACK --> MOCK_ENGINE
    end

    subgraph LAYER_4 [LỚP 4: NHẬT KÝ KIỂM TOÁN & GIÁM SÁT AI - AI AUDIT]
        MOCK_ENGINE --> AI_OUTPUT[Kết quả AI chuẩn hóa]
        OLLAMA_LOCAL --> AI_OUTPUT
        CLOUD_API --> AI_OUTPUT
        AI_OUTPUT --> SAVE_LOG[(Lưu Bảng ai_invocation_logs)]
    end
```

---

## 5. MÔ HÌNH PHÂN QUYỀN TRUY CẬP DỰA TRÊN VAI TRÒ (RBAC MODEL)

### 5.1. Ma trận Phân quyền Toàn diện (RBAC Endpoint Matrix)
| Nhóm Endpoint REST API | Admin | Lễ tân (Receptionist) | Bác sĩ (Doctor) | Kế toán (Accountant) |
|---|:---:|:---:|:---:|:---:|
| `POST /api/v1/auth/login`, `GET /me` | **Full** | **Full** | **Full** | **Full** |
| `CRUD /api/v1/users` (Tài khoản người dùng) | **Full** | ❌ Chặn (403) | ❌ Chặn (403) | ❌ Chặn (403) |
| `CRUD /api/v1/clinics`, `/specialties` | **Full** | Read-Only | Read-Only | Read-Only |
| `CRUD /api/v1/doctors`, `/shifts` | **Full** | Read-Only | Read-Only | Read-Only |
| `CRUD /api/v1/patients` (Hồ sơ bệnh nhân) | **Full** | **Full** | Read-Only | Read-Only |
| `POST/PUT /api/v1/appointments` (Lịch hẹn) | **Full** | **Full** | Read-Only (Lịch mình) | ❌ Chặn (403) |
| `GET/POST /api/v1/queue` (Hàng đợi phòng khám)| **Full** | **Full** | Read-Only (Phòng mình)| ❌ Chặn (403) |
| `CRUD /api/v1/medical_records` (Phiếu khám) | Read-Only | ❌ Chặn (403) | **Full** (Ca mình phụ trách)| ❌ Chặn (403) |
| `CRUD /api/v1/prescriptions` (Đơn thuốc) | Read-Only | ❌ Chặn (403) | **Full** (Kê đơn) | Read-Only |
| `CRUD /api/v1/medicines` (Danh mục kho dược) | **Full** | Read-Only | Read-Only | Read-Only |
| `CRUD /api/v1/invoices` (Hóa đơn viện phí) | Read-Only | Read-Only | ❌ Chặn (403) | **Full** (Thu tiền/In) |
| `POST /api/v1/ai/pre-visit-summary` | Read-Only | ❌ Chặn (403) | **Full** | ❌ Chặn (403) |
| `POST /api/v1/ai/discharge-instructions` | Read-Only | ❌ Chặn (403) | **Full** | ❌ Chặn (403) |
| `POST /api/v1/ai/faq` (Chatbot quy trình) | **Full** | **Full** | **Full** | **Full** |
| `GET /api/v1/audit`, `GET /api/v1/stats` | **Full** | ❌ Chặn (403) | ❌ Chặn (403) | ❌ Chặn (403) |

---

## 6. THUẬT TOÁN KIỂM TRA XUNG ĐỘT LỊCH HẸN (CONFLICT DETECTION ENGINE)

Thuật toán hoạt động dựa trên nguyên lý kiểm tra giao khoảng thời gian (Interval Intersection) kết hợp hai chiều không gian (Bác sĩ & Phòng khám):

$$\text{Overlap}(A, B) \iff (Start_A < End_B) \land (End_A > Start_B)$$

```mermaid
graph TD
    START[Yêu cầu Đặt / Đổi Lịch Hẹn] --> P1[Lấy: doctor_id, clinic_id, start_time, end_time]
    P1 --> Q1[Truy vấn Appointments giao thời gian với bác sĩ]
    Q1 --> C1{Tìm thấy lịch của Doctor?}
    C1 -->|Có & status != CANCELLED| ERR1[Trả về lỗi: Bác sĩ đã có lịch hẹn khác]
    C1 -->|Không| Q2[Truy vấn Appointments giao thời gian tại phòng khám]
    Q2 --> C2{Tìm thấy lịch tại Clinic?}
    C2 -->|Có & status != CANCELLED| ERR2[Trả về lỗi: Phòng khám đã được sử dụng]
    C2 -->|Không| OK[Hợp lệ: Cho phép tạo lịch hẹn mới]
```

```python
# Code logic đặc tả tại backend/app/core/conflict_checker.py
def check_appointment_conflict(
    db: Session,
    doctor_id: int,
    clinic_id: int,
    start_time: datetime,
    end_time: datetime,
    exclude_appointment_id: Optional[int] = None
) -> Tuple[bool, Optional[str]]:
    # 1. Kiểm tra xung đột Bác sĩ
    doc_conflict = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.status != AppointmentStatus.CANCELLED,
        Appointment.start_time < end_time,
        Appointment.end_time > start_time
    )
    if exclude_appointment_id:
        doc_conflict = doc_conflict.filter(Appointment.id != exclude_appointment_id)
    if doc_conflict.first():
        return False, "Bác sĩ đã có lịch hẹn khác trong khoảng thời gian này."

    # 2. Kiểm tra xung đột Phòng khám
    room_conflict = db.query(Appointment).filter(
        Appointment.clinic_id == clinic_id,
        Appointment.status != AppointmentStatus.CANCELLED,
        Appointment.start_time < end_time,
        Appointment.end_time > start_time
    )
    if exclude_appointment_id:
        room_conflict = room_conflict.filter(Appointment.id != exclude_appointment_id)
    if room_conflict.first():
        return False, "Phòng khám đã được sử dụng trong khoảng thời gian này."

    return True, None
```

---

## 7. BIỂU ĐỒ TRÌNH TỰ NGHIỆP VỤ Y TẾ CHÍNH (SEQUENCE DIAGRAMS)

### 7.1. Trình tự Đặt lịch Khám & Kiểm tra Xung đột
```mermaid
sequenceDiagram
    autonumber
    actor LễTân as Lễ tân (Receptionist)
    participant UI as React Frontend
    participant API as FastAPI Router
    participant Engine as Conflict Checker
    participant DB as PostgreSQL Database

    LễTân->>UI: Chọn Bệnh nhân, Bác sĩ, Khung giờ (09:00 - 09:30)
    UI->>API: POST /api/v1/appointments (Payload + JWT Token)
    API->>API: Xác thực JWT & Kiểm tra quyền Receptionist
    API->>Engine: check_appointment_conflict(doc_id, room_id, start, end)
    Engine->>DB: Query các lịch hẹn giao thời gian (status != CANCELLED)
    DB-->>Engine: Kết quả rỗng (Không xung đột)
    Engine-->>API: (True, None)
    API->>DB: INSERT INTO appointments (status='PENDING')
    DB-->>API: Bản ghi lịch hẹn ID: 105
    API-->>UI: HTTP 201 Created (Appointment JSON)
    UI-->>LễTân: Hiển thị thông báo Đặt lịch thành công!
```

### 7.2. Trình tự Khám bệnh, Gọi AI Dặn dò & Thanh toán Hóa đơn
```mermaid
sequenceDiagram
    autonumber
    actor BácSĩ as Bác sĩ (Doctor)
    actor KếToán as Kế toán (Accountant)
    participant UI as React SPA
    participant API as FastAPI Backend
    participant AI as AI Engine (PII + Provider)
    participant DB as CSDL Quan hệ

    BácSĩ->>UI: Mở ca khám bệnh nhân BN-20260829-0001
    UI->>API: POST /api/v1/ai/pre-visit-summary
    API->>AI: generate_pre_visit_summary(patient_history)
    AI->>AI: Khử PII -> Guardrails -> Mock/LLM -> Gắn Disclaimer
    AI-->>API: Bản tóm tắt bệnh sử + Cảnh báo dị ứng
    API-->>UI: Hiển thị AI Pre-visit Card
    BácSĩ->>UI: Nhập Sinh hiệu, Chẩn đoán ICD-10, Kê đơn thuốc
    BácSĩ->>UI: Bấm "Sinh Dặn Dò Sau Khám (AI)"
    UI->>API: POST /api/v1/ai/discharge-instructions
    API->>AI: generate_discharge_instructions(encounter_data)
    AI-->>API: Lịch uống thuốc chi tiết + Hướng dẫn dinh dưỡng + Disclaimer
    API-->>UI: Đưa hướng dẫn vào hồ sơ khám
    BácSĩ->>UI: Bấm "Hoàn tất ca khám"
    UI->>API: PUT /api/v1/medical_records/{id}/complete
    API->>DB: Cập nhật status='COMPLETED' & Tạo Invoice 'PENDING'
    
    KếToán->>UI: Mở màn hình thu ngân, thấy Hóa đơn chờ
    UI->>API: GET /api/v1/invoices/pending
    KếToán->>UI: Kiểm tra BHYT 80%, Bấm "Tạo mã VietQR"
    UI->>UI: Hiển thị mã VietQR động
    KếToán->>UI: Xác nhận đã nhận tiền (CASH/TRANSFER)
    UI->>API: POST /api/v1/invoices/{id}/pay
    API->>DB: Cập nhật status='PAID' & Trừ tồn kho thuốc nguyên tử
    DB-->>API: Thành công
    API-->>UI: Hóa đơn đã thanh toán -> Mở Modal In Biên lai A4/A5
```
