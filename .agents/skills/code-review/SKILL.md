---
name: code-review
description: Quy chuẩn đánh giá và kiểm toán mã nguồn đa chiều (Multi-Dimensional Code Review) cho hệ thống y tế CMS-AI, phân loại mức độ rủi ro CRITICAL/HIGH/MEDIUM/LOW và kích hoạt cổng Human Gate 2.
objective: Cung cấp phương pháp luận và danh mục kiểm tra mã nguồn cho Kỹ sư và AI Codex nhằm rà soát tính đúng đắn nghiệp vụ, kiểm soát phân quyền RBAC, tối ưu hóa truy vấn CSDL, bảo vệ dữ liệu PII và tuân thủ Taste-Skill.
inputs:
  - Các thay đổi mã nguồn (Pull Requests, Git Commits, Patch files)
  - Quy chuẩn lập trình sạch và Taste-Skill (docs/SKILL.md)
  - Ma trận phân quyền 4 vai trò RBAC và thiết kế 14 bảng CSDL
  - Kết quả chạy test suite tự động và phân tích tĩnh (Static Analysis)
process:
  - 1. Tiếp nhận phạm vi thay đổi và thiết lập ranh giới kiểm toán mã nguồn
  - 2. Kiểm toán Tính Đúng đắn Nghiệp vụ Y tế (Clinical Business Correctness)
  - 3. Kiểm toán Tuân thủ Phân quyền (RBAC Isolation & Authorization Bypasses)
  - 4. Kiểm toán Hiệu năng & Tối ưu Cơ sở Dữ liệu (Database Queries & N+1 Prevention)
  - 5. Kiểm toán Tích hợp Trợ lý AI & Khử Định danh PII (AI Safety & Privacy)
  - 6. Kiểm toán Giao diện Người dùng & Chuẩn Taste-Skill (UI/UX Ergonomics)
  - 7. Phân loại phát hiện theo mức độ nghiêm trọng (Severity Classification) và lập báo cáo Human Gate 2
rules:
  - Bất kỳ vi phạm nào thuộc mức CRITICAL hoặc HIGH đều phải BLOCK quá trình merge/release
  - Mọi phát hiện lỗi phải có dẫn chứng cụ thể: Tệp tin, dòng mã, nguyên nhân và giải pháp khắc phục
  - Không phê duyệt code có ngoại lệ trần trụi (Naked Exceptions) hoặc rò rỉ stack trace
  - Bắt buộc kiểm tra việc gọi qua PII Anonymizer trước bất kỳ hàm gọi AI Provider nào
outputs:
  - docs/code-review.md (Báo cáo đánh giá mã nguồn chi tiết, ma trận phát hiện và biên bản Human Gate 2)
verification:
  - Xác nhận 100% các lỗi CRITICAL và HIGH đã được khắc phục hoàn toàn
  - Chạy lại bộ test suite hồi quy (Regression Test) đảm bảo không phát sinh lỗi phụ
  - Phê duyệt chính thức của Technical Lead và Security Reviewer tại Human Gate 2
---

# Kỹ năng Đánh giá & Kiểm toán Mã nguồn Đa chiều (Code Review Skill)

## 1. Objective (Mục tiêu Kỹ năng)

Kỹ năng này quy định tiêu chuẩn chuyên môn và quy trình từng bước cho Kỹ sư Phần mềm và AI Codex thực hiện kiểm toán mã nguồn đa chiều (Multi-Dimensional Code Review) trên toàn bộ hệ thống **CMS-AI**.

Mục tiêu cốt lõi:
1. Đánh giá tính đúng đắn nghiệp vụ lâm sàng, đảm bảo các thuật toán cốt lõi (kiểm tra xung đột lịch khám, trừ tồn kho thuốc, tính khấu trừ BHYT) vận hành chính xác 100%.
2. Ngăn ngừa triệt để các lỗ hổng leo thang đặc quyền (Privilege Escalation) hoặc vượt quyền truy cập trong mô hình RBAC 4 vai trò.
3. Kiểm soát hiệu năng và tương tác cơ sở dữ liệu: Loại bỏ vấn đề N+1 queries, thiếu chỉ mục hoặc rò rỉ phiên kết nối DB Session.
4. Kiểm toán an toàn AI: Đảm bảo 100% dữ liệu PII được che giấu và luôn có tuyên bố miễn trừ trách nhiệm y tế.
5. Vận hành cổng kiểm soát **Human Gate 2 (Implementation & Code Review Gate)** trước khi phát hành phiên bản.

---

## 2. Terminology & Conceptual Model (Mô hình Khái niệm)

Trong không gian Đánh giá Mã nguồn:

