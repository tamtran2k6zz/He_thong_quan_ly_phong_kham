# PROMPT GIAO VIỆC: XÂY DỰNG TÍNH NĂNG AI SINH HƯỚNG DẪN DẶN DÒ SAU KHÁM (DISCHARGE INSTRUCTIONS)
## Giai đoạn SDLC: Giai đoạn 3 – Administrative AI Assistant (KT3)
### Kỹ năng áp dụng: `.agents/skills/discharge-instructions/SKILL.md`

---

## 1. THÔNG TIN NGỮ CẢNH & MỤC TIÊU
* **Dự án:** Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp Trợ lý AI Hành chính (CMS-AI).
* **Đơn vị thực hiện:** Nhóm 07 (Đinh Gia Bảo - Trưởng nhóm, Trần Đặng Công Tâm).
* **Mục tiêu:** Phát triển tính năng AI tự động tổng hợp thông tin từ phiếu khám và đơn thuốc đã ký của bác sĩ để sinh ra tờ "Hướng dẫn Dặn dò Sau Khám & Nhắc Tái Khám" cho người bệnh; trình bày trực quan bảng chia lịch uống thuốc 4 bữa (Sáng - Trưa - Chiều - Tối), chế độ dinh dưỡng sinh hoạt kiêng cữ và các dấu hiệu cảnh báo khẩn cấp cần quay lại viện ngay.

---

## 2. VAI TRÒ CỦA AI AGENT (PERSONA)
Bạn là **Patient Education & Clinical Communication AI Specialist Agent (Chuyên gia AI Truyền thông Y tế & Hướng dẫn Người bệnh)**, am hiểu tâm lý người bệnh, có khả năng chuyển hóa các thuật ngữ dược học phức tạp thành hướng dẫn sinh hoạt đời thường dễ hiểu, rõ ràng, đặc biệt thân thiện với người cao tuổi.

---

## 3. RÀNG BUỘC KỸ THUẬT & QUY TẮC CỐT LÕI (GUARDRAILS)
1. **Dựa trên Đơn thuốc Đã duyệt:** AI chỉ được phép lập lịch uống thuốc dựa trên đúng danh mục thuốc và liều dùng mà Bác sĩ đã kê; tuyệt đối không tự ý thêm bớt thuốc.
2. **Quy tắc Bác sĩ Phê duyệt (Doctor-in-the-Loop Approval):** Bản hướng dẫn do AI sinh ra phải được hiển thị trên màn hình EMR để Bác sĩ xem xét, chỉnh sửa (nếu cần) và bấm nút "Phê duyệt & In" trước khi giao cho bệnh nhân.
3. **Mục Cảnh báo Dấu hiệu Đỏ (Red-Flag Warning Signs):** Bắt buộc phải có danh mục các triệu chứng nguy kịch (Khó thở dữ dội, sốt cao co giật, đau ngực lan ra cánh tay...) yêu cầu bệnh nhân đến ngay cơ sở y tế gần nhất.
4. **Định dạng Bảng Lịch uống thuốc Trực quan:** Chia rõ 4 cột Sáng - Trưa - Chiều - Tối và thời điểm uống (Trước ăn / Sau ăn).

---

## 4. NỘI DUNG MASTER PROMPT ĐÃ GIAO CHO AI AGENT

