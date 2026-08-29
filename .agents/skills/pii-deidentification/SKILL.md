---
name: pii-deidentification
description: Standard operating procedure for medical data privacy sanitization and PII de-identification on Vietnamese patient records before AI model invocation.
objective: Eliminate risk of Personal Identifiable Information (PII) leakage into LLM providers while preserving clinical context, vital signs, ICD-10 codes, and medical terminology.
inputs:
  - Raw clinical text, patient profile data, or medical consultation records
  - Patient identifiers (Full Name, CCCD/CMND, Phone number, Address, BHYT number, Email)
  - Target processing pipeline (Online Cloud LLM, Local Ollama LLM, Mock Provider)
process:
  - Step 1: Input text ingestion and normalization
  - Step 2: Explicit entity redaction (Patient Name)
  - Step 3: Regex-based pattern matching (Phone, CCCD, BHYT, Email, Address)
  - Step 4: Token replacement with standardized anonymization tags
  - Step 5: Token mapping preservation for authorized reversible de-identification
  - Step 6: Clinical data integrity verification (Vitals, Dosages, ICD-10 untouched)
  - Step 7: Audit logging of anonymized prompts to AIInvocationLog
rules:
  - Zero PII transmission to external LLMs without explicit tokenization
  - Preservation of medical metrics (blood pressure, temperature, heart rate, dosage, ICD-10)
  - Reversible mapping kept securely in memory or localized session context only
  - Mandatory audit log recording sanitized prompt and token metadata
outputs:
  - Anonymized prompt text containing standardized tokens
  - Reversible token mapping dictionary (Token -> Original Value)
  - Sanitization status report with entity counts
verification:
  - Automated regex test suite checking 100% masking on Vietnamese phone formats, 12-digit CCCDs, 15-character BHYT cards, labeled names and addresses
  - Negative validation verifying blood pressure (e.g. 120/80 mmHg), dosages (e.g. 500mg), and ICD-10 codes (e.g. J02.9, E11) remain unmasked
---

# Quy chuẩn Khử định danh Dữ liệu Y tế (Medical PII De-Identification Skill)

> **Mục tiêu**: Bảo vệ tuyệt đối quyền riêng tư dữ liệu bệnh nhân Việt Nam, tuân thủ Luật Khám bệnh, chữa bệnh 2023, Nghị định 13/2023/NĐ-CP về Bảo vệ dữ liệu cá nhân, và tiêu chuẩn quốc tế HIPAA Privacy Rule (Safe Harbor Method) khi tương tác với các hệ thống Trí tuệ nhân tạo (AI Engine).

---

## 1. Objective (Mục tiêu Kỹ năng)

1. **Bảo mật thông tin định danh cá nhân (PII)**: Tự động phát hiện, che giấu hoặc thay thế toàn bộ dữ liệu nhạy cảm của bệnh nhân (Họ tên, Số điện thoại, Số CCCD/CMND, Số thẻ BHYT, Địa chỉ thường trú/tạm trú, Email) thành các token ẩn danh trước khi gửi đến mô hình ngôn ngữ lớn (LLM).
2. **Bảo tồn tính toàn vẹn y khoa (Clinical Data Preservation)**: Đảm bảo các chỉ số sinh hiệu (Huyết áp, Mạch, Nhiệt độ, SpO2, BMI), mã bệnh ICD-10, tên thuốc, hàm lượng, liều dùng và thuật ngữ chuyên môn không bị biến dạng hoặc che nhầm trong quá trình khử định danh.
3. **Hỗ trợ Khôi phục hai chiều có kiểm soát (Reversible Token Mapping)**: Cung cấp cơ chế khôi phục token thành thông tin gốc khi trả kết quả về giao diện cho bác sĩ phụ trách, đồng thời đảm bảo cơ sở dữ liệu kiểm toán (Audit Log) chỉ lưu trữ phiên bản đã khử định danh.

---

## 2. Terminology & Conceptual Model (Phân định Khái niệm)