```
+-----------------------------------------------------------------------------------------------+
|                                    MÔ HÌNH KHÁI NIỆM CODE REVIEW                              |
+-----------------------------------------------------------------------------------------------+
|  1. CODEX (AI Agent)         : Kỹ sư Kiểm toán Mã nguồn (Code Reviewer Agent). Phân tích AST, |
|                                phát hiện vi phạm quy chuẩn, gợi ý refactor và chỉ ra bug ẩn.  |
|  2. SKILL (Procedural Standard): Quy chuẩn đánh giá đa chiều, ma trận phân loại độ nghiêm     |
|                                trọng CRITICAL/HIGH/MEDIUM/LOW, checklist Human Gate 2 (Skill). |
|  3. TOOL (Environment Action): Công cụ `grep_search`, `view_file`, `git diff`, công cụ linting |
|                                và test runner.                                                |
|  4. MCP (Model Context Protocol): Giao thức trích xuất ngữ cảnh mã nguồn và lịch sử commit.   |
+-----------------------------------------------------------------------------------------------+
```

---

## 3. Inputs & Prerequisites (Đầu vào & Điều kiện Tiên quyết)

1. **Bộ mã nguồn thay đổi**: Toàn bộ mã Backend (`backend/app/`) và Frontend (`frontend/src/`).
2. **Quy chuẩn Lập trình & Taste-Skill**: `docs/SKILL.md` và `.agents/skills/implementation/SKILL.md`.
3. **Kết quả Kiểm thử Tự động**: Báo cáo thực thi Pytest (223+ test cases Passed).

---

## 4. Execution Process (Quy trình Thực thi Từng bước)

```
[Bước 1: Thiết lập Phạm vi] ---> [Bước 2: Kiểm toán Nghiệp vụ] ---> [Bước 3: Kiểm toán RBAC]
                                                                                |
[Bước 6: Kiểm toán Taste-Skill] <--- [Bước 5: Kiểm toán AI PII] <--- [Bước 4: Kiểm toán CSDL]
           |
           v
[Bước 7: Phân loại Rủi ro & Kích hoạt Cổng Human Gate 2]
```

### Bước 1: Thiết lập Phạm vi & Phân loại Thay đổi
1. Liệt kê toàn bộ các tệp tin được thêm mới, sửa đổi hoặc xóa bỏ.
2. Xác định các phân hệ bị ảnh hưởng (Core, Models, Routers, AI Engine, UI Pages).

### Bước 2: Kiểm toán Tính Đúng đắn Nghiệp vụ Y tế (Clinical Business Logic)
Rà soát từng dòng mã xử lý logic:
- **Thuật toán Xung đột Lịch (`conflict_checker.py`)**: Kiểm tra đầy đủ điều kiện giao khoảng thời gian $(S_1 < E_2 \land E_1 > S_2)$ trên cả bác sĩ và phòng khám.
- **Tính toán Viện phí (`invoices.py`)**: Kiểm tra công thức: $\text{Tổng thanh toán} = \text{Tiền khám} + \text{Tiền CLS} + \text{Tiền thuốc} - \text{BHYT chi trả}$.
- **Trừ Kho Dược (`prescriptions.py`)**: Kiểm tra điều kiện `medicine.stock >= quantity` trước khi trừ tồn kho. Nếu không đủ thuốc, hệ thống phải raise lỗi `400 Bad Request` và rollback transaction.

### Bước 3: Kiểm toán Tuân thủ Phân quyền (RBAC Isolation)
Rà soát ma trận ủy quyền:
- **Kiểm tra Dependencies**: Mọi endpoint bắt buộc có `Depends(RoleChecker([...]))`.
- **Kiểm tra Quyền Bác sĩ**: Bác sĩ chỉ được xem và sửa phiếu khám được phân công (`record.doctor_id == current_user.doctor.id` hoặc `admin`).
- **Kiểm tra Quyền Kế toán**: Lễ tân và Bác sĩ không được cấp quyền gọi API xác nhận thanh toán (`/api/v1/payments`).

### Bước 4: Kiểm toán Hiệu năng & Tương tác CSDL (Database Efficiency)
- **Chống N+1 Queries**: Kiểm tra các truy vấn lấy danh sách phiếu khám hoặc đơn thuốc, bắt buộc sử dụng `joinedload()` hoặc `selectinload()` khi nạp quan hệ liên kết.
- **Quản lý Session**: Đảm bảo mọi session mở ra đều được đóng trong khối `finally: db.close()` hoặc thông qua FastAPI Dependency `get_db`.
- **Transaction Rollback**: Mọi khối `try...except` thao tác DB phải có `db.rollback()` trước khi raise HTTPException.

### Bước 5: Kiểm toán Tích hợp Trợ lý AI & Khử Định danh PII
- **PII Redaction Pipeline**: Kiểm tra luồng gọi AI: Bắt buộc truyền qua `PIIAnonymizer.anonymize()` trước khi đưa vào prompt của LLM.
- **Medical Disclaimer**: Kiểm tra đầu ra của mọi endpoint AI: Bắt buộc có trường `disclaimer` chứa chuỗi `TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y TẾ`.
- **Offline Fallback**: Xác nhận khi không có biến môi trường `GEMINI_API_KEY` hoặc `OLLAMA_HOST`, hệ thống tự động khởi tạo `MockDeterministicAIProvider` mà không crash ứng dụng.

