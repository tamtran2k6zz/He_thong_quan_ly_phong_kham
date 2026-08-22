# TÀI LIỆU ĐẶC TẢ SDLC - GIAI ĐOẠN 4 (BÁO CÁO TỔNG KẾT CUỐI KỲ)
## BÁO CÁO ĐÁNH GIÁ AN TOÀN BẢO MẬT, HƯỚNG DẪN TRIỂN KHAI, SỔ TAY NGƯỜI DÙNG & KỊCH BẢN DEMO 8 BƯỚC
### DỰ ÁN: HỆ THỐNG QUẢN LÝ PHÒNG KHÁM ĐA KHOA THÔNG MINH TÍCH HỢP TRỢ LÝ AI HÀNH CHÍNH
*(Clinic Management System with Administrative AI Assistant - CMS-AI)*

---

## 1. BÁO CÁO ĐÁNH GIÁ AN TOÀN & BẢO MẬT HỆ THỐNG

### 1.1. Đánh giá Kiểm soát Phân quyền & Cô lập Dữ liệu (RBAC Security)
Hệ thống CMS-AI triển khai mô hình phòng thủ theo chiều sâu (Defense-in-Depth) chống lại các nguy cơ leo thang đặc quyền:
1. **Chống Leo thang Đặc quyền Ngang/Dọc (Privilege Escalation Defense):** Mọi endpoint API đều được kiểm tra token JWT và lớp phụ thuộc `RoleChecker`. Lễ tân không thể xem hồ sơ bệnh án hoặc kê đơn; Bác sĩ không thể can thiệp thu tiền hay chỉnh sửa tài khoản quản trị; Kế toán chỉ được thao tác trên hóa đơn viện phí.
2. **Bảo vệ Mật khẩu & Phiên làm việc:** Mật khẩu người dùng được băm một chiều bằng thuật toán `Bcrypt` (12 vòng lặp). Token JWT có thời hạn hiệu lực rõ ràng và chứa chữ ký mật mã `HS256` không thể giả mạo.

### 1.2. Đánh giá Khử định danh PII & Quyền riêng tư Y tế
- **100% Thông tin Nhạy cảm Được Che:** Dữ liệu cá nhân (CCCD 12 số, SĐT, Mã BHYT, Họ tên bệnh nhân) được module `PIIAnonymizer` tự động chuyển đổi thành các mã đại diện (`[PATIENT_NAME_REDACTED]`, `[CCCD_REDACTED]`) trước khi đưa vào prompt của bất kỳ mô hình AI nào.
- **Không Lưu trữ Dữ liệu Nhạy cảm trên Prompt Log:** Bảng `ai_invocation_logs` chỉ lưu trữ chuỗi prompt **sau khi đã được khử định danh**, đảm bảo không rò rỉ dữ liệu ngay cả khi cơ sở dữ liệu nhật ký bị thanh tra.

### 1.3. Hệ thống Ghi Nhật ký Kiểm toán Toàn diện (Audit Logging)
Mọi hành vi đọc hoặc chỉnh sửa dữ liệu bệnh nhân, lập đơn thuốc, thanh toán viện phí đều tự động tạo bản ghi trong bảng `audit_logs` gồm: `user_id`, `action`, `entity_type`, `entity_id`, `ip_address`, `timestamp`. Ban quản trị có thể truy vết chính xác ai đã thực hiện thao tác nào vào thời điểm nào.

---

## 2. HƯỚNG DẪN TRIỂN KHAI VÀ KHỞI CHẠY HỆ THỐNG

### 2.1. Triển khai bằng Docker Compose (Khuyên dùng cho Môi trường Đóng gói / Server)

Hệ thống được đóng gói hoàn chỉnh thành cụm 4 Container:
1. `clinic_backend`: Chạy FastAPI REST API & AI Engine trên cổng `8000`.
2. `clinic_frontend`: Chạy React Single Page Application (Nginx) trên cổng `3000`.
3. `clinic_postgres`: Cơ sở dữ liệu quan hệ PostgreSQL 16 trên cổng `5432`.
4. `clinic_pgadmin`: Giao diện quản trị database trực quan trên cổng `5050`.

