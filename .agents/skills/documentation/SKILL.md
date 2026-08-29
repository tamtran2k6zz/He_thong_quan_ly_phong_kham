---
name: documentation
description: Quy chuẩn biên soạn tài liệu học phần và báo cáo minh chứng 4 giai đoạn SDLC (Comprehensive 4-Stage SDLC Documentation Standards) cho Hệ thống CMS-AI kết hợp báo cáo tổng kết AI-Augmented SDLC.
objective: Cung cấp phương pháp luận và cấu trúc chuẩn cho Kỹ sư và AI Codex biên soạn bộ tài liệu kỹ thuật chất lượng cao, bao gồm 4 giai đoạn KT1-KT4, báo cáo minh chứng thực hành AI-Augmented SDLC, kịch bản demo và hướng dẫn sử dụng theo từng vai trò.
inputs:
  - Tài liệu đặc tả yêu cầu, kiến trúc, CSDL, kiểm thử và bảo mật đã nghiệm thu
  - Mã nguồn Backend và Frontend hoàn chỉnh
  - Dữ liệu minh chứng các lỗi do AI sinh ra và quá trình con người phát hiện, sửa lỗi
  - Cấu hình triển khai Docker Compose và các script chạy nhanh (.bat)
process:
  - 1. Lập kế hoạch tài liệu hóa đồng bộ theo 4 cột mốc SDLC (KT1 -> KT4)
  - 2. Biên soạn Báo cáo Giai đoạn 1 (KT1): Khảo sát, Phân tích 4 Actor, Use Case, ERD và Ranh giới Đạo đức AI
  - 3. Biên soạn Báo cáo Giai đoạn 2 (KT2): Kiến trúc Kỹ thuật, Mô hình RBAC, Thuật toán Trùng lịch và RESTful API
  - 4. Biên soạn Báo cáo Giai đoạn 3 (KT3): Tích hợp AI Hành chính, Khử PII, Thiết kế Prompt và Ma trận Test AI
  - 5. Biên soạn Báo cáo Giai đoạn 4 (KT4): Hướng dẫn Triển khai Docker, Vận hành và Hướng dẫn Sử dụng 4 Roles
  - 6. Biên soạn Báo cáo Tổng kết AI-Augmented SDLC (AI-Augmented-SDLC-Report.md & Human Gates 1-3)
  - 7. Rà soát tính nhất quán, đánh phiên bản (SemVer) và kích hoạt Human Gate 3
rules:
  - Mọi sơ đồ phân tích phải có cả định dạng văn bản / bảng biểu / ASCII song song với Mermaid
  - Mọi API endpoint đặc tả phải có đầy đủ Method, Path, Auth Header, Request Body và Response JSON mẫu
  - Tài liệu phải phản ánh 100% mã nguồn thực tế, tuyệt đối không chèn số liệu giả tạo hoặc chưa kiểm chứng
  - Không để sót các placeholder như TODO, TBD, hoặc nội dung chưa hoàn thiện trong tài liệu nộp bài
outputs:
  - docs/SDLC_GiaiDoan1_PhanTich_ThietKe.md (Tài liệu KT1)
  - docs/SDLC_GiaiDoan2_ChucNang_QuanLy.md (Tài liệu KT2)
  - docs/SDLC_GiaiDoan3_TichHopAI_TestAI.md (Tài liệu KT3)
  - docs/SDLC_GiaiDoan4_BaoCao_HuongDan_TrienKhai.md (Tài liệu KT4)
  - docs/AI-Augmented-SDLC-Report.md (Báo cáo tổng kết AI-Augmented SDLC)
  - README.md (Hướng dẫn tổng quan và khởi chạy dự án)
verification:
  - Kiểm tra tính đầy đủ mục lục và định dạng Markdown chuẩn mực
  - Đối chiếu 100% các ví dụ curl / JSON với mã nguồn API Backend thực tế
  - Xác nhận báo cáo tổng kết AI có đầy đủ minh chứng phát hiện lỗi AI và sửa lỗi của con người
  - Phê duyệt chính thức của Hội đồng Đánh giá và Giảng viên tại Human Gate 3
---

# Kỹ năng Biên soạn Tài liệu SDLC & Báo cáo Minh chứng AI (Documentation Skill)

## 1. Objective (Mục tiêu Kỹ năng)

