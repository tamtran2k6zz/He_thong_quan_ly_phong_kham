---
name: discharge-instructions
description: Standard operating procedure for generating structured, patient-friendly post-visit discharge instructions, medication timing charts, dietary advice, emergency warning signs, and follow-up reminders.
objective: Enhance patient treatment adherence and post-visit safety by translating physician clinical diagnoses, prescriptions, and advice into clear, actionable, and structured home-care instructions.
inputs:
  - Medical Record ID / Encounter data
  - Confirmed physician ICD-10 diagnosis and clinical notes
  - Electronic prescription items (Medicine names, dosages, frequencies, specific administration instructions)
  - Recommended follow-up interval in days
process:
  - Step 1: Query medical record and associated prescription items from database
  - Step 2: Extract medication schedule details (Morning, Noon, Afternoon, Night, Before/After Meals)
  - Step 3: Sanitize patient identifiers via PII De-identification engine
  - Step 4: Construct prompt with DISCHARGE_SYSTEM_PROMPT
  - Step 5: Invoke AI provider to synthesize easy-to-understand lifestyle and dietary guidelines
  - Step 6: Identify disease-specific emergency red flags (Fever > 38.5C, Chest pain, Dyspnea, Drug rash)
  - Step 7: Append mandatory Medical Disclaimer and compute exact follow-up date
  - Step 8: Present instructions to attending physician for review and printout generation
rules:
  - Instructions must be 100% strictly aligned with the doctor's prescribed medications; never invent new drugs
  - Clear emergency escalation signs (Red Flags) must always be included
  - Mandatory Medical Disclaimer injection on every printed and digital discharge payload
  - Doctor approval is required before handing the printed sheet to the patient (Human-in-the-loop Gate)
outputs:
  - Structured discharge JSON object containing medication timetable, nutrition advice, warning signs, and follow-up date
  - Formatted printable discharge summary view for patient take-home package
  - Invocation record logged in AIInvocationLog table
verification:
  - Pytest test cases verifying correct medication list inclusion in discharge response
  - Integration tests ensuring follow-up days and warning signs are accurately structured
  - Validation confirming PII is anonymized in logs while restored on printed patient instructions
---

# Quy chuẩn Sinh Hướng dẫn Sau khám & Nhắc Tái khám (Post-Visit Discharge Instructions Skill)

> **Mục tiêu**: Chuẩn hóa quy trình tạo tài liệu dặn dò sau khám (Discharge Summary & Home Care Instructions) cho bệnh nhân sau khi kết thúc phiên khám bệnh; cung cấp lịch uống thuốc chi tiết, chế độ dinh dưỡng - sinh hoạt tương thích với bệnh lý, các dấu hiệu cảnh báo nguy hiểm cần tái khám ngay và lịch hẹn tái khám rõ ràng.

---

## 1. Objective (Mục tiêu Kỹ năng)

1. **Nâng cao Tuân thủ Điều trị (Treatment Adherence)**: Chuyển đổi các thuật ngữ chuyên môn phức tạp và đơn thuốc viết tắt thành bảng hướng dẫn uống thuốc dễ hiểu (sáng, trưa, chiều, tối, trước hoặc sau ăn), giúp bệnh nhân và người nhà dùng đúng liều, đúng giờ.
2. **Cung cấp Chế độ Chăm sóc & Dinh dưỡng Phù hợp (Dietary & Lifestyle Guidance)**: Tự động tổng hợp lời khuyên về chế độ ăn (ví dụ: hạn chế muối cho bệnh nhân tăng huyết áp, kiêng đường ngọt cho bệnh nhân đái tháo đường) và chế độ nghỉ ngơi.
3. **Thiết lập Cảnh báo Dấu hiệu Nguy hiểm (Red Flag Warning Signs)**: Liệt kê rõ ràng các triệu chứng bất thường cần đến bệnh viện/phòng khám cấp cứu ngay (sốt cao co giật, khó thở, tức ngực, dị ứng ngứa môi sau uống thuốc).
4. **Tự động hóa Nhắc Lịch Tái khám (Follow-up Scheduling)**: Tính toán chính xác ngày tái khám dựa trên số ngày hẹn của Bác sĩ để hỗ trợ Lễ tân đặt lịch trước.