Hệ thống phân định rạch ròi 4 tầng khái niệm theo kiến trúc AI-Augmented SDLC:

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. CODEX (AI Autonomous Agent)                                         │
│    - Tác nhân AI thực thi tác vụ phân tích, tổng hợp hoặc hỗ trợ       │
│    - Không có quyền truy cập trực tiếp vào PII thô của bệnh nhân       │
├────────────────────────────────────────────────────────────────────────┤
│ 2. SKILL (Quy trình & Tiêu chuẩn Thủ tục - File này)                   │
│    - Định nghĩa tri thức, mẫu regex, quy tắc thay thế token,           │
│      nguyên tắc khôi phục và chính sách an toàn y tế                   │
├────────────────────────────────────────────────────────────────────────┤
│ 3. TOOL (Thao tác Môi trường / Hàm thực thi Backend)                   │
│    - Module `backend/app/ai_engine/anonymizer.py` (Class PIIAnonymizer)│
│    - Thực thi logic regex, xử lý chuỗi và tạo mapping dictionary       │
├────────────────────────────────────────────────────────────────────────┤
│ 4. MCP / Provider (Giao thức Kết nối Dịch vụ Ngoài)                    │
│    - Ollama Provider, Gemini/OpenAI Cloud Provider, Mock Provider      │
│    - Nhận dữ liệu ĐÃ KHỬ ĐỊNH DANH qua kênh truyền an toàn             │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Inputs & Prerequisites (Dữ liệu Đầu vào & Điều kiện Tiên quyết)

### 3.1. Dữ liệu Đầu vào
- **Raw Clinical Text**: Đoạn văn bản lâm sàng tự do, tóm tắt lý do khám, tiền sử bệnh, lời dặn bác sĩ.
- **Explicit Metadata**: Họ tên bệnh nhân (`patient_name`), Mã hồ sơ bệnh nhân (`medical_code`).
- **Target Channel**: Kênh đích (Local Ollama / Gemini API / OpenAI API / Deterministic Mock Engine).

### 3.2. Điều kiện Tiên quyết
- Engine regex đã được biên dịch sẵn (`re.compile`) trong bộ nhớ để đảm bảo hiệu năng xử lý < 2ms/request.
- Session người dùng được xác thực qua JWT hợp lệ và có quyền truy cập theo RBAC.

---

## 4. Execution Process (Quy trình Thực thi Từng bước)

```
[Raw Text Input] 
       │
       ▼
[BƯỚC 1: Explicit Name Redaction] ────► Thay thế Họ tên chỉ định thành [PATIENT_NAME_REDACTED]
       │
       ▼
[BƯỚC 2: Labeled Name Pattern]    ────► Regex nhận diện "Bệnh nhân: ...", "Họ và tên: ..."
       │
       ▼
[BƯỚC 3: Email Sanitization]       ────► Regex nhận diện địa chỉ email RFC 5322
       │
       ▼
[BƯỚC 4: Labeled Address Masking] ────► Regex nhận diện "Địa chỉ: ...", "Nơi cư trú: ..."
       │
       ▼
[BƯỚC 5: BHYT Card Redaction]     ────► Regex nhận diện thẻ BHYT (2 chữ cái + 10-13 số)
       │
       ▼
[BƯỚC 6: Phone Number Masking]    ────► Regex nhận diện SĐT (+84, 09x, 03x, 07x, 08x, 05x)
       │
       ▼
[BƯỚC 7: CCCD / CMND Masking]     ────► Regex nhận diện 12 số CCCD / 9 số CMND
       │
       ▼
[BƯỚC 8: Clinical Integrity Check]────► Kiểm tra không che nhầm Vitals / Liều thuốc / ICD-10
       │
       ▼
[Sanitized Prompt + Token Map]    ────► Chuyển sang AI Provider & Ghi log AIInvocationLog
```

### 4.1. Chi tiết Bảng Mẫu Regex Chuẩn Việt Nam

