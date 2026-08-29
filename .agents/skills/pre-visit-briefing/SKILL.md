---
name: pre-visit-briefing
description: Standard operating procedure for generating fast, high-trust, AI-augmented pre-visit clinical summaries for doctors before examining patients.
objective: Reduce physician cognitive overload by summarizing patient medical history, highlighting drug allergies, surfacing chronic conditions, and collating recent encounters within a 10-second readable briefing.
inputs:
  - Patient ID / Medical Code
  - Patient demographic profile (Age, Gender)
  - Documented drug allergies and food hypersensitivities
  - Longitudinal medical history and chronic comorbidities
  - Past 3 clinical encounter records (Exam dates, Diagnoses, Chief complaints, Treatments)
process:
  - Step 1: Query patient profile and past medical records from database
  - Step 2: Extract chronic condition keywords (Hypertension, Diabetes, Asthma, Gout, CVD)
  - Step 3: Format clinical context and apply PII de-identification
  - Step 4: Construct prompt with PRE_VISIT_SYSTEM_PROMPT
  - Step 5: Execute AI generation via active provider (Mock, Ollama, Cloud)
  - Step 6: Post-process output, append Medical Disclaimer, and assemble structured response
  - Step 7: Record AI invocation audit log with latency and model metadata
  - Step 8: Deliver briefing card to Doctor's Consultation Queue UI under Human Gate 3 review
rules:
  - AI summary is strictly administrative and informational; it does NOT diagnose or propose new clinical treatment
  - Drug allergies must be formatted prominently in critical red alerts
  - Zero hallucination: only summarize documented facts from patient records
  - Mandatory Medical Disclaimer injection on every output payload
  - Doctor review required prior to recording clinical examination findings (Human Gate 3)
outputs:
  - Structured JSON response containing patient summary, alerts, chronic conditions list, and disclaimer
  - Visual AI Briefing Card rendered in React frontend
  - Audit log entry in AIInvocationLog table
verification:
  - Automated tests verifying allergy warnings are extracted correctly from test patients
  - Unit tests ensuring prompt undergoes PII masking prior to LLM call
  - E2E tests confirming Doctor UI receives structured briefing card with Medical Disclaimer
---

# Quy chuẩn Tóm tắt Hồ sơ Bệnh án Trước khám (Pre-Visit Briefing AI Skill)

> **Mục tiêu**: Tối ưu hóa thời gian tiếp cận bệnh án của Bác sĩ chuyên khoa, tự động tổng hợp tiền sử bệnh lý, làm nổi bật các dị ứng thuốc nguy hiểm và tóm tắt các lần khám gần nhất trong một bản tóm tắt súc tích, đọc hiểu trong 10 giây, giảm thiểu sai sót y khoa và nâng cao an toàn người bệnh.

---

## 1. Objective (Mục tiêu Kỹ năng)

1. **Giảm tải Nhận thức cho Bác sĩ (Cognitive Load Reduction)**: Tự động trích xuất và tổng hợp dữ liệu từ nhiều lần khám trước đó thành 1 bản tóm tắt lâm sàng trực quan, giúp bác sĩ nắm bắt bệnh cảnh ngay trước khi bệnh nhân bước vào phòng khám.
2. **Cảnh báo Đỏ Dị ứng Thuốc (Critical Allergy Alerts)**: Làm nổi bật ngay lập tức các dị ứng thuốc (như Penicillin, Aspirin, Sulfonamides, v.v.) nhằm ngăn ngừa các biến cố bất lợi do thuốc (Adverse Drug Events - ADE).
3. **Phát hiện Bệnh lý Mạn tính Nền (Chronic Comorbidities Detection)**: Tự động lọc và hiển thị danh sách các bệnh nền (Tăng huyết áp, Đái tháo đường, Hen phế quản, Bệnh tim thiếu máu cục bộ, Suy thận, Gout) để phục vụ việc lựa chọn thuốc an toàn.
4. **Đảm bảo An toàn & Ranh giới Đạo đức AI**: AI chỉ đóng vai trò tóm tắt dữ liệu lịch sử sẵn có, tuyệt đối không suy đoán hoặc đưa ra chẩn đoán mới; bắt buộc có sự thẩm định của Bác sĩ (Human Gate 3).

