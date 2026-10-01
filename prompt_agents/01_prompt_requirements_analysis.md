# PROMPT GIAO VIỆC: PHÂN TÍCH YÊU CẦU NGHIỆP VỤ & THIẾT LẬP RANH GIỚI ĐẠO ĐỨC AI
## Giai đoạn SDLC: Giai đoạn 1 – Requirements Engineering (KT1)
### Kỹ năng áp dụng: `.agents/skills/requirements-analysis/SKILL.md`

---

## 1. THÔNG TIN NGỮ CẢNH & MỤC TIÊU
* **Dự án:** Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp Trợ lý AI Hành chính (CMS-AI).
* **Đơn vị thực hiện:** Nhóm 07 (Đinh Gia Bảo - Trưởng nhóm, Trần Đặng Công Tâm).
* **Mục tiêu:** Khảo sát nghiệp vụ phòng khám tư nhân, phân tách chính xác 4 vai trò người dùng (Admin, Receptionist, Doctor, Accountant), đặc tả chi tiết các yêu cầu chức năng (FR) và phi chức năng (NFR), xây dựng User Stories chuẩn INVEST và Acceptance Criteria định dạng Gherkin, đồng thời thiết lập ranh giới đạo đức AI kiên quyết không can thiệp vào chuyên môn y tế của bác sĩ.

---

## 2. VAI TRÒ CỦA AI AGENT (PERSONA)
Bạn là **Lead Healthcare Business Analyst Agent (Chuyên viên Phân tích Nghiệp vụ Y tế Cấp cao)**, am hiểu sâu sắc quy trình vận hành phòng khám đa khoa tại Việt Nam, nắm vững Luật Khám bệnh, chữa bệnh 2023 và Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân.

---

## 3. RÀNG BUỘC KỸ THUẬT & QUY TẮC CỐT LÕI (GUARDRAILS)
1. **Tuyệt đối tuân thủ nguyên tắc "No Medical Diagnosis":** AI chỉ đóng vai trò Trợ lý Hành chính (Administrative Assistant) với 3 tính năng: (1) Tóm tắt tiền sử bệnh án cho bác sĩ xem nhanh; (2) Chatbot hỏi đáp thủ tục phòng khám; (3) Sinh mẫu dặn dò sau khám theo mẫu được duyệt. Tuyệt đối không cho phép AI tự chẩn đoán bệnh học hoặc kê đơn thuốc.
2. **Quyền riêng tư dữ liệu người bệnh (PII Protection):** Mọi luồng thông tin bệnh nhân phải được ẩn danh trước khi chuyển tới mô hình ngôn ngữ lớn (LLM).
3. **Phân quyền tối thiểu (Least Privilege):** 4 vai trò phải có phạm vi chức năng độc lập, không cho phép Lễ tân xem chi tiết bệnh án chuyên sâu, Kế toán chỉ được thao tác viện phí.
4. **Tính kiểm thử được (Testability):** Toàn bộ User Stories phải có Acceptance Criteria dạng Given-When-Then để làm căn cứ viết automated test.

---

## 4. NỘI DUNG MASTER PROMPT ĐÃ GIAO CHO AI AGENT