Kỹ năng này định hình toàn bộ các quy chuẩn chuyên nghiệp, phương pháp luận và cấu trúc bắt buộc để Kỹ sư Phần mềm và AI Codex biên soạn bộ hồ sơ tài liệu học phần hoàn chỉnh cho **Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp Trợ lý AI Hành chính (CMS-AI)**.

Mục tiêu cốt lõi:
1. Chuẩn hóa 4 bộ tài liệu đặc tả kỹ thuật theo 4 giai đoạn phát triển phần mềm (SDLC KT1 đến KT4).
2. Xây dựng tài liệu hướng dẫn sử dụng chi tiết (User Guide) theo từng phân hệ giao diện của 4 nhóm vai trò (Admin, Lễ tân, Bác sĩ, Kế toán).
3. Biên soạn Báo cáo Tổng kết Mô hình Thực hành **AI-Augmented SDLC** (`docs/AI-Augmented-SDLC-Report.md`), minh chứng rõ ràng sự phối hợp giữa Codex - Skill - Tool - MCP, các điểm kiểm soát **Human Gate 1, 2, 3**, cùng danh mục các lỗi do AI sinh ra đã được con người phát hiện và hiệu chỉnh.
4. Đảm bảo tính nhất quán tuyệt đối giữa tài liệu mô tả và mã nguồn thực tế của dự án.

---

## 2. Terminology & Conceptual Model (Mô hình Khái niệm)

Trong không gian Tài liệu hóa Hệ thống:

```
+-----------------------------------------------------------------------------------------------+
|                                    MÔ HÌNH KHÁI NIỆM TÀI LIỆU HÓA                             |
+-----------------------------------------------------------------------------------------------+
|  1. CODEX (AI Agent)         : Kỹ sư Tài liệu Kỹ thuật (Technical Writer Agent). Biên soạn,   |
|                                tổng hợp số liệu, cấu trúc báo cáo và trích xuất sơ đồ.        |
|  2. SKILL (Procedural Standard): Quy chuẩn tài liệu 4 giai đoạn SDLC, mẫu báo cáo KT1-KT4,     |
|                                cấu trúc User Guide và khung báo cáo AI-Augmented SDLC (Skill).|
|  3. TOOL (Environment Action): Công cụ chuyển đổi định dạng, kiểm tra liên kết, sinh tài liệu |
|                                Markdown và đo lường độ hoàn thiện.                            |
|  4. MCP (Model Context Protocol): Giao thức trích xuất tự động thông tin cấu hình từ codebase. |
+-----------------------------------------------------------------------------------------------+
```

---

## 3. Inputs & Prerequisites (Đầu vào & Điều kiện Tiên quyết)

1. **Bộ tài liệu thiết kế & phân tích**: `docs/requirements.md`, `docs/architecture.md`, `docs/database-design.md`.
2. **Bộ báo cáo kiểm thử & an ninh**: `docs/test-report.md`, `docs/code-review.md`, `docs/security-review.md`.
3. **Mã nguồn và Docker Artifacts**: `docker-compose.yml`, scripts khởi chạy `.bat`.
4. **Nhật ký tương tác AI**: Lịch sử các quyết định, các trường hợp AI Hallucination đã được sửa đổi.

---

## 4. Execution Process (Quy trình Thực thi Từng bước)

```
[Bước 1: Kế hoạch 4 Cột mốc] ---> [Bước 2: Tài liệu KT1] ---> [Bước 3: Tài liệu KT2]
                                                                        |
[Bước 6: Báo cáo AI-Augmented] <--- [Bước 5: Tài liệu KT4] <--- [Bước 4: Tài liệu KT3]
           |
           v
[Bước 7: Kích hoạt Cổng Human Gate 3 (Final Release Sign-off)]
```

### Bước 1: Lập Kế hoạch Tài liệu hóa theo 4 Cột mốc SDLC

| Cột mốc | Tên Tài liệu Bắt buộc | Phạm vi & Nội dung Cốt lõi |
|:---:|---|---|
| **KT1** | `docs/SDLC_GiaiDoan1_PhanTich_ThietKe.md` | Khảo sát bài toán, 4 Actors, Use Case Diagram, Luồng khám khép kín, Sơ đồ ERD 14 bảng, Ranh giới đạo đức AI. |
| **KT2** | `docs/SDLC_GiaiDoan2_ChucNang_QuanLy.md` | Kiến trúc Backend/Frontend, Ma trận RBAC 4 vai trò, Thuật toán xung đột lịch khám, Đặc tả toàn bộ RESTful API. |
| **KT3** | `docs/SDLC_GiaiDoan3_TichHopAI_TestAI.md` | Kiến trúc AI 3 lớp, Bộ Regex khử PII Việt Nam, Thiết kế System Prompts, Ma trận 223+ Test Cases Pytest. |
| **KT4** | `docs/SDLC_GiaiDoan4_BaoCao_HuongDan_TrienKhai.md` | Triển khai Docker Compose, Hướng dẫn cài đặt/vận hành, Hướng dẫn sử dụng 4 Roles, Kịch bản Demo chấm điểm. |

