---
name: security-review
description: Quy chuẩn kiểm toán an toàn thông tin và bảo mật dữ liệu y tế (Medical Data Security Audit) theo chuẩn OWASP Top 10, Nghị định 13/2023/NĐ-CP và cơ chế phòng vệ Prompt Injection Guardrails cho CMS-AI.
objective: Cung cấp phương pháp luận mô hình hóa đe dọa (STRIDE), kiểm toán lỗ hổng mã nguồn, kiểm soát rò rỉ dữ liệu định danh bệnh nhân (PII), bảo vệ tính toàn vẹn JWT và thiết lập hàng rào phòng thủ tấn công AI.
inputs:
  - Tài liệu kiến trúc và luồng dữ liệu y tế (docs/architecture.md)
  - Mã nguồn Backend và Frontend (backend/app/, frontend/src/)
  - Bộ biểu thức Regex khử định danh PII (backend/app/ai_engine/anonymizer.py)
  - Ma trận các vector tấn công giả lập (SQLi, XSS, JWT Forgery, Prompt Injection, Jailbreak)
process:
  - 1. Xây dựng Mô hình Đe dọa Y tế (Medical Threat Modeling theo chuẩn STRIDE)
  - 2. Kiểm toán Xác thực, Quản lý Phiên và Chống Giả mạo JWT (Authentication & JWT Audit)
  - 3. Kiểm toán Nguy cơ Rò rỉ Dữ liệu Định danh Cá nhân (PII Leakage Audit)
  - 4. Kiểm toán Lỗ hổng Ứng dụng Web OWASP Top 10 (SQLi, XSS, CSRF, CORS)
  - 5. Kiểm toán Hàng rào Phòng thủ Trợ lý AI (Prompt Injection & Non-Diagnostic Guardrails)
  - 6. Kiểm toán Tính Đầy đủ của Hệ thống Ghi Nhật ký Kiểm toán (Audit Trail Completeness)
  - 7. Lập Báo cáo Đánh giá An ninh Y tế (Security Audit Report) và Kế hoạch Khắc phục
rules:
  - Tuyệt đối không cho phép bất kỳ chuỗi PII thô nào thoát khỏi ranh giới ứng dụng sang AI Provider
  - Toàn bộ câu truy vấn cơ sở dữ liệu phải được tham số hóa 100% qua ORM, cấm nối chuỗi raw SQL
  - JWT Token phải được ký bằng thuật toán an toàn (HS256 với secret key độ phức tạp cao >= 256 bits)
  - Bắt buộc kích hoạt CORS Middleware hạn chế chỉ cho phép nguồn gốc (Origin) của Frontend
outputs:
  - docs/security-review.md (Báo cáo kiểm toán bảo mật toàn diện, ma trận STRIDE và kết quả kiểm thử đối kháng)
verification:
  - 100% các payload tấn công SQL Injection và XSS bị vô hiệu hóa hoàn toàn
  - 100% payload tấn công Prompt Injection đòi chẩn đoán bệnh bị từ chối thành công
  - Xác nhận không có bản ghi nào trong ai_invocation_logs chứa số CCCD, SĐT hoặc BHYT thật
  - Phê duyệt chính thức của Chuyên gia Bảo mật Thông tin (Security Auditor)
---

# Kỹ năng Kiểm toán An toàn Dữ liệu Y tế & Bảo mật AI (Security Review Skill)

## 1. Objective (Mục tiêu Kỹ năng)

Kỹ năng này quy định tiêu chuẩn chuyên môn và quy trình từng bước cho Kỹ sư Bảo mật và AI Codex thực hiện kiểm toán an ninh toàn diện cho **Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp Trợ lý AI Hành chính (CMS-AI)**.

Mục tiêu cốt lõi:
1. Nhận diện và triệt tiêu các mối đe dọa an ninh thông tin theo mô hình **STRIDE** (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege).
2. Đảm bảo tuân thủ nghiêm ngặt **Nghị định 13/2023/NĐ-CP** về Bảo vệ dữ liệu cá nhân và các nguyên tắc bảo mật y tế quốc tế (HIPAA Security Rule).
3. Đánh giá tính vững chắc của hàng rào phòng thủ **AI Guardrails** trước các cuộc tấn công phi kỹ thuật (Social Engineering), Prompt Injection, System Prompt Leakage và Jailbreak.
4. Kiểm toán độ toàn vẹn của hệ thống ghi vết kiểm toán (`audit_logs` và `ai_invocation_logs`).

