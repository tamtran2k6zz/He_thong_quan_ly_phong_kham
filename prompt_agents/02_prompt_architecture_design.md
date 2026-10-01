# PROMPT GIAO VIỆC: THIẾT KẾ KIẾN TRÚC HỆ THỐNG Y TẾ PHÂN TẦNG & AI 3 LỚP
## Giai đoạn SDLC: Giai đoạn 1 – Architecture & System Design (KT1)
### Kỹ năng áp dụng: `.agents/skills/architecture-design/SKILL.md`

---

## 1. THÔNG TIN NGỮ CẢNH & MỤC TIÊU
* **Dự án:** Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp Trợ lý AI Hành chính (CMS-AI).
* **Đơn vị thực hiện:** Nhóm 07 (Đinh Gia Bảo - Trưởng nhóm, Trần Đặng Công Tâm).
* **Mục tiêu:** Thiết kế kiến trúc tổng thể phần mềm phân tầng hiện đại (Clean Architecture / Service Layering) kết hợp Vành đai An toàn AI 3 Lớp (3-Layer Administrative AI Engine), thuật toán toán học phát hiện xung đột lịch khám thời gian thực và lập hồ sơ 5 quyết định kiến trúc cốt lõi chuẩn ADR (Architectural Decision Records).

---

## 2. VAI TRÒ CỦA AI AGENT (PERSONA)
Bạn là **Chief Healthcare System Architect Agent (Kiến trúc sư Trưởng Hệ thống Y tế)**, chuyên gia thiết kế các hệ thống y tế chịu lỗi cao (Fault-tolerant EMR/HIS systems), thông thạo mô hình microservices/modular monolith, bảo mật API Gateway và kiến trúc RAG an toàn cho dữ liệu nhạy cảm.

---

## 3. RÀNG BUỘC KỸ THUẬT & QUY TẮC CỐT LÕI (GUARDRAILS)
1. **Phân tách trách nhiệm rạch ròi:** Tầng Giao tiếp (FastAPI Routers), Tầng Nghiệp vụ (Medical Services), Tầng AI (AI Engines) và Tầng Truy xuất Dữ liệu (SQLAlchemy ORM) phải độc lập hoàn toàn.
2. **Kiến trúc Vành đai AI 3 Lớp (3-Layer AI Perimeter):** 
   - Lớp 1 (PII Anonymization Filter): Khử sạch mọi thông tin định danh bệnh nhân trước khi prompt rời khỏi hệ thống.
   - Lớp 2 (Ethical Guardrail & Output Formatter): Chặn câu hỏi chẩn đoán và nhúng Medical Disclaimer.
   - Lớp 3 (Multi-Provider Orchestrator): Điều phối Gemini / OpenAI / Ollama và tự động kích hoạt **Deterministic Mock AI Engine** khi ngắt kết nối mạng.
3. **Động cơ kiểm tra xung đột lịch:** Sử dụng giải thuật giao thoa khoảng thời gian toán học: `Overlap(A, B) <=> (Start_A < End_B) and (End_A > Start_B)`.
4. **Chuẩn hóa hồ sơ ADR:** Các quyết định kiến trúc lớn phải ghi nhận rõ bối cảnh, các giải pháp cân nhắc, quyết định chọn lựa và hệ quả kỹ thuật (Trade-offs).

---

## 4. NỘI DUNG MASTER PROMPT ĐÃ GIAO CHO AI AGENT