---

## 2. Terminology & Conceptual Model (Phân định Khái niệm)

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. CODEX (AI Autonomous Agent)                                         │
│    - Mô hình AI (Ollama LLM / Cloud API / Deterministic Mock)          │
│    - Tiếp nhận prompt đã che PII và tạo văn bản tóm tắt theo format     │
├────────────────────────────────────────────────────────────────────────┤
│ 2. SKILL (Quy trình & Tiêu chuẩn Thủ tục - File này)                   │
│    - Định nghĩa cấu trúc prompt, danh mục bệnh mạn tính, quy tắc cảnh  │
│      báo dị ứng, ranh giới đạo đức y khoa và tiêu chuẩn Human Gate 3    │
├────────────────────────────────────────────────────────────────────────┤
│ 3. TOOL (Thao tác Môi trường / Service Layer)                          │
│    - `AdminAIService.generate_pre_visit_summary()`                     │
│    - Module truy vấn DB SQLAlchemy, bóc tách `MedicalRecord`, khử PII  │
├────────────────────────────────────────────────────────────────────────┤
│ 4. MCP / UI Component (Giao diện Tác vụ Bác sĩ)                        │
│    - Component `AIPreVisitCard.jsx` hiển thị trên `ConsultationFormPage`│
│    - Badge cảnh báo nguy cơ và nút xác nhận đã đọc thông tin           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Inputs & Prerequisites (Dữ liệu Đầu vào & Điều kiện Tiên quyết)

### 3.1. Dữ liệu Đầu vào (Payload)
- `patient_id` (int): Mã định danh bệnh nhân trong CSDL.
- `patient_data` (dict, tùy chọn khi test offline):
  - `full_name` (str): Họ và tên bệnh nhân.
  - `medical_code` (str): Mã hồ sơ y tế (VD: `BN-20260829-0001`).
  - `age` (int) & `gender` (str): Tuổi và giới tính sinh học.
  - `drug_allergies` (str): Danh sách dị ứng thuốc đã ghi nhận.
  - `medical_history` (str): Tiền sử bệnh bản thân và gia đình.
  - `recent_visits_summary` (str): Danh sách 3 đợt khám gần nhất.

### 3.2. Điều kiện Tiên quyết
- Bệnh nhân đã được tiếp đón tại quầy Lễ tân và được xếp vào hàng đợi khám (Queue) của Bác sĩ.
- Bác sĩ đang đăng nhập với phiên JWT hợp lệ mang quyền `doctor` hoặc `admin`.

---

## 4. Execution Process (Quy trình Thực thi Từng bước)

```
[Bác sĩ mở Phiếu khám Bệnh nhân]
               │
               ▼
[BƯỚC 1: Truy vấn Dữ liệu Hồ sơ & 3 Lần khám gần nhất từ DB]
               │
               ▼
[BƯỚC 2: Trích xuất Bệnh Mạn tính & Cảnh báo Dị ứng Thuốc]
               │
               ▼
[BƯỚC 3: Xây dựng Prompt Thô & Khử Định danh PII]
               │
               ▼
[BƯỚC 4: Gọi AI Engine với PRE_VISIT_SYSTEM_PROMPT]
               │
               ▼
[BƯỚC 5: Gắn Tuyên bố Miễn trừ Trách nhiệm Y tế (Medical Disclaimer)]
               │
               ▼
[BƯỚC 6: Ghi Log AI Invocation Log (Prompt đã che, Độ trễ, Model)]
               │
               ▼
[BƯỚC 7: Trả JSON về Frontend & Render AIPreVisitCard]
               │
               ▼
[BƯỚC 8: HUMAN GATE 3 - Bác sĩ Thẩm định Trước khi Khám lâm sàng]
```

### 4.1. Cấu hình System Prompt Chuẩn (PRE_VISIT_SYSTEM_PROMPT)

