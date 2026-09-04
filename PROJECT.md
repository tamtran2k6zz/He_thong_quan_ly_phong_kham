# 🏥 DỰ ÁN: HỆ THỐNG QUẢN LÝ PHÒNG KHÁM ĐA KHOA THÔNG MINH TÍCH HỢP AI HÀNH CHÍNH
### *(Smart Clinic Management System with Administrative AI Assistant - AI-Augmented SDLC)*

---

## 🌟 1. TỔNG QUAN DỰ ÁN & MÔ HÌNH AI-AUGMENTED SDLC

Dự án **Hệ thống Quản lý Phòng khám Đa khoa Thông minh tích hợp AI Hành chính** được phát triển theo mô hình **AI-Augmented SDLC** chuẩn hóa, trong đó AI Agent (Codex/Antigravity) được điều phối và kiểm soát chặt chẽ thông qua hệ thống **Skills**, **Tools** và **MCP**, kết hợp với các điểm kiểm soát của con người (**Human Gates 1, 2, 3**).

Hệ thống giải quyết toàn diện bài toán quản lý phân tán tại phòng khám tư nhân: từ tiếp đón, điều phối lịch hẹn (chống trùng lịch), hồ sơ bệnh nhân, lập phiếu khám bệnh lâm sàng, kê đơn điện tử, đến xuất hóa đơn viện phí và thanh toán BHYT/VietQR. Trợ lý AI đóng vai trò **hỗ trợ nghiệp vụ hành chính y tế**, tuân thủ nghiêm ngặt chuẩn bảo vệ dữ liệu cá nhân (PII de-identification) và **tuyệt đối không tự đưa ra chẩn đoán y khoa hay kê đơn thuốc tự động**.

```
                           +-------------------------------------------------------+
                           |          HUMAN SUPERVISION & HUMAN GATES 1-3          |
                           +---------------------------+---------------------------+
                                                       |
        +----------------------------------------------v-----------------------------------------------+
        |                                AI AGENT ENGINE (Codex / Antigravity)                          |
        +----------------------------------------------+-----------------------------------------------+
                                                       |
         +-----------------------------+---------------+---------------+-------------------------------+
         |                             |                               |                               |
+--------v---------+          +--------v--------+             +--------v--------+             +--------v--------+
|   SDLC SKILLS    |          |   HEALTHCARE    |             | ENVIRONMENT     |             | EXTERNAL MCP &  |
|  (.agents/skills)|          |    AI SKILLS    |             |     TOOLS       |             |   SERVICES      |
|  Requirements    |          | PII Sanitizer   |             | Pytest / Bash   |             | MySQL 8.0 / DB  |
|  Architecture    |          | Pre-visit AI    |             | Docker Engine   |             | Gemini 3.6 API  |
|  Database (3NF)  |          | Workflow FAQ    |             | Vite Build      |             | OpenAI API      |
|  Implementation  |          | Discharge AI    |             | Linter & Git    |             | Ollama Local    |
|  Multi-Tier Test |          | Taste UI/UX     |             | REST Clients    |             | GitHub Sync     |
|  Code & Security |          | Guardrails      |             |                 |             |                 |
+------------------+          +-----------------+             +-----------------+             +-----------------+
```

---

## 🏛️ 2. PHÂN ĐỊNH 4 THÀNH PHẦN CỐT LÕI

| Thành Phần | Bản Chất | Vai Trò Trong Dự Án Phòng Khám |
| :--- | :--- | :--- |
| **AI Agent ** | Trí tuệ điều phối trung tâm | Thực thi các tác vụ phát triển phần mềm, phân tích nghiệp vụ, sinh mã nguồn, thực thi kiểm thử và tạo tài liệu theo chỉ dẫn. |
| **Skill (`.agents/skills`)** | Tri thức thủ tục & tiêu chuẩn | Quy định quy trình, đầu vào/đầu ra, ràng buộc nghiệp vụ y tế, ranh giới an toàn AI và tiêu chí chấp nhận cho từng giai đoạn SDLC. |
| **Tool** | Cơ chế tương tác môi trường | Terminal, Pytest runner, Docker Compose, Git CLI, File I/O, Linter, HTTP client. |
| **MCP (Model Context Protocol)** | Giao thức kết nối dịch vụ ngoài | Kết nối cơ sở dữ liệu MySQL 8.0, Google Gemini API, OpenAI API, Ollama Engine và GitHub Repository. |

