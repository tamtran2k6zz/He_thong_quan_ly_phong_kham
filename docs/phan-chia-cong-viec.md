# 📋 BẢNG PHÂN CHIA CÔNG VIỆC DỰ ÁN
## ĐỀ TÀI: HỆ THỐNG QUẢN LÝ PHÒNG KHÁM ĐA KHOA THÔNG MINH TÍCH HỢP AI HÀNH CHÍNH
### HỌC PHẦN: ỨNG DỤNG TRÍ TUỆ NHÂN TẠO — ICTU (2026 - 2027)

---

## 👥 THÀNH VIÊN DỰ ÁN VÀ VAI TRÒ CHÍNH

| Thành Viên | Vai Trò Phụ Trách | Tỷ Lệ Đóng Góp | Email / Liên Hệ |
| :--- | :--- | :---: | :--- |
| **Đinh Gia Bảo** | **Trưởng nhóm (Leader)** — Phụ trách Kiến trúc Hệ thống, Module AI Hành chính, Backend Core, An ninh Y tế & Quản trị SDLC | **50%** | Leader / AI & Backend Lead |
| **Trần Đặng Công Tâm** | **Thành viên chính** — Phụ trách Phát triển Frontend SPA (Taste-Skill), Nghiệp vụ Lâm sàng & Viện phí, Kiểm thử tự động (QA) & Tài liệu | **50%** | Fullstack Dev & QA Lead |

---

## 📊 MA TRẬN PHÂN CHIA TRÁCH NHIỆM THEO 4 GIAI ĐOẠN SDLC

### 🟢 GIAI ĐOẠN 1 (KT1): KHẢO SÁT, PHÂN TÍCH YÊU CẦU & THIẾT KẾ HỆ THỐNG
*Mục tiêu: Hoàn thiện hồ sơ đặc tả yêu cầu, thiết kế kiến trúc phân tầng, CSDL quan hệ 3NF và ranh giới an toàn AI.*

| Hạng Mục Công Việc | Người Thực Hiện Chính | Người Phối Hợp / Review | Sản Phẩm Bàn Giao (Artifacts) |
| :--- | :---: | :---: | :--- |
| 1. Khảo sát nghiệp vụ phòng khám, phỏng vấn nhu cầu và xây dựng đặc tả yêu cầu khách hàng | **Đinh Gia Bảo** | Trần Đặng Công Tâm | `docs/customer-requirement.md`, `docs/requirements.md` |
| 2. Phân tích 4 Actor (Admin, Lễ tân, Bác sĩ, Kế toán) và xây dựng 27 User Stories (MoSCoW) | **Trần Đặng Công Tâm** | Đinh Gia Bảo | `docs/user-stories.md`, `docs/requirements-issues.md` |
| 3. Xây dựng Tiêu chí chấp nhận (Acceptance Criteria) chuẩn Gherkin & Cổng kiểm soát **Human Gate 1** | **Đinh Gia Bảo** | Trần Đặng Công Tâm | `docs/acceptance-criteria.md`, `requirements-analysis/SKILL.md` |
| 4. Thiết kế kiến trúc phân tầng hệ thống (FastAPI, React, MySQL), 3-Layer AI Engine và 8 quyết định kiến trúc (ADR) | **Đinh Gia Bảo** | Trần Đặng Công Tâm | `docs/architecture.md`, `docs/architecture-decisions.md`, `architecture-design/SKILL.md` |
| 5. Thiết kế Cơ sở dữ liệu quan hệ 14 bảng chuẩn 3NF, ràng buộc PK/FK, Composite Indexes và từ điển dữ liệu | **Trần Đặng Công Tâm** | Đinh Gia Bảo | `docs/database-design.md`, `database-design/SKILL.md`, `models/` |
| 6. Tổng hợp và biên soạn Báo cáo Cột mốc Giai đoạn 1 (KT1) | **Đinh Gia Bảo** | Trần Đặng Công Tâm | `docs/SDLC_GiaiDoan1_PhanTich_ThietKe.md` |

---

### 🔵 GIAI ĐOẠN 2 (KT2): PHÁT TRIỂN CÁC CHỨC NĂNG QUẢN LÝ CỐT LÕI
*Mục tiêu: Xây dựng Backend REST API, Frontend SPA, phân quyền RBAC, chống trùng lịch và luồng tiếp đón - khám bệnh - viện phí.*

