---
name: architecture-design
description: Quy chuẩn thiết kế kiến trúc hệ thống y tế phân tầng (Healthcare Layered Architecture), tích hợp Trợ lý AI Hành chính 3 lớp, bộ phát hiện xung đột lịch khám và kiểm soát phân quyền RBAC cho CMS-AI.
objective: Cung cấp phương pháp luận và chuẩn mực thiết kế kiến trúc phần mềm y tế hiện đại, đảm bảo tính mô-đun hóa cao, an toàn dữ liệu người bệnh, khả năng hoạt động ngoại tuyến 100% và ghi nhận quyết định kiến trúc chuẩn ADR.
inputs:
  - Tài liệu đặc tả yêu cầu nghiệp vụ (docs/requirements.md, docs/user-stories.md)
  - Ma trận phân quyền 4 vai trò RBAC (Admin, Receptionist, Doctor, Accountant)
  - Yêu cầu về ranh giới bảo mật y tế và khử định danh PII
  - Ràng buộc công nghệ: Python 3.10+ / FastAPI, React 18+ / Vite, SQLite / PostgreSQL
process:
  - 1. Phân tích các động lực kiến trúc (Architectural Drivers & Quality Attributes)
  - 2. Thiết kế kiến trúc phân tầng Backend (Clean Architecture / Service Layering)
  - 3. Thiết kế kiến trúc 3-Layer Administrative AI Engine (PII Filter -> Guardrail -> Multi-Provider)
  - 4. Thiết kế kiến trúc Frontend SPA phân quyền (Role-based Routing & Clinical UI Tokens)
  - 5. Thiết kế giải thuật cốt lõi: Động cơ phát hiện xung đột lịch khám (Conflict Detection Engine)
  - 6. Thiết lập Ranh giới An ninh & Luồng Dữ liệu (Security Perimeters & Data Flow Diagrams)
  - 7. Lập hồ sơ Quyết định Kiến trúc chuẩn ADR (Architectural Decision Records)
rules:
  - Tuyệt đối phân tách rõ ràng giữa tầng HTTP, tầng Nghiệp vụ (Service) và tầng Dữ liệu (ORM)
  - Tầng AI phải tuân thủ nghiêm ngặt mô hình 3 lớp: Bắt buộc ẩn danh PII trước khi gọi Provider
  - Bắt buộc có lớp Fallback Deterministic Mock Engine để hệ thống tự vận hành khi không có mạng
  - Không cho phép frontend gọi trực tiếp tới các dịch vụ bên ngoài mà không qua Backend Gateway
outputs:
  - docs/architecture.md (Tài liệu đặc tả kiến trúc toàn diện và sơ đồ phân tầng)
  - docs/architecture-decisions.md (Tập hợp các hồ sơ quyết định kiến trúc chuẩn ADR)
verification:
  - Đối chiếu tính độc lập giữa các module và kiểm tra sự cô lập dữ liệu giữa 4 vai trò
  - Kiểm thử khả năng chịu lỗi và tự động fallback về Mock AI khi ngắt kết nối internet
  - Đánh giá giải thuật xung đột lịch khám bảo đảm độ phức tạp tối ưu O(1) hoặc O(N_slot)
  - Thẩm định toàn diện từ Kiến trúc sư trưởng và Chuyên gia Bảo mật Y tế
---

# Kỹ năng Thiết kế Kiến trúc Hệ thống Y tế & Trợ lý AI (Architecture Design Skill)

## 1. Objective (Mục tiêu Kỹ năng)

Kỹ năng này quy chuẩn hóa quy trình thiết kế và tài liệu hóa kiến trúc tổng thể cho **Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp Trợ lý AI Hành chính (CMS-AI)**. 

Mục tiêu cốt lõi:
1. Xây dựng cấu trúc phân tầng chịu lỗi cao (Fault-tolerant Layered Architecture), phân tách độc lập giữa Tầng Giao tiếp API, Tầng Xác thực & Phân quyền, Tầng Nghiệp vụ Y tế, Tầng AI Hành chính và Tầng Dữ liệu.
2. Thiết kế động cơ AI 3 lớp bảo mật độc lập: Đảm bảo dữ liệu PII được khử định danh 100% trước khi đến mô hình LLM, đồng thời tích hợp sẵn cơ chế **Deterministic Mock Engine** cho phép vận hành trơn tru khi hoàn toàn mất kết nối mạng.
3. Chuẩn hóa thuật toán phát hiện xung đột lịch khám (Conflict Detection Engine) đảm bảo không bao giờ xảy ra tình trạng chồng chéo bác sĩ hoặc phòng khám.
4. Ghi nhận minh bạch các đánh đổi kỹ thuật (Trade-offs) thông qua các bản ghi Quyết định Kiến trúc (Architectural Decision Records - ADRs).

