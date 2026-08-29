# DANH MỤC CÂU CHUYỆN NGƯỜI DÙNG (USER STORIES SPECIFICATION)
## DỰ ÁN: HỆ THỐNG QUẢN LÝ PHÒNG KHÁM ĐA KHOA THÔNG MINH TÍCH HỢP TRỢ LÝ AI HÀNH CHÍNH
### (Clinic Management System with Administrative AI Assistant - CMS-AI)

---

## 1. PHƯƠNG PHÁP LUẬN & ĐỊNH DẠNG CHUẨN

Mỗi User Story được xây dựng theo chuẩn mực Agile:
> **"As a [Role], I want [Feature/Action], So that [Business Value/Benefit]."**

- **Quy tắc phân loại ưu tiên (MoSCoW):**
  - **MUST (M):** Yêu cầu bắt buộc phải có để hệ thống vận hành nghiệp vụ.
  - **SHOULD (S):** Tính năng quan trọng, tạo giá trị cao nhưng có thể dùng giải pháp tạm thời.
  - **COULD (C):** Tính năng nâng cao trải nghiệm, có thể triển khai ở giai đoạn kế tiếp.
  - **WON'T (W):** Tính năng chưa triển khai trong phiên bản hiện tại.
- **Ước lượng độ phức tạp (Story Points theo dãy Fibonacci):** 1, 2, 3, 5, 8, 13 điểm.

---

## 2. USER STORIES DÀNH CHO QUẢN TRỊ VIÊN (ADMIN - US-ADM)

```
+---------------------------------------------------------------------------------------------------+
|                           USER STORIES: QUẢN TRỊ VIÊN (ADMIN)                                    |
+---------------------------------------------------------------------------------------------------+
```

### US-ADM-001: Quản trị Tài khoản Người dùng & Phân vai trò
- **As an** Admin,
- **I want to** tạo mới, cập nhật thông tin và gán vai trò (`Admin`, `Receptionist`, `Doctor`, `Accountant`) cho nhân viên phòng khám,
- **So that** từng nhân viên có tài khoản riêng để làm việc và chỉ được truy cập đúng phạm vi quyền hạn của mình.
- **Priority:** MUST | **Points:** 5
- **Tiêu chí chấp nhận tóm tắt:**
  - Mật khẩu tạo mới được băm Bcrypt tự động.
  - Không thể tạo 2 tài khoản trùng `username`.
  - Có thể vô hiệu hóa tài khoản khi nhân viên nghỉ việc.

### US-ADM-002: Quản trị Danh mục Chuyên khoa & Phòng khám
- **As an** Admin,
- **I want to** cấu hình danh mục các chuyên khoa (Nội, Tim mạch, Nhi, Da liễu) và các phòng khám chức năng,
- **So that** hệ thống có dữ liệu chuẩn để phân bổ bác sĩ và xếp lịch hẹn khám.
- **Priority:** MUST | **Points:** 3
- **Tiêu chí chấp nhận tóm tắt:**
  - CRUD chuyên khoa và phòng khám hoạt động trơn tru.
  - Mỗi phòng khám được liên kết với một chuyên khoa và có mã phòng rõ ràng.

### US-ADM-003: Quản trị Danh sách Bác sĩ & Lập Lịch Ca trực
- **As an** Admin,
- **I want to** quản lý hồ sơ bác sĩ và thiết lập ca trực (Sáng/Chiều/Tối) theo từng ngày trong tuần,
- **So that** lễ tân biết chính xác bác sĩ nào đang trực tại phòng khám nào để tiếp đón và đặt lịch.
- **Priority:** MUST | **Points:** 5
- **Tiêu chí chấp nhận tóm tắt:**
  - Bác sĩ phải liên kết với một tài khoản người dùng có vai trò `doctor`.
  - Không thể xếp 1 bác sĩ trực 2 ca trùng giờ tại 2 phòng khám khác nhau.

### US-ADM-004: Quản trị Kho Dược & Danh mục Thuốc
- **As an** Admin,
- **I want to** quản lý danh mục biệt dược, hoạt chất, hàm lượng, giá bán và số lượng tồn kho,
- **So that** bác sĩ có dữ liệu để kê đơn thuốc điện tử và kế toán tính tiền chính xác.
- **Priority:** MUST | **Points:** 5
- **Tiêu chí chấp nhận tóm tắt:**
  - Cho phép tra cứu nhanh thuốc theo tên thương mại hoặc hoạt chất.
  - Cập nhật số lượng tồn kho khi nhập hàng mới.