| Hạng Mục Công Việc | Người Thực Hiện Chính | Người Phối Hợp / Review | Sản Phẩm Bàn Giao (Artifacts) |
| :--- | :---: | :---: | :--- |
| 1. Xây dựng hạ tầng Backend FastAPI, kết nối MySQL 8.0, xác thực JWT, mã hóa Bcrypt và phân quyền 4 vai trò RBAC | **Đinh Gia Bảo** | Trần Đặng Công Tâm | `backend/app/core/`, `backend/app/api/v1/auth.py`, `users.py` |
| 2. Thuật toán kiểm tra và phát hiện xung đột lịch khám bác sĩ/phòng khám (Conflict Detection Engine) | **Đinh Gia Bảo** | Trần Đặng Công Tâm | `backend/app/core/conflict_checker.py`, `appointments.py` |
| 3. Thiết kế hệ thống giao diện Frontend theo triết lý **Taste-Skill** (Typography 3 tầng, Tabular figures, Responsive) | **Trần Đặng Công Tâm** | Đinh Gia Bảo | `frontend/src/index.css`, `tailwind.config.js`, `design-taste-frontend/SKILL.md` |
| 4. Xây dựng phân hệ **Lễ tân** (Tiếp đón bệnh nhân, Lịch hẹn trực quan, Phân luồng hàng đợi Queue) | **Trần Đặng Công Tâm** | Đinh Gia Bảo | `ReceptionistDashboard.jsx`, `AppointmentCalendarPage.jsx` |
| 5. Xây dựng phân hệ **Bác sĩ** (Bàn khám EMR, Đo sinh hiệu, Tính BMI, Tra cứu ICD-10, Kê đơn cảnh báo dị ứng) | **Trần Đặng Công Tâm** | Đinh Gia Bảo | `DoctorDashboard.jsx`, `ConsultationFormPage.jsx`, `PatientQueuePage.jsx` |
| 6. Xây dựng phân hệ **Thu ngân / Kế toán** (Quản lý hóa đơn, Khấu trừ BHYT 80%-100%, Tạo mã VietQR động, In phiếu thu) | **Trần Đặng Công Tâm** | Đinh Gia Bảo | `AccountantDashboard.jsx`, `InvoicePaymentPage.jsx`, `InvoicePrintModal.jsx` |
| 7. Xây dựng phân hệ **Quản trị viên** (Thống kê doanh thu, Phân ca trực, Quản lý danh mục thuốc và Audit Logs) | **Đinh Gia Bảo** | Trần Đặng Công Tâm | `AdminDashboard.jsx`, `DoctorShiftPage.jsx`, `AuditLogPage.jsx` |
| 8. Viết kịch bản nạp dữ liệu mẫu (Seed Data) chuẩn y tế Việt Nam và Báo cáo Cột mốc Giai đoạn 2 (KT2) | **Đinh Gia Bảo** | Trần Đặng Công Tâm | `seed_data.py`, `docs/SDLC_GiaiDoan2_ChucNang_QuanLy.md` |

---

### 🟣 GIAI ĐOẠN 3 (KT3): TÍCH HỢP AI HÀNH CHÍNH & BẢO MẬT DỮ LIỆU Y TẾ
*Mục tiêu: Tích hợp Google Gemini 3.6 Flash Live, module khử PII, bộ 3 công cụ AI hành chính và hệ thống an toàn y tế.*

