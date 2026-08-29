---
name: requirements-analysis
description: Quy trình chuẩn hóa phân tích yêu cầu nghiệp vụ y tế, phân rã vai trò RBAC, xác định ranh giới đạo đức AI và xây dựng User Stories/Acceptance Criteria cho Hệ thống Quản lý Phòng khám Đa khoa thông minh (CMS-AI).
objective: Cung cấp phương pháp luận và quy chuẩn kỹ thuật cho AI Agent và Kỹ sư Phần mềm thực hiện phân tích yêu cầu phần mềm y tế, đảm bảo không hallucination, tuân thủ nghiêm ngặt nguyên tắc phân quyền và bảo vệ dữ liệu người bệnh.
inputs:
  - Tài liệu khảo sát nghiệp vụ phòng khám đa khoa (Khách hàng, Stakeholders)
  - Quy định pháp lý y tế (Luật Khám bệnh, chữa bệnh, Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân)
  - Danh mục vai trò và trách nhiệm các bộ phận (Admin, Lễ tân, Bác sĩ, Kế toán)
  - Mục tiêu tích hợp Trợ lý AI Hành chính và phạm vi ứng dụng AI
process:
  - 1. Khảo sát hiện trạng và xác định mục tiêu chuyển đổi số phòng khám
  - 2. Mô hình hóa 4 nhóm vai trò (Actors) và thiết lập phạm vi trách nhiệm
  - 3. Phân tách Yêu cầu Chức năng (Functional Requirements - FR)
  - 4. Xác lập Yêu cầu Phi Chức năng (Non-Functional Requirements - NFR)
  - 5. Thiết lập Ranh giới Đạo đức AI & Giới hạn Pháp lý Y tế (AI Ethical Boundaries)
  - 6. Chuyển hóa yêu cầu thành User Stories chuẩn INVEST và Acceptance Criteria (Gherkin format)
  - 7. Nhận diện rủi ro, xung đột yêu cầu và kích hoạt Human Gate 1
rules:
  - Tuyệt đối không cho phép AI tự động chẩn đoán bệnh lý hoặc tự ý kê đơn thuốc
  - Đảm bảo nguyên tắc đặc quyền tối thiểu (Least Privilege) cho cả 4 vai trò
  - Tất cả dữ liệu đầu vào y tế phải có quy định che giấu thông tin định danh (PII)
  - Mọi yêu cầu nghiệp vụ phải có tiêu chí nghiệm thu kiểm thử được (Testable)
outputs:
  - docs/customer-requirement.md (Yêu cầu khách hàng và bài toán nghiệp vụ)
  - docs/requirements.md (Đặc tả chi tiết FR-001..FR-038 và NFR-001..NFR-010)
  - docs/user-stories.md (Danh sách User Stories phân theo 4 vai trò)
  - docs/acceptance-criteria.md (Bộ tiêu chí nghiệm thu định dạng Given-When-Then)
  - docs/requirements-issues.md (Danh mục vấn đề cần làm rõ và biên bản Human Gate 1)
verification:
  - Kiểm tra tính đầy đủ của 4 vai trò và toàn bộ luồng khám chữa bệnh khép kín
  - Xác nhận 100% User Stories có Acceptance Criteria định dạng Gherkin
  - Thẩm định ranh giới AI: Không có bất kỳ tính năng chẩn đoán tự động nào
  - Phê duyệt chính thức của Product Owner / Chuyên gia y tế tại Human Gate 1
---

# Kỹ năng Phân tích Yêu cầu Nghiệp vụ Y tế & AI Hành chính (Requirements Analysis Skill)

## 1. Objective (Mục tiêu Kỹ năng)

Kỹ năng này quy định quy chuẩn chuyên môn và quy trình từng bước giúp Kỹ sư Phần mềm và AI Codex thực hiện phân tích, bóc tách và chuẩn hóa toàn bộ yêu cầu nghiệp vụ cho **Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp Trợ lý AI Hành chính (CMS-AI)**. 

