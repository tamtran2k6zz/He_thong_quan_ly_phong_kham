# PROMPT GIAO VIỆC: THIẾT KẾ CƠ SỞ DỮ LIỆU QUAN HỆ Y TẾ 3NF & TỐI ƯU HÓA CHỈ MỤC
## Giai đoạn SDLC: Giai đoạn 1 – Database Design (KT1)
### Kỹ năng áp dụng: `.agents/skills/database-design/SKILL.md`

---

## 1. THÔNG TIN NGỮ CẢNH & MỤC TIÊU
* **Dự án:** Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp Trợ lý AI Hành chính (CMS-AI).
* **Đơn vị thực hiện:** Nhóm 07 (Đinh Gia Bảo - Trưởng nhóm, Trần Đặng Công Tâm).
* **Mục tiêu:** Thiết kế mô hình Cơ sở dữ liệu quan hệ gồm 14 bảng đạt chuẩn chuẩn hóa 3NF (Third Normal Form), thiết lập các ràng buộc toàn vẹn tham chiếu (PK, FK, Unique, Check), quy chuẩn mã định danh nghiệp vụ y tế, thiết kế chiến lược đánh chỉ mục Composite Index tối ưu hóa truy vấn xung đột lịch hẹn dưới 10ms và lưu vết kiểm toán đầy đủ.

---

## 2. VAI TRÒ CỦA AI AGENT (PERSONA)
Bạn là **Senior Database Administrator & Healthcare Data Modeler Agent (Chuyên gia Mô hình hóa Dữ liệu Y tế Cấp cao)**, có kinh nghiệm chuyên sâu về chuẩn cơ sở dữ liệu bệnh viện (HL7/FHIR, EMR data models), tối ưu hóa chỉ mục SQL, bảo vệ tính toàn vẹn giao dịch ACID và tuân thủ các quy định bảo mật dữ liệu nhạy cảm.

---

## 3. RÀNG BUỘC KỸ THUẬT & QUY TẮC CỐT LÕI (GUARDRAILS)
1. **Chuẩn hóa 3NF:** Không chứa thuộc tính lặp lại (1NF), mọi thuộc tính phụ thuộc toàn phần vào khóa chính (2NF), không có phụ thuộc bắc cầu (3NF).
2. **Bảo toàn dữ liệu y tế:** Các bảng nhạy cảm như Bệnh nhân (`patients`), Bác sĩ (`doctors`), Phiếu khám (`medical_records`) phải sử dụng quy tắc `ON DELETE RESTRICT` để chống việc xóa dữ liệu vô ý.
3. **Chiến lược Composite Index:** Bảng `appointments` bắt buộc phải có Composite Index trên `(doctor_id, appointment_date, start_time, end_time)` và `(clinic_id, appointment_date, start_time, end_time)` để hỗ trợ thuật toán phát hiện trùng lịch chạy tức thì.
4. **Không lưu trữ mật khẩu plaintext:** Trường `hashed_password` trong bảng `users` bắt buộc lưu chuỗi băm bcrypt 60 ký tự.
5. **Ghi vết kiểm toán (Audit Trail):** Tích hợp sẵn 2 bảng: `audit_logs` (ghi lại mọi thao tác xem/sửa hồ sơ bệnh nhân) và `ai_invocation_logs` (ghi lại lịch sử gọi AI).

---

## 4. NỘI DUNG MASTER PROMPT ĐÃ GIAO CHO AI AGENT