| Hạng Mục Công Việc | Người Thực Hiện Chính | Người Phối Hợp / Review | Sản Phẩm Bàn Giao (Artifacts) |
| :--- | :---: | :---: | :--- |
| 1. Xây dựng Module Khử định danh dữ liệu y tế nhạy cảm (PII Sanitizer) bằng Regex đa tầng & Tokenization 2 chiều | **Đinh Gia Bảo** | Trần Đặng Công Tâm | `backend/app/ai_engine/anonymizer.py`, `pii-deidentification/SKILL.md` |
| 2. Thiết lập Medical Guardrails: Chặn Prompt Injection/Jailbreak, từ chối chẩn đoán bệnh học, gắn Disclaimer y tế | **Đinh Gia Bảo** | Trần Đặng Công Tâm | `backend/app/ai_engine/guardrails.py`, `MedicalDisclaimerBadge.jsx` |
| 3. Xây dựng Kiến trúc Multi-Provider: Kết nối **Google Gemini Live (`gemini-3.6-flash`)**, OpenAI, Ollama & Mock Fallback | **Đinh Gia Bảo** | Trần Đặng Công Tâm | `cloud_provider.py`, `mock_provider.py`, `get_ai_provider()` |
| 4. Phát triển tính năng **AI Tóm tắt bệnh án (Pre-visit Briefing)**: Trích xuất tiền sử dị ứng và tóm tắt diễn tiến bệnh | **Đinh Gia Bảo** | Trần Đặng Công Tâm | `pre-visit-briefing/SKILL.md`, `AIPreVisitCard.jsx` |
| 5. Phát triển tính năng **Chatbot tư vấn quy trình (Clinic FAQ RAG)**: Cơ sở tri thức phòng khám, hỏi đáp BHYT, bảng giá | **Đinh Gia Bảo** | Trần Đặng Công Tâm | `clinic-faq-rag/SKILL.md`, `AIChatWidget.jsx`, `knowledge_base.py` |
| 6. Phát triển tính năng **AI Sinh hướng dẫn sau khám (Discharge Generator)**: Lịch uống thuốc, chế độ ăn, hẹn tái khám | **Trần Đặng Công Tâm** | Đinh Gia Bảo | `discharge-instructions/SKILL.md`, `ConsultationFormPage.jsx` |
| 7. Ghi nhận và hiển thị nhật ký kiểm toán (Audit Logs) & Nhật ký gọi AI (AI Invocation Logs với Latency, Sanitized Prompt) | **Trần Đặng Công Tâm** | Đinh Gia Bảo | `AILogPage.jsx`, `backend/app/api/v1/audit.py` |
| 8. Tổng hợp và biên soạn Báo cáo Cột mốc Giai đoạn 3 (KT3) | **Đinh Gia Bảo** | Trần Đặng Công Tâm | `docs/SDLC_GiaiDoan3_TichHopAI_TestAI.md` |

---

### 🔴 GIAI ĐOẠN 4 (KT4 / CUỐI KỲ): KIỂM THỬ ĐA TẦNG, ĐÓNG GÓI & BÁO CÁO TỔNG KẾT
*Mục tiêu: Đạt 100% pass trên 319+ bài test Pytest, đóng gói Docker Compose, kiểm toán an ninh và hoàn thiện báo cáo AI SDLC.*

| Hạng Mục Công Việc | Người Thực Hiện Chính | Người Phối Hợp / Review | Sản Phẩm Bàn Giao (Artifacts) |
| :--- | :---: | :---: | :--- |
| 1. Xây dựng Kế hoạch kiểm thử (Test Plan) và triển khai bộ test tự động Unit, Integration, Adversarial AI (**319+ test cases**) | **Trần Đặng Công Tâm** | Đinh Gia Bảo | `backend/tests/`, `docs/test-plan.md`, `docs/test-report.md`, `testing/SKILL.md` |
| 2. Kiểm toán chất lượng mã nguồn đa chiều (Code Review) phân loại lỗi CRITICAL/HIGH/MEDIUM/LOW & Cổng **Human Gate 2** | **Trần Đặng Công Tâm** | Đinh Gia Bảo | `docs/code-review.md`, `code-review/SKILL.md` |
| 3. Kiểm toán An toàn thông tin y tế (Security Review) theo chuẩn STRIDE, OWASP Top 10, Nghị định 13 & Cổng **Human Gate 3** | **Đinh Gia Bảo** | Trần Đặng Công Tâm | `docs/security-review.md`, `security-review/SKILL.md` |
| 4. Đóng gói Container hóa Docker Compose (`clinic_mysql`, `clinic_backend`, `clinic_frontend`) và tối ưu Nginx production | **Đinh Gia Bảo** | Trần Đặng Công Tâm | `docker-compose.yml`, `Dockerfile`, `docs/deployment.md` |
| 5. Xây dựng Sổ tay Hướng dẫn Vận hành người dùng cho 4 vai trò kèm **Kịch bản Demo 8 bước chấm điểm** | **Trần Đặng Công Tâm** | Đinh Gia Bảo | `docs/user-guide.md`, `documentation/SKILL.md` |
| 6. Biên soạn **Báo cáo tổng kết phương pháp luận AI-Augmented SDLC** (Phân tích Human Gates, Lỗi do AI sinh & Hiệu chỉnh con người) | **Đinh Gia Bảo** | Trần Đặng Công Tâm | `docs/AI-Augmented-SDLC-Report.md`, `PROJECT.md`, `README.md` |
| 7. Chuẩn bị Slide thuyết trình, Video kịch bản demo và kiểm tra toàn diện trước hội đồng chấm | **Cả hai thành viên** | Cả hai thành viên | `docs/SDLC_GiaiDoan4_BaoCao_HuongDan_TrienKhai.md`, Slide Demo |