---

## 2. Terminology & Conceptual Model (Mô hình Khái niệm)

Trong không gian Kiểm toán Bảo mật Hệ thống:

```
+-----------------------------------------------------------------------------------------------+
|                                   MÔ HÌNH KHÁI NIỆM AN TOÀN THÔNG TIN                         |
+-----------------------------------------------------------------------------------------------+
|  1. CODEX (AI Agent)         : Kỹ sư Kiểm toán An toàn Thông tin (Security Auditor Agent).    |
|                                Dò quét lỗ hổng, xây dựng payload tấn công giả lập, audit mã.  |
|  2. SKILL (Procedural Standard): Phương pháp luận STRIDE, quy chuẩn kiểm toán PII y tế,       |
|                                tiêu chuẩn đánh giá AI Guardrails và ma trận OWASP (Skill này).|
|  3. TOOL (Environment Action): Công cụ quét mã tĩnh, thực thi adversarial test payloads trong |
|                                Pytest, kiểm tra header an toàn HTTP.                          |
|  4. MCP (Model Context Protocol): Giao thức trao đổi log bảo mật và cảnh báo xâm nhập.       |
+-----------------------------------------------------------------------------------------------+
```

---

## 3. Inputs & Prerequisites (Đầu vào & Điều kiện Tiên quyết)

1. **Kiến trúc & Luồng Dữ liệu**: `docs/architecture.md`.
2. **Cấu hình Bảo mật Backend**: `backend/app/core/security.py`, `backend/app/core/rbac.py`, `backend/app/ai_engine/anonymizer.py`, `backend/app/ai_engine/guardrails.py`.
3. **Danh mục Quy định Tuân thủ**: Nghị định 13/2023/NĐ-CP, OWASP Top 10 API Security 2023.

---

## 4. Execution Process (Quy trình Thực thi Từng bước)

```
[Bước 1: STRIDE Threat Modeling] ---> [Bước 2: Audit JWT & RBAC] ---> [Bước 3: Audit PII Pipeline]
                                                                                   |
[Bước 6: Audit Hệ thống Logs]    <--- [Bước 5: Audit AI Guardrails] <--- [Bước 4: OWASP Web Audit]
           |
           v
[Bước 7: Lập Báo cáo Đánh giá An ninh Y tế Toàn diện]
```

### Bước 1: Xây dựng Mô hình Đe dọa Y tế (Medical STRIDE Threat Modeling)

Phân tích 6 lớp rủi ro trên toàn bộ hệ thống phòng khám:

| Mối Đe Dọa (STRIDE) | Rủi ro Nghiệp vụ Phòng khám | Biện pháp Phòng vệ Triển khai trong CMS-AI |
|---|---|---|
| **Spoofing (Giả mạo)** | Kẻ xấu mạo danh Bác sĩ để xem hồ sơ bệnh án hoặc kê đơn thuốc giả mạo. | Xác thực JWT chữ ký HS256, kiểm tra tính hợp lệ của token và trạng thái `is_active` tại mỗi request. |
| **Tampering (Can thiệp trái phép)** | Người dùng thay đổi chi phí hóa đơn hoặc sửa đổi lịch hẹn của người khác. | Kiểm soát phân quyền RBAC chặt chẽ; Bác sĩ không sửa được hóa đơn; Thuật toán xung đột chặn ghi đè lịch. |
| **Repudiation (Chối bỏ trách nhiệm)** | Nhân viên chối bỏ việc đã xem trộm hồ sơ bệnh nhân hoặc chỉnh sửa số tiền. | Ghi nhận đầy đủ `audit_logs` (User ID, Thao tác, Thời gian, Địa chỉ IP, Dữ liệu thay đổi). |
| **Information Disclosure (Lộ lọt thông tin)** | Lộ số CCCD, SĐT, mã BHYT hoặc bệnh sử nhạy cảm sang bên thứ ba hoặc nhà cung cấp LLM. | Tích hợp bộ lọc `PIIAnonymizer` tự động thay thế thông tin cá nhân bằng mã ẩn danh trước khi truyền đi. |
| **Denial of Service (Từ chối dịch vụ)** | Tấn công làm tràn ngập hàng đợi khám hoặc spam gọi API AI gây quá tải chi phí. | Tích hợp Rate Limiting, phân trang danh sách (Pagination), sử dụng Mock AI khi ngoại tuyến. |
| **Elevation of Privilege (Leo thang đặc quyền)**| Lễ tân gửi request chỉnh sửa đơn thuốc hoặc Kế toán tự nâng quyền lên Admin. | `RoleChecker` dependency thực thi tại tầng router; Không tin cậy dữ liệu client gửi lên. |