```markdown
Bạn hãy đóng vai trò là Patient Education AI Specialist. Hãy xây dựng toàn diện tính năng AI Sinh Hướng dẫn Dặn dò Sau khám cho dự án CMS-AI của Nhóm 07:

BƯỚC 1: XÂY DỰNG SKILL SINH HƯỚNG DẪN (.agents/skills/discharge-instructions/SKILL.md)
Tạo file SKILL.md quy định quy chuẩn dặn dò sau khám: Cấu trúc 5 phần của tờ hướng dẫn xuất viện chuẩn y khoa (1. Chẩn đoán & Lời dặn chung; 2. Bảng chia lịch uống thuốc 4 bữa; 3. Chế độ ăn uống sinh hoạt kiêng cữ; 4. Dấu hiệu cảnh báo đỏ nguy hiểm; 5. Lịch hẹn tái khám đề xuất).

BƯỚC 2: THIẾT KẾ CẤU TRÚC DỮ LIỆU ĐẦU RA (JSON Schema)
Định nghĩa cấu trúc kết xuất của AI gồm các trường:
- `diagnosis_summary`: Tóm tắt chẩn đoán bằng ngôn ngữ bình dân.
- `medication_schedule`: Mảng các đối tượng thuốc (tên thuốc, dạng dùng, sáng, trưa, chiều, tối, uống trước/sau ăn, lưu ý đặc biệt).
- `dietary_advice`: Lời khuyên nên ăn gì, kiêng gì (VD: tiểu đường kiêng đồ ngọt, tăng huyết áp giảm muối).
- `lifestyle_guidelines`: Vận động, nghỉ ngơi, uống đủ nước.
- `emergency_warning_signs`: Các dấu hiệu cảnh báo đỏ cấp cứu.
- `follow_up_recommendation`: Đề xuất ngày tái khám sau 7 ngày hoặc 14 ngày.
- `medical_disclaimer`: Tuyên bố miễn trừ trách nhiệm y tế.

BƯỚC 3: HIỆN THỰC HÓA API BACKEND (/api/v1/ai/discharge-instructions/{record_id})
1. Truy vấn `MedicalRecord` và `Prescription` tương ứng theo `record_id`.
2. Kiểm tra điều kiện tiên quyết: Ca khám phải ở trạng thái `COMPLETED` và đơn thuốc đã được tạo.
3. Khử định danh PII tên và thông tin liên hệ của bệnh nhân.
4. Gửi prompt đến AI Provider yêu cầu sinh định dạng bảng JSON.
5. Nếu chế độ offline/lỗi mạng, kích hoạt hàm `MockAIService.generate_discharge_instructions()`.
6. Lưu vết vào bảng `ai_invocation_logs`.
7. Trả về kết quả cho frontend.

BƯỚC 4: THIẾT KẾ GIAO DIỆN XEM VÀ IN HƯỚNG DẪN TRÊN REACT (frontend)
Xây dựng modal / component `DischargeInstructionsModal.jsx`:
- Bảng lịch uống thuốc trực quan có các biểu tượng mặt trời mọc (Sáng), mặt trời trưa (Trưa), hoàng hôn (Chiều), mặt trăng (Tối).
- Ô ghi chú cảnh báo đỏ có viền nổi bật.
- Nút "Bác sĩ phê duyệt & In phiếu hướng dẫn" kết nối với máy in phòng khám.
```

---

## 5. SẢN PHẨM ARTIFACTS KẾT XUẤT
1. [`.agents/skills/discharge-instructions/SKILL.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/.agents/skills/discharge-instructions/SKILL.md)
2. Module mã nguồn tích hợp trong `backend/app/api/v1/ai.py`
3. Component giao diện `frontend/src/components/DischargeInstructionsModal.jsx`
4. Bộ kiểm thử tự động trong `backend/tests/test_m3_ai.py`

---

## 6. KIỂM CHỨNG & HIỆU CHỈNH CỦA CON NGƯỜI (HUMAN GATE 3)
* **Lỗi do AI đề xuất:** AI ban đầu xếp thuốc kháng sinh nhóm Fluoroquinolone và thuốc kháng axit dạ dày chứa nhôm/magiê uống cùng một thời điểm vào bữa sáng. Về mặt dược học, ion kim loại sẽ tạo phức chelate làm mất hoàn toàn tác dụng của thuốc kháng sinh.
* **Hành động hiệu chỉnh của Kỹ sư Con người:** Kỹ sư Trưởng đã bổ sung quy tắc kiểm tra tương tác thuốc cơ bản vào Prompt và Logic hệ thống: Tự động tách giờ uống của các loại thuốc có tương tác bất lợi cách nhau tối thiểu 2 giờ, đồng thời bắt buộc Bác sĩ phải xem qua bảng chia lịch trước khi in phát cho người bệnh.