---

## 2. Terminology & Conceptual Model (Phân định Khái niệm)

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. CODEX (AI Autonomous Agent)                                         │
│    - Agent tiếp nhận chẩn đoán và đơn thuốc đã được Bác sĩ phê duyệt   │
│    - Sinh nội dung dặn dò ngôn ngữ thân thiện, chuẩn văn phong y tế   │
├────────────────────────────────────────────────────────────────────────┤
│ 2. SKILL (Quy trình & Tiêu chuẩn Thủ tục - File này)                   │
│    - Quy định cấu trúc bảng thuốc, tiêu chí dấu hiệu nguy hiểm, mẫu     │
│      dặn dò theo nhóm bệnh và quy trình kiểm duyệt con người           │
├────────────────────────────────────────────────────────────────────────┤
│ 3. TOOL (Thao tác Môi trường / Service Function)                       │
│    - `AdminAIService.generate_discharge_instructions()`               │
│    - Truy vấn CSDL `Prescription`, `PrescriptionItem`, `MedicalRecord` │
├────────────────────────────────────────────────────────────────────────┤
│ 4. MCP / Print & Export Component                                      │
│    - Modal in phiếu dặn dò `InvoicePrintModal.jsx` / `DischargeView`   │
│    - Định dạng xuất PDF / In nhiệt cho bệnh nhân mang về nhà          │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Inputs & Prerequisites (Dữ liệu Đầu vào & Điều kiện Tiên quyết)

### 3.1. Dữ liệu Đầu vào
- `medical_record_id` (int): Mã định danh phiếu khám đã hoàn thành.
- `discharge_data` (dict, tùy chọn khi test trực tiếp):
  - `patient_name` (str): Tên bệnh nhân.
  - `diagnosis_text` (str): Chẩn đoán bệnh bằng lời của bác sĩ.
  - `diagnosis_icd10` (str): Mã bệnh ICD-10 (VD: `J02.9`, `K21.0`).
  - `doctor_advice` (str): Lời dặn dò chuyên môn của bác sĩ.
  - `follow_up_days` (int): Số ngày hẹn tái khám (VD: 7 ngày, 14 ngày, 30 ngày).
  - `prescriptions` (list): Danh sách thuốc đã kê gồm tên thuốc, hàm lượng, số lượng, liều dùng, cách dùng.

### 3.2. Điều kiện Tiên quyết
- Phiếu khám lâm sàng đã có kết luận chẩn đoán và đã được Bác sĩ ký số / lưu đơn thuốc vào CSDL.
- Bệnh nhân đã hoàn tất thăm khám và chuẩn bị chuyển sang bước thanh toán / nhận thuốc.

---

## 4. Execution Process (Quy trình Thực thi Từng bước)

```
[Bác sĩ hoàn tất Kê đơn & Kết luận Khám]
                  │
                  ▼
[BƯỚC 1: Truy vấn Chi tiết Đơn thuốc & Lời dặn từ CSDL]
                  │
                  ▼
[BƯỚC 2: Định dạng Danh mục Thuốc thành Bảng Uống Thuốc Chuẩn]
                  │
                  ▼
[BƯỚC 3: Khử định danh PII trước khi gửi Prompt]
                  │
                  ▼
[BƯỚC 4: Gọi AI Engine với DISCHARGE_SYSTEM_PROMPT]
                  │
                  ▼
[BƯỚC 5: Tổng hợp Chế độ Ăn uống, Sinh hoạt & Dấu hiệu Cấp cứu]
                  │
                  ▼
[BƯỚC 6: Gắn Medical Disclaimer & Ghi log AIInvocationLog]
                  │
                  ▼
[BƯỚC 7: Trả JSON về Frontend & Bác sĩ Xem lại (HUMAN GATE)]
                  │
                  ▼
[BƯỚC 8: In Bản Hướng Dẫn Kèm Đơn Thuốc Trao Cho Bệnh Nhân]
```

