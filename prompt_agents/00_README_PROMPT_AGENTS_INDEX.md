# TỔNG MỤC LỤC BỘ PROMPTS ĐIỀU PHỐI AI AGENT (CODEX PROMPTS ARCHIVE)
## HỆ THỐNG QUẢN LÝ PHÒNG KHÁM ĐA KHOA THÔNG MINH TÍCH HỢP TRỢ LÝ AI HÀNH CHÍNH (CMS-AI)
### Đề tài Thực hành Môn học: Ứng dụng Trí tuệ Nhân tạo - AI-Augmented SDLC
**Nhóm thực hiện:** Nhóm 07  
* **Đinh Gia Bảo (Trưởng nhóm)**
* **Trần Đặng Công Tâm**  
**Thời gian thực hiện:** 27/07/2026 – 27/09/2026 (9 tuần)

---

## 1. MỤC ĐÍCH VÀ CƠ SỞ KHOA HỌC

Trong phương pháp luận **AI-Augmented SDLC**, AI Agent (Codex / Claude / GPT-4o) không đơn thuần là công cụ sinh code (code generation), mà được tổ chức thành một thực thể thực hiện các quy trình kỹ thuật phần mềm có kiểm soát thông qua cấu trúc 4 trụ cột:

```
+---------------------------------------------------------------------------------------------------+
|                                 MÔ HÌNH VẬN HÀNH AI AGENT TRONG SDLC                              |
+---------------------------------------------------------------------------------------------------+
|  1. CODEX (AI Agent)         : Kỹ sư/Chuyên viên AI thực thi các vai trò tư duy nghiệp vụ.        |
|  2. SKILL (Standard SOP)     : Bản quy chuẩn quy trình, tiêu chuẩn kỹ thuật (.agents/skills/).    |
|  3. TOOL (Environment Action): Công cụ thao tác file, kiểm thử, terminal, git, docker.            |
|  4. MCP (Context Protocol)   : Giao thức truy xuất schema CSDL, tài liệu và ngữ cảnh dự án.      |
|  *  HUMAN GATE (1 -> 3)      : Các điểm kiểm soát tối cao của Kỹ sư Con người (Human-in-the-Loop).|
+---------------------------------------------------------------------------------------------------+
```

Thư mục `prompt_agents/` này lưu trữ đầy đủ **100% các Prompt/Task đã giao cho AI Agent** xuyên suốt 4 giai đoạn của vòng đời SDLC, tương ứng với toàn bộ **15 Kỹ năng (Skills)** và **hơn 20 Artifacts** đã được tạo ra trong dự án.

---

## 2. MA TRẬN ÁNH XẠ PROMPT - SKILL - ARTIFACT - HUMAN GATE

