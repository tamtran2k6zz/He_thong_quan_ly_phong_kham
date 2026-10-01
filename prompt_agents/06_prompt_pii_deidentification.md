# PROMPT GIAO VIỆC: XÂY DỰNG MODULE KHỬ ĐỊNH DANH DỮ LIỆU Y TẾ (PII DE-IDENTIFICATION)
## Giai đoạn SDLC: Giai đoạn 3 – AI Integration & Medical Privacy (KT3)
### Kỹ năng áp dụng: `.agents/skills/pii-deidentification/SKILL.md`

---

## 1. THÔNG TIN NGỮ CẢNH & MỤC TIÊU
* **Dự án:** Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp Trợ lý AI Hành chính (CMS-AI).
* **Đơn vị thực hiện:** Nhóm 07 (Đinh Gia Bảo - Trưởng nhóm, Trần Đặng Công Tâm).
* **Mục tiêu:** Xây dựng module xử lý quyền riêng tư y tế theo Nghị định 13/2023/NĐ-CP, tự động nhận diện và che giấu/thay thế 100% các trường định danh nhạy cảm (Số CCCD, Số điện thoại Việt Nam, Mã thẻ BHYT, Họ tên bệnh nhân) bằng các token ẩn danh trước khi chuyển prompt sang các mô hình AI bên ngoài.

---

## 2. VAI TRÒ CỦA AI AGENT (PERSONA)
Bạn là **Healthcare Privacy & Compliance Engineer Agent (Kỹ sư An toàn & Tuân thủ Dữ liệu Y tế)**, chuyên gia về quy định bảo vệ dữ liệu người bệnh (HIPAA, GDPR, Nghị định 13/2023/NĐ-CP), am hiểu kỹ thuật xử lý văn bản tiếng Việt và biểu thức chính quy (Regex) hiệu năng cao.

---

## 3. RÀNG BUỘC KỸ THUẬT & QUY TẮC CỐT LÕI (GUARDRAILS)
1. **Zero Data Leakage:** Tuyệt đối không cho phép bất kỳ chuỗi số CCCD (12 số), số điện thoại VN (10 số), mã BHYT (15 ký tự) nào xuất hiện trong prompt gửi đến OpenAI/Gemini.
2. **Tránh Che nhầm Dữ liệu Y khoa (False Positives):** Regex không được che nhầm các thông số sinh hiệu lâm sàng như Huyết áp (120/80 mmHg), Nhịp tim (85 bpm), Liều thuốc (500mg, 10ml).
3. **Hiệu năng cao (< 1ms):** Biên dịch sẵn các mẫu biểu thức chính quy (`re.compile`), thực hiện thay thế trên bộ nhớ nội bộ, không phụ thuộc dịch vụ ngoài.
4. **Cơ chế Khôi phục 2 chiều (Reversible Tokenization):** Có bảng ánh xạ tạm thời trong phiên làm việc để khôi phục tên bệnh nhân nếu giao diện bác sĩ yêu cầu hiển thị lại.

---

## 4. NỘI DUNG MASTER PROMPT ĐÃ GIAO CHO AI AGENT

```markdown
Bạn hãy đóng vai trò là Healthcare Privacy & Compliance Engineer. Hãy xây dựng toàn diện module Khử định danh Dữ liệu Y tế cho dự án CMS-AI của Nhóm 07:

BƯỚC 1: XÂY DỰNG SKILL KHỬ ĐỊNH DANH PII (.agents/skills/pii-deidentification/SKILL.md)
Tạo file SKILL.md quy chuẩn hóa quy trình khử định danh: Định nghĩa các loại PII theo luật Việt Nam, danh mục thẻ thay thế ([PATIENT_REDACTED], [PHONE_REDACTED], [CCCD_REDACTED], [BHYT_REDACTED]), bảng regex patterns và quy trình kiểm chuẩn lâm sàng.

BƯỚC 2: HIỆN THỰC HÓA CLASS PIIAnonymizer (backend/app/ai/anonymizer.py)
Xây dựng lớp `PIIAnonymizer` có 2 phương thức chính:
1. `anonymize(text: str, patient_name: str = None) -> Tuple[str, dict]`:
   - Thay thế số CCCD 12 chữ số bằng `[CCCD_REDACTED]`.
   - Thay thế số điện thoại Việt Nam (đầu 03, 05, 07, 08, 09, 10 chữ số) bằng `[PHONE_REDACTED]`.
   - Thay thế mã thẻ BHYT (2 chữ cái + 13 chữ số) bằng `[BHYT_REDACTED]`.
   - Nếu có cung cấp `patient_name`, thay thế toàn bộ họ tên và các từ đơn trong tên bằng `[PATIENT_REDACTED]`.
   - Trả về văn bản đã che và bảng ánh xạ khôi phục `mask_mapping`.
2. `deanonymize(text: str, mask_mapping: dict) -> str`:
   - Duyệt qua bảng ánh xạ và thay thế ngược các token về giá trị ban đầu phục vụ hiển thị nội bộ.

BƯỚC 3: XÂY DỰNG BỘ TEST CHỐNG CHE NHẦM THÔNG SỐ LÂM SÀNG
Viết các test cases kiểm thử:
- Đảm bảo các chỉ số: "Huyết áp 120/80 mmHg, SpO2 98%, thân nhiệt 37.5 C, uống Paracetamol 500mg" không bao giờ bị nhận nhầm thành SĐT hay CCCD.
- Kiểm tra văn bản có nhiều thông tin nhạy cảm đan xen đều được che giấu 100%.
```

---

## 5. SẢN PHẨM ARTIFACTS KẾT XUẤT
1. [`.agents/skills/pii-deidentification/SKILL.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/.agents/skills/pii-deidentification/SKILL.md)
2. Module mã nguồn [`backend/app/ai/anonymizer.py`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/backend/app/ai/anonymizer.py)
3. Bộ test case bảo mật trong [`backend/tests/test_m3_anonymizer.py`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/backend/tests/test_m3_anonymizer.py)

---

## 6. KIỂM CHỨNG & HIỆU CHỈNH CỦA CON NGƯỜI (HUMAN GATE 3)
* **Lỗi do AI đề xuất:** Regex nhận diện số điện thoại ban đầu của AI quá tham lam (`\d{9,11}`), dẫn đến việc chuỗi ghi chép liều thuốc *"Uống 500mg sáng và 500mg tối"* hoặc huyết áp *"120/80"* bị AI che nhầm thành `[PHONE_REDACTED]`, làm mất ngữ cảnh bệnh học nghiêm trọng.
* **Hành động hiệu chỉnh của Kỹ sư Con người:** Kỹ sư Trưởng đã can thiệp, siết chặt ranh giới từ `\b` và chỉ định đích danh các đầu số nhà mạng viễn thông Việt Nam (`03|05|07|08|09\d{8}`), loại trừ toàn bộ các chuỗi có chứa đơn vị đo y khoa (`mg`, `ml`, `mmHg`, `/`).