---

## 2. Terminology & Conceptual Model (Mô hình Khái niệm)

Trong không gian Thiết kế Kiến trúc phần mềm:

```
+-----------------------------------------------------------------------------------------------+
|                                      MÔ HÌNH KHÁI NIỆM KIẾN TRÚC                              |
+-----------------------------------------------------------------------------------------------+
|  1. CODEX (AI Agent)         : Kỹ sư Kiến trúc Hệ thống (System Architect Agent). Đề xuất các |
|                                mẫu thiết kế (Design Patterns), phân lớp module, sơ đồ DFD.    |
|  2. SKILL (Procedural Standard): Quy chuẩn thiết kế kiến trúc phân tầng y tế, mẫu ADR, chuẩn  |
|                                bảo mật 3 lớp AI và giải thuật kiểm tra xung đột (Skill này).  |
|  3. TOOL (Environment Action): Công cụ trực quan hóa sơ đồ (ASCII/Mermaid), công cụ benchmark |
|                                hiệu năng và kiểm tra cấu trúc thư mục mã nguồn.               |
|  4. MCP (Model Context Protocol): Giao thức trao đổi metadata kiến trúc giữa các agent phân tán.|
+-----------------------------------------------------------------------------------------------+
```

---

## 3. Inputs & Prerequisites (Đầu vào & Điều kiện Tiên quyết)

1. **Tài liệu Yêu cầu Nghiệp vụ**: `docs/requirements.md` (FR-001..FR-038) và `docs/user-stories.md`.
2. **Yêu cầu Phi chức năng cốt lõi**:
   - Khả năng chuyển đổi CSDL linh hoạt giữa SQLite (Dev/Test zero-config) và PostgreSQL 16 (Production).
   - Thời gian đáp ứng của API < 200ms, AI Mock Latency < 10ms.
   - Chuẩn bảo mật y tế: Không rò rỉ PII, kiểm soát truy cập phân quyền RBAC 4 vai trò.
3. **Các ràng buộc hạ tầng**: Môi trường Docker Compose, hỗ trợ chạy local trên Windows bằng các file `.bat`.

---

## 4. Execution Process (Quy trình Thực thi Từng bước)

```
[Bước 1: Phân tích Drivers] ---> [Bước 2: Phân tầng Backend] ---> [Bước 3: Thiết kế AI 3 lớp]
                                                                                |
[Bước 6: An ninh & DFD]     <--- [Bước 5: Giải thuật Xung đột] <--- [Bước 4: Kiến trúc Frontend]
           |
           v
[Bước 7: Lập hồ sơ Quyết định Kiến trúc (ADRs)]
```

### Bước 1: Phân tích Động lực Kiến trúc (Architectural Drivers)
Xác định 4 trụ cột kiến trúc quyết định thành công của hệ thống:
1. **Medical Privacy & Data Integrity**: Dữ liệu y tế là bất khả xâm phạm; dữ liệu PII phải được lọc trước bất kỳ xử lý ngoại vi nào.
2. **Deterministic Offline Resiliency**: Phòng khám không được phép ngừng trệ khi mất internet; các tính năng AI phải có chế độ Rule-based Deterministic Fallback 100%.
3. **Role Isolation & Least Privilege**: 4 vai trò (Admin, Lễ tân, Bác sĩ, Kế toán) tuyệt đối không được đọc hoặc ghi chéo dữ liệu ngoài thẩm quyền.
4. **Sub-second Scheduling Accuracy**: Thuật toán kiểm tra lịch khám phải chạy tức thì và chính xác tuyệt đối ở mức mili-giây.

### Bước 2: Thiết kế Kiến trúc Phân tầng Backend (Layered Backend Architecture)

Hệ thống Backend FastAPI tuân thủ cấu trúc phân tầng hướng dịch vụ (Service-Oriented Layering):