Mục tiêu cốt lõi:
1. Chuyển hóa các nhu cầu vận hành thực tế của phòng khám thành tài liệu đặc tả kỹ thuật chính xác, phi mơ hồ.
2. Thiết lập ranh giới phân quyền rõ ràng giữa 4 nhóm vai trò: Quản trị viên (Admin), Lễ tân (Receptionist), Bác sĩ (Doctor), Kế toán/Thu ngân (Accountant).
3. Thiết lập ranh giới an toàn và đạo đức AI (AI Ethical Boundaries), ngăn chặn triệt để hiện tượng AI Hallucination hoặc AI can thiệp vào chuyên môn chẩn đoán của bác sĩ.
4. Đảm bảo tính kiểm thử được (Testability) 100% thông qua các kịch bản kiểm thử hành vi Given-When-Then.

---

## 2. Terminology & Conceptual Model (Mô hình Khái niệm)

Để phối hợp hiệu quả trong môi trường AI-Augmented SDLC, 4 khái niệm nền tảng được định nghĩa rạch ròi như sau:

```
+-----------------------------------------------------------------------------------------------+
|                                      MÔ HÌNH KHÁI NIỆM SDLC                                   |
+-----------------------------------------------------------------------------------------------+
|  1. CODEX (AI Agent)         : Thực thể trí tuệ nhân tạo thực thi các tác vụ tư duy,          |
|                                tổng hợp thông tin, suy luận logic và đề xuất giải pháp.        |
|  2. SKILL (Procedural Standard): Bộ quy chuẩn thủ tục, tri thức chuyên môn định hình phương   |
|                                pháp luận và các bước thực thi chuẩn cho Codex (Tài liệu này). |
|  3. TOOL (Environment Action): Các công cụ thao tác môi trường thực tế (Đọc/Ghi file,        |
|                                chạy lệnh kiểm thử, grep tìm kiếm, phân tích cú pháp).        |
|  4. MCP (Model Context Protocol): Giao thức kết nối chuẩn hóa giữa Codex và các nguồn dữ liệu|
|                                bên ngoài hoặc hệ sinh thái công cụ của phòng khám.            |
+-----------------------------------------------------------------------------------------------+
```

- **Codex (AI Agent)**: Đóng vai trò Chuyên viên Phân tích Nghiệp vụ (Business Analyst Agent). Codex tiếp nhận mô tả bài toán, áp dụng tri thức từ Skill để trích xuất các yêu cầu mà không được tự ý bịa đặt (No Requirement Invention).
- **Skill (Procedural Standard)**: Bản đặc tả thủ tục này, xác định rõ từng bước phân tích, cấu trúc tài liệu đầu ra, ma trận phân quyền và các điều kiện nghiệm thu.
- **Tool**: Các thao tác thực tế trên workspace (ví dụ: `write_to_file` để sinh tài liệu đặc tả, `view_file` để đối chiếu yêu cầu gốc).
- **MCP (Protocol)**: Giao thức truyền tải ngữ cảnh bệnh án, danh mục thuốc, lịch khám vào phiên làm việc của Codex một cách bảo mật.

---

## 3. Inputs & Prerequisites (Đầu vào & Điều kiện Tiên quyết)

### 3.1. Các tài liệu đầu vào bắt buộc
1. **Yêu cầu Khách hàng gốc (`ORIGINAL_REQUEST.md`)**: Mô tả bài toán phòng khám, các điểm nghẽn thực tế và định hướng áp dụng AI.
2. **Quy định Pháp lý & Chuẩn Y tế**:
   - Luật Khám bệnh, chữa bệnh số 15/2023/QH15.
   - Nghị định số 13/2023/NĐ-CP về Bảo vệ dữ liệu cá nhân (PII).
   - Bộ mã danh mục dùng chung của Bộ Y tế (ICD-10, Danh mục thuốc tân dược).
3. **Danh mục các Stakeholders tham gia phỏng vấn**:
   - Ban Giám đốc chuyên môn (Đại diện Bác sĩ).
   - Trưởng bộ phận Tiếp đón & Chăm sóc khách hàng (Đại diện Lễ tân).
   - Kế toán trưởng & Thu ngân (Đại diện Tài chính).
   - Quản trị viên Hệ thống CNTT (Đại diện Kỹ thuật).

### 3.2. Điều kiện tiên quyết
- Môi trường làm việc đã thiết lập đầy đủ workspace `.agents/` và thư mục tài liệu `docs/`.
- Đã xác định rõ phạm vi công nghệ: FastAPI Backend, React SPA Frontend, PostgreSQL/SQLite, 3-Layer AI Engine.