### Bước 2: Kiểm toán Xác thực, Quản lý Phiên & Chống Giả mạo JWT
1. **Thuật toán Băm Mật khẩu**: Sử dụng `passlib.context.CryptContext` với thuật toán `bcrypt` (12 rounds).
2. **Cấu trúc Payload JWT**:
   - `sub`: User ID (duy nhất).
   - `username`: Tên đăng nhập.
   - `role`: Chuỗi vai trò (`admin`, `receptionist`, `doctor`, `accountant`).
   - `exp`: Thời điểm hết hạn (mặc định 8 giờ).
3. **Chống Tấn công Algorithm Confusion**: Chỉ chấp nhận thuật toán `HS256`, từ chối nghiêm ngặt các token có `alg: none`.

### Bước 3: Kiểm toán Nguy cơ Rò rỉ Dữ liệu Định danh Cá nhân (PII Leakage Audit)
Kiểm tra hiệu quả của bộ Regex tiếng Việt:
- **Số điện thoại**: Bắt chính xác 100% các đầu số `03x, 05x, 07x, 08x, 09x` và `+84`.
- **Số CCCD/CMND**: Bắt chính xác chuỗi 9 chữ số và 12 chữ số.
- **Mã thẻ BHYT**: Bắt chính xác định dạng 15 ký tự (2 chữ cái đầu + 13 chữ số).
- **Tên bệnh nhân**: Tự động lấy từ trường `full_name` để replace thành `[PATIENT_NAME_REDACTED]`.

*Đoạn mã kiểm tra tính ẩn danh an toàn trong `backend/app/ai_engine/anonymizer.py`:*
```python
def test_pii_safety_assert():
    anonymizer = PIIAnonymizer()
    raw_prompt = "Bệnh nhân Nguyễn Văn An, CCCD 001202003456, SĐT 0987654321, BHYT GD4010123456789 bị đau dạ dày."
    anonymized_text, mapping = anonymizer.anonymize(raw_prompt, patient_name="Nguyễn Văn An")
    
    assert "Nguyễn Văn An" not in anonymized_text
    assert "001202003456" not in anonymized_text
    assert "0987654321" not in anonymized_text
    assert "GD4010123456789" not in anonymized_text
    assert "[PATIENT_NAME_REDACTED]" in anonymized_text
    assert "[CCCD_REDACTED]" in anonymized_text
    assert "[PHONE_REDACTED]" in anonymized_text
```

### Bước 4: Kiểm toán Lỗ hổng Ứng dụng Web (OWASP Top 10)
1. **SQL Injection (SQLi)**: 100% câu truy vấn sử dụng SQLAlchemy ORM (`db.query().filter()`). Không có bất kỳ câu lệnh nào ghép chuỗi thô `f"SELECT * FROM users WHERE username = '{user}'"`.
2. **Cross-Site Scripting (XSS)**: Frontend React tự động encode dữ liệu khi render JSX; Dữ liệu nhập vào ghi chú lâm sàng được kiểm tra độ dài và định dạng qua Pydantic.
3. **Cross-Origin Resource Sharing (CORS)**: Cấu hình `CORSMiddleware` cho phép chính xác origin của frontend (mặc định `http://localhost:3000`, `http://localhost:5173`), chặn các origin không rõ nguồn gốc.