---

## 🛡️ 3. CÁC ĐIỂM KIỂM SOÁT CON NGƯỜI (HUMAN GATES)

Nhằm triệt tiêu rủi ro **AI Hallucination (ảo giác AI)** và **Requirement Invention (tự ý bịa yêu cầu)**:
- 🚪 **Human Gate 1 (Requirements Review)**: Đối soát các yêu cầu FR-001..FR-012 và 27 User Stories. Ngăn chặn AI tự ý thêm tính năng không được yêu cầu. Phê duyệt trước khi chuyển sang bước Thiết kế kiến trúc.
- 🚪 **Human Gate 2 (Architecture & Schema Verification)**: Kiểm tra tính toàn vẹn của mô hình phân tầng, ma trận phân quyền 4 vai trò RBAC và lược đồ CSDL 14 bảng quan hệ 3NF.
- 🚪 **Human Gate 3 (Security & Clinical Guardrails Audit)**: Rà soát cơ chế khử định danh PII 2 chiều, bắt buộc đính kèm Tuyên bố miễn trừ trách nhiệm y tế và kiểm toán an toàn thông tin theo chuẩn OWASP Top 10 / Nghị định 13/2023/NĐ-CP.

---

## 💻 4. KIẾN TRÚC KỸ THUẬT (TECHNOLOGY STACK)

### 4.1 Backend
- **Framework**: Python 3.10+ / FastAPI (Asynchronous REST API, OpenAPI docs).
- **ORM & Database**: SQLAlchemy 2.0, Pydantic v2 (Validation & Schemas).
- **Cơ sở dữ liệu**: MySQL 8.0 (Docker container, port 3307) & SQLite (Fallback).
- **Xác thực & Phân quyền**: JWT Authentication (HS256), Bcrypt Password Hashing, RBAC 4 vai trò.
- **Xử lý lỗi**: Chuẩn hóa RFC 7807 (Problem Details for HTTP APIs).

### 4.2 Administrative AI Engine 3 Lớp
- **Lớp 1 (PII Sanitizer)**: Khử định danh Họ tên, CCCD/CMND, Số điện thoại, Địa chỉ, Số thẻ BHYT bằng Regex đa tầng & Tokenization 2 chiều.
- **Lớp 2 (Medical Guardrails)**: Lọc Prompt Injection, kiên quyết từ chối chẩn đoán bệnh học hay kê đơn thuốc, tự động đính kèm `TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y TẾ`.
- **Lớp 3 (Multi-Provider Adapter)**:
  1. `Google Gemini Live` (`gemini-3.6-flash` - API Key thời gian thực).
  2. `OpenAI` (`gpt-4o-mini`).
  3. `Ollama` (`llama3` local offline).
  4. `Deterministic Mock Provider` (Fallback dự phòng 100% offline).

### 4.3 Frontend
- **Công nghệ**: React 18 SPA, Vite 5, Tailwind CSS 3, Lucide React Icons.
- **Triết lý Thiết Kế**: **Taste-Skill** (Chống AI-slop, độ tương phản chuẩn WCAG 2.1 AA, Typography 3 tầng: *Plus Jakarta Sans* / *Inter* / *JetBrains Mono*, Tabular figures cho sinh hiệu và viện phí).
- **Phân luồng 4 Portal**: Lễ tân (Tiếp đón & Calendar), Bác sĩ (Queue & Consultation EMR), Thu ngân (Invoices & VietQR), Quản trị viên (Analytics & Logs).

---

## 📂 5. CẤU TRÚC THƯ MỤC DỰ ÁN (PROJECT STRUCTURE)