```bash
# 1. Di chuyển vào thư mục dự án
cd "d:/ICTU/Nam 3/ICTU_2026-2027/Ứng dụng trí tuệ nhân tạo - Project/He_thong_quan_ly_phong_kham"

# 2. Cấu hình file môi trường (nếu cần thay đổi cổng hoặc khóa AI)
cp .env.example .env

# 3. Khởi chạy toàn bộ hệ thống
docker compose up --build -d

# 4. Kiểm tra trạng thái các container đang chạy
docker compose ps

# 5. Dừng hệ thống khi kết thúc phiên làm việc
docker compose down
```

### 2.2. Khởi chạy Cục bộ trên Windows bằng File Script (.bat)

Dành cho môi trường phát triển cục bộ và máy chấm lab không cài đặt Docker:

- **Cách 1: Chạy toàn bộ (Khuyên dùng):**
  Nhấp đúp chuột vào file `run_all.bat` tại thư mục gốc. Hệ thống sẽ tự động tạo môi trường ảo Python `.venv`, cài đặt thư viện, nạp dữ liệu mẫu và mở 2 cửa sổ chạy song song Backend (`http://localhost:8000`) và Frontend (`http://localhost:5173`).
- **Cách 2: Chạy riêng Backend:** Chạy `run_backend.bat`.
- **Cách 3: Chạy riêng Frontend:** Chạy `run_frontend.bat`.
- **Cách 4: Chạy toàn bộ Test tự động:** Chạy `run_tests.bat`.

---

## 3. SỔ TAY HƯỚNG DẪN SỬ DỤNG THEO TỪNG VAI TRÒ (USER MANUAL)

### 3.1. Danh sách Tài khoản Đăng nhập Mẫu
| Vai trò | Tên đăng nhập | Mật khẩu | Chức danh / Họ tên |
|---|---|---|---|
| **Admin** | `admin` | `admin123` | Quản trị viên Hệ thống |
| **Lễ tân** | `receptionist` | `rec123` | Nguyễn Thị Thu Hà |
| **Bác sĩ (Tim mạch)** | `dr_nam` | `doc123` | BS.CKII Nguyễn Văn Nam |
| **Bác sĩ (Tiêu hóa)** | `dr_huong` | `doc123` | ThS.BS Lê Thu Hương |
| **Bác sĩ (Nhi khoa)** | `dr_minh` | `doc123` | BS.CKI Phạm Hoàng Minh |
| **Bác sĩ (Tai Mũi Họng)** | `dr_lan` | `doc123` | BS Vũ Mai Lan |
| **Kế toán** | `accountant` | `acc123` | Trần Bích Phương |

---

### 3.2. Hướng dẫn dành cho Lễ tân (Receptionist)
1. **Đăng nhập:** Truy cập `http://localhost:5173`, nhập `receptionist` / `rec123`.
2. **Đăng ký Bệnh nhân Mới:**
   - Vào menu *Tiếp đón & Bệnh nhân* $\rightarrow$ Chọn *Thêm bệnh nhân*.
   - Nhập Họ tên, Ngày sinh, Số điện thoại, CCCD, Số thẻ BHYT, Tiền sử dị ứng.
   - Nhấn *Lưu hồ sơ*. Hệ thống tự động cấp mã y tế dạng `BN-YYYYMMDD-XXXX`.
3. **Đặt Lịch hẹn & Điều phối Khám:**
   - Vào menu *Lịch hẹn & Lịch khám*. Chọn Bệnh nhân, Chuyên khoa, Bác sĩ và Khung giờ.
   - Thuật toán kiểm tra xung đột sẽ tự động cảnh báo nếu bác sĩ đã có lịch trùng.
   - Khi bệnh nhân đến quầy: Nhấn nút **Tiếp đón (Check-in)** để cấp số thứ tự vào phòng khám.
4. **Tra cứu Quy trình bằng AI Chatbot:**
   - Nhấp vào biểu tượng Trợ lý AI ở góc màn hình để hỏi các quy định về BHYT, bảng giá và thủ tục hành chính.

---

### 3.3. Hướng dẫn dành cho Bác sĩ (Doctor)
1. **Đăng nhập:** Nhập tài khoản `dr_nam` / `doc123`.
2. **Tiếp nhận Hàng đợi Khám:**
   - Tại màn hình *Phòng khám Bác sĩ*, xem danh sách bệnh nhân đang chờ theo số thứ tự.
   - Nhấn vào bệnh nhân để mở phiên khám.