### 4.1. Cấu hình System Prompt (DISCHARGE_SYSTEM_PROMPT)

```text
Bạn là Trợ lý AI Hành chính hỗ trợ Bác sĩ tạo bản Hướng dẫn dặn dò sau khám và Nhắc lịch tái khám cho bệnh nhân (Post-visit Discharge Instructions).
Dựa trên thông tin chẩn đoán, lời dặn của bác sĩ và đơn thuốc đã kê:
1. Trình bày rõ ràng Lịch uống thuốc (Tên thuốc, liều lượng, thời điểm uống: trước/sau ăn).
2. Tóm tắt chế độ ăn uống, sinh hoạt, nghỉ ngơi phù hợp với bệnh lý.
3. Liệt kê các dấu hiệu bất thường cần đến cơ sở y tế ngay.
4. Nhắc nhở thời gian tái khám theo chỉ định.
5. Ngôn ngữ thân thiện, dễ hiểu cho người bệnh và thân nhân.
```

### 4.2. Bộ Quy tắc Cảnh báo Dấu hiệu Nguy hiểm (Emergency Red Flags Matrix)
Tất cả các bản hướng dẫn sau khám bắt buộc phải có ít nhất 3 dấu hiệu cấp cứu:
1. **Dấu hiệu Phản ứng Thuốc**: Nổi ban đỏ rải rác, ngứa toàn thân, sưng mí mắt, sưng môi, khó thở sau khi uống thuốc -> *Ngừng thuốc ngay và đến cơ sở y tế gần nhất*.
2. **Dấu hiệu Toàn thân Nặng**: Sốt cao liên tục trên 38.5°C không hạ sau khi dùng thuốc hạ sốt, li bì, nôn ói liên tục không uống được nước.
3. **Dấu hiệu Chuyên khoa**: Đau ngực dữ dội lan ra cánh tay trái, khó thở tím tái, đau bụng tăng dần liên tục không giảm.

---

## 5. Human-in-the-loop Governance (Kiểm soát Con người)

| Vai trò | Điểm Kiểm soát | Hành động Bắt buộc |
|---|---|---|
| **Bác sĩ (Doctor)** | *Pre-print Review Gate* | Xem lại toàn bộ bảng hướng dẫn do AI sinh ra trước khi nhấn nút "In đơn & Hướng dẫn". Bác sĩ có quyền sửa đổi bất kỳ câu chữ nào. |
| **Dược sĩ / Lễ tân** | *Dispensing Cross-Check* | Khi phát thuốc tại quầy, đối chiếu danh sách thuốc trên bản dặn dò với số lượng và tên thuốc thực tế trong túi thuốc trao cho bệnh nhân. |
| **Bệnh nhân / Thân nhân** | *Patient Acknowledgment* | Được giải thích trực tiếp cách uống thuốc và ký xác nhận đã hiểu rõ lịch tái khám. |

---

## 6. Business & Compliance Rules (Quy định Nghiệp vụ & Pháp lý)

1. **Khớp Tuyệt đối với Đơn Thuốc (Prescription Exact Match)**:
   - AI tuyệt đối không tự thêm tên thuốc mới, không tự thay đổi liều lượng đã được Bác sĩ kê trong CSDL `PrescriptionItem`.
2. **Medical Disclaimer Bắt buộc**:
   - Mọi bản in và bản kỹ thuật số phải có dòng cảnh báo: `⚠️ TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y TẾ: Trợ lý AI chỉ phục vụ mục đích hành chính...`.
3. **Khôi phục Định danh khi In ấn (Safe De-anonymization for Printing)**:
   - Trên bản in trao cho bệnh nhân, tên bệnh nhân và mã hồ sơ được khôi phục chính xác từ CSDL phòng khám để đảm bảo quyền lợi cá nhân của người bệnh.

---

## 7. Expected Outputs & Deliverables (Sản phẩm Đầu ra)