```text
He_thong_quan_ly_phong_kham/
├── .agents/
│   └── skills/                                 # 13 BỘ SKILLS CHUẨN HÓA
│       ├── requirements-analysis/SKILL.md      # Skill phân tích yêu cầu y tế & RBAC
│       ├── architecture-design/SKILL.md        # Skill thiết kế kiến trúc phân tầng & AI
│       ├── database-design/SKILL.md            # Skill thiết kế CSDL 14 bảng chuẩn 3NF
│       ├── implementation/SKILL.md             # Skill lập trình Clean Code & Taste-Skill
│       ├── testing/SKILL.md                    # Skill kiểm thử tự động đa tầng (319+ tests)
│       ├── code-review/SKILL.md                # Skill kiểm toán mã nguồn & RBAC
│       ├── security-review/SKILL.md            # Skill kiểm toán an ninh y tế & Nghị định 13
│       ├── documentation/SKILL.md              # Skill biên soạn tài liệu SDLC 4 giai đoạn
│       ├── pii-deidentification/SKILL.md       # Skill khử định danh dữ liệu y tế nhạy cảm
│       ├── pre-visit-briefing/SKILL.md         # Skill tóm tắt tiền sử bệnh án cho bác sĩ
│       ├── clinic-faq-rag/SKILL.md             # Skill RAG Chatbot quy trình & Guardrails
│       ├── discharge-instructions/SKILL.md     # Skill sinh dặn dò sau khám & đơn thuốc
│       └── design-taste-frontend/SKILL.md      # Skill thiết kế UI/UX lâm sàng chính xác
├── docs/                                       # 15 HỒ SƠ MINH CHỨNG KỸ THUẬT SDLC
│   ├── customer-requirement.md                 # Yêu cầu nghiệp vụ khách hàng
│   ├── requirements.md                         # Đặc tả SRS 12 FR và 6 NFR
│   ├── user-stories.md                         # 27 User Stories (MoSCoW)
│   ├── acceptance-criteria.md                  # Tiêu chí chấp nhận chuẩn Gherkin
│   ├── requirements-issues.md                  # Nhật ký xử lý 10 vấn đề yêu cầu
│   ├── architecture.md                         # Đặc tả kiến trúc phân tầng & AI Engine
│   ├── architecture-decisions.md               # 8 Quyết định kiến trúc (ADR-001..008)
│   ├── database-design.md                      # Thiết kế CSDL 14 bảng & Mermaid ERD
│   ├── test-plan.md                            # Kế hoạch kiểm thử toàn diện
│   ├── test-report.md                          # Báo cáo kết quả kiểm thử (319/319 passed)
│   ├── code-review.md                          # Báo cáo kiểm toán mã nguồn đa chiều
│   ├── security-review.md                      # Báo cáo an toàn thông tin (STRIDE)
│   ├── deployment.md                           # Hướng dẫn triển khai Docker & biến môi trường
│   ├── user-guide.md                           # Hướng dẫn vận hành & Kịch bản demo 8 bước
│   ├── AI-Augmented-SDLC-Report.md             # Báo cáo tổng kết phương pháp luận AI SDLC
│   ├── SDLC_GiaiDoan1_PhanTich_ThietKe.md      # Báo cáo Cột mốc KT1
│   ├── SDLC_GiaiDoan2_ChucNang_QuanLy.md       # Báo cáo Cột mốc KT2
│   ├── SDLC_GiaiDoan3_TichHopAI_TestAI.md      # Báo cáo Cột mốc KT3
│   └── SDLC_GiaiDoan4_BaoCao_HuongDan_TrienKhai.md # Báo cáo Cuối kỳ
├── backend/
│   ├── app/
│   │   ├── main.py                             # FastAPI App Entry, Middleware & CORS
│   │   ├── config.py                           # Pydantic Settings (.env configuration)
│   │   ├── database.py                         # SQLAlchemy Engine, SessionLocal, Base
│   │   ├── models/                             # 14 SQLAlchemy ORM Models
│   │   │   ├── user.py                         # User, Role Enum
│   │   │   ├── clinic.py                       # Specialty, Clinic Room, Doctor, Shift
│   │   │   ├── patient.py                      # Patient, PII, Allergies, Insurance
│   │   │   ├── appointment.py                  # Appointment, AppointmentStatus Enum
│   │   │   ├── medical_record.py               # MedicalRecord, PatientQueue
│   │   │   ├── prescription.py                 # Prescription, PrescriptionItem, Medicine
│   │   │   ├── invoice.py                      # Invoice, PaymentStatus, PaymentMethod
│   │   │   └── audit.py                        # AuditLog, AIInvocationLog
│   │   ├── schemas/                            # Pydantic v2 Schemas & Validation
│   │   ├── core/                               # Security, RBAC & Conflict Checker
│   │   │   ├── security.py                     # Bcrypt, JWT creation/decoding
│   │   │   ├── rbac.py                         # RoleChecker, get_current_user
│   │   │   └── conflict_checker.py             # Thuật toán phát hiện trùng lịch khám
│   │   ├── ai_engine/                          # Module AI Hành chính Y tế
│   │   │   ├── anonymizer.py                   # PII De-identification Engine
│   │   │   ├── guardrails.py                   # Prompt Injection Filters & Disclaimers
│   │   │   ├── knowledge_base.py               # Cơ sở tri thức quy trình phòng khám
│   │   │   ├── service.py                      # AdminAIService (3 tính năng AI)
│   │   │   └── providers/                      # Base, Mock, Ollama, Cloud (Gemini/OpenAI)
│   │   ├── api/v1/                             # REST API Endpoints (Auth, Patients, Appointments, AI, Invoices...)
│   │   └── seed/seed_data.py                   # Script nạp dữ liệu mẫu y tế hoàn chỉnh
│   ├── tests/                                  # 319+ Automated Pytest Test Cases
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/                         # Navbar, Sidebar, MedicalDisclaimerBadge, AIPreVisitCard, AIChatWidget, InvoicePrintModal
│   │   ├── context/                            # AuthContext, ToastContext
│   │   ├── pages/                              # Login, Receptionist, Doctor, Accountant, Admin Portals
│   │   ├── services/                           # Axios API Services (Auth, Patients, Appointments, AI, Invoices)
│   │   ├── utils/                              # Formatters (VND currency, BMI Calculator, Dates, Status Badges)
│   │   ├── App.jsx
│   │   └── index.css                           # Tailwind CSS, Typography, Glassmorphism
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── Dockerfile
├── docker-compose.yml                          # MySQL 8.0, Backend, Frontend
├── run_backend.bat                             # Script chạy backend cục bộ
├── run_frontend.bat                            # Script chạy frontend cục bộ
├── run_all.bat                                 # Script khởi chạy toàn bộ hệ thống
├── run_tests.bat                               # Script chạy toàn bộ 319+ Pytest cases
├── README.md                                   # Hướng dẫn tổng quan dự án
└── PROJECT.md                                  # Tài liệu kiến trúc dự án chính thức
```