```text
Bạn là Trợ lý AI Hành chính hỗ trợ Bác sĩ xem nhanh tóm tắt hồ sơ bệnh án trước khi vào khám (Pre-visit Briefing).
Dựa trên dữ liệu hồ sơ bệnh nhân được cung cấp:
1. Trích xuất và làm nổi bật: Cảnh báo Dị ứng thuốc/thực phẩm (NẾU CÓ).
2. Tóm tắt tiền sử bệnh lý mạn tính và các đợt khám/điều trị gần nhất.
3. Trình bày ngắn gọn, súc tích theo định dạng gạch đầu dòng rõ ràng để Bác sĩ nắm bắt trong 10 giây.
4. Không tự ý thêm bớt các triệu chứng hoặc chẩn đoán không có trong hồ sơ.
```

### 4.2. Danh mục Từ khóa Bệnh Mạn tính Nhận diện Tự động
Hệ thống tự động rà soát chuỗi `medical_history` để nhận diện các nhóm bệnh:
1. **Tim mạch**: Tăng huyết áp, Suy tim, Bệnh mạch vành, Rối loạn nhịp.
2. **Nội tiết / Chuyển hóa**: Đái tháo đường (Type 1, Type 2), Rối loạn lipid máu, Gout, Bệnh lý tuyến giáp.
3. **Hô hấp**: Hen phế quản (Asthma), COPD, Viêm phế quản mạn tính.
4. **Tiêu hóa**: Viêm loét dạ dày - tá tràng, Trào ngược dạ dày thực quản (GERD), Viêm gan B/C.
5. **Thận - Tiết niệu**: Suy thận mạn, Sỏi thận.

---

## 5. Human-in-the-loop Governance (Kiểm soát Con người & Human Gate 3)

| Trọng tâm | Quy định Bắt buộc |
|---|---|
| **Human Gate 3 (Clinical Validation Gate)** | Bác sĩ chuyên khoa bắt buộc phải xem xét bản tóm tắt AI, đối chiếu trực tiếp với triệu chứng lâm sàng và lời khai của người bệnh trước khi: <br>1. Đưa ra chẩn đoán ICD-10 cuối cùng. <br>2. Chỉ định cận lâm sàng (xét nghiệm, X-quang, siêu âm). <br>3. Kê đơn thuốc điều trị. |
| **Cơ chế Chỉnh sửa & Ghi đè (Override)** | Bác sĩ có toàn quyền chỉnh sửa lại thông tin tiền sử hoặc bổ sung dị ứng mới phát hiện vào hồ sơ bệnh nhân mà không bị ràng buộc bởi nội dung do AI sinh ra. |
| **Trách nhiệm Pháp lý** | Mọi quyết định chẩn đoán và điều trị thuộc về Bác sĩ phụ trách phòng khám; bản tóm tắt AI không có giá trị pháp lý thay thế chữ ký bác sĩ. |

---

## 6. Business & Compliance Rules (Quy tắc Nghiệp vụ & Bảo mật)

1. **Phân quyền RBAC**:
   - Chỉ người dùng có vai trò `doctor` (được phân công khám) hoặc `admin` mới được quyền gọi API `/api/v1/ai/pre-visit-summary`.
   - Lễ tân (`receptionist`) và Thu ngân (`accountant`) bị chặn 403 Forbidden nếu cố truy cập dữ liệu tóm tắt y khoa này.
2. **Khử định danh Bắt buộc (Mandatory PII De-identification)**:
   - Trước khi gửi nội dung tóm tắt sang LLM, trường `full_name` phải được thay bằng `[PATIENT_NAME_REDACTED]`.
   - Không đưa số điện thoại, CCCD, địa chỉ vào prompt tóm tắt lâm sàng.
3. **Medical Disclaimer Bắt buộc**:
   - Tất cả các payload trả về phải đính kèm chuỗi `MEDICAL_DISCLAIMER`.

---

## 7. Expected Outputs & Deliverables (Sản phẩm Đầu ra)

