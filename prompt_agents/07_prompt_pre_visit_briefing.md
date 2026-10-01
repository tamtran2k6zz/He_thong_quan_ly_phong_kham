# PROMPT GIAO VIỆC: XÂY DỰNG TÍNH NĂNG AI TÓM TẮT HỒ SƠ TIỀN KHÁM (PRE-VISIT BRIEFING)
## Giai đoạn SDLC: Giai đoạn 3 – Administrative AI Assistant (KT3)
### Kỹ năng áp dụng: `.agents/skills/pre-visit-briefing/SKILL.md`

---

## 1. THÔNG TIN NGỮ CẢNH & MỤC TIÊU
* **Dự án:** Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp Trợ lý AI Hành chính (CMS-AI).
* **Đơn vị thực hiện:** Nhóm 07 (Đinh Gia Bảo - Trưởng nhóm, Trần Đặng Công Tâm).
* **Mục tiêu:** Phát triển tính năng Trợ lý AI tóm tắt hồ sơ bệnh án tự động trong vòng 10 giây cho bác sĩ trước khi bắt đầu phiên khám lâm sàng; trích xuất cô đọng tiền sử bệnh mạn tính, các chẩn đoán điều trị trong 5 lần khám gần nhất và bắt buộc làm nổi bật cảnh báo dị ứng thuốc nguy hiểm.

---

## 2. VAI TRÒ CỦA AI AGENT (PERSONA)
Bạn là **Clinical AI Prompt Engineer & Healthcare UX Agent (Kỹ sư Prompt Y tế & Trải nghiệm Bác sĩ)**, chuyên thiết kế prompt cho các mô hình LLM trong môi trường lâm sàng áp lực cao, am hiểu thói quen đọc bệnh án của bác sĩ chuyên khoa và quy chuẩn định dạng thông tin cứu sinh khẩn cấp.

---

## 3. RÀNG BUỘC KỸ THUẬT & QUY TẮC CỐT LÕI (GUARDRAILS)
1. **Quy tắc 10 giây (10-Second Readability):** Tóm tắt phải có định dạng gạch đầu dòng ngắn gọn, cô đọng, không viết thành đoạn văn dài dòng gây mất thời gian của bác sĩ.
2. **Cảnh báo Dị ứng Thuốc Đỏ (Red-Alert Allergies):** Bất kỳ thông tin dị ứng thuốc nào (Penicillin, Aspirin, Sulfonamide...) phải được đặt ngay ở đầu tóm tắt với nhãn `[CẢNH BÁO DỊ ỨNG THUỐC]`.
3. **Bắt buộc Khử PII:** Dữ liệu đầu vào bắt buộc phải đi qua `PIIAnonymizer.anonymize()` trước khi gửi tới mô hình AI.
4. **Tuyên bố Miễn trừ Y tế (Medical Disclaimer):** Toàn bộ kết quả trả về bắt buộc có câu disclaimer: *"Tóm tắt do AI hỗ trợ hành chính, bác sĩ cần đối soát hồ sơ gốc trước khi ra quyết định lâm sàng"*.
5. **Offline Fallback:** Nếu mất mạng hoặc API lỗi, hệ thống phải tự động fallback sang Deterministic Rule-based Summarizer.

---

## 4. NỘI DUNG MASTER PROMPT ĐÃ GIAO CHO AI AGENT