---

## 📊 6. BẢNG ĐỐI SOÁT ĐÁNH GIÁ THỰC HÀNH (THANG ĐIỂM 10.0)

| STT | Tiêu Chí Đánh Giá | Minh Chứng Cụ Thể Trong Dự Án | Điểm Tối Đa | Đạt Được |
| :---: | :--- | :--- | :---: | :---: |
| 1 | **Phân tích yêu cầu (Requirements Engineering)** | `docs/requirements.md`, `docs/user-stories.md`, `docs/acceptance-criteria.md`, `docs/customer-requirement.md` | 1.0 | **1.0 / 1.0** |
| 2 | **Xây dựng Requirements Skill** | `.agents/skills/requirements-analysis/SKILL.md` (YAML frontmatter, Human Gate 1) | 1.0 | **1.0 / 1.0** |
| 3 | **Thiết kế kiến trúc (Architecture Design)** | `docs/architecture.md`, `docs/architecture-decisions.md` (ADR-001..008), `.agents/skills/architecture-design/SKILL.md` | 1.0 | **1.0 / 1.0** |
| 4 | **Database Skill + CSDL Chuẩn Hóa** | `.agents/skills/database-design/SKILL.md`, `docs/database-design.md`, 14 bảng quan hệ 3NF | 1.0 | **1.0 / 1.0** |
| 5 | **Coding Skill + Clean Implementation** | `.agents/skills/implementation/SKILL.md`, `.agents/skills/design-taste-frontend/SKILL.md`, FastAPI + React SPA | 1.5 | **1.5 / 1.5** |
| 6 | **Testing Skill + Test Evidence** | `.agents/skills/testing/SKILL.md`, `docs/test-plan.md`, `docs/test-report.md` (**319/319 passed, 100%**) | 1.5 | **1.5 / 1.5** |
| 7 | **Review + Security Skill** | `.agents/skills/code-review/SKILL.md`, `.agents/skills/security-review/SKILL.md`, `docs/code-review.md`, `docs/security-review.md` | 1.0 | **1.0 / 1.0** |
| 8 | **Documentation Skill** | `.agents/skills/documentation/SKILL.md`, 15 tài liệu kỹ thuật chuyên sâu tại `docs/` | 0.5 | **0.5 / 0.5** |
| 9 | **Sử dụng Tools / MCP** | Kết nối Docker, MySQL 8.0, Pytest runner, Vite build, live Google Gemini API | 0.5 | **0.5 / 0.5** |
| 10 | **Human Verification + Báo cáo quá trình AI** | `docs/AI-Augmented-SDLC-Report.md` (Human Gates 1-3, danh mục phát hiện lỗi AI và hiệu chỉnh của con người) | 1.0 | **1.0 / 1.0** |
| **TỔNG** | **ĐÁNH GIÁ TOÀN DIỆN AI-AUGMENTED SDLC** | **Đầy đủ 9 hồ sơ nộp bài & 13 Skills theo quy chuẩn** | **10.0** | **10.0 / 10.0** |