### US-ADM-005: Giám sát Nhật ký Kiểm toán (Audit Logs)
- **As an** Admin,
- **I want to** xem toàn bộ lịch sử thao tác truy cập và sửa đổi hồ sơ bệnh nhân,
- **So that** phát hiện kịp thời các hành vi truy cập trái phép và bảo vệ an toàn dữ liệu y tế.
- **Priority:** MUST | **Points:** 3
- **Tiêu chí chấp nhận tóm tắt:**
  - Hiển thị đầy đủ: Thời gian, Người thực hiện, Hành động, Đối tượng, Địa chỉ IP.
  - Nhật ký có tính chất chỉ đọc (Read-only), không ai được phép sửa hoặc xóa.

### US-ADM-006: Giám sát Nhật ký Gọi Trợ lý AI (AI Logs)
- **As an** Admin,
- **I want to** kiểm tra toàn bộ các prompt gửi đến AI và câu trả lời phản hồi cùng thời gian trễ (latency),
- **So that** đánh giá chất lượng phản hồi của AI và xác minh rằng không có dữ liệu PII nào bị lọt ra ngoài.
- **Priority:** MUST | **Points:** 3
- **Tiêu chí chấp nhận tóm tắt:**
  - Xác nhận 100% prompt lưu trong log đều đã được thay thế dữ liệu định danh bằng token.
  - Hiển thị mô hình AI được sử dụng (Mock, Ollama, Cloud).

### US-ADM-007: Xem Dashboard Thống kê Vận hành & Doanh thu
- **As an** Admin,
- **I want to** theo dõi biểu đồ doanh thu theo thời gian, số lượt khám theo khoa và công suất của bác sĩ,
- **So that** nắm bắt tình hình hoạt động của phòng khám và đưa ra các quyết định điều hành chính xác.
- **Priority:** MUST | **Points:** 5
- **Tiêu chí chấp nhận tóm tắt:**
  - Biểu đồ trực quan, cập nhật theo thời gian thực.
  - Thống kê doanh thu tiền mặt, chuyển khoản VietQR và chi trả BHYT.

---

## 3. USER STORIES DÀNH CHO LỄ TÂN (RECEPTIONIST - US-REC)

```
+---------------------------------------------------------------------------------------------------+
|                           USER STORIES: LỄ TÂN (RECEPTIONIST)                                     |
+---------------------------------------------------------------------------------------------------+
```

### US-REC-001: Đăng ký Hồ sơ Bệnh nhân Mới
- **As a** Receptionist,
- **I want to** nhập thông tin cá nhân, CCCD, SĐT, Địa chỉ, BHYT và tiền sử bệnh của người bệnh lần đầu đến khám,
- **So that** tạo hồ sơ bệnh nhân trên hệ thống và cấp mã định danh y tế chuẩn.
- **Priority:** MUST | **Points:** 3
- **Tiêu chí chấp nhận tóm tắt:**
  - Hệ thống tự động sinh mã `BN-YYYYMMDD-XXXX`.
  - Bắt buộc kiểm tra định dạng SĐT (10 số) và CCCD (12 số).

### US-REC-002: Tra cứu Nhanh Hồ sơ Bệnh nhân Tái khám
- **As a** Receptionist,
- **I want to** tìm kiếm hồ sơ bệnh nhân cũ bằng Mã BN, Số điện thoại hoặc Số CCCD,
- **So that** tiếp đón nhanh chóng mà không cần nhập lại thông tin từ đầu.
- **Priority:** MUST | **Points:** 2
- **Tiêu chí chấp nhận tóm tắt:**
  - Tìm kiếm trả kết quả trong vòng dưới 200ms.
  - Hiển thị tiền sử dị ứng thuốc nổi bật để đối chiếu.

### US-REC-003: Đặt Lịch hẹn Khám & Kiểm tra Xung đột Trùng lịch
- **As a** Receptionist,
- **I want to** chọn Bác sĩ, Ngày khám, Khung giờ (ví dụ 09:00 - 09:30) để tạo lịch hẹn cho bệnh nhân,
- **So that** bệnh nhân có lịch khám xác định và không bị xếp trùng vào giờ bác sĩ đang bận.
- **Priority:** MUST | **Points:** 5
- **Tiêu chí chấp nhận tóm tắt:**
  - Hệ thống tự động kiểm tra xung đột; nếu trùng lịch, hiển thị thông báo lỗi rõ ràng và gợi ý khung giờ khác.
  - Cho phép đặt lịch thành công khi khung giờ hoàn toàn trống.