---

## 4. Execution Process (Quy trình Thực thi Từng bước)

Quy trình phân tích yêu cầu gồm 7 bước tuần tự và chặt chẽ:

```
[Bước 1: Khảo sát Hiện trạng] ---> [Bước 2: Phân tích 4 Actors] ---> [Bước 3: Bóc tách Yêu cầu FR]
                                                                                |
[Bước 6: User Stories & AC]  <--- [Bước 5: Ranh giới Đạo đức AI] <--- [Bước 4: Xác lập NFR]
           |
           v
[Bước 7: Kích hoạt Human Gate 1 (Business Scope Verification)]
```

### Bước 1: Khảo sát Hiện trạng & Nhận diện Điểm nghẽn Vận hành
1. Thu thập dữ liệu vận hành từ các phòng khám mẫu: Thống kê thời gian chờ khám, tỷ lệ trùng lịch hẹn, sai sót trong kê đơn thuốc và thất thoát viện phí.
2. Xác định mục tiêu số hóa:
   - Giảm 80% thời gian tạo và điều phối lịch hẹn.
   - Triệt tiêu 100% tình trạng đặt trùng lịch bác sĩ và phòng khám.
   - Giảm 60% thời gian bác sĩ tra cứu bệnh sử cũ thông qua tính năng AI Tóm tắt bệnh án.
   - Minh bạch hóa 100% hóa đơn viện phí và tích hợp thanh toán VietQR.

### Bước 2: Mô hình hóa 4 Nhóm Vai trò (Actor Modeling & RBAC Mapping)
Phân định rạch ròi quyền hạn và trách nhiệm của từng nhóm người dùng:

| Actor | Phạm vi Nghiệp vụ cốt lõi | Quyền Hạn Dữ liệu |
|---|---|---|
| **Quản trị viên (Admin)** | Quản trị tài khoản, phân quyền, cấu hình phòng khám, bác sĩ, chuyên khoa, ca làm việc, kho thuốc, xem Audit Log và thống kê doanh thu toàn viện. | Toàn quyền trên cấu hình và giám sát; Không trực tiếp khám bệnh hoặc kê đơn. |
| **Lễ tân (Receptionist)** | Tiếp đón bệnh nhân, tạo hồ sơ mới, tra cứu mã định danh y tế, đặt/đổi/hủy lịch hẹn, phát số vào hàng đợi khám, sử dụng AI FAQ Chatbot tư vấn thủ tục. | Đọc/Ghi thông tin hành chính bệnh nhân và lịch hẹn; Không xem chi tiết chẩn đoán bệnh án hay đơn thuốc. |
| **Bác sĩ (Doctor)** | Tiếp nhận hàng đợi bệnh nhân tại phòng khám, xem AI Pre-visit Summary, ghi nhận sinh hiệu, chẩn đoán ICD-10, chỉ định dịch vụ, kê đơn thuốc điện tử, sinh hướng dẫn sau khám bằng AI. | Toàn quyền trên phiếu khám và đơn thuốc do mình phụ trách; Không chỉnh sửa cấu hình hệ thống hay thu viện phí. |
| **Kế toán (Accountant)** | Tiếp nhận phiếu khám hoàn tất, tổng hợp viện phí (tiền khám + cận lâm sàng + thuốc), áp dụng tỷ lệ chi trả BHYT, thu tiền (Tiền mặt/VietQR), in phiếu thu. | Đọc/Ghi dữ liệu hóa đơn và thanh toán; Không chỉnh sửa thông tin chẩn đoán hoặc đơn thuốc của bác sĩ. |

### Bước 3: Phân rã Danh mục Yêu cầu Chức năng (Functional Requirements - FR)
Phân rã thành 38 yêu cầu chức năng (FR-001 đến FR-038) chia theo 6 phân hệ lớn:
1. **Phân hệ 1: Xác thực, Phân quyền & Quản trị Hệ thống (FR-001 -> FR-007)**:
   - Đăng nhập JWT, quản lý người dùng, quản lý chuyên khoa, phòng khám, hồ sơ bác sĩ, ca làm việc, nạp dữ liệu mẫu.