3. **Xem AI Pre-visit Briefing:**
   - Thẻ AI tự động hiển thị tóm tắt: Tiền sử bệnh, dị ứng thuốc nguy hiểm (được đánh dấu cảnh báo màu đỏ), lịch sử đợt khám trước.
4. **Ghi nhận Khám lâm sàng & Chỉ định:**
   - Nhập sinh hiệu: Huyết áp (mmHg), Mạch, Thân nhiệt.
   - Nhập chẩn đoán xác định và mã chuẩn ICD-10 (ví dụ `I10 - Tăng huyết áp vô căn`).
   - Chỉ định cận lâm sàng (Điện tâm đồ, Siêu âm...) nếu cần.
5. **Kê Đơn thuốc Điện tử & Dặn dò AI:**
   - Chọn thuốc từ danh mục (Amoxicillin, Amlodipine...), nhập số lượng và liều dùng.
   - Nhấn nút **Sinh dặn dò sau khám bằng AI (AI Discharge Instructions)**: Hệ thống tự động tạo lịch uống thuốc, chế độ ăn kiêng và dấu hiệu cần tái khám.
   - Bác sĩ kiểm tra nội dung và nhấn **Hoàn tất ca khám**.

---

### 3.4. Hướng dẫn dành cho Kế toán / Thu ngân (Accountant)
1. **Đăng nhập:** Nhập tài khoản `accountant` / `acc123`.
2. **Tiếp nhận Hồ sơ Chờ Thanh toán:**
   - Vào menu *Thu ngân & Viện phí*. Danh sách các ca khám vừa hoàn tất sẽ hiển thị trạng thái `Chờ thanh toán`.
3. **Tổng hợp Chi phí & Khấu trừ BHYT:**
   - Nhấp vào hóa đơn: Hệ thống tự động liệt kê chi tiết: Tiền khám + Tiền xét nghiệm + Tiền thuốc.
   - Áp dụng tự động mức giảm trừ BHYT (nếu bệnh nhân có thẻ).
4. **Xác nhận Thu tiền & In Phiếu thu:**
   - Chọn hình thức: **Tiền mặt** hoặc **Chuyển khoản VietQR** (hệ thống tự động sinh mã QR động kèm số tiền chính xác).
   - Nhấn **Xác nhận thanh toán** $\rightarrow$ Hóa đơn chuyển trạng thái `ĐÃ THANH TOÁN`.
   - Nhấn nút **In Hóa đơn** để xuất phiếu thu viện phí chuẩn khổ giấy in cho người bệnh.

---

### 3.5. Hướng dẫn dành cho Quản trị viên (Admin)
1. **Đăng nhập:** Nhập tài khoản `admin` / `admin123`.
2. **Quản lý Tài khoản & Phân quyền:** Thêm mới, chỉnh sửa thông tin, khóa tài khoản nhân viên.
3. **Quản lý Bác sĩ & Ca trực:** Cập nhật chuyên khoa, phòng khám, xếp lịch trực trong tuần.
4. **Quản lý Danh mục Thuốc:** Thêm thuốc mới, cập nhật đơn giá, theo dõi số lượng tồn kho.
5. **Giám sát Nhật ký Kiểm toán & AI:**
   - Xem *Audit Logs*: Lịch sử truy cập hồ sơ bệnh nhân của từng nhân viên y tế.
   - Xem *AI Invocation Logs*: Kiểm tra các prompt đã được khử định danh PII, model xử lý, thời gian phản hồi.
6. **Báo cáo Thống kê:** Biểu đồ doanh thu thực tế, biểu đồ phân bổ lượt khám theo từng chuyên khoa và hiệu suất bác sĩ.

---

## 4. KỊCH BẢN DEMO ĐÁNH GIÁ CHẤM ĐIỂM HOÀN CHỈNH (8 BƯỚC TIÊU CHUẨN)

Hội đồng giám khảo / Giảng viên có thể thực hiện kiểm chứng toàn diện đồ án theo đúng 8 bước tuần tự dưới đây:

```
[BƯỚC 1: ADMIN]       Kiểm tra hạ tầng, tài khoản, danh mục thuốc & ca trực
      |
      v
[BƯỚC 2: LỄ TÂN]      Đăng ký hồ sơ bệnh nhân mới (Sinh mã BN-YYYYMMDD-XXXX)
      |
      v
[BƯỚC 3: LỄ TÂN]      Đặt lịch khám & Chứng minh Thuật toán Chống trùng lịch
      |
      v
[BƯỚC 4: LỄ TÂN]      Tiếp đón phát số thứ tự hàng đợi & Hỏi Chatbot AI quy trình
      |
      v
[BƯỚC 5: BÁC SĨ]      Mở hàng đợi, đọc Thẻ AI Pre-visit Briefing (Cảnh báo dị ứng)
      |
      v
[BƯỚC 6: BÁC SĨ]      Khám bệnh, chẩn đoán ICD-10, kê đơn thuốc & Sinh dặn dò AI
      |
      v
[BƯỚC 7: KẾ TOÁN]     Tổng hợp viện phí, khấu trừ BHYT, thu tiền VietQR & In hóa đơn
      |
      v
[BƯỚC 8: ADMIN]       Kiểm tra Audit Log, AI Request Log (Khử PII) & Biểu đồ doanh thu
```

---

### Bước 1: Quản trị viên (Admin) Kiểm tra Cấu hình & Danh mục
- **Thao tác:** Đăng nhập `admin` / `admin123`.
- **Minh chứng:**
  - Xem Dashboard tổng quan hệ thống.
  - Kiểm tra danh sách 4 chuyên khoa (*Nội tổng quát, Tim mạch, Tiêu hóa, Nhi khoa*).
  - Kiểm tra danh mục thuốc và số lượng tồn kho khả dụng.

### Bước 2: Lễ tân (Receptionist) Đăng ký Hồ sơ Bệnh nhân Mới
- **Thao tác:** Đăng nhập `receptionist` / `rec123`. Vào mục *Đăng ký Bệnh nhân*.
- **Nhập thông tin:**
  - Họ tên: `Hoàng Minh Đức`
  - Ngày sinh: `15/08/1985` - Giới tính: `Nam`
  - Điện thoại: `0912345678` - CCCD: `001085012345`
  - Mã BHYT: `GD4010123456789`
  - Tiền sử dị ứng: `Dị ứng nghiêm trọng với Penicillin và Aspirin`
- **Kết quả:** Hệ thống cấp mã hồ sơ `BN-20260822-0001` thành công.

### Bước 3: Đặt lịch hẹn & Thử nghiệm Thuật toán Chống Trùng lịch
- **Thao tác:** Đặt lịch khám cho bệnh nhân `Hoàng Minh Đức` với Bác sĩ `BS.CKII Nguyễn Văn Nam` (Phòng P.101).
- **Thử nghiệm Xung đột (Conflict Test):**
  - Cố tình chọn khung giờ mà Bác sĩ Nam đã có lịch hẹn trước đó.
  - **Kết quả mong đợi:** Hệ thống hiển thị cảnh báo từ chối: *"Bác sĩ đã có lịch hẹn khác trong khung giờ này. Vui lòng chọn khung giờ khác."*
- **Đặt lịch thành công:** Chọn khung giờ còn trống (ví dụ: `09:30 - 10:00`). Hệ thống ghi nhận lịch hẹn `CONFIRMED`.

### Bước 4: Tiếp đón Bệnh nhân & Sử dụng Chatbot AI
- **Thao tác:** Tại danh sách lịch hẹn trong ngày, bấm nút **Tiếp đón (Check-in)**. Bệnh nhân nhận số thứ tự khám `STT: 01`.
- **Thử nghiệm AI Chatbot:**
  - Lễ tân mở widget Chatbot AI và hỏi: *"Bệnh nhân dùng BHYT trái tuyến thì thủ tục thanh toán như thế nào?"*
  - **Kết quả mong đợi:** Chatbot trích xuất kiến thức chuẩn về quy định chuyển tuyến BHYT và mức hưởng, đính kèm Tuyên bố miễn trừ trách nhiệm y tế.
  - Thử hỏi câu hỏi bệnh học: *"Bệnh nhân đau ngực trái nên uống kháng sinh gì?"* $\rightarrow$ Chatbot từ chối đưa ra chẩn đoán và hướng dẫn đưa bệnh nhân vào gặp bác sĩ ngay.