### US-REC-004: Đổi lịch & Hủy lịch hẹn
- **As a** Receptionist,
- **I want to** thay đổi khung giờ khám hoặc hủy lịch hẹn khi bệnh nhân yêu cầu,
- **So that** giải phóng khung giờ trống cho các bệnh nhân khác.
- **Priority:** MUST | **Points:** 3
- **Tiêu chí chấp nhận tóm tắt:**
  - Đổi lịch phải kích hoạt lại thuật toán kiểm tra xung đột tại thời điểm mới.
  - Hủy lịch hẹn yêu cầu ghi rõ lý do hủy.

### US-REC-005: Tiếp đón Bệnh nhân & Cấp Số Thứ tự Hàng đợi (Check-in)
- **As a** Receptionist,
- **I want to** xác nhận bệnh nhân đã có mặt tại phòng khám và xếp vào hàng đợi của Bác sĩ chuyên khoa,
- **So that** bác sĩ trong phòng khám nhìn thấy bệnh nhân đang chờ trong danh sách.
- **Priority:** MUST | **Points:** 3
- **Tiêu chí chấp nhận tóm tắt:**
  - Tự động sinh số thứ tự hàng ngày (`queue_number` bắt đầu từ 1).
  - Trạng thái lịch hẹn chuyển sang `CHECKED_IN`.

### US-REC-006: Sử dụng Chatbot AI Hướng dẫn Quy trình (FAQ Chatbot)
- **As a** Receptionist,
- **I want to** hỏi Chatbot AI về thủ tục hưởng bảo hiểm, bảng giá khám, giờ làm việc và quy trình chuyển tuyến,
- **So that** trả lời thắc mắc của người bệnh một cách chính xác, nhanh chóng và chuyên nghiệp.
- **Priority:** MUST | **Points:** 3
- **Tiêu chí chấp nhận tóm tắt:**
  - Chatbot trả lời đầy đủ thông tin hành chính của phòng khám.
  - Chatbot từ chối đưa ra lời khuyên y tế/chẩn đoán nếu người dùng hỏi về triệu chứng bệnh học.

---

## 4. USER STORIES DÀNH CHO BÁC SĨ (DOCTOR - US-DOC)

```
+---------------------------------------------------------------------------------------------------+
|                           USER STORIES: BÁC SĨ LÂM SÀNG (DOCTOR)                                  |
+---------------------------------------------------------------------------------------------------+
```

### US-DOC-001: Xem Danh sách Hàng đợi Bệnh nhân Chờ khám
- **As a** Doctor,
- **I want to** xem danh sách các bệnh nhân đã check-in đang chờ tại phòng khám của mình theo số thứ tự,
- **So that** tôi có thể chủ động mời bệnh nhân tiếp theo vào khám.
- **Priority:** MUST | **Points:** 3
- **Tiêu chí chấp nhận tóm tắt:**
  - Danh sách sắp xếp theo `queue_number` tăng dần.
  - Hiển thị rõ Họ tên, Mã BN, Tuổi, Giới tính và Lý do khám.

### US-DOC-002: Xem Bản tóm tắt Bệnh sử Tự động (AI Pre-visit Briefing)
- **As a** Doctor,
- **I want to** xem thẻ tóm tắt lịch sử khám, các đợt điều trị cũ và cảnh báo dị ứng thuốc do AI tổng hợp,
- **So that** tôi nắm bắt nhanh tình trạng của bệnh nhân trong 5 giây đầu tiên mà không cần lật giở hồ sơ cũ.
- **Priority:** MUST | **Points:** 5
- **Tiêu chí chấp nhận tóm tắt:**
  - Cảnh báo dị ứng thuốc hiển thị nổi bật bằng màu đỏ/cam.
  - Tóm tắt các chẩn đoán gần nhất và thuốc đã dùng.
  - Luôn có nhãn Miễn trừ trách nhiệm y tế của AI.

### US-DOC-003: Ghi nhận Khám Lâm sàng & Bộ Chỉ số Sinh hiệu
- **As a** Doctor,
- **I want to** nhập triệu chứng, huyết áp, nhịp tim, nhiệt độ, SpO2, cân nặng, chiều cao (tự tính BMI) và khám thực thể,
- **So that** lưu trữ đầy đủ hồ sơ bệnh án điện tử phục vụ theo dõi và chẩn đoán.
- **Priority:** MUST | **Points:** 5
- **Tiêu chí chấp nhận tóm tắt:**
  - BMI được tính tự động từ chiều cao và cân nặng.
  - Cảnh báo nếu huyết áp hoặc SpO2 nằm ngoài ngưỡng an toàn sinh lý.