| Loại PII | Mẫu Biểu thức Chính quy (Regex Pattern) | Token Thay Thế | Ví dụ Đầu vào -> Đầu ra |
|---|---|---|---|
| **Họ tên có nhãn** | `(?:Bệnh nhân\|Họ và tên\|Họ tên\|Tên BN\|Khách hàng\|Người bệnh):\s*([A-ZÀ-Ỹ][a-zà-ỹ]+(?:\s+[A-ZÀ-Ỹ][a-zà-ỹ]+){1,5})` | `[PATIENT_NAME_REDACTED]` | `Bệnh nhân: Nguyễn Văn An` -> `Bệnh nhân: [PATIENT_NAME_REDACTED]` |
| **Số Điện thoại VN** | `(?:\+84\|84\|0)[\s.-]?(?:3[2-9]\|5[25689]\|7[06-9]\|8[1-9]\|9\d)(?:[\s.-]?\d){7}\b` | `[PHONE_REDACTED]` | `0912.345.678` -> `[PHONE_REDACTED]` |
| **Số CCCD (12 số) / CMND (9 số)** | `\b(?:\d{12}\|\d{9})\b` | `[CCCD_REDACTED]` | `001202009876` -> `[CCCD_REDACTED]` |
| **Thẻ BHYT (15/13 ký tự)** | `\b[A-Z]{2}\d{10,13}\b` | `[BHYT_REDACTED]` | `GD4010123456789` -> `[BHYT_REDACTED]` |
| **Địa chỉ chi tiết có nhãn** | `(?:Địa chỉ\|Nơi cư trú\|Thường trú\|Tạm trú):\s*([^.\n,]+(?:,[^.\n,]+){1,4})` | `[ADDRESS_REDACTED]` | `Địa chỉ: 45 Cầu Giấy, Quan Hoa, Hà Nội` -> `Địa chỉ: [ADDRESS_REDACTED]` |
| **Thư điện tử (Email)** | `\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z\|a-z]{2,}\b` | `[EMAIL_REDACTED]` | `patient.an@gmail.com` -> `[EMAIL_REDACTED]` |

### 4.2. Quy tắc Khôi phục (Deanonymization)
1. Chỉ áp dụng khôi phục tại tầng View Frontend của Bác sĩ phụ trách hoặc Lễ tân trong phiên làm việc hiện tại.
2. Hàm `PIIAnonymizer.deanonymize(sanitized_text, mapping)` thay thế chính xác từng token theo thứ tự ngược lại.
3. Không bao giờ gửi `token_mapping` cho bên thứ ba hoặc lưu trữ dạng plaintext ngoài bộ nhớ đệm an toàn.

---

## 5. Human-in-the-loop Governance (Kiểm soát Con người)

| Điểm Kiểm soát | Tên Gate | Trách nhiệm | Mô tả Hành động |
|---|---|---|---|
| **Human Gate 1** | *Reception Privacy Verification* | Lễ tân (Receptionist) | Kiểm tra tính chính xác của thông tin hành chính khi nhập liệu, đảm bảo mã số thẻ BHYT và CCCD hợp lệ trước khi đẩy vào hệ thống. |
| **Human Gate 2** | *PII Audit Log Review* | Quản trị viên (Admin) | Định kỳ rà soát bảng `AIInvocationLog` trên Admin Dashboard để phát hiện các trường hợp chuỗi PII lạ chưa được che (False Negatives). |
| **Human Gate 3** | *Clinical Context Inspection* | Bác sĩ (Doctor) | Xác nhận nội dung tóm tắt từ AI vẫn giữ đúng ý nghĩa bệnh án sau khi các thông tin cá nhân đã được ẩn danh. |

---

## 6. Business & Compliance Rules (Quy định Nghiệp vụ & Tuân thủ)

### 6.1. Ma trận Phân quyền RBAC 4 Vai trò

