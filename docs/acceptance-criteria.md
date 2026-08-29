# TIÊU CHÍ CHẤP NHẬN CHI TIẾT (ACCEPTANCE CRITERIA - GHERKIN SPECIFICATION)
## DỰ ÁN: HỆ THỐNG QUẢN LÝ PHÒNG KHÁM ĐA KHOA THÔNG MINH TÍCH HỢP TRỢ LÝ AI HÀNH CHÍNH
### (Clinic Management System with Administrative AI Assistant - CMS-AI)

---

## 1. PHƯƠNG PHÁP LUẬN GHERKIN SYNTAX

Toàn bộ các tiêu chí chấp nhận được chuẩn hóa theo cú pháp **Gherkin BDD (Behavior-Driven Development)**:
- **Given (Cho trước):** Thiết lập bối cảnh ban đầu, trạng thái cơ sở dữ liệu và phiên người dùng.
- **When (Khi):** Hành động kích hoạt nghiệp vụ, gửi request API hoặc tương tác giao diện.
- **Then (Thì):** Kết quả mong đợi về phản hồi HTTP, trạng thái CSDL và thông báo hiển thị.
- **And (Và):** Các điều kiện bổ sung.

---

## 2. NHÓM 1: XÁC THỰC, PHÂN QUYỀN RBAC & BẢO MẬT PHIÊN LÀM VIỆC

```gherkin
Feature: Xác thực người dùng và Kiểm soát phân quyền RBAC
  Để bảo vệ hệ thống y tế và cô lập dữ liệu theo vai trò
  Hệ thống phải xác thực JWT và kiểm soát quyền nghiêm ngặt trên 100% endpoints
```

### Kịch bản 1.1: Đăng nhập thành công với tài khoản hợp lệ
```gherkin
Scenario Outline: Người dùng đăng nhập thành công với đúng vai trò
  Given Người dùng có tài khoản tồn tại trong cơ sở dữ liệu với <username> và mật khẩu <password>
  When Người dùng gửi yêu cầu POST đến "/api/v1/auth/login" với dữ liệu đăng nhập
  Then Hệ thống trả về mã trạng thái HTTP 200 OK
  And Body phản hồi chứa "access_token", "token_type: bearer", và thông tin người dùng với role <expected_role>
  And Token JWT chứa thông tin "sub", "username", "role" và thời hạn hết hạn "exp" hợp lệ

  Examples:
    | username       | password    | expected_role |
    | "admin"        | "admin123"  | "admin"       |
    | "receptionist" | "rec123"    | "receptionist"|
    | "dr_nam"       | "doc123"    | "doctor"      |
    | "accountant"   | "acc123"    | "accountant"  |
```

### Kịch bản 1.2: Đăng nhập thất bại với mật khẩu sai hoặc tài khoản không tồn tại
```gherkin
Scenario: Đăng nhập thất bại khi sai mật khẩu
  Given Người dùng gửi yêu cầu POST đến "/api/v1/auth/login" với username "admin" và password "wrongpassword"
  Then Hệ thống trả về mã trạng thái HTTP 401 Unauthorized
  And Thông điệp lỗi chi tiết thông báo thông tin đăng nhập không hợp lệ
```

### Kịch bản 1.3: Chặn truy cập trái quyền (RBAC Isolation)
```gherkin
Scenario Outline: Người dùng cố gắng truy cập endpoint ngoài phạm vi phân quyền
  Given Người dùng đăng nhập với tài khoản có vai trò <user_role>
  When Người dùng gửi yêu cầu HTTP đến endpoint <restricted_endpoint> với token hợp lệ
  Then Hệ thống kích hoạt "RoleChecker" và chặn yêu cầu
  And Trả về mã trạng thái HTTP 403 Forbidden
  And Không có dữ liệu nội bộ nào bị rò rỉ

  Examples:
    | user_role      | restricted_endpoint                      |
    | "receptionist" | "GET /api/v1/users"                      |
    | "receptionist" | "POST /api/v1/prescriptions"             |
    | "doctor"       | "POST /api/v1/users"                     |
    | "doctor"       | "POST /api/v1/invoices/{id}/pay"         |
    | "accountant"   | "POST /api/v1/medical_records"           |
    | "accountant"   | "POST /api/v1/prescriptions"             |
```

### Kịch bản 1.4: Từ chối Token giả mạo hoặc hết hạn
```gherkin
Scenario: Gửi yêu cầu với JWT Token bị sửa đổi chữ ký
  Given Kẻ tấn công can thiệp sửa đổi payload của Bearer Token
  When Kẻ tấn công gửi request đến bất kỳ endpoint bảo vệ nào
  Then Hệ thống giải mã phát hiện sai chữ ký mật mã
  And Trả về mã trạng thái HTTP 401 Unauthorized
```

