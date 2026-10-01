# PROMPT GIAO VIỆC: MÔ HÌNH HÓA TRỰC QUAN UML & THIẾT KẾ HƯỚNG ĐỐI TƯỢNG (OOD)
## Giai đoạn SDLC: Giai đoạn 1 & 2 – Object-Oriented Design & Visual Modeling
### Kỹ năng áp dụng: `.agents/skills/diagram-design/SKILL.md`

---

## 1. THÔNG TIN NGỮ CẢNH & MỤC TIÊU
* **Dự án:** Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp Trợ lý AI Hành chính (CMS-AI).
* **Đơn vị thực hiện:** Nhóm 07 (Đinh Gia Bảo - Trưởng nhóm, Trần Đặng Công Tâm).
* **Mục tiêu:** Xây dựng tài liệu thiết kế hướng đối tượng (OOD) toàn diện từ 10 lớp nghiệp vụ cốt lõi, mô hình hóa trực quan hệ thống biểu đồ UML 2.5 (Use Case 4 Actor, Class Diagram 10 thực thể, 5 Sequence Diagrams, 2 Activity Diagrams, 3 State Machine Diagrams) và cung cấp bộ AI Visualization Prompts phục vụ render đồ họa vector báo cáo bảo vệ.

---

## 2. VAI TRÒ CỦA AI AGENT (PERSONA)
Bạn là **Lead Software Modeling & UML Systems Engineer Agent (Kỹ sư Trưởng Mô hình hóa Phần mềm & UML)**, thành thạo chuẩn UML 2.5 của OMG, có khả năng viết mã nguồn Mermaid.js và PlantUML chuẩn xác, không lỗi cú pháp, trực quan hóa được các luồng nghiệp vụ phức tạp.

---

## 3. RÀNG BUỘC KỸ THUẬT & QUY TẮC CỐT LÕI (GUARDRAILS)
1. **Tác nhân AI trong Use Case:** AI Assistant phải được định vị là Supporting Actor, tuyệt đối không gán Use Case tự chẩn đoán bệnh.
2. **Quan hệ `<<include>>` và `<<extend>>`:** Sử dụng đúng ngữ nghĩa UML 2.5:
   - `<<include>>`: Đặt lịch -> Kiểm tra xung đột; Gọi AI -> Khử định danh PII; Kê đơn -> Kiểm tra dị ứng thuốc & Tồn kho dược.
   - `<<extend>>`: Kê đơn -> Cảnh báo sốc phản vệ; Gọi AI -> Tự động chuyển Fallback Offline Mock.
3. **Đặc tả 10 Class cốt lõi:** Phải khớp 100% với tài liệu thiết kế hướng đối tượng: `User`, `Patient`, `Doctor`, `Appointment`, `ConflictChecker`, `MedicalRecord`, `Medicine`, `Invoice`, `PIIAnonymizer`, `AdminAIService`.
4. **Cú pháp Mermaid:** 100% các khối mã Mermaid phải render trơn tru trong Markdown, không dùng ký tự đặc biệt gây vỡ khối render.

---

## 4. NỘI DUNG MASTER PROMPT ĐÃ GIAO CHO AI AGENT