```markdown
Bạn hãy đóng vai trò là Chief Healthcare System Architect. Hãy thực hiện toàn diện quy trình Thiết kế Kiến trúc Hệ thống cho dự án CMS-AI của Nhóm 07:

BƯỚC 1: XÂY DỰNG SKILL THIẾT KẾ KIẾN TRÚC (.agents/skills/architecture-design/SKILL.md)
Tạo file SKILL.md định nghĩa quy chuẩn kiến trúc phân tầng y tế: Phân tách 5 tầng hệ thống (Client Tier, API Gateway Tier, Medical Service Tier, 3-Layer AI Perimeter, Persistence Tier), giải thuật Conflict Detection và quy trình thẩm định kiến trúc.

BƯỚC 2: BIÊN SOẠN TÀI LIỆU ĐẶC TẢ KIẾN TRÚC TOÀN DIỆN (docs/architecture.md)
Trình bày chi tiết:
1. Tổng quan kiến trúc hệ thống (System Architecture Overview) kèm sơ đồ Mermaid trực quan.
2. Thiết kế Tầng Frontend SPA: React 18, Vite, Tailwind CSS, Lucide Icons, kiến trúc Role-based Routing theo 4 vai trò.
3. Thiết kế Tầng Backend API: FastAPI, Pydantic v2 validation, JWT Authentication Middleware, RFC 7807 Error Handling.
4. Thiết kế Chi tiết Vành đai An toàn AI Hành chính 3 Lớp:
   - Cơ chế hoạt động của PII Anonymizer (Regex-based).
   - Cơ chế Guardrail từ chối chẩn đoán y khoa tự động.
   - Cơ chế Multi-provider và thuật toán Fallback sang Mock Engine khi mất kết nối mạng.
5. Thuật toán kiểm tra xung đột lịch khám hai chiều: Kiểm tra trùng lịch Bác sĩ (Doctor Overlap) VÀ trùng buồng khám (Clinic Overlap).
6. Luồng dữ liệu (Data Flow Diagrams - DFD Level 0, Level 1) cho quy trình tiếp đón, khám bệnh, kê đơn và viện phí.

BƯỚC 3: XÂY DỰNG TẬP HỒ SƠ QUYẾT ĐỊNH KIẾN TRÚC CHUẨN ADR (docs/architecture-decisions.md)
Soạn thảo chi tiết 5 bản ghi Quyết định Kiến trúc (Architectural Decision Records) theo mẫu chuẩn y tế:
- ADR-001: Lựa chọn Kiến trúc Modular Monolith với FastAPI Backend và React SPA thay vì Microservices phân tán.
- ADR-002: Lựa chọn Cơ chế Vành đai AI 3 Lớp với Bộ khử định danh PII độc lập bảo vệ quyền riêng tư người bệnh.
- ADR-003: Xây dựng Giải thuật Phát hiện Xung đột Lịch khám hai chiều bảo đảm tính toàn vẹn thời gian thực.
- ADR-004: Tích hợp Deterministic Mock AI Engine làm cơ chế Fallback ngoại tuyến bảo đảm hệ thống vận hành 100% không phụ thuộc Internet.
- ADR-005: Lựa chọn CSDL Quan hệ kép (SQLite cho môi trường Dev/Test và MySQL/PostgreSQL cho Production).
```

---

## 5. SẢN PHẨM ARTIFACTS KẾT XUẤT
1. [`.agents/skills/architecture-design/SKILL.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/.agents/skills/architecture-design/SKILL.md)
2. [`docs/architecture.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/docs/architecture.md)
3. [`docs/architecture-decisions.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/docs/architecture-decisions.md)

---

## 6. KIỂM CHỨNG & HIỆU CHỈNH CỦA CON NGƯỜI (HUMAN GATE 2)
* **Lỗi do AI đề xuất:** AI ban đầu đề xuất thuật toán kiểm tra xung đột chỉ lọc theo `doctor_id`, dẫn đến kịch bản 2 bác sĩ khác nhau cùng được xếp lịch vào chung một buồng khám tại cùng một khung giờ.
* **Hành động hiệu chỉnh của Kỹ sư Con người:** Kỹ sư Trưởng đã can thiệp, yêu cầu thuật toán phải kiểm tra đồng thời trên cả 2 chiều: Xung đột ca trực Bác sĩ (`doctor_id`) VÀ Xung đột buồng khám (`clinic_id`), với công thức giao thoa mở toán học chặt chẽ.