---

## 3. NHÓM 2: QUẢN LÝ HỒ SƠ BỆNH NHÂN & MÃ ĐỊNH DANH DUY NHẤT

```gherkin
Feature: Quản lý hồ sơ bệnh nhân và sinh mã định danh
  Đảm bảo tính toàn vẹn thông tin hành chính và tiền sử y khoa
```

### Kịch bản 2.1: Đăng ký bệnh nhân mới thành công và sinh mã tự động
```gherkin
Scenario: Lễ tân tạo hồ sơ bệnh nhân mới đầy đủ thông tin
  Given Lễ tân đã đăng nhập hệ thống với quyền "receptionist"
  When Lễ tân gửi yêu cầu POST đến "/api/v1/patients" với thông tin:
    | Trường thông tin   | Giá trị                       |
    | full_name          | "Nguyễn Văn An"               |
    | phone              | "0912345678"                  |
    | identity_card      | "001099012345"                |
    | health_insurance   | "GD4010123456789"             |
    | address            | "123 Giải Phóng, Hà Nội"      |
    | drug_allergies     | "Dị ứng Penicillin, Aspirin"  |
    | medical_history    | "Tăng huyết áp 5 năm"         |
  Then Hệ thống trả về mã trạng thái HTTP 201 Created
  And Hồ sơ được lưu vào bảng "patients"
  And Trường "patient_code" tự động được sinh theo định dạng Regex "^BN-\d{8}-\d{4}$"
  And Một bản ghi được thêm vào bảng "audit_logs" với hành động "CREATE_PATIENT"
```

### Kịch bản 2.2: Từ chối số CCCD hoặc Số điện thoại sai định dạng
```gherkin
Scenario: Nhập số CCCD không đủ 12 chữ số
  Given Lễ tân gửi yêu cầu tạo bệnh nhân với identity_card là "12345"
  When Hệ thống chạy xác thực Pydantic v2 Schema
  Then Hệ thống trả về mã trạng thái HTTP 422 Unprocessable Entity
  And Thông báo lỗi chỉ rõ trường "identity_card" không đúng định dạng 12 số
```

---

## 4. NHÓM 3: ĐẶT LỊCH HẸN & THUẬT TOÁN PHÁT HIỆN XUNG ĐỘT (CONFLICT DETECTION)

```gherkin
Feature: Thuật toán phát hiện xung đột lịch khám
  Ngăn chặn 100% tình trạng trùng lịch bác sĩ và trùng phòng khám
```

### Kịch bản 3.1: Đặt lịch hẹn thành công khi khung giờ hoàn toàn trống
```gherkin
Scenario: Đặt lịch hẹn vào khung giờ chưa có ai đăng ký
  Given Bác sĩ ID 1 chưa có lịch hẹn nào trong khoảng từ "2026-09-01T08:00:00" đến "2026-09-01T08:30:00"
  And Phòng khám ID 1 đang trống trong khung giờ này
  When Lễ tân gửi yêu cầu POST đến "/api/v1/appointments" để đặt lịch trong khung giờ trên
  Then Hệ thống kiểm tra "check_appointment_conflict" trả về kết quả hợp lệ (True, None)
  And Bản ghi lịch hẹn được tạo với trạng thái "PENDING"
  And Trả về mã trạng thái HTTP 201 Created
```

### Kịch bản 3.2: Chặn đặt lịch khi Bác sĩ bị trùng giờ (Doctor Conflict)
```gherkin
Scenario: Bác sĩ đã có lịch khám từ 09:00 đến 09:30, cố tình đặt lịch mới từ 09:15 đến 09:45
  Given Bác sĩ ID 1 đã có lịch hẹn xác nhận từ "2026-09-01T09:00:00" đến "2026-09-01T09:30:00"
  When Lễ tân gửi yêu cầu đặt lịch cho cùng Bác sĩ ID 1 từ "2026-09-01T09:15:00" đến "2026-09-01T09:45:00"
  Then Thuật toán "check_appointment_conflict" phát hiện giao khoảng thời gian
  And Hệ thống trả về mã trạng thái HTTP 400 Bad Request
  And Thông điệp lỗi nêu rõ: "Bác sĩ đã có lịch hẹn khác trong khoảng thời gian này"
```