### 7.1. Cấu trúc JSON Phản hồi (`DischargeInstructionsResponse`)
```json
{
  "medical_record_id": 45,
  "diagnosis": "Viêm loét dạ dày - tá tràng (K25.9)",
  "medication_schedule": [
    {
      "medicine_name": "Nexium 40mg (Esomeprazole)",
      "dosage": "1 viên",
      "frequency": "1 lần/ngày",
      "instructions": "Uống trước bữa ăn sáng 30 phút, nuốt nguyên viên thuốc không nhai"
    },
    {
      "medicine_name": "Gaviscon Suspension",
      "dosage": "1 gói",
      "frequency": "3 lần/ngày",
      "instructions": "Uống sau 3 bữa ăn chính và trước khi đi ngủ"
    }
  ],
  "dietary_guidelines": "Ăn thức ăn chín mềm, chia nhỏ bữa ăn (4-5 bữa/ngày). Tuyệt đối kiêng rượu bia, cà phê, ớt, tiêu, đồ chua lên men và thức uống có ga. Tránh nằm ngay sau khi ăn ít nhất 2 giờ.",
  "activity_recommendations": "Tránh căng thẳng thần kinh (stress), ngủ đủ 7-8 tiếng/ngày, không thức khuya sau 22h30.",
  "warning_signs": [
    "Đau bụng dữ dội đột ngột, bụng cứng như gỗ",
    "Nôn ra máu hoặc đi ngoài phân đen như bã cà phê",
    "Chóng mặt, hoa mắt, vã mồ hôi lạnh, ngất xỉu",
    "Nổi mề đay, khó thở sau khi uống thuốc"
  ],
  "follow_up_advice": "Tái khám sau 14 ngày (ngày 12/09/2026) kèm kết quả nội soi kiểm tra hoặc tái khám ngay khi có dấu hiệu bất thường.",
  "instructions": "HƯỚNG DẪN CHĂM SÓC VÀ UỐNG THUỐC TẠI NHÀ\n...",
  "content": "HƯỚNG DẪN CHĂM SÓC VÀ UỐNG THUỐC TẠI NHÀ\n...",
  "disclaimer": "⚠️ TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y TẾ: Trợ lý AI chỉ phục vụ mục đích hành chính và hỗ trợ thông tin quy trình. Kết quả từ AI KHÔNG thay thế cho chẩn đoán, kết luận chuyên môn hoặc chỉ định điều trị của bác sĩ.",
  "disclaimer_included": true
}
```

### 7.2. Giao diện In ấn (`InvoicePrintModal.jsx` / `DischargeSection`)
- Bảng lịch uống thuốc dạng lưới (Grid) chia rõ các cột: Tên thuốc - Liều lượng - Buổi Sáng - Buổi Trưa - Buổi Tối - Lời dặn.
- Hộp cảnh báo dấu hiệu cấp cứu có viền màu hổ phách (`border-amber-400 bg-amber-50`).
- Chữ ký bác sĩ điều trị và lời chúc sức khỏe.

---

## 8. Verification & Quality Acceptance Criteria (Tiêu chí Nghiệm thu)

### 8.1. Kiểm thử Tự động (Automated Verification)
```bash
pytest backend/tests/test_ai_features.py -k "test_discharge_instructions" -v
```

### 8.2. Tiêu chí Chấp thuận (Acceptance Criteria)
- [x] **100% Khớp Đơn Thuốc**: Toàn bộ danh mục thuốc trong đơn được đưa vào trường `medication_schedule` với hướng dẫn sử dụng rõ ràng.
- [x] **Bao hàm Đủ 4 Mục Trọng Yếu**: 1. Lịch uống thuốc; 2. Chế độ ăn uống/sinh hoạt; 3. Dấu hiệu nguy hiểm (Warning Signs); 4. Ngày hẹn tái khám.
- [x] **Tính Toán Ngày Tái Khám Chính Xác**: Số ngày tái khám khớp với chỉ định của bác sĩ trong phiếu khám.
- [x] **Bảo Mật PII**: Trong quá trình gọi AI, toàn bộ dữ liệu định danh được che chắn an toàn và lưu vào `AIInvocationLog`.
- [x] **Đính Kèm Medical Disclaimer**: Luôn có cảnh báo pháp lý y tế trên mọi ấn bản.