2. **Phân hệ 2: Quản lý Hồ sơ Bệnh nhân & Đặt lịch Hẹn (FR-008 -> FR-012)**:
   - Đăng ký mã định danh bệnh nhân tự động (`BN-YYYYMMDD-XXXX`), quản lý dị ứng/tiền sử, đặt lịch hẹn trực quan, thuật toán phát hiện xung đột lịch khám thời gian thực, quản lý vòng đời lịch hẹn.
3. **Phân hệ 3: Tiếp đón & Điều phối Hàng đợi (FR-013 -> FR-015)**:
   - Tiếp đón bệnh nhân tại quầy, phát số thứ tự hàng đợi, điều phối bệnh nhân vào phòng khám của bác sĩ.
4. **Phân hệ 4: Khám bệnh, Cận lâm sàng & Kê đơn Thuốc (FR-016 -> FR-023)**:
   - Hàng đợi bác sĩ theo thời gian thực, ghi nhận sinh hiệu (Huyết áp, Mạch, SpO2, Thân nhiệt, BMI), chẩn đoán mã ICD-10, chỉ định dịch vụ xét nghiệm/chẩn đoán hình ảnh, kê đơn thuốc điện tử, trừ tồn kho dược tự động.
5. **Phân hệ 5: Trợ lý AI Hành chính & Bảo mật Dữ liệu (FR-024 -> FR-031)**:
   - Tự động khử định danh dữ liệu PII (CCCD, SĐT, BHYT, Tên, Địa chỉ), AI Tóm tắt bệnh án (Pre-visit Briefing), AI Chatbot quy trình (Clinic Workflow FAQ), AI Sinh dặn dò sau khám (Discharge Instructions), Tuyên bố miễn trừ trách nhiệm y tế bắt buộc, Hàng rào từ chối chẩn đoán, Mock Offline AI Engine, Audit Logging & AI Invocation Logging.
6. **Phân hệ 6: Viện phí, Thanh toán & Báo cáo Thống kê (FR-032 -> FR-038)**:
   - Tổng hợp hóa đơn viện phí tự động, tính khấu trừ BHYT (80%, 100%), thanh toán Tiền mặt & VietQR tự động, in phiếu thu chuẩn khổ A4/A5, Dashboard thống kê doanh thu và lượt khám theo chuyên khoa/bác sĩ.

### Bước 4: Xác lập Danh mục Yêu cầu Phi Chức năng (Non-Functional Requirements - NFR)
- **NFR-001 (Bảo mật - Security)**: 100% mật khẩu mã hóa bằng Bcrypt; Phiên làm việc xác thực bằng JWT mã hóa HS256 có thời hạn hết hạn; Tuân thủ kiểm soát truy cập RBAC ở mọi API endpoint.
- **NFR-002 (Bảo vệ Dữ liệu Y tế - Privacy)**: Không gửi bất kỳ thông tin PII nào của bệnh nhân ra ngoài hệ thống hoặc truyền vào mô hình AI mà chưa qua khử định danh.
- **NFR-003 (Độ khả dụng & Ngoại tuyến - Availability & Offline Resiliency)**: Hệ thống phải hoạt động 100% tính năng AI ở chế độ Offline Mock Engine khi mất kết nối internet hoặc không có API key.
- **NFR-004 (Hiệu năng - Performance)**: Thời gian phản hồi API CRUD < 200ms; Thời gian kiểm tra xung đột lịch hẹn < 50ms; Tải trang Frontend < 1.5s.
- **NFR-005 (Tính Toàn vẹn Dữ liệu - Data Integrity)**: Cơ sở dữ liệu đạt chuẩn 3NF, bảo đảm ràng buộc khóa ngoại (Foreign Keys) và ACID transactions khi kê đơn/thanh toán.
- **NFR-006 (Giao diện Công thái học - Clinical UI/UX Taste)**: Giao diện tuân thủ chuẩn Taste-Skill: Tương phản cao, số liệu dạng tabular figures, không sử dụng AI-slop animations gây xao nhãng.

### Bước 5: Thiết lập Ranh giới Đạo đức AI & Giới hạn Pháp lý Y tế (AI Ethical Boundaries)
Xác định rõ những điều AI **ĐƯỢC PHÉP** và **TUYỆT ĐỐI KHÔNG ĐƯỢC PHÉP** thực hiện:

```
+-----------------------------------------------------------------------------------------------+
|                                    AI ETHICAL BOUNDARY MATRIX                                 |
+-----------------------------------------------------------------------------------------------+
|  ✅ ĐƯỢC PHÉP (ADMINISTRATIVE ONLY)           |  ❌ TUYỆT ĐỐI NGHIÊM CẤM (NON-DIAGNOSTIC)       |
|-----------------------------------------------+-----------------------------------------------|
|  1. Tóm tắt lịch sử khám và tiền sử dị ứng     |  1. Tự động đưa ra kết luận chẩn đoán bệnh     |
|  2. Trả lời câu hỏi về thủ tục, BHYT, bảng giá|  2. Tự động kê đơn thuốc hoặc chỉ định liều   |
|  3. Soạn thảo lời dặn dò sau khám theo mẫu   |  3. Đưa ra lời khuyên thay thế chỉ định bác sĩ|
|  4. Tự động đính kèm cảnh báo miễn trừ y tế   |  4. Xử lý dữ liệu PII chưa qua ẩn danh        |
+-----------------------------------------------------------------------------------------------+
```

### Bước 6: Xây dựng User Stories & Acceptance Criteria (Gherkin Format)
Mỗi User Story phải tuân thủ cấu trúc INVEST và đi kèm Acceptance Criteria cụ thể:

*Ví dụ User Story US-008 (Đặt lịch khám không trùng lặp):*
- **Là**: Lễ tân phòng khám,
- **Tôi muốn**: Hệ thống tự động kiểm tra và ngăn chặn việc đặt lịch nếu bác sĩ hoặc phòng khám đã có người đặt trong cùng khung giờ,
- **Để**: Tránh việc chồng chéo lịch khám và không để bệnh nhân phải chờ đợi.

*Acceptance Criteria (Gherkin):*
```gherkin
Scenario: Đặt lịch hẹn thành công khi khung giờ còn trống
  Given Bác sĩ "Nguyễn Văn A" có ca làm việc lúc 08:00 - 12:00 tại Phòng 101
  And Chưa có bệnh nhân nào đặt lịch vào khung giờ 09:00 - 09:30
  When Lễ tân tạo lịch hẹn cho bệnh nhân "Trần Thị B" vào lúc 09:00
  Then Hệ thống chấp nhận lịch hẹn với trạng thái "CONFIRMED"
  And Trả về mã lịch hẹn mới.

Scenario: Chặn đặt lịch khi bác sĩ đã có lịch hẹn trùng lặp
  Given Bác sĩ "Nguyễn Văn A" đã có lịch hẹn đã xác nhận lúc 09:00 - 09:30
  When Lễ tân cố gắng tạo một lịch hẹn khác cho bác sĩ "Nguyễn Văn A" lúc 09:15
  Then Hệ thống từ chối yêu cầu với mã lỗi 400 Bad Request
  And Trả về thông báo lỗi: "Bác sĩ Nguyễn Văn A đã có lịch khám trong khoảng thời gian này."
```

### Bước 7: Kích hoạt Human Gate 1 (Business & Scope Verification)
- Tổng hợp toàn bộ hồ sơ yêu cầu thành 5 tài liệu chuẩn.
- Tổ chức phiên phản biện và thẩm định với Product Owner / Chuyên gia y tế.
- Ký biên bản nghiệm thu phạm vi yêu cầu (Scope Sign-off) trước khi chuyển sang giai đoạn Thiết kế Kiến trúc.

---

## 5. Human-in-the-loop Governance (Cơ chế Kiểm soát Con người)

### 5.1. Định nghĩa Điểm kiểm soát Human Gate 1
Human Gate 1 là rào chắn kiểm soát nghiêm ngặt nhất trong giai đoạn Phân tích Yêu cầu nhằm triệt tiêu hiện tượng **AI Requirement Invention** (AI tự bịa ra yêu cầu không có trong thực tế).