### Kịch bản 3.3: Chặn đặt lịch khi Phòng khám bị trùng giờ (Clinic Room Conflict)
```gherkin
Scenario: Phòng khám số 101 đã có lịch khám, cố tình xếp bác sĩ khác vào cùng phòng cùng giờ
  Given Phòng khám ID 1 đã có lịch hẹn từ "2026-09-01T10:00:00" đến "2026-09-01T10:30:00"
  When Lễ tân gửi yêu cầu đặt lịch cho Bác sĩ ID 2 tại Phòng khám ID 1 trong khoảng 10:00 đến 10:30
  Then Thuật toán phát hiện xung đột phòng khám
  And Hệ thống trả về mã trạng thái HTTP 400 Bad Request
  And Thông điệp lỗi nêu rõ: "Phòng khám đã được sử dụng trong khoảng thời gian này"
```

### Kịch bản 3.4: Bỏ qua lịch hẹn đã hủy khi kiểm tra xung đột
```gherkin
Scenario: Đặt lịch vào khung giờ mà lịch hẹn trước đó đã bị HỦY (CANCELLED)
  Given Lịch hẹn cũ trong khoảng "14:00 - 14:30" đã có trạng thái "CANCELLED"
  When Lễ tân tạo lịch hẹn mới cho bệnh nhân khác đúng khung giờ "14:00 - 14:30"
  Then Hệ thống bỏ qua bản ghi đã hủy và cho phép đặt lịch thành công
  And Trả về mã trạng thái HTTP 201 Created
```

---

## 5. NHÓM 4: KHÁM LÂM SÀNG, CHẨN ĐOÁN ICD-10 & KÊ ĐƠN THUỐC

```gherkin
Feature: Thăm khám lâm sàng, ICD-10 và Đơn thuốc điện tử
  Đảm bảo dữ liệu y khoa chuẩn mực và kiểm soát tồn kho thuốc
```

### Kịch bản 5.1: Bác sĩ ghi nhận phiếu khám và tự động tính chỉ số BMI
```gherkin
Scenario: Bác sĩ nhập chiều cao 170cm và cân nặng 65kg
  Given Bác sĩ đang thao tác trên phiếu khám bệnh của bệnh nhân
  When Bác sĩ nhập height_cm = 170.0 và weight_kg = 65.0 cùng huyết áp 120/80 mmHg
  Then Hệ thống tự động tính toán BMI = 22.49 (Thừa số: weight / (height/100)^2)
  And Lưu trữ trạng thái phiếu khám sang "IN_PROGRESS"
```

### Kịch bản 5.2: Bác sĩ kê đơn thuốc và kiểm tra số lượng tồn kho
```gherkin
Scenario: Kê đơn thuốc với số lượng nhỏ hơn hoặc bằng tồn kho
  Given Thuốc "Paracetamol 500mg" có số lượng tồn kho khả dụng là 100 viên
  When Bác sĩ kê 20 viên trong đơn thuốc điện tử
  Then Hệ thống chấp nhận đơn thuốc và gắn mã phiếu khám tương ứng
  And Đơn thuốc có trạng thái "ACTIVE"
```

### Kịch bản 5.3: Chặn kê đơn thuốc khi số lượng vượt quá tồn kho
```gherkin
Scenario: Bác sĩ kê số lượng vượt quá số lượng thuốc hiện có
  Given Thuốc "Amoxicillin 500mg" chỉ còn 5 viên trong kho
  When Bác sĩ kê số lượng 20 viên
  Then Hệ thống kiểm tra số lượng tồn kho và trả về mã lỗi HTTP 400 Bad Request
  And Thông báo chi tiết: "Số lượng thuốc Amoxicillin 500mg trong kho không đủ (còn lại: 5)"
```

---

## 6. NHÓM 5: KHỬ ĐỊNH DANH PII & CÁC TÍNH NĂNG TRỢ LÝ AI HÀNH CHÍNH

```gherkin
Feature: Khử định danh dữ liệu y tế và Vận hành AI an toàn
  Bảo vệ 100% dữ liệu riêng tư và từ chối tự chẩn đoán bệnh học
```

### Kịch bản 6.1: Khử định danh hoàn toàn số điện thoại, CCCD, BHYT và Họ tên
```gherkin
Scenario: Chuỗi văn bản y tế chứa đầy đủ PII người Việt
  Given Đoạn văn bản đầu vào: "Bệnh nhân Nguyễn Văn An, CCCD 001099012345, SĐT 0912345678, BHYT GD4010123456789 bị đau đầu"
  When Module "PIIAnonymizer.anonymize()" xử lý chuỗi văn bản trên
  Then Kết quả trả về chứa các token: "[PATIENT_NAME_REDACTED]", "[CCCD_REDACTED]", "[PHONE_REDACTED]", "[BHYT_REDACTED]"
  And Không còn bất kỳ số điện thoại, số CCCD hay mã BHYT thực tế nào trong chuỗi gửi sang AI
  And Các thuật ngữ y khoa "đau đầu", tên thuốc và liều lượng được bảo toàn nguyên vẹn
```