### Bước 5: Kiểm toán Hàng rào Phòng thủ Trợ lý AI (AI Guardrails Audit)
1. **Non-Diagnostic Guardrail**: Kiểm tra System Prompt bắt buộc:
   ```
   BẠN LÀ TRỢ LÝ HÀNH CHÍNH PHÒNG KHÁM. BẠN TUYỆT ĐỐI KHÔNG ĐƯỢC PHÉP ĐƯA RA CHẨN ĐOÁN Y KHOA HOẶC KÊ ĐƠN THUỐC.
   NẾU NGƯỜI DÙNG HỎI VỀ CHẨN ĐOÁN HOẶC ĐIỀU TRỊ BỆNH, HÃY TỪ CHỐI LỊCH SỰ VÀ KHUYÊN HỌ ĐẾN GẶP BÁC SĨ.
   ```
2. **Medical Disclaimer Injection**: Kiểm tra hàm `post_process_response()` luôn tự động nối chuỗi `TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y TẾ` vào cuối phản hồi.

### Bước 6: Kiểm toán Hệ thống Ghi Nhật ký (Audit Trail)
- Xác nhận bảng `audit_logs` lưu trữ mọi thao tác truy cập bệnh án.
- Xác nhận bảng `ai_invocation_logs` lưu trữ prompt sau khi đã khử PII, không lưu prompt chứa thông tin nhạy cảm.

### Bước 7: Lập Báo cáo Đánh giá An ninh Y tế (Security Audit Report)
Tổng hợp kết quả vào `docs/security-review.md` với ma trận đánh giá chi tiết: Các mục kiểm thử, kết quả (Pass/Fail), bằng chứng thực nghiệm và khuyến nghị duy trì an ninh.

---

## 5. Human-in-the-loop Governance (Cơ chế Kiểm soát Con người)

### 5.1. Thẩm quyền Duyệt An ninh
- Chuyên gia An toàn Thông tin (CISO / Security Lead) và Trưởng ban Y khoa (Medical Director) thẩm định và ký phê duyệt báo cáo.

### 5.2. Tiêu chí Đánh giá Phê duyệt
- [ ] 1. Không còn bất kỳ lỗ hổng bảo mật nào ở mức CRITICAL hoặc HIGH.
- [ ] 2. 100% dữ liệu PII được khử thành công trước khi gửi tới bất kỳ LLM nào.
- [ ] 3. Hàng rào AI Guardrail chặn đứng 100% các prompt injection chẩn đoán bệnh.
- [ ] 4. Mọi tương tác đọc/sửa dữ liệu y tế đều sinh Audit Log đầy đủ.

---

## 6. Business & Compliance Rules (Quy tắc Nghiệp vụ & Tuân thủ)

1. **Tuân thủ Nghị định 13/2023/NĐ-CP**: Xử lý dữ liệu cá nhân người bệnh với sự đồng thuận, có mục đích rõ ràng và áp dụng biện pháp bảo vệ kỹ thuật tương xứng.
2. **Bảo mật Khóa Bí mật**: Không bao giờ commit file `.env` chứa khóa thật vào Git. Luôn sử dụng `.env.example` làm mẫu cấu hình.

---

## 7. Expected Outputs & Deliverables (Tài liệu Đầu ra Bắt buộc)

1. `docs/security-review.md`: Tài liệu Báo cáo Kiểm toán An toàn Dữ liệu Y tế & AI Security toàn diện.
2. Bộ test cases đối kháng an ninh trong `backend/tests/test_e2e_scenarios.py` và `backend/tests/test_ai_features.py`.

---

## 8. Verification & Quality Acceptance Criteria (Tiêu chí Nghiệm thu Chất lượng)

- **Kết quả Kiểm thử Tấn công (Penetration Test Results)**: 100% vector tấn công giả lập (SQLi, XSS, JWT tampered, Prompt Injection) bị hệ thống phát hiện và chặn đứng an toàn.
- **Tính Toàn vẹn PII**: Không phát hiện bất kỳ chuỗi PII thô nào trong database logs của bảng `ai_invocation_logs`.
- **Ký duyệt An ninh**: Báo cáo được ký phê duyệt chính thức bởi Chuyên gia Bảo mật Y tế.