```markdown
Bạn hãy đóng vai trò là Clinical AI Prompt Engineer. Hãy xây dựng toàn diện tính năng AI Pre-visit Briefing cho dự án CMS-AI của Nhóm 07:

BƯỚC 1: XÂY DỰNG SKILL TÓM TẮT HỒ SƠ (.agents/skills/pre-visit-briefing/SKILL.md)
Tạo file SKILL.md quy định tiêu chuẩn tóm tắt bệnh án: Cấu trúc 4 phần của một bản briefing hoàn chỉnh (1. Cảnh báo dị ứng; 2. Bệnh nền mạn tính; 3. Lịch sử các lần khám gần nhất; 4. Lý do đến khám hôm nay), quy định độ dài tối đa 200 từ và quy tắc an toàn y tế.

BƯỚC 2: THIẾT KẾ SYSTEM PROMPT & CLINICAL PROMPT TEMPLATE
Xây dựng prompt template truyền vào cho LLM:
- Khóa ngữ cảnh: "Bạn là Trợ lý AI Hành chính y tế hỗ trợ Bác sĩ. Bạn KHÔNG được đưa ra chẩn đoán mới, chỉ tóm tắt sự kiện đã có trong bệnh án."
- Dữ liệu đưa vào: Tiền sử dị ứng, bệnh mạn tính, 5 phiếu khám gần nhất đã được khử định danh PII.
- Định dạng kết xuất JSON có cấu trúc gồm: `allergies_alert`, `chronic_conditions`, `recent_visits_summary`, `chief_complaint`, `medical_disclaimer`.

BƯỚC 3: HIỆN THỰC HÓA API SERVICE TRONG BACKEND (backend/app/ai/)
Tạo hàm `generate_pre_visit_summary(patient_id: int, db: Session)`:
1. Truy vấn thông tin `Patient` và các `MedicalRecord` liên quan từ CSDL.
2. Gọi `PIIAnonymizer.anonymize()` che sạch số điện thoại, CCCD.
3. Gửi prompt tới `AIProvider` (Gemini / OpenAI / Ollama).
4. Nếu có lỗi mạng hoặc API timeout, lập tức kích hoạt `MockAIService.generate_pre_visit_summary()`.
5. Ghi vết toàn bộ prompt và response vào bảng `ai_invocation_logs`.
6. Trả về kết quả cho Router `/api/v1/ai/pre-visit-summary/{patient_id}`.

BƯỚC 4: THIẾT KẾ THẺ TÓM TẮT TRÊN GIAO DIỆN PHÒNG KHÁM BÁC SĨ (frontend)
Xây dựng component `PreVisitSummaryCard.jsx` hiển thị ngay đầu màn hình khám bệnh: Badge cảnh báo dị ứng màu đỏ nổi bật, bảng tóm tắt 3 lần khám gần nhất và nút xem chi tiết hồ sơ gốc.
```

---

## 5. SẢN PHẨM ARTIFACTS KẾT XUẤT
1. [`.agents/skills/pre-visit-briefing/SKILL.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/.agents/skills/pre-visit-briefing/SKILL.md)
2. Module mã nguồn tích hợp trong `backend/app/api/v1/ai.py`
3. Component giao diện `frontend/src/components/PreVisitBriefing.jsx`
4. Bộ kiểm thử tự động trong `backend/tests/test_m3_ai.py`

---

## 6. KIỂM CHỨNG & HIỆU CHỈNH CỦA CON NGƯỜI (HUMAN GATE 3)
* **Lỗi do AI đề xuất:** AI ban đầu tự ý tổng hợp các triệu chứng cũ của bệnh nhân và suy diễn thêm câu kết luận: *"Khả năng cao bệnh nhân đã chuyển biến sang đái tháo đường tuýp 2, bác sĩ nên chỉ định tiêm Insulin"*. Đây là lỗi vi phạm nghiêm trọng ranh giới đạo đức y khoa (AI tự chẩn đoán và tự chỉ định điều trị).
* **Hành động hiệu chỉnh của Kỹ sư Con người:** Kỹ sư Trưởng đã ngay lập tức khóa chặt System Prompt bằng chỉ thị cấm đoán nghiêm ngặt (Strict Negative Constraint): *"Chỉ được liệt kê các sự kiện lịch sử đã được bác sĩ trước đó kết luận; tuyệt đối không đưa ra bất kỳ dự đoán, chẩn đoán hay gợi ý điều trị nào mới"*.