```
+-------------------------------------------------------------------------------+
|                            FASTAPI BACKEND APPLICATION                        |
|                                                                               |
|  [HTTP Clients] ---> [CORS Middleware] ---> [JWT Auth & RoleChecker]          |
|                                                            |                  |
|                                                            v                  |
|  [Pydantic v2 Schemas] <--------------------------- [API Routers v1]          |
|            |                                               |                  |
|            v                                               v                  |
|  [Business Logic / Services] <--------------------> [Conflict Engine]         |
|            |                                               |                  |
|            v                                               v                  |
|  [3-Layer AI Engine (PII Filter -> Provider)] <---> [SQLAlchemy 2.0 ORM]     |
|                                                            |                  |
|                                                            v                  |
|                                            [Database: PostgreSQL / SQLite]    |
+-------------------------------------------------------------------------------+
```

1. **Tầng API Routing & Middleware (`backend/app/api/v1/`)**: Tiếp nhận HTTP request, áp dụng Rate Limiting, CORS và Dependency Injection.
2. **Tầng Xác thực & Phân quyền (`backend/app/core/`)**: Xác thực JWT tokens, phân quyền RBAC thông qua callable dependency `RoleChecker(allowed_roles)`.
3. **Tầng Xác thực Dữ liệu (`backend/app/schemas/`)**: Pydantic v2 schemas với cấu hình `ConfigDict(from_attributes=True)` tách biệt Request Body, Response Model và Internal DTOs.
4. **Tầng Nghiệp vụ & Động cơ Cốt lõi (`backend/app/services/`, `backend/app/core/conflict_checker.py`)**: Xử lý logic lâm sàng, trừ tồn kho thuốc, tính toán viện phí và phát hiện trùng lịch.
5. **Tầng ORM & Cơ sở dữ liệu (`backend/app/models/`, `backend/app/database.py`)**: Quản lý phiên làm việc SQLAlchemy 2.0 (`SessionLocal`), transaction an toàn và mapping quan hệ 14 thực thể.

### Bước 3: Thiết kế Kiến trúc Trợ lý AI Hành chính 3 Lớp (3-Layer AI Engine)

Nhằm đảm bảo an toàn y tế và khả năng độc lập mạng, module AI được thiết kế theo 3 tầng cô lập:

```
+---------------------------------------------------------------------------------------------------+
|                                3-LAYER ADMINISTRATIVE AI ENGINE                                   |
|                                                                                                   |
|  +---------------------------------------------------------------------------------------------+  |
|  | LỚP 1: TẦNG KHỬ ĐỊNH DANH PII (PRIVACY & DE-IDENTIFICATION LAYER)                           |  |
|  | - Regex Engine lọc số CCCD/CMND, Số điện thoại VN, Mã thẻ BHYT, Tên bệnh nhân, Địa chỉ.    |  |
|  | - Thay thế bằng các tokens chuẩn: [PATIENT_NAME_REDACTED], [CCCD_REDACTED], [PHONE_REDACTED] |  |
|  | - Bảo toàn 100% thuật ngữ y khoa, triệu chứng, tiền sử dị ứng và chỉ số sinh hiệu.          |  |
|  +----------------------------------------------+----------------------------------------------+  |
|                                                 | (Prompt đã được ẩn danh)                        |
|                                                 v                                                 |
|  +---------------------------------------------------------------------------------------------+  |
|  | LỚP 2: TẦNG HÀNG RÀO BẢO VỆ & MIỄN TRỪ Y TẾ (GUARDRAILS & LEGAL DISCLAIMER LAYER)           |  |
|  | - Prompt Injection Defense: Phát hiện và triệt tiêu jailbreak attempts.                      |  |
|  | - Non-Diagnostic Filter: Kiên quyết từ chối yêu cầu tự chẩn đoán bệnh học hoặc tự kê đơn.   |  |
|  | - Legal Disclaimer Injection: Bắt buộc đính kèm TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y TẾ.         |  |
|  +----------------------------------------------+----------------------------------------------+  |
|                                                 | (Safe & Bound Prompt)                           |
|                                                 v                                                 |
|  +---------------------------------------------------------------------------------------------+  |
|  | LỚP 3: TẦNG NHÀ CUNG CẤP & DỰ PHÒNG NGOẠI TUYẾN (MULTI-PROVIDER & FALLBACK LAYER)            |  |
|  |                                                                                             |  |
|  |  +----------------------------+  +-----------------------+  +----------------------------+   |  |
|  |  | Deterministic Mock Engine  |  |   Ollama Local LLM    |  | Gemini / OpenAI Cloud API  |   |  |
|  |  |  (100% Offline / Zero Lat) |  | (Llama 3 / Qwen Local)|  | (Cloud Provider Adapter)  |   |  |
|  |  +----------------------------+  +-----------------------+  +----------------------------+   |  |
|  |                ^                             ^                            ^                  |  |
|  |                +-----------------------------+----------------------------+                  |  |
|  |                        (Tự động Fallback về Mock Engine khi offline / lỗi API)               |  |
|  +---------------------------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------------------------+
```