| STT | Tên File Prompt trong `prompt_agents/` | Kỹ năng Liên quan (`.agents/skills/`) | Sản phẩm Đầu ra (Artifacts Tạo ra) | Cổng Kiểm soát Con người |
| :---: | :--- | :--- | :--- | :---: |
| **01** | `01_prompt_requirements_analysis.md` | `requirements-analysis` | `docs/customer-requirement.md`, `docs/requirements.md`, `docs/user-stories.md`, `docs/acceptance-criteria.md`, `docs/requirements-issues.md` | **Human Gate 1** (Bác bỏ AI tự chẩn đoán) |
| **02** | `02_prompt_architecture_design.md` | `architecture-design` | `docs/architecture.md`, `docs/architecture-decisions.md` (ADR-001..ADR-005) | **Human Gate 2** (Kiến trúc 3 lớp AI an toàn) |
| **03** | `03_prompt_database_design.md` | `database-design` | `docs/database-design.md`, Schema 14 bảng 3NF, Indexes tối ưu xung đột lịch | **Human Gate 2** (Toàn vẹn khóa ngoại & ACID) |
| **04** | `04_prompt_diagram_design.md` | `diagram-design` | `docs/thiet-ke-huong-doi-tuong-class-diagram.md`, Sơ đồ Use Case, Class, Sequence, Activity, State | **Human Gate 1 & 2** (Ranh giới Actor & Class OOD) |
| **05** | `05_prompt_implementation_fullstack.md` | `implementation` | Mã nguồn FastAPI Backend (`backend/app/`), React SPA Frontend (`frontend/src/`), Seed data | **Human Gate 2** (Xử lý transaction viện phí) |
| **06** | `06_prompt_pii_deidentification.md` | `pii-deidentification` | Module `backend/app/ai/anonymizer.py` (Khử sạch CCCD, SĐT, BHYT) | **Human Gate 3** (Kiểm chuẩn không rò rỉ PII) |
| **07** | `07_prompt_pre_visit_briefing.md` | `pre-visit-briefing` | Service `backend/app/ai/pre_visit.py`, API tóm tắt hồ sơ 10 giây cho bác sĩ | **Human Gate 3** (Làm nổi bật cảnh báo dị ứng) |
| **08** | `08_prompt_clinic_faq_rag.md` | `clinic-faq-rag` | Service `backend/app/ai/faq_chatbot.py`, Guardrail chặn câu hỏi chẩn đoán | **Human Gate 1 & 3** (Chặn Jailbreak & Disclaimer) |
| **09** | `09_prompt_discharge_instructions.md` | `discharge-instructions` | Service `backend/app/ai/discharge.py`, Sinh bảng lịch uống thuốc 4 bữa | **Human Gate 3** (Bác sĩ bắt buộc duyệt trước khi in) |
| **10** | `10_prompt_design_taste_frontend.md` | `design-taste-frontend` | Bộ Clinical UI Design Tokens, Typography, Bảng điều khiển 4 vai trò | **Human Gate 2** (Chống AI-slop, công thái học y tế) |
| **11** | `11_prompt_testing_automation.md` | `testing` | `docs/test-plan.md`, `docs/test-report.md`, Bộ 319+ Unit/Integration Tests | **Human Gate 2** (Bảo đảm 100% test pass) |
| **12** | `12_prompt_code_review.md` | `code-review` | `docs/code-review.md`, Báo cáo kiểm toán mã nguồn đa chiều | **Human Gate 2** (Phân loại rủi ro CRITICAL/HIGH) |
| **13** | `13_prompt_security_review.md` | `security-review` | `docs/security-review.md`, Báo cáo an toàn thông tin OWASP & Nghị định 13 | **Human Gate 2 & 3** (Phòng thủ Prompt Injection) |
| **14** | `14_prompt_documentation_sdlc_reports.md`| `documentation` | `docs/Reports/AI-Augmented-SDLC-Report.md`, 4 Báo cáo SDLC, `user-guide.md`, `deployment.md` | **Human Gate 1..3** (Minh chứng AI và đối soát) |
| **15** | `15_prompt_professional_writing.md` | `professional-writing` | Chuẩn hóa văn phong toàn bộ tài liệu học phần, loại bỏ từ ngữ sáo rỗng | **Human Gate 1..3** (Độ chính xác học thuật) |

---

## 3. CẤU TRÚC CHUẨN CỦA MỖI FILE PROMPT

Mỗi file trong thư mục này được cấu trúc nhất quán gồm 6 phần:
1. **Thông tin Ngữ cảnh & Mục tiêu (Context & Objectives):** Xác định giai đoạn SDLC, đề tài CMS-AI, tác nhân con người.
2. **Vai trò AI Agent (Persona & Role):** Định vị chuyên môn cụ thể của Agent (BA Agent, Architect Agent, Security Auditor Agent...).
3. **Kỹ năng & Ràng buộc Kỹ thuật (Skills & Technical Guardrails):** Trích dẫn SKILL.md và các điều cấm kỵ (ví dụ: cấm AI tự chẩn đoán bệnh tật).
4. **Nội dung Prompt Giao việc Chi tiết (Exact Master Prompt):** Toàn văn câu lệnh/nhiệm vụ giao cho Agent thực thi.
5. **Sản phẩm Artifacts Kết xuất (Generated Artifacts):** Danh mục file mã nguồn, file tài liệu markdown hoặc sơ đồ do Agent sinh ra.
6. **Nhận xét Kiểm chứng & Hiệu chỉnh của Con người (Human Verification & Correction Log):** Ghi rõ lỗi AI mắc phải (Hallucination) và cách kỹ sư con người can thiệp sửa đổi.