### Bước 2: Biên soạn Tài liệu Giai đoạn 1 (KT1)
- **Khảo sát Thực trạng**: Nêu rõ 5 điểm nghẽn của phòng khám truyền thống (ùn tắc tiếp đón, quá tải tra cứu hồ sơ, sai sót kê đơn, thất thoát viện phí, rò rỉ dữ liệu).
- **Mô hình hóa 4 Actors**: Bảng phân vai chi tiết cho Admin, Receptionist, Doctor, Accountant.
- **Biểu đồ Use Case & Luồng Nghiệp vụ**: Sơ đồ Use case toàn cảnh và sơ đồ luồng lâm sàng 4 bước.
- **Thiết kế CSDL Quan hệ**: Sơ đồ ERD chi tiết và mô tả 14 bảng quan hệ.
- **Ranh giới Đạo đức AI**: Cam kết không tự chẩn đoán/kê đơn, luôn có cảnh báo miễn trừ y tế.

### Bước 3: Biên soạn Tài liệu Giai đoạn 2 (KT2)
- **Kiến trúc Kỹ thuật**: Sơ đồ phân tầng FastAPI Backend và React Vite Tailwind Frontend SPA.
- **Ma trận Phân quyền RBAC**: Bảng chi tiết quyền hạn trên từng nhóm endpoint API và cơ chế `RoleChecker`.
- **Thuật toán Xung đột Lịch**: Diễn giải toán học của điều kiện giao nhau $[S_1, E_1) \cap [S_2, E_2) \neq \emptyset$ và đoạn mã Python thực thi.
- **Đặc tả RESTful API**: Liệt kê đầy đủ các endpoint với Request/Response JSON mẫu, mã trạng thái HTTP chuẩn.

### Bước 4: Biên soạn Tài liệu Giai đoạn 3 (KT3)
- **Kiến trúc AI 3 Lớp**: Mô tả chi tiết Tầng Khử PII -> Tầng Guardrails & Disclaimer -> Tầng Multi-Provider & Mock Fallback.
- **Kỹ thuật Khử Định danh PII**: Bảng quy chuẩn Regex cho CCCD, SĐT, BHYT, Tên và Địa chỉ tại Việt Nam.
- **Thiết kế Prompt Y tế**: Cấu trúc Prompt mẫu cho Tóm tắt bệnh án, FAQ Chatbot và Dặn dò xuất viện.
- **Chiến lược Kiểm thử Đa tầng**: Ma trận kiểm thử 5 tầng và kết quả thực thi 223+ test cases đạt 100%.

### Bước 5: Biên soạn Tài liệu Giai đoạn 4 (KT4)
- **Môi trường & Container hóa**: Kiến trúc Docker Compose với 4 dịch vụ (`backend`, `frontend`, `postgres`, `pgadmin`).
- **Hướng dẫn Cài đặt & Vận hành**: Hướng dẫn chạy nhanh qua script `.bat` và cấu hình biến môi trường `.env`.
- **Hướng dẫn Sử dụng theo 4 Vai trò (User Guide)**: Ảnh minh họa/Mô tả thao tác từng bước cho Lễ tân (tiếp đón, đặt lịch), Bác sĩ (khám, AI briefing, kê đơn), Kế toán (thu ngân, VietQR) và Admin (quản trị, logs, charts).
- **Kịch bản Demo Chấm điểm**: Kịch bản thực hiện liền mạch trong 10-15 phút phục vụ bảo vệ đồ án.