### Bước 4: Thiết kế Kiến trúc Frontend SPA (React 18 + Vite + Tailwind CSS)
1. **Kiến trúc Định tuyến Phân quyền (Role-Based Protected Routes)**:
   - Sử dụng `ProtectedRoute` bọc quanh từng nhánh URL: `/receptionist/*`, `/doctor/*`, `/accountant/*`, `/admin/*`.
   - Ngăn chặn truy cập trái phép ngay từ tầng Client và tự động chuyển hướng về `/unauthorized` hoặc `/login`.
2. **Quản lý Trạng thái & API Client**:
   - `AuthContext`: Quản lý JWT token trong `localStorage`, giải mã User Profile và trạng thái đăng nhập.
   - `ToastContext`: Cung cấp hệ thống thông báo trạng thái tức thời (Success, Error, Warning).
   - `Axios Interceptors`: Tự động gắn header `Authorization: Bearer <token>` và bắt mã lỗi `401` để force logout.
3. **Medical UI Tokens & Clinical Taste-Skill**:
   - Áp dụng triệt để bộ màu y tế (Slate-900, Sky-600, Teal-600, Emerald-500, Rose-500).
   - Typography phân cấp rõ ràng, số liệu y tế và giá tiền luôn dùng `tabular-nums font-mono`.

### Bước 5: Thiết kế Giải thuật Cốt lõi: Động cơ Phát hiện Xung đột Lịch khám (Conflict Detection)
Mô hình toán học kiểm tra xung đột giữa yêu cầu đặt lịch mới $[S_{new}, E_{new})$ và lịch đã tồn tại $[S_i, E_i)$:

$$\text{Conflict}(A_{new}, A_i) \iff (S_{new} < E_i) \land (E_{new} > S_i)$$

với điều kiện:
- Cùng Bác sĩ ($Doctor_{new} = Doctor_i$) HOẶC cùng Phòng khám ($Clinic_{new} = Clinic_i$).
- Trạng thái lịch hẹn $Status_i \in \{PENDING, CONFIRMED, CHECKED\_IN\}$.
- Bỏ qua chính nó khi thực hiện đổi lịch ($id_i \neq id_{new}$).

*Mã thực thi chuẩn hóa trong `backend/app/core/conflict_checker.py`:*
```python
def check_appointment_conflict(
    db: Session,
    doctor_id: int,
    clinic_id: int,
    start_time: datetime,
    end_time: datetime,
    exclude_appointment_id: Optional[int] = None
) -> Tuple[bool, Optional[str]]:
    # 1. Kiểm tra xung đột bác sĩ
    doctor_conflict = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.status.in_(["pending", "confirmed", "checked_in"]),
        Appointment.appointment_time < end_time,
        Appointment.end_time > start_time,
        Appointment.id != exclude_appointment_id if exclude_appointment_id else True
    ).first()
    if doctor_conflict:
        return False, f"Bác sĩ đã có lịch hẹn khác trong khung giờ này ({doctor_conflict.appointment_time.strftime('%H:%M')} - {doctor_conflict.end_time.strftime('%H:%M')})."

    # 2. Kiểm tra xung đột phòng khám
    clinic_conflict = db.query(Appointment).filter(
        Appointment.clinic_id == clinic_id,
        Appointment.status.in_(["pending", "confirmed", "checked_in"]),
        Appointment.appointment_time < end_time,
        Appointment.end_time > start_time,
        Appointment.id != exclude_appointment_id if exclude_appointment_id else True
    ).first()
    if clinic_conflict:
        return False, f"Phòng khám đã có bệnh nhân khác được xếp trong khung giờ này."

    return True, None
```