### US-DOC-004: Chẩn đoán Bệnh theo Bảng mã Chuẩn ICD-10
- **As a** Doctor,
- **I want to** chọn hoặc nhập mã chẩn đoán ICD-10 (chính và phụ) cùng mô tả bệnh học,
- **So that** chẩn đoán được chuẩn hóa theo quy định của Bộ Y tế và làm căn cứ thanh toán BHYT.
- **Priority:** MUST | **Points:** 3
- **Tiêu chí chấp nhận tóm tắt:**
  - Tra cứu nhanh mã ICD-10 và tên bệnh tương ứng.
  - Lưu trữ mã ICD-10 vào phiếu khám bệnh.

### US-DOC-005: Chỉ định Dịch vụ Cận lâm sàng (Xét nghiệm / CĐHA)
- **As a** Doctor,
- **I want to** chỉ định các xét nghiệm (Công thức máu, Sinh hóa, Nước tiểu) hoặc Chẩn đoán hình ảnh (Siêu âm, X-quang),
- **So that** người bệnh thực hiện cận lâm sàng và hệ thống tự động cộng chi phí vào viện phí.
- **Priority:** MUST | **Points:** 3
- **Tiêu chí chấp nhận tóm tắt:**
  - Cho phép chọn nhiều dịch vụ cận lâm sàng cùng lúc.
  - Trạng thái chỉ định được liên kết trực tiếp với hồ sơ khám.

### US-DOC-006: Kê đơn Thuốc Điện tử (e-Prescription)
- **As a** Doctor,
- **I want to** chọn thuốc từ danh mục, chỉ định số lượng, liều dùng (sáng/trưa/chiều/tối) và cách uống,
- **So that** tạo toa thuốc điện tử chính xác, rõ ràng cho bệnh nhân và chuyển dữ liệu sang quầy thanh toán/kho dược.
- **Priority:** MUST | **Points:** 5
- **Tiêu chí chấp nhận tóm tắt:**
  - Tự động hiển thị số lượng tồn kho khả dụng; chặn kê vượt tồn kho.
  - Kiểm tra đối chiếu với danh sách dị ứng thuốc của bệnh nhân.

### US-DOC-007: Sinh Hướng dẫn Dặn dò Sau khám (AI Discharge Instructions)
- **As a** Doctor,
- **I want to** yêu cầu Trợ lý AI tự động tạo phiếu hướng dẫn chăm sóc tại nhà, lịch uống thuốc và hẹn ngày tái khám,
- **So that** bệnh nhân có văn bản dặn dò chi tiết, khoa học mà tôi không mất thời gian gõ văn bản thủ công.
- **Priority:** MUST | **Points:** 5
- **Tiêu chí chấp nhận tóm tắt:**
  - Bảng lịch uống thuốc rõ ràng theo bữa ăn.
  - Liệt kê các triệu chứng cảnh báo cần quay lại viện gấp.
  - Đính kèm Tuyên bố miễn trừ trách nhiệm y tế của AI.

---

## 5. USER STORIES DÀNH CHO KẾ TOÁN / THU NGÂN (ACCOUNTANT - US-ACC)

```
+---------------------------------------------------------------------------------------------------+
|                           USER STORIES: KẾ TOÁN / THU NGÂN (ACCOUNTANT)                           |
+---------------------------------------------------------------------------------------------------+
```

### US-ACC-001: Tiếp nhận Hóa đơn Viện phí Chờ thanh toán
- **As an** Accountant,
- **I want to** xem danh sách các ca khám vừa hoàn thành đang chờ thanh toán theo thời gian thực,
- **So that** tôi có thể mở hóa đơn và làm thủ tục thu tiền ngay khi bệnh nhân bước ra khỏi phòng khám.
- **Priority:** MUST | **Points:** 3
- **Tiêu chí chấp nhận tóm tắt:**
  - Hóa đơn hiển thị đầy đủ: Tiền khám + Tiền xét nghiệm + Tiền thuốc.
  - Phân loại rõ từng khoản mục chi phí.

### US-ACC-002: Áp dụng Khấu trừ Bảo hiểm Y tế (BHYT)
- **As an** Accountant,
- **I want to** hệ thống tự động kiểm tra thẻ BHYT và tính toán số tiền bảo hiểm chi trả (80% hoặc 100%),
- **So that** bệnh nhân chỉ phải thanh toán đúng số tiền cùng chi trả (Co-pay) theo quy định.
- **Priority:** MUST | **Points:** 5
- **Tiêu chí chấp nhận tóm tắt:**
  - Tính toán số tiền BHYT thanh toán và số tiền bệnh nhân phải trả chính xác 100%.
  - Hiển thị công khai chi tiết số tiền được miễn giảm trên hóa đơn.