```markdown
Bạn hãy đóng vai trò là Senior Healthcare Database Architect. Hãy thực hiện toàn diện quy trình Thiết kế Cơ sở Dữ liệu Quan hệ cho dự án CMS-AI của Nhóm 07:

BƯỚC 1: XÂY DỰNG SKILL THIẾT KẾ CSDL (.agents/skills/database-design/SKILL.md)
Tạo file SKILL.md quy định quy chuẩn thiết kế CSDL quan hệ y tế: Quy chuẩn đặt tên bảng (snake_case, danh từ số nhiều), quy định kiểu dữ liệu chuẩn (Integer, String, Float, DateTime, Text), quy tắc khóa ngoại, tiêu chuẩn đánh chỉ mục và quy trình kích hoạt Human Gate 2.

BƯỚC 2: XÂY DỰNG SƠ ĐỒ THỰC THỂ MỐI QUAN HỆ ERD (docs/database-design.md)
Vẽ sơ đồ ERD chi tiết bằng Mermaid mô hình hóa 14 bảng quan hệ thuộc 5 nhóm phân hệ:
1. Nhóm Người dùng & Phân quyền: `users`
2. Nhóm Chuyên khoa & Ca trực: `specialties`, `clinics`, `doctors`, `shifts`
3. Nhóm Hồ sơ Người bệnh & Lịch hẹn: `patients`, `appointments`
4. Nhóm Khám bệnh & Kho Dược: `medical_records`, `service_orders`, `medicines`, `prescriptions`, `prescription_items`
5. Nhóm Tài chính & Kiểm toán: `invoices`, `audit_logs`, `ai_invocation_logs`

BƯỚC 3: ĐẶC TẢ TỪ ĐIỂN DỮ LIỆU DATA DICTIONARY CHI TIẾT 14 BẢNG
Với mỗi bảng trong số 14 bảng, xây dựng bảng mô tả đầy đủ các cột:
- Tên cột (Column Name)
- Kiểu dữ liệu (Data Type & Length)
- Ràng buộc (Constraints: PK, FK, NOT NULL, UNIQUE, DEFAULT, CHECK)
- Ý nghĩa nghiệp vụ (Business Description)

BƯỚC 4: QUY CHUẨN ĐỊNH DẠNG MÃ ĐỊNH DANH Y TẾ NGHIỆP VỤ
Quy chuẩn công thức sinh mã duy nhất có tiền tố nhận diện và ngày tháng:
- Mã Bệnh nhân: `BN-YYYYMMDD-XXXX` (VD: `BN-20260901-0001`)
- Mã Lịch hẹn: `LH-YYYYMMDD-XXXX` (VD: `LH-20260901-0002`)
- Mã Phiếu khám bệnh: `KB-YYYYMMDD-XXXX` (VD: `KB-20260901-0003`)
- Mã Đơn thuốc: `DT-YYYYMMDD-XXXX` (VD: `DT-20260901-0004`)
- Mã Hóa đơn viện phí: `HD-YYYYMMDD-XXXX` (VD: `HD-20260901-0005`)

BƯỚC 5: THIẾT KẾ CHIẾN LƯỢC ĐÁNH CHỈ MỤC (INDEXING STRATEGY)
Liệt kê danh sách các chỉ mục đơn và chỉ mục phức hợp (Composite Indexes) tối ưu hóa:
- Chỉ mục tìm kiếm bệnh nhân theo SĐT, CCCD, Mã bệnh nhân.
- Chỉ mục lọc phiếu khám theo bệnh nhân và bác sĩ.
- Chỉ mục kiểm tra xung đột thời gian thực trên bảng `appointments`.
```

---

## 5. SẢN PHẨM ARTIFACTS KẾT XUẤT
1. [`.agents/skills/database-design/SKILL.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/.agents/skills/database-design/SKILL.md)
2. [`docs/database-design.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/docs/database-design.md)
3. Schema định nghĩa 14 models SQLAlchemy trong [`backend/app/models/`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/backend/app/models)

---

## 6. KIỂM CHỨNG & HIỆU CHỈNH CỦA CON NGƯỜI (HUMAN GATE 2)
* **Lỗi do AI đề xuất:** AI ban đầu định nghĩa quan hệ giữa Bệnh nhân và Phiếu khám bệnh là `ON DELETE CASCADE`. Điều này có nghĩa nếu một nhân viên lỡ tay xóa hồ sơ bệnh nhân, toàn bộ lịch sử bệnh án, kết quả cận lâm sàng và đơn thuốc điều trị của bệnh nhân đó sẽ bị xóa sạch theo.
* **Hành động hiệu chỉnh của Kỹ sư Con người:** Kỹ sư Trưởng đã can thiệp, chuyển toàn bộ các quan hệ dữ liệu lâm sàng sang `ON DELETE RESTRICT`, đồng thời yêu cầu thực thi cơ chế Soft Delete hoặc lưu trữ vĩnh viễn dữ liệu y tế theo quy định lưu trữ hồ sơ bệnh án tối thiểu 10 năm của Bộ Y tế.