### Bước 5: Bác sĩ (Doctor) Tiếp nhận Bệnh nhân & Xem AI Pre-visit Briefing
- **Thao tác:** Đăng xuất, đăng nhập Bác sĩ `dr_nam` / `doc123`.
- **Minh chứng:**
  - Bác sĩ thấy bệnh nhân `Hoàng Minh Đức` (STT 01) trong hàng đợi của phòng mình.
  - Bấm tiếp nhận: Thẻ **AI Pre-visit Briefing** hiển thị nổi bật cảnh báo:
    - ⚠️ **DỊ ỨNG THUỐC:** `Penicillin, Aspirin (Nguy cơ sốc phản vệ)`.
    - **Tóm tắt tiền sử:** `Tăng huyết áp 3 năm, không có biến cố tim mạch cấp`.
    - **Disclaimer:** `Tuyên bố miễn trừ trách nhiệm y tế...`

### Bước 6: Khám bệnh, Kê đơn thuốc & Sinh Hướng dẫn Xuất viện AI
- **Thao tác:** Bác sĩ thực hiện thăm khám:
  - Sinh hiệu: Huyết áp `145/90 mmHg`, Mạch `82 l/p`, Thân nhiệt `36.8°C`.
  - Triệu chứng: `Đau đầu vùng gáy, chóng mặt nhẹ khi thay đổi tư thế`.
  - Chẩn đoán ICD-10: `I10 - Tăng huyết áp vô căn`.
  - Chỉ định: `Đo điện tim (ECG)`.
  - Kê đơn thuốc: Chọn `Amlodipine 5mg` (Số lượng: 30 viên, 1 viên/ngày vào buổi sáng).
  - Bấm nút **Sinh Dặn Dò AI (AI Discharge Instructions)**: AI tạo lịch uống thuốc, chế độ ăn nhạt (< 5g muối/ngày), tập thể dục nhẹ nhàng và dấu hiệu huyết áp > 180 cần cấp cứu.
  - Bác sĩ bấm **Hoàn tất ca khám**.

### Bước 7: Kế toán (Accountant) Tổng hợp Viện phí & Thanh toán VietQR
- **Thao tác:** Đăng xuất, đăng nhập `accountant` / `acc123`.
- **Minh chứng:**
  - Mở danh sách hóa đơn: Thấy hồ sơ của bệnh nhân `Hoàng Minh Đức` ở trạng thái `Chờ thanh toán`.
  - Chi tiết hóa đơn:
    - Tiền khám: `150,000 VNĐ`
    - Tiền dịch vụ (ECG): `100,000 VNĐ`
    - Tiền thuốc (Amlodipine): `90,000 VNĐ`
    - Tổng chi phí: `340,000 VNĐ`
    - Giảm trừ BHYT (80% danh mục): `-200,000 VNĐ`
    - Thực thu: `140,000 VNĐ`.
  - Bấm nút **Thanh toán VietQR**: Hệ thống hiển thị mã VietQR động chuẩn NAPAS247.
  - Bấm **Xác nhận đã thanh toán** và bấm **In Phiếu thu viện phí**.

### Bước 8: Quản trị viên (Admin) Giám sát Logs & Thống kê Doanh thu
- **Thao tác:** Đăng nhập lại `admin` / `admin123`.
- **Minh chứng An toàn & Thống kê:**
  - Mở mục *Audit Logs*: Ghi nhận toàn bộ thao tác của `receptionist`, `dr_nam`, `accountant`.
  - Mở mục *AI Request Logs*: Thấy các bản ghi gọi AI tóm tắt hồ sơ và sinh dặn dò; **toàn bộ dữ liệu tên bệnh nhân và số CCCD đều đã được chuyển thành mã ẩn danh `[PATIENT_NAME_REDACTED]`**, không lưu thông tin cá nhân.
  - Mở mục *Thống kê Báo cáo*: Doanh thu phòng khám và lượt khám tại chuyên khoa Tim mạch được cập nhật tăng trưởng tức thời trên biểu đồ.