### Bước 6: Kiểm toán Giao diện Người dùng & Chuẩn Taste-Skill
- **Kiểm tra Anti-Slop**: Không có các gradient tím/xanh lòe loẹt, không có card bo góc quá lớn `rounded-3xl` gây lãng phí không gian.
- **Kiểm tra Số liệu Tabular**: Mọi trường số tiền, mã định danh, giờ khám phải có `tabular-nums font-mono`.
- **Kiểm tra Responsive & Accessibility**: Giao diện hiển thị rõ nét trên màn hình phòng khám từ 1366x768 trở lên.

### Bước 7: Phân loại Rủi ro & Lập Báo cáo Human Gate 2
Mỗi phát hiện được phân cấp theo 4 mức độ nghiêm trọng:

```
+-----------------------------------------------------------------------------------------------+
|                                    SEVERITY CLASSIFICATION MATRIX                             |
+-----------------------------------------------------------------------------------------------+
| Mức độ | Ý nghĩa & Tiêu chuẩn Phân loại                           | Hành động Bắt buộc        |
|:-------|:---------------------------------------------------------|:--------------------------|
| **CRITICAL** | Lỗ hổng bảo mật nghiêm trọng (SQLi, Bypass RBAC,    | **BLOCK MERGE / RELEASE** |
|              | rò rỉ dữ liệu PII bệnh nhân ra ngoài internet).    | Bắt buộc fix ngay lập tức.|
| **HIGH**     | Sai sót logic nghiệp vụ (tính sai tiền, trừ sai    | **BLOCK MERGE**           |
|              | kho thuốc, xung đột lịch bị bỏ lọt).              | Bắt buộc fix trước merge. |
| **MEDIUM**   | Hiệu năng chưa tối ưu (N+1 query), thiếu index,    | Cần khắc phục trong sprint|
|              | xử lý lỗi chưa chuẩn RFC 7807.                    | hoặc tạo task theo dõi.   |
| **LOW**      | Vấn đề phong cách code, đặt tên biến, comment thừa,| Khuyến nghị cải thiện     |
|              | căn chỉnh CSS nhẹ.                                 | không block release.      |
+-----------------------------------------------------------------------------------------------+
```

---

## 5. Human-in-the-loop Governance (Cơ chế Kiểm soát Con người)

### 5.1. Cổng Kiểm soát Human Gate 2 (Implementation & Code Review Gate)
Human Gate 2 là trạm kiểm soát chất lượng kỹ thuật bắt buộc:
- **Người ký duyệt**: Technical Lead và Chuyên gia An toàn Thông tin.
- **Quy tắc Veto**: Chỉ cần 1 lỗi mức **CRITICAL** hoặc **HIGH** tồn tại, cổng Human Gate 2 sẽ tự động đóng và từ chối phát hành (Reject).

### 5.2. Danh mục Kiểm tra Thẩm định Human Gate 2
- [ ] 1. Toàn bộ 4 vai trò RBAC được bảo vệ nghiêm ngặt ở tầng API.
- [ ] 2. Không có hardcoded secrets hoặc thông tin nhạy cảm trong commit history.
- [ ] 3. PII Anonymizer hoạt động chuẩn xác trước khi gọi AI.
- [ ] 4. Giao diện tuân thủ Taste-Skill, không có lỗi console.
- [ ] 5. 223+ test cases tự động trong Pytest vượt qua 100%.

---

## 6. Business & Compliance Rules (Quy tắc Nghiệp vụ & Tuân thủ)

1. **Bất khả xâm phạm RBAC**: Tuyệt đối không chấp nhận giải pháp "tạm thời mở full quyền để test". Mọi tính năng phải được test với đúng vai trò được định nghĩa.
2. **Minh chứng Đánh giá**: Báo cáo Code Review phải lưu trữ công khai trong `docs/code-review.md` làm minh chứng đánh giá chất lượng học phần.

---

## 7. Expected Outputs & Deliverables (Tài liệu Đầu ra Bắt buộc)

1. `docs/code-review.md`: Tài liệu Báo cáo Đánh giá Mã nguồn Toàn diện, Danh mục phát hiện (Findings), Ma trận phân loại mức độ rủi ro và Biên bản nghiệm thu Human Gate 2.

---

## 8. Verification & Quality Acceptance Criteria (Tiêu chí Nghiệm thu Chất lượng)

- **Tính Minh bạch (Transparency)**: 100% các phát hiện đều có số dòng mã và snippet cụ thể.
- **Tính Khắc phục Triệt để (Remediation)**: 100% lỗi CRITICAL và HIGH được xử lý dứt điểm trước khi đóng cổng.
- **Biên bản Nghiệm thu**: Có đầy đủ nhận xét và chữ ký phê duyệt của Tech Lead tại Human Gate 2.