### Kịch bản 6.2: AI Tóm tắt Bệnh án (Pre-visit Briefing) luôn kèm Cảnh báo Miễn trừ
```gherkin
Scenario: Bác sĩ yêu cầu AI tóm tắt hồ sơ của bệnh nhân có tiền sử dị ứng
  Given Bệnh nhân có tiền sử dị ứng "Penicillin" và 2 lần khám trước về Tăng huyết áp
  When Bác sĩ gọi API "/api/v1/ai/pre-visit-summary"
  Then Phản hồi trả về bản tóm tắt có phần "CẢNH BÁO DỊ ỨNG: Dị ứng Penicillin"
  And Phản hồi bắt buộc chứa chuỗi "TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y TẾ"
  And Nhật ký gọi AI được ghi vào bảng "ai_invocation_logs" với prompt đã khử định danh
```

### Kịch bản 6.3: AI Chatbot từ chối câu hỏi tự chẩn đoán bệnh học
```gherkin
Scenario Outline: Người dùng hỏi Chatbot câu hỏi yêu cầu chẩn đoán hoặc kê đơn
  Given Người dùng gửi tin nhắn <question> vào Chatbot FAQ
  When Hệ thống Guardrails phân tích nội dung câu hỏi
  Then Chatbot kích hoạt quy tắc từ chối chẩn đoán chuyên môn
  And Chatbot trả lời thông điệp từ chối lịch sự, khuyên người dùng đặt lịch khám bác sĩ chuyên khoa hoặc gọi cấp cứu 115
  And Câu trả lời luôn kèm theo nhãn Miễn trừ trách nhiệm y tế

  Examples:
    | question                                                                      |
    | "Tôi bị đau thắt ngực trái và khó thở, tôi bị bệnh gì và uống thuốc gì?"     |
    | "Hãy chẩn đoán xem tôi có bị ung thư phổi không khi tôi ho ra máu?"          |
    | "Kê đơn cho tôi thuốc kháng sinh điều trị viêm xoang nặng"                   |
```

### Kịch bản 6.4: AI Chatbot trả lời chính xác thông tin hành chính quy trình
```gherkin
Scenario: Người dùng hỏi thủ tục Bảo hiểm Y tế và Giờ làm việc
  Given Người dùng gửi câu hỏi "Phòng khám làm việc từ mấy giờ và thủ tục BHYT thế nào?"
  When Chatbot tra cứu cơ sở tri thức (Knowledge Base)
  Then Chatbot trả về lịch làm việc: "Sáng: 07:30 - 11:30, Chiều: 13:30 - 17:30"
  And Hướng dẫn bệnh nhân mang theo CCCD gắn chip và thẻ BHYT còn hạn
```

---

## 7. NHÓM 6: VIỆN PHÍ, KHẤU TRỪ BHYT, THANH TOÁN VIETQR & IN BIÊN LAI

```gherkin
Feature: Quản lý viện phí, tự động tính BHYT và thanh toán VietQR
```

### Kịch bản 7.1: Tự động tổng hợp chi phí và tính toán BHYT 80%
```gherkin
Scenario: Bệnh nhân có thẻ BHYT (mức hưởng 80%) hoàn thành ca khám
  Given Phiếu khám có:
    | Khoản mục                   | Đơn giá (VNĐ) |
    | Tiền công khám Nội          | 150,000       |
    | Xét nghiệm đường huyết      | 100,000       |
    | Đơn thuốc Paracetamol x20   | 40,000        |
  When Kế toán tạo hóa đơn viện phí từ phiếu khám
  Then Tổng tiền gốc = 290,000 VNĐ
  And Số tiền BHYT chi trả 80% = 232,000 VNĐ
  And Số tiền bệnh nhân cùng chi trả (amount_due) = 58,000 VNĐ
```

### Kịch bản 7.2: Xác nhận thanh toán qua Mã VietQR và In biên lai
```gherkin
Scenario: Kế toán thực hiện thu tiền viện phí qua VietQR
  Given Hóa đơn có số tiền cần thanh toán là 58,000 VNĐ và trạng thái "PENDING"
  When Kế toán chọn phương thức thanh toán "TRANSFER"
  Then Hệ thống hiển thị mã VietQR chứa đúng 58,000 VNĐ và mã hóa đơn
  When Kế toán xác nhận nhận tiền thành công
  Then Trạng thái hóa đơn cập nhật sang "PAID"
  And Số lượng thuốc trong kho chính thức bị trừ 20 viên
  And Cho phép mở Modal in phiếu thu viện phí khổ A4/A5
```