### 5.2. Danh mục Kiểm tra Thẩm định Human Gate 1 (Checklist)
- [ ] 1. Toàn bộ 4 nhóm vai trò có phạm vi quyền hạn phù hợp với quy trình khám chữa bệnh thực tế.
- [ ] 2. Không có bất kỳ yêu cầu nào cho phép AI đưa ra chẩn đoán y khoa hoặc thay đổi đơn thuốc của bác sĩ.
- [ ] 3. 100% luồng xử lý AI đều có bước khử định danh dữ liệu PII trước khi gọi mô hình.
- [ ] 4. Đầy đủ các kịch bản kiểm tra xung đột trùng lịch của bác sĩ và phòng khám.
- [ ] 5. Mọi User Story đều có tiêu chí nghiệm thu định dạng Given-When-Then rõ ràng, có thể tự động hóa thành test case.

---

## 6. Business & Compliance Rules (Quy tắc Nghiệp vụ & Tuân thủ)

1. **Quy tắc Phân quyền (RBAC)**:
   - Tài khoản Lễ tân không bao giờ được cấp quyền truy cập vào bảng `prescriptions` hoặc `medical_records` để xem chi tiết bệnh học.
   - Tài khoản Bác sĩ không có quyền thao tác trực tiếp trên bảng `invoices` để sửa đổi số tiền thanh toán.
2. **Quy tắc Bảo mật Dữ liệu Y tế (Medical Privacy)**:
   - Dữ liệu PII của bệnh nhân (CCCD, SĐT, BHYT, Địa chỉ) phải được lưu trữ trong cơ sở dữ liệu có kiểm soát truy cập và ghi nhật ký kiểm toán (Audit Log) mỗi khi được đọc/sửa.
3. **Quy tắc Tuyên bố Miễn trừ Trách nhiệm (Medical Disclaimer)**:
   - 100% kết quả đầu ra của Trợ lý AI (Pre-visit Briefing, FAQ Chatbot, Discharge Instructions) phải tự động đính kèm câu khuyến cáo: `TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y TẾ: Nội dung do AI tổng hợp mang tính chất hỗ trợ hành chính. AI không thay thế chẩn đoán chuyên môn của bác sĩ.`

---

## 7. Expected Outputs & Deliverables (Tài liệu Đầu ra Bắt buộc)

Quá trình thực thi kỹ năng này bắt buộc phải tạo ra/cập nhật 5 tài liệu sau trong thư mục `docs/`:

1. `docs/customer-requirement.md`: Tài liệu tóm lược bài toán thực tế, bối cảnh phòng khám và các mục tiêu chuyển đổi số.
2. `docs/requirements.md`: Bảng đặc tả chi tiết 38 Yêu cầu Chức năng (FR-001 -> FR-038) và 6 Yêu cầu Phi Chức năng (NFR-001 -> NFR-006).
3. `docs/user-stories.md`: Tập hợp các User Stories chuẩn INVEST phân theo 4 vai trò.
4. `docs/acceptance-criteria.md`: Bảng tiêu chí nghiệm thu định dạng Gherkin cho toàn bộ các chức năng.
5. `docs/requirements-issues.md`: Báo cáo nhận diện các điểm mơ hồ, mâu thuẫn yêu cầu và biên bản phê duyệt Human Gate 1.

---

## 8. Verification & Quality Acceptance Criteria (Tiêu chí Đánh giá Chất lượng)

Kỹ năng Phân tích Yêu cầu được coi là hoàn thành xuất sắc khi đáp ứng đầy đủ các tiêu chuẩn sau:

- **Tính Đầy đủ (Completeness)**: Bao phủ 100% chu trình khám chữa bệnh từ Đặt lịch -> Tiếp đón -> Khám lâm sàng -> Kê đơn -> Viện phí -> Hướng dẫn sau khám.
- **Tính Nhất quán (Consistency)**: Không có mâu thuẫn quyền hạn giữa ma trận RBAC và các Use Case.
- **Tính Kiểm thử được (Testability)**: 100% Acceptance Criteria có thể chuyển đổi trực tiếp thành các test cases tự động trong Pytest.
- **Tuân thủ Đạo đức AI (AI Ethics Compliance)**: Không có bất kỳ kẽ hở nào cho phép AI đưa ra quyết định lâm sàng độc lập.
- **Phê duyệt Human Gate 1**: Có chữ ký hoặc xác nhận chính thức từ Product Owner / Chuyên gia nghiệp vụ y tế.