### Bước 6: Biên soạn Báo cáo Tổng kết AI-Augmented SDLC (`AI-Augmented-SDLC-Report.md`)
Tài liệu này là minh chứng phương pháp luận thực hành AI-Augmented SDLC:
1. **Mô hình Phối hợp**: Phân tích sự tương tác giữa Codex (AI Agent), Skill (Quy chuẩn), Tool (Thao tác) và MCP (Giao thức).
2. **Cơ chế Human-in-the-loop**: Báo cáo đánh giá việc thực thi tại **Human Gate 1** (Phê duyệt yêu cầu), **Human Gate 2** (Kiểm duyệt mã nguồn), và **Human Gate 3** (Nghiệm thu toàn diện).
3. **Danh mục Lỗi do AI sinh ra & Sự can thiệp của Con người (AI Errors & Human Corrections)**:
   - *Lỗi 1 (Hallucination về chẩn đoán)*: AI tự động sinh tên bệnh lý -> Con người thiết lập Guardrail cấm tuyệt đối chẩn đoán.
   - *Lỗi 2 (Bỏ sót xung đột phòng khám)*: AI chỉ kiểm tra trùng lịch bác sĩ -> Con người bổ sung kiểm tra trùng phòng khám.
   - *Lỗi 3 (Rò rỉ số thẻ BHYT)*: Regex ban đầu chỉ bắt 10 số -> Con người hiệu chỉnh Regex bắt đúng chuẩn 15 ký tự BHYT Việt Nam.

### Bước 7: Đánh Phiên bản & Kích hoạt Human Gate 3 (Final Release Gate)
- Đồng bộ số phiên bản (Version 2.0.0) trên toàn bộ tài liệu và mã nguồn.
- Trình bày trước Hội đồng Đánh giá / Giảng viên hướng dẫn để ký biên bản nghiệm thu cuối kỳ.

---

## 5. Human-in-the-loop Governance (Cơ chế Kiểm soát Con người)

### 5.1. Cổng Kiểm soát Human Gate 3 (Final Release & Documentation Sign-off Gate)
Human Gate 3 là cổng nghiệm thu cao nhất:
- **Người ký duyệt**: Giảng viên Hướng dẫn, Trưởng ban Đề án và Toàn thể Hội đồng Chuyên môn.

### 5.2. Danh mục Kiểm tra Thẩm định Human Gate 3
- [ ] 1. Đầy đủ 4 bộ tài liệu SDLC KT1, KT2, KT3, KT4 trong thư mục `docs/`.
- [ ] 2. Báo cáo tổng kết AI-Augmented SDLC ghi nhận trung thực các bài học kinh nghiệm và sự sửa lỗi của con người.
- [ ] 3. Hướng dẫn sử dụng trực quan, mạch lạc, dễ thao tác theo từng vai trò.
- [ ] 4. Kịch bản demo sẵn sàng thực thi mượt mà, không gặp lỗi runtime.

---

## 6. Business & Compliance Rules (Quy tắc Nghiệp vụ & Tuân thủ)

1. **Tính Trung thực Học thuật**: Nghiêm cấm ngụy tạo kết quả kiểm thử hoặc làm đẹp số liệu báo cáo. Toàn bộ logs, latency và test pass rate phải trích xuất từ môi trường thực tế.
2. **Chuẩn Ngôn ngữ**: Tài liệu chính biên soạn bằng Tiếng Việt kỹ thuật chuẩn mực, các thuật ngữ công nghệ quốc tế (JWT, RBAC, PII, RESTful API, 3NF) được giữ nguyên theo quy ước ngành.

---

## 7. Expected Outputs & Deliverables (Tài liệu Đầu ra Bắt buộc)

1. `docs/SDLC_GiaiDoan1_PhanTich_ThietKe.md`
2. `docs/SDLC_GiaiDoan2_ChucNang_QuanLy.md`
3. `docs/SDLC_GiaiDoan3_TichHopAI_TestAI.md`
4. `docs/SDLC_GiaiDoan4_BaoCao_HuongDan_TrienKhai.md`
5. `docs/AI-Augmented-SDLC-Report.md`
6. `README.md`

---

## 8. Verification & Quality Acceptance Criteria (Tiêu chí Nghiệm thu Chất lượng)

- **Tính Hoàn chỉnh (Completeness)**: 100% các phần mục trong mẫu tài liệu được điền đầy đủ nội dung chuyên sâu, không có nội dung sơ sài.
- **Tính Thực chứng (Empirical Evidence)**: Đầy đủ các đoạn code minh họa, câu lệnh chạy và ảnh/sơ đồ luồng logic.
- **Sẵn sàng Bàn giao (Release Readiness)**: Bộ tài liệu đáp ứng hoàn hảo tiêu chí chấm điểm học phần và sẵn sàng đưa vào vận hành thực tế.