```markdown
Bạn hãy đóng vai trò là Lead UML Systems Engineer. Hãy thực hiện toàn diện quy trình Thiết kế Hướng đối tượng và Mô hình hóa Biểu đồ cho dự án CMS-AI của Nhóm 07:

BƯỚC 1: XÂY DỰNG SKILL THIẾT KẾ BIỂU ĐỒ (.agents/skills/diagram-design/SKILL.md)
Tạo file SKILL.md quy định quy chuẩn mô hình hóa: Phương pháp luận Use Case, quy chuẩn Class Diagram từ 10 lớp, quy chuẩn Sequence Diagrams cho 5 luồng cốt lõi, Activity Diagrams cho quy trình khám khép kín và State Machine Diagrams.

BƯỚC 2: BIÊN SOẠN TÀI LIỆU THIẾT KẾ HƯỚNG ĐỐI TƯỢNG (docs/thiet-ke-huong-doi-tuong-class-diagram.md)
Trình bày chi tiết:
1. Mô hình lớp (Class Diagram) tổng thể kết nối 10 thực thể cốt lõi kèm các mối quan hệ Association, Aggregation, Composition, Dependency.
2. Đặc tả chi tiết từng Class theo biểu mẫu học phần:
   - Các thuộc tính: Tên, Kiểu dữ liệu, Kích thước/Ràng buộc, Mô tả ý nghĩa.
   - Các phương thức: Tên, Mô tả, Tham số đầu vào (tên, kiểu, kích thước), Kết quả đầu ra (tên, kiểu, kích thước), Luồng xử lý từng bước, Điều kiện bắt đầu (Pre-conditions), Điều kiện kết thúc (Post-conditions).
   - Áp dụng đầy đủ cho 10 lớp: User, Patient, Doctor, Appointment, ConflictChecker, MedicalRecord, Medicine, Invoice, PIIAnonymizer, AdminAIService.

BƯỚC 3: MÔ HÌNH HÓA 5 BIỂU ĐỒ TUẦN TỰ SEQUENCE DIAGRAMS
Thiết kế biểu đồ tương tác thời gian thực bằng Mermaid cho 5 kịch bản quan trọng nhất:
- Kịch bản 1: Lễ tân đặt lịch khám & Động cơ ConflictChecker phát hiện xung đột thời gian thực.
- Kịch bản 2: Bác sĩ mở ca khám & Trợ lý AI tóm tắt tiền sử bệnh án 10 giây (kèm bước Khử định danh PII).
- Kịch bản 3: Bác sĩ kê đơn thuốc, kiểm tra dị ứng tiền sử người bệnh và trừ kho Dược.
- Kịch bản 4: Thu ngân lập hóa đơn viện phí, tính khấu trừ BHYT và sinh mã thanh toán VietQR động Napas247.
- Kịch bản 5: Chatbot FAQ quy trình phòng khám kích hoạt Guardrail chặn câu hỏi chẩn đoán bệnh học.

BƯỚC 4: THIẾT KẾ BIỂU ĐỒ HOẠT ĐỘNG VÀ BIỂU ĐỒ TRẠNG THÁI
- Activity Diagram: Mô hình hóa quy trình khám chữa bệnh khép kín (End-to-End Workflow) và giải thuật kiểm tra xung đột thời gian thực.
- State Machine Diagram: Vòng đời trạng thái của Lịch hẹn (`Appointment`: PENDING -> CONFIRMED -> CHECKED_IN -> IN_PROGRESS -> COMPLETED), Phiếu khám (`MedicalRecord`: IN_EXAM -> COMPLETED) và Hóa đơn (`Invoice`: PENDING -> PAID).

BƯỚC 5: XÂY DỰNG BỘ AI VISUALIZATION PROMPTS
Soạn sẵn 4 mẫu prompt chi tiết để sinh viên có thể dán vào ChatGPT / Midjourney / Draw.io / PlantUML nhằm xuất ra hình ảnh đồ họa vector trực quan phục vụ báo cáo.
```

---

## 5. SẢN PHẨM ARTIFACTS KẾT XUẤT
1. [`.agents/skills/diagram-design/SKILL.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/.agents/skills/diagram-design/SKILL.md)
2. [`docs/thiet-ke-huong-doi-tuong-class-diagram.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/docs/thiet-ke-huong-doi-tuong-class-diagram.md)
3. Script sinh tài liệu Word OOD chuẩn chỉnh: [`scripts/generate_class_diagram_docx.py`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/scripts/generate_class_diagram_docx.py)

---

## 6. KIỂM CHỨNG & HIỆU CHỈNH CỦA CON NGƯỜI (HUMAN GATE 2)
* **Lỗi do AI đề xuất:** Khi vẽ sơ đồ Sequence cho tính năng AI Pre-visit Briefing, AI đã cho gọi trực tiếp từ `Frontend` sang `LLM Cloud API` mà bỏ qua bước lọc dữ liệu qua module `PIIAnonymizer` và không ghi log vào CSDL.
* **Hành động hiệu chỉnh của Kỹ sư Con người:** Kỹ sư Trưởng đã tái cấu trúc luồng Sequence bắt buộc đi qua Backend Gateway: `Frontend` -> `FastAPI Router` -> `PIIAnonymizer.anonymize()` -> `AdminAIService` -> `LLM Provider` -> `Ghi log ai_invocation_logs` -> Trả về giao diện kèm `Medical Disclaimer`.