| Vai trò (Role) | Quyền xem PII gốc | Quyền xem Token Mapping | Quyền xem AI Invocation Log |
|---|---|---|---|
| **Admin** | Không (chỉ xem dưới dạng ẩn danh) | Không | Có (đầy đủ metadata và thời gian gọi) |
| **Receptionist** | Có (đối với bệnh nhân tại quầy) | Có (trong phiên tiếp đón) | Không |
| **Doctor** | Có (đối với bệnh nhân đang khám) | Có (trong phiên khám bệnh) | Không |
| **Accountant** | Có (đối với hóa đơn/thẻ BHYT) | Không | Không |

### 6.2. Quy định Bảo toàn Dữ liệu Y tế (Non-PII Invariance)
- **Huyết áp**: `120/80 mmHg` tuyệt đối không bị phân tách thành 3 số hay nhầm với CMND.
- **Nhiệt độ**: `37.5 °C`, `38°C` không bị lọc.
- **Mã ICD-10**: `J02.9`, `E11.9`, `I10`, `K21` giữ nguyên 100%.
- **Liều thuốc**: `500mg x 2 viên/ngày`, `1 gói x 3 lần` giữ nguyên 100%.

---

## 7. Expected Outputs & Deliverables (Sản phẩm Đầu ra)

1. **Chuỗi văn bản đã khử định danh (`anonymized_prompt`)**:
   ```
   Bệnh nhân: [PATIENT_NAME_REDACTED]
   Mã hồ sơ: BN-20260829-0012
   Tuổi: 45, Giới tính: Nam
   Dị ứng thuốc: Penicillin
   Tiền sử bệnh: Tăng huyết áp độ 2 (I10)
   Lần khám gần nhất:
   - Ngày 15/08/2026: Viêm họng cấp (J02.9) (Đau rát họng, nuốt vướng)
   ```
2. **Từ điển ánh xạ token (`token_mapping`)**:
   ```json
   {
     "[PATIENT_NAME_REDACTED]": "Nguyễn Văn An",
     "[PHONE_REDACTED]": "0912345678",
     "[CCCD_REDACTED]": "001202009876",
     "[BHYT_REDACTED]": "GD4010123456789"
   }
   ```
3. **Bản ghi log kiểm toán AI (`AIInvocationLog`)**:
   - Trường `anonymized_prompt` lưu trữ văn bản đã che.
   - Không chứa bất kỳ số điện thoại, CCCD hay tên thật của bệnh nhân.

---

## 8. Verification & Quality Acceptance Criteria (Tiêu chí Đánh giá & Nghiệm thu)

### 8.1. Ma trận Kiểm thử Tự động (Automated Verification)
Chạy lệnh kiểm thử độc lập cho module khử định danh PII:
```bash
pytest backend/tests/test_pii_anonymizer.py -v
```

### 8.2. Tiêu chí Chấp thuận (Acceptance Criteria)
- [x] **100% Phát hiện Số điện thoại VN**: Tất cả các đầu số di động (09x, 03x, 07x, 08x, 05x) và định dạng quốc tế (`+84`, `84`) kèm dấu chấm/khoảng trắng đều được thay thế bằng `[PHONE_REDACTED]`.
- [x] **100% Phát hiện CCCD/CMND**: Chuỗi 12 chữ số liên tiếp hoặc 9 chữ số liên tiếp bị thay thế thành `[CCCD_REDACTED]` hoặc `[ID_REDACTED]`.
- [x] **100% Phát hiện Thẻ BHYT**: Chuỗi 15 ký tự (mã đối tượng 2 chữ cái + 10-13 chữ số) bị thay thế thành `[BHYT_REDACTED]`.
- [x] **100% Bảo tồn Chỉ số Sinh hiệu**: Không làm biến đổi huyết áp, nhịp tim, nhiệt độ, chỉ số BMI và mã bệnh ICD-10.
- [x] **Khôi phục Nguyên vẹn (Idempotent De-anonymization)**: `PIIAnonymizer.deanonymize(redacted, mapping) == original_text`.
- [x] **Không Rò rỉ trong AI Invocation Log**: Không có bản ghi `AIInvocationLog` nào chứa dữ liệu PII thô.