### Bước 6: Thiết lập Ranh giới An ninh & Luồng Dữ liệu (Security Perimeters)
1. **Perimeter 1 (Internet / Client Boundary)**: HTTPS / TLS 1.3, Rate Limiter (100 req/min/IP), CORS restricted to Frontend Origin.
2. **Perimeter 2 (Application Boundary)**: JWT HS256 Token Validation, RoleChecker Dependency Injection, RFC 7807 Exception Sanitizer.
3. **Perimeter 3 (AI Gateway Boundary)**: Bắt buộc đi qua `PIIAnonymizer.anonymize()`, Guardrail Disclaimer injection.
4. **Perimeter 4 (Database Boundary)**: Tham số hóa 100% câu truy vấn qua SQLAlchemy ORM, Mã hóa mật khẩu Bcrypt với salt rounds = 12.

### Bước 7: Lập Hồ sơ Quyết định Kiến trúc chuẩn ADR (Architectural Decision Records)
Biên soạn danh mục các quyết định kiến trúc trọng yếu vào `docs/architecture-decisions.md` theo cấu trúc:
- **ADR-001**: Lựa chọn FastAPI và SQLAlchemy 2.0 làm nền tảng Backend y tế hiệu năng cao.
- **ADR-002**: Lựa chọn mô hình AI phân lớp 3 tầng kết hợp Deterministic Mock Fallback Engine.
- **ADR-003**: Thiết lập giải thuật phát hiện xung đột lịch khám tại tầng Backend Core thay vì Database Stored Procedures.
- **ADR-004**: Áp dụng chuẩn Taste-Skill cho giao diện Frontend y tế (Anti-slop UI).

---

## 5. Human-in-the-loop Governance (Cơ chế Kiểm soát Con người)

### 5.1. Thẩm quyền Duyệt Kiến trúc
- Kiến trúc sư trưởng (Chief Architect) và Chuyên gia An toàn thông tin (Security Specialist) trực tiếp đánh giá và ký duyệt tài liệu kiến trúc.

### 5.2. Tiêu chí Đánh giá Phê duyệt
- [ ] 1. Sơ đồ phân tầng rõ ràng, không có quan hệ phụ thuộc vòng (Circular Dependencies).
- [ ] 2. Kiến trúc AI có lớp khử PII bắt buộc và có Fallback Mock hoạt động độc lập 100%.
- [ ] 3. Giải thuật phát hiện xung đột bao phủ đủ cả 2 chiều: Bác sĩ và Phòng khám.
- [ ] 4. Đầy đủ các bản ghi ADR lý giải nguyên nhân và hệ quả của từng quyết định công nghệ.

---

## 6. Business & Compliance Rules (Quy tắc Nghiệp vụ & Tuân thủ)

1. **Tính độc lập nhà cung cấp AI**: Backend không phụ thuộc cứng vào bất kỳ nhà cung cấp Cloud LLM nào. Mọi tương tác AI phải thông qua interface trừu tượng `AIProvider`.
2. **Nguyên tắc Không Hardcode**: Tuyệt đối không hardcode JWT Secret Key, Database URL, hoặc API Keys trong mã nguồn. Mọi cấu hình phải nạp qua `backend/app/config.py` và file `.env`.
3. **Tuân thủ Chuẩn Xử lý Lỗi (RFC 7807)**: Mọi phản hồi lỗi từ API phải có cấu trúc chuẩn JSON gồm: `status_code`, `error_code`, `message`, `timestamp`.

---

## 7. Expected Outputs & Deliverables (Tài liệu Đầu ra Bắt buộc)

1. `docs/architecture.md`: Tài liệu đặc tả kiến trúc toàn diện gồm sơ đồ phân tầng, luồng dữ liệu DFD, mô hình AI 3 lớp và giải thuật xung đột.
2. `docs/architecture-decisions.md`: Tập hợp các bản ghi quyết định kiến trúc chuẩn ADR (ADR-001 đến ADR-005).

---

## 8. Verification & Quality Acceptance Criteria (Tiêu chí Nghiệm thu Chất lượng)

- **Tính Khả thi (Feasibility)**: Kiến trúc có thể chuyển thể trực tiếp thành cấu trúc thư mục và mã nguồn hoạt động thật.
- **Tính Chống chịu lỗi (Resilience)**: Khi tắt kết nối mạng, hệ thống vẫn vượt qua 100% test cases của bộ kiểm thử tự động.
- **Hiệu năng Thiết kế (Design Performance)**: Đảm bảo thời gian xử lý API trung bình < 200ms trên môi trường kiểm thử tiêu chuẩn.
- **Tính Toàn vẹn Bảo mật (Security Soundness)**: Không có luồng dữ liệu PII nào đi thẳng ra ngoài biên giới ứng dụng.