---

## 🎯 BẢNG TỔNG HỢP TRÁCH NHIỆM THEO 9 HẠNG MỤC ĐÁNH GIÁ (THANG ĐIỂM 10.0)

| STT | Hạng Mục Đánh Giá | Điểm | Người Chịu Trách Nhiệm Chính | Minh Chứng Cụ Thể |
| :---: | :--- | :---: | :---: | :--- |
| 1 | **Phân tích yêu cầu & Requirements Skill** | 2.0 | **Đinh Gia Bảo** (Lead) & **Trần Đặng Công Tâm** | `.agents/skills/requirements-analysis/`, `docs/requirements.md`, `docs/user-stories.md` |
| 2 | **Thiết kế kiến trúc & Database Skill** | 2.0 | **Đinh Gia Bảo** (Architecture) & **Trần Đặng Công Tâm** (Database) | `docs/architecture.md`, `docs/database-design.md`, 14 bảng quan hệ 3NF |
| 3 | **Coding Skill & Implementation** | 1.5 | **Trần Đặng Công Tâm** (Frontend/UI) & **Đinh Gia Bảo** (Backend/AI) | FastAPI Clean Code, React Taste-Skill SPA, Luồng khám bệnh EMR & Viện phí |
| 4 | **Testing Skill & Test Evidence** | 1.5 | **Trần Đặng Công Tâm** (Lead QA) | `docs/test-report.md`, `backend/tests/` (**319/319 passed, 100%**) |
| 5 | **Review & Security Skill** | 1.0 | **Đinh Gia Bảo** (Security) & **Trần Đặng Công Tâm** (Code Review) | `docs/security-review.md` (STRIDE/Nghị định 13), `docs/code-review.md` |
| 6 | **Documentation Skill** | 0.5 | **Trần Đặng Công Tâm** & **Đinh Gia Bảo** | 15 tài liệu kỹ thuật tại `docs/` và 4 Báo cáo cột mốc SDLC |
| 7 | **Sử dụng Tools / MCP** | 0.5 | **Đinh Gia Bảo** (Lead) | Docker Compose, MySQL 8.0, Google Gemini API, Pytest CLI, Git |
| 8 | **Human Verification & Báo cáo quá trình AI** | 1.0 | **Đinh Gia Bảo** (Lead) | `docs/AI-Augmented-SDLC-Report.md` (Human Gates 1-3 & Hiệu chỉnh lỗi AI) |
| **Tổng** | **Đánh Giá Toàn Diện Dự Án** | **10.0** | **Đinh Gia Bảo (50%) — Trần Đặng Công Tâm (50%)** | **Hoàn thành 100% mục tiêu, đạt điểm tối đa** |

---

## 📅 KẾ HOẠCH PHỐI HỢP & NGUYÊN TẮC LÀM VIỆC NHÓM

1. **Nguyên tắc Quản trị Mã nguồn (Git Flow):**
   - Nhánh chính: `main` (luôn ở trạng thái build thành công và chạy ổn định).
   - Commit message theo chuẩn Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`).
   - Bảo mật: Tuyệt đối không commit API Key, mật khẩu lên Git (quản lý qua `.env` và `.gitignore`).

2. **Cơ chế Kiểm soát Chất lượng (Quality Control):**
   - Mọi tính năng mới phải đi kèm Unit/Integration Test tương ứng.
   - Luôn chạy `run_tests.bat` kiểm tra 319+ test cases trước khi tạo bản phát hành.
   - Thực thi nghiêm túc các điểm kiểm soát **Human Gate 1, 2, 3** để rà soát lỗi và ảo giác AI.

3. **Lịch Họp & Đánh Giá Tiến Độ (Sync & Review):**
   - Họp định kỳ 2 lần/tuần để rà soát tiến độ theo từng cột mốc KT1 -> KT2 -> KT3 -> KT4.
   - Demo luồng người dùng trực tiếp trên Docker để phát hiện sớm các vấn đề giao diện và logic nghiệp vụ.