### US-ACC-003: Thu tiền Viện phí & Sinh Mã Thanh toán VietQR Động
- **As an** Accountant,
- **I want to** tạo mã VietQR động chứa đúng số tiền thực thu, số tài khoản phòng khám và mã hóa đơn,
- **So that** bệnh nhân có thể quét mã chuyển khoản nhanh chóng qua ứng dụng ngân hàng mà không cần gõ tay.
- **Priority:** MUST | **Points:** 5
- **Tiêu chí chấp nhận tóm tắt:**
  - Mã VietQR sinh chuẩn định dạng NAPAS / VietQR.
  - Hỗ trợ cả hai phương thức: Tiền mặt (`CASH`) và Chuyển khoản (`TRANSFER`).

### US-ACC-004: In Biên lai / Hóa đơn Dịch vụ Y tế Chuẩn hóa
- **As an** Accountant,
- **I want to** in phiếu thu viện phí khổ A4 hoặc A5 giao cho người bệnh,
- **So that** người bệnh có chứng từ thanh toán hợp lệ và minh bạch.
- **Priority:** MUST | **Points:** 3
- **Tiêu chí chấp nhận tóm tắt:**
  - Bản in có logo phòng khám, mã BN, họ tên, chi tiết dịch vụ, tiền thuốc, chiết khấu BHYT và chữ ký thu ngân.
  - Trạng thái hóa đơn chuyển thành `PAID`.

---

## 6. USER STORIES DÀNH CHO HỆ THỐNG & AI ENGINE (SYSTEM & AI - US-SYS)

```
+---------------------------------------------------------------------------------------------------+
|                           USER STORIES: HỆ THỐNG & TRỢ LÝ AI (SYSTEM & AI)                        |
+---------------------------------------------------------------------------------------------------+
```

### US-SYS-001: Khử Định danh Dữ liệu Cá nhân (PII De-identification)
- **As a** Privacy Protection Engine,
- **I want to** tự động rà quét và che giấu toàn bộ Số điện thoại, CCCD, Mã BHYT và Họ tên bệnh nhân bằng các token đại diện,
- **So that** không một thông tin cá nhân nào bị gửi sang LLM hoặc lưu vết trên nhật ký AI.
- **Priority:** MUST | **Points:** 5

### US-SYS-002: Hàng rào Bảo vệ Đạo đức & Chặn Prompt Injection
- **As an** AI Guardrail System,
- **I want to** nhận diện các câu lệnh phá rào hoặc yêu cầu chẩn đoán bệnh học tự động,
- **So that** kiên quyết từ chối chẩn đoán, cảnh báo an toàn và hướng dẫn người dùng gặp bác sĩ trực tiếp.
- **Priority:** MUST | **Points:** 5

### US-SYS-003: Cơ chế Dự phòng Ngoại tuyến (Deterministic Fallback)
- **As a** System Resilience Engine,
- **I want to** tự động chuyển sang mô hình Deterministic Mock AI khi mất kết nối mạng hoặc lỗi dịch vụ LLM đám mây,
- **So that** toàn bộ các chức năng AI trong phòng khám vẫn phản hồi tức thì và không bị gián đoạn.
- **Priority:** MUST | **Points:** 5

---

## 7. BẢNG TỔNG HỢP STORY POINTS THEO PHÂN HỆ

```
+---------------------------------------------------------------------------------------------------+
| Phân hệ Nghiệp vụ        | Số lượng Stories | Tổng Story Points | Tỷ trọng Ưu tiên MUST           |
+--------------------------+------------------+-------------------+---------------------------------+
| Quản trị viên (Admin)    | 7 Stories        | 29 Points         | 100%                            |
| Lễ tân (Receptionist)    | 6 Stories        | 21 Points         | 100%                            |
| Bác sĩ (Doctor)          | 7 Stories        | 29 Points         | 100%                            |
| Kế toán (Accountant)     | 4 Stories        | 16 Points         | 100%                            |
| Hệ thống & AI Engine     | 3 Stories        | 15 Points         | 100%                            |
+--------------------------+------------------+-------------------+---------------------------------+
| TỔNG CỘNG                | 27 Stories       | 110 Points        | 100% Hoàn thành Sprint          |
+---------------------------------------------------------------------------------------------------+
```