### 7.1. Cấu trúc JSON Phản hồi (`PreVisitSummaryResponse`)
```json
{
  "patient_id": 12,
  "patient_name": "Nguyễn Văn An",
  "medical_code": "BN-20260829-0012",
  "age": 48,
  "gender": "Nam",
  "allergies": "Dị ứng Penicillin (sốc phản vệ độ 1), dị ứng tôm cua",
  "medical_history": "Tăng huyết áp 5 năm điều trị liên tục, Đái tháo đường type 2",
  "recent_visits_summary": "- Ngày 10/07/2026: Tăng huyết áp vô căn (I10) (Đau đầu, chóng mặt)\n- Ngày 05/05/2026: Đái tháo đường không phụ thuộc insulin (E11) (Tái khám định kỳ)",
  "chronic_conditions": [
    "Tăng huyết áp",
    "Đái tháo đường"
  ],
  "clinical_alerts": [
    "CẢNH BÁO DỊ ỨNG: Dị ứng Penicillin (sốc phản vệ độ 1), dị ứng tôm cua",
    "Bệnh mạn tính cần theo dõi: Tăng huyết áp, Đái tháo đường"
  ],
  "summary": "• CẢNH BÁO: Bệnh nhân có tiền sử dị ứng nghiêm trọng với kháng sinh nhóm Penicillin.\n• Tiền sử mạn tính: Đang điều trị Tăng huyết áp và Đái tháo đường type 2.\n• 2 lần khám gần nhất: Đều ghi nhận kiểm soát huyết áp và đường huyết định kỳ.\n• Lưu ý lâm sàng: Tránh kê đơn nhóm Beta-lactam/Penicillin; kiểm tra tương tác thuốc hạ áp.",
  "content": "• CẢNH BÁO: Bệnh nhân có tiền sử dị ứng nghiêm trọng với kháng sinh nhóm Penicillin...",
  "disclaimer": "⚠️ TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y TẾ: Trợ lý AI chỉ phục vụ mục đích hành chính và hỗ trợ thông tin quy trình. Kết quả từ AI KHÔNG thay thế cho chẩn đoán, kết luận chuyên môn hoặc chỉ định điều trị của bác sĩ.",
  "disclaimer_included": true
}
```

### 7.2. Giao diện UI (`AIPreVisitCard.jsx`)
- Khối cảnh báo màu đỏ (`bg-rose-50 border-rose-200 text-rose-800`) khi bệnh nhân có dị ứng thuốc.
- Khối huy hiệu xanh lục (`badge bg-teal-50 text-teal-700`) cho danh sách bệnh mạn tính.
- Khối nội dung tóm tắt định dạng gạch đầu dòng rõ ràng kèm nhãn `AI-ASSISTED SUMMARY`.

---

## 8. Verification & Quality Acceptance Criteria (Tiêu chí Nghiệm thu)

### 8.1. Kiểm thử Tự động (Automated Verification)
```bash
pytest backend/tests/test_ai_features.py -k "test_pre_visit_summary" -v
```

### 8.2. Tiêu chí Chấp thuận (Acceptance Criteria)
- [x] **Trích xuất Đầy đủ Cảnh báo Dị ứng**: 100% bệnh nhân có dị ứng thuốc hiển thị cảnh báo đỏ nổi bật trong mảng `clinical_alerts`.
- [x] **Tự động Phát hiện Bệnh Mạn tính**: Nhận diện chính xác các từ khóa bệnh tim mạch, đái tháo đường, hen suyễn trong tiền sử.
- [x] **Khử định danh PII Hoàn tất**: Log kiểm toán trong `AIInvocationLog` không chứa tên bệnh nhân hoặc số điện thoại.
- [x] **Đính kèm Tuyên bố Miễn trừ**: Trường `disclaimer_included` luôn là `true` và chuỗi `MEDICAL_DISCLAIMER` hiện diện trong phản hồi.
- [x] **Tuân thủ Human Gate 3**: Giao diện yêu cầu bác sĩ xem xét tóm tắt trước khi nhấn nút "Lưu phiếu khám".