```markdown
Bạn hãy đóng vai trò là Senior Healthcare Business Analyst và AI Ethicist. Hãy thực hiện toàn diện quy trình Phân tích Yêu cầu Nghiệp vụ cho dự án "Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp AI Hành chính (CMS-AI)" của Nhóm 07:

BƯỚC 1: XÂY DỰNG SKILL ĐẶC TẢ (.agents/skills/requirements-analysis/SKILL.md)
Tạo file SKILL.md chuẩn hóa theo cấu trúc: YAML Frontmatter (name, description, objective, inputs, process, rules, outputs, verification), Mô hình Khái niệm 4 trụ cột (Codex, Skill, Tool, MCP), Ma trận 4 vai trò người dùng, Ranh giới đạo đức y tế và quy trình kích hoạt Human Gate 1.

BƯỚC 2: KHẢO SÁT BÀI TOÁN & YÊU CẦU KHÁCH HÀNG (docs/customer-requirement.md)
Phân tích hiện trạng 5 điểm nghẽn của phòng khám truyền thống: (1) Ùn tắc tiếp đón vào giờ cao điểm; (2) Nguy cơ xung đột trùng lịch khám bác sĩ; (3) Bác sĩ mất thời gian đọc bệnh án giấy dày cộm; (4) Quá tải bộ phận trực tổng đài hỏi đáp thủ tục BHYT; (5) Sai sót trong tính toán giảm trừ viện phí BHYT. Đề xuất giải pháp số hóa toàn diện tích hợp 3 tính năng AI Hành chính.

BƯỚC 3: ĐẶC TẢ CHI TIẾT YÊU CẦU CHỨC NĂNG & PHI CHỨC NĂNG (docs/requirements.md)
- Phân tách tối thiểu 38 Yêu cầu Chức năng (FR-001 đến FR-038) trải rộng trên 7 phân hệ:
  + Phân hệ 1: Quản trị Hệ thống & Phân quyền RBAC (Admin)
  + Phân hệ 2: Tiếp đón & Quản lý Hồ sơ Bệnh nhân (Lễ tân)
  + Phân hệ 3: Quản lý Lịch hẹn & Thuật toán Xung đột Khám bệnh
  + Phân hệ 4: Khám bệnh Lâm sàng & Kê đơn Dược phẩm (Bác sĩ)
  + Phân hệ 5: Viện phí, BHYT & Thanh toán VietQR (Thu ngân / Kế toán)
  + Phân hệ 6: Trợ lý AI Hành chính 3 Lớp (Pre-visit Briefing, FAQ Chatbot, Discharge Instructions)
  + Phân hệ 7: Báo cáo Thống kê & Nhật ký Kiểm toán (Audit Logs & AI Invocation Logs)
- Xác lập 10 Yêu cầu Phi Chức năng (NFR-001 đến NFR-010): Thời gian phản hồi API < 200ms, AI Latency < 3s, Bảo mật dữ liệu y tế theo Nghị định 13/2023/NĐ-CP, Hoạt động ngoại tuyến 100% nhờ Deterministic Mock AI Engine.

BƯỚC 4: XÂY DỰNG DANH SÁCH USER STORIES (docs/user-stories.md)
Viết toàn bộ User Stories theo cú pháp: "Là một [Vai trò], tôi muốn [Hành động] để [Lợi ích mang lại]". Phân loại theo 4 vai trò chính (Admin, Receptionist, Doctor, Accountant) và tác nhân bên ngoài (Patient).

BƯỚC 5: ĐẶC TẢ BỘ TIÊU CHÍ NGHIỆM THU ACCEPTANCE CRITERIA (docs/acceptance-criteria.md)
Xây dựng bộ tiêu chí nghiệm thu định dạng Gherkin (Given - When - Then) cho từng User Story, bao gồm cả kịch bản thành công (Happy Path), kịch bản ranh giới ngoại lệ (Edge Cases) và kịch bản tấn công/xâm phạm dữ liệu (Adversarial/Security Scenarios).

BƯỚC 6: NHẬN DIỆN VẤN ĐỀ VÀ BIÊN BẢN CỔNG KIỂM SOÁT CON NGƯỜI (docs/requirements-issues.md)
Tổng hợp các xung đột yêu cầu tiềm ẩn, các điểm AI có nguy cơ ảo giác (Hallucination) và tạo biên bản nghiệm thu Human Gate 1 có chữ ký phê duyệt của Trưởng nhóm Đinh Gia Bảo.
```

---

## 5. SẢN PHẨM ARTIFACTS KẾT XUẤT
1. [`.agents/skills/requirements-analysis/SKILL.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/.agents/skills/requirements-analysis/SKILL.md)
2. [`docs/customer-requirement.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/docs/customer-requirement.md)
3. [`docs/requirements.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/docs/requirements.md)
4. [`docs/user-stories.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/docs/user-stories.md)
5. [`docs/acceptance-criteria.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/docs/acceptance-criteria.md)
6. [`docs/requirements-issues.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/docs/requirements-issues.md)

---

## 6. KIỂM CHỨNG & HIỆU CHỈNH CỦA CON NGƯỜI (HUMAN GATE 1)
* **Lỗi do AI đề xuất (AI Hallucination):** AI ban đầu đề xuất tính năng *"AI tự động chẩn đoán bệnh lý cho bệnh nhân dựa trên mô tả triệu chứng và tự sinh đơn thuốc"*.
* **Hành động hiệu chỉnh của Kỹ sư Con người:** Kỹ sư Trưởng Đinh Gia Bảo đã kích hoạt **Human Gate 1**, kiên quyết loại bỏ hoàn toàn tính năng này vì vi phạm pháp luật y tế và đạo đức y khoa. Quy định lại phạm vi: AI tuyệt đối không chẩn đoán bệnh, chỉ hỗ trợ hành chính; toàn bộ kết quả AI phải đi kèm tuyên bố miễn trừ y tế (`Medical Disclaimer`) và quyền ký duyệt 100% thuộc về bác sĩ.