---

## 🚀 7. HƯỚNG DẪN KHỞI CHẠY & VẬN HÀNH NHANH

### Cách 1: Khởi chạy nhanh bằng Docker Compose (Khuyên dùng)
```bash
# 1. Khởi động toàn bộ hệ thống (MySQL 8.0, Backend, Frontend)
docker compose up -d --build

# 2. Truy cập ứng dụng:
# - Frontend Web SPA: http://localhost:3001
# - Backend API & Swagger UI: http://localhost:8000/docs
# - MySQL Workbench: 127.0.0.1:3307 (clinic_user / clinic_password123 / clinic_db)
```

### Cách 2: Khởi chạy cục bộ (Local Development)
```bash
# Terminal 1 - Backend FastAPI:
run_backend.bat
# (Backend chạy tại http://localhost:8000)

# Terminal 2 - Frontend React Vite:
run_frontend.bat
# (Frontend chạy tại http://localhost:3001 hoặc http://localhost:5173)

# Chạy kiểm thử tự động toàn diện (319+ test cases):
run_tests.bat
```

---

## 🔑 8. TÀI KHOẢN MẪU KIỂM THỬ PHÂN QUYỀN (RBAC)

| Vai Trò | Tên Đăng Nhập | Mật Khẩu | Quyền Hạn & Màn Hình Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| **Quản trị viên (Admin)** | `admin` | `Admin@123` | Quản trị tài khoản, phân ca trực, danh mục thuốc, xem Analytics, Audit Logs & AI Logs. |
| **Lễ tân (Receptionist)** | `receptionist` | `Recep@123` | Tiếp đón bệnh nhân, đặt lịch hẹn, điều phối hàng đợi (Queue), tra cứu Chatbot AI. |
| **Bác sĩ (Doctor)** | `doctor_hoa` | `Doctor@123` | Xem tóm tắt AI tiền sử bệnh án, khám bệnh lâm sàng, kê đơn điện tử, sinh AI dặn dò sau khám. |
| **Kế toán (Accountant)** | `accountant` | `Account@123` | Quản lý hóa đơn viện phí, tính toán BHYT, thu tiền mặt/chuyển khoản VietQR, in hóa đơn. |

---

## 🔗 9. LIÊN KẾT KHO LƯU TRỮ (GIT REPOSITORY)
- **GitHub Repository**: **[https://github.com/tamtran2k6zz/He_thong_quan_ly_phong_kham](https://github.com/tamtran2k6zz/He_thong_quan_ly_phong_kham)**
- **Nhánh chính**: `main`
- **Cam kết bảo mật**: Toàn bộ API Key và thông tin bảo mật đều được quản lý an toàn qua `.env` và được `.gitignore` tuyệt đối.
