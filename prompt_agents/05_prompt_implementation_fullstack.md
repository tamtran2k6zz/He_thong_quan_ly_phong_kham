# PROMPT GIAO VIỆC: LẬP TRÌNH SẠCH FULLSTACK FASTAPI & REACT SPA
## Giai đoạn SDLC: Giai đoạn 2 – Core Implementation (KT2)
### Kỹ năng áp dụng: `.agents/skills/implementation/SKILL.md`

---

## 1. THÔNG TIN NGỮ CẢNH & MỤC TIÊU
* **Dự án:** Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp Trợ lý AI Hành chính (CMS-AI).
* **Đơn vị thực hiện:** Nhóm 07 (Đinh Gia Bảo - Trưởng nhóm, Trần Đặng Công Tâm).
* **Mục tiêu:** Xây dựng toàn diện mã nguồn Backend (FastAPI, SQLAlchemy, Pydantic v2, JWT RBAC) và Frontend (React 18 SPA, Vite, Tailwind CSS, Lucide Icons), tích hợp sẵn bộ dữ liệu mẫu (Seed Data) chuẩn phòng khám Việt Nam và đóng gói môi trường Docker Compose.

---

## 2. VAI TRÒ CỦA AI AGENT (PERSONA)
Bạn là **Lead Fullstack Healthcare Software Engineer Agent (Kỹ sư Trưởng Lập trình Fullstack Y tế)**, chuyên gia lập trình sạch (Clean Code, SOLID principles, PEP 8), có kinh nghiệm sâu sắc về xây dựng SPA y tế thẩm mỹ cao, không lỗi giao diện, tối ưu hóa giao dịch CSDL nguyên tử (Atomic Transactions).

---

## 3. RÀNG BUỘC KỸ THUẬT & QUY TẮC CỐT LÕI (GUARDRAILS)
1. **Pydantic v2 Validation:** 100% Request và Response schemas phải định nghĩa rõ ràng kiểu dữ liệu, thông điệp lỗi tiếng Việt thân thiện, không bao giờ để lộ lỗi 500 unhandled.
2. **RFC 7807 Error Handling:** Toàn bộ ngoại lệ API phải được bọc theo chuẩn Problem Details (`type`, `title`, `status`, `detail`).
3. **Bảo vệ Giao dịch Viện phí:** Các thao tác thanh toán hóa đơn, trừ kho dược, khóa phiếu khám bắt buộc phải nằm trong một transaction duy nhất (`db.commit()`), tự động rollback khi phát sinh lỗi.
4. **Không hardcode Secrets:** Tuyệt đối không hardcode API key, Secret key trong mã nguồn; bắt buộc đọc qua file `.env`.
5. **Giao diện Clinical UI Precision:** Màu sắc theo quy chuẩn y tế (Xanh Cyan `#007A8C`, Slate, Trắng ngà), không dùng hiệu ứng hoạt họa lố lăng (Anti AI-slop).

---

## 4. NỘI DUNG MASTER PROMPT ĐÃ GIAO CHO AI AGENT

```markdown
Bạn hãy đóng vai trò là Lead Fullstack Healthcare Engineer. Hãy hiện thực hóa toàn diện mã nguồn phần mềm cho dự án CMS-AI của Nhóm 07:

BƯỚC 1: XÂY DỰNG SKILL LẬP TRÌNH SẠCH (.agents/skills/implementation/SKILL.md)
Tạo file SKILL.md định nghĩa quy chuẩn code clean, cấu trúc thư mục backend/frontend, quy định xử lý lỗi RFC 7807, quy chuẩn Pydantic v2 và quy trình thẩm định mã nguồn trước khi tích hợp.

BƯỚC 2: HIỆN THỰC HÓA BACKEND FASTAPI (backend/app/)
1. Cấu hình hệ thống & Security:
   - `backend/app/config.py`: Đọc cấu hình từ `.env`, hỗ trợ Gemini, OpenAI, Ollama và Mock AI.
   - `backend/app/database.py`: Kết nối SQLite/MySQL, session factory, event listener bật foreign keys.
   - `backend/app/core/security.py`: Băm bcrypt, tạo và giải mã JWT token.
   - `backend/app/core/rbac.py`: Dependency `require_roles([RoleEnum...])` kiểm soát phân quyền 4 vai trò.
   - `backend/app/core/conflict_checker.py`: Hiện thực giải thuật kiểm tra trùng lịch khám 2 chiều.
2. Data Models & Schemas:
   - 14 models SQLAlchemy trong `backend/app/models/` (User, Patient, Doctor, Shift, Appointment, MedicalRecord, Medicine, Invoice...).
   - Pydantic v2 schemas tương ứng trong `backend/app/schemas/`.
3. REST API Routers (`backend/app/api/v1/`):
   - `auth.py`: Đăng nhập, lấy thông tin cá nhân `me`.
   - `patients.py`: CRUD hồ sơ bệnh nhân, tìm kiếm theo tên/CCCD/SĐT.
   - `doctors.py`: Danh mục bác sĩ, chuyên khoa, ca làm việc.
   - `appointments.py`: Đặt lịch, đổi lịch, hủy lịch, check-in.
   - `medical_records.py`: Khám lâm sàng, chỉ định CLS, kê đơn thuốc, hoàn tất ca khám.
   - `medicines.py`: Quản lý kho dược, trừ kho thuốc.
   - `invoices.py`: Lập hóa đơn, tính giảm trừ BHYT, sinh link VietQR động, thanh toán.
   - `stats.py`: Thống kê lượt khám, doanh thu theo ngày/tháng.
   - `ai.py`: 3 endpoints AI Hành chính (Pre-visit, FAQ Chatbot, Discharge).
4. Dữ liệu mẫu (Seed Data):
   - `backend/app/seed/seed_data.py`: Tự động nạp 7 tài khoản nhân viên (Admin, Lễ tân, Thu ngân, 4 Bác sĩ), 6 chuyên khoa, 6 buồng khám, 28 loại thuốc, 10 bệnh nhân mẫu, lịch hẹn và hóa đơn mẫu.

BƯỚC 3: HIỆN THỰC HÓA FRONTEND REACT SPA (frontend/src/)
1. Cấu trúc giao diện phân quyền 4 vai trò:
   - Lễ tân: Tiếp đón nhanh, đặt lịch hẹn trực quan Calendar, check-in, Chatbot FAQ.
   - Bác sĩ: Hàng đợi chờ khám (Queue), xem tóm tắt AI Pre-visit, khám lâm sàng ICD-10, kê đơn có cảnh báo dị ứng thuốc, sinh dặn dò xuất viện AI.
   - Thu ngân: Danh sách hóa đơn chờ, tính tiền BHYT, hiển thị mã VietQR động để quét Mobile Banking, in phiếu thu.
   - Admin: Dashboard biểu đồ thống kê, quản trị nhân sự, giám sát Audit logs và AI invocation logs.
2. Thiết kế Clinical Precision UI với Tailwind CSS, icon Lucide React và font chữ Tabular Figures cho bảng số liệu viện phí.

BƯỚC 4: ĐÓNG GÓI DOCKER COMPOSE & SCRIPTS KHỞI CHẠY
Tạo `docker-compose.yml` (MySQL 8.0, Backend FastAPI, Frontend Nginx) và các file batch chạy nhanh trên Windows (`run_backend.bat`, `run_frontend.bat`, `run_all.bat`).
```

---

## 5. SẢN PHẨM ARTIFACTS KẾT XUẤT
1. [`.agents/skills/implementation/SKILL.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/.agents/skills/implementation/SKILL.md)
2. Mã nguồn toàn diện Backend trong [`backend/app/`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/backend/app)
3. Mã nguồn toàn diện Frontend trong [`frontend/src/`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/frontend/src)
4. Bộ nạp dữ liệu mẫu [`backend/app/seed/seed_data.py`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/backend/app/seed/seed_data.py)
5. Cấu hình triển khai [`docker-compose.yml`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/docker-compose.yml)

---

## 6. KIỂM CHỨNG & HIỆU CHỈNH CỦA CON NGƯỜI (HUMAN GATE 2)
* **Lỗi do AI đề xuất:** AI ban đầu viết logic xuất kho thuốc trong đơn thuốc thành các câu lệnh riêng biệt không dùng `with db.begin():`, khiến nếu một loại thuốc bị lỗi hoặc đứt kết nối mạng thì các thuốc trước đó vẫn bị trừ kho oan uổng.
* **Hành động hiệu chỉnh của Kỹ sư Con người:** Kỹ sư Trưởng đã yêu cầu tái cấu trúc toàn bộ việc kê đơn và xuất kho thành một transaction nguyên tử duy nhất; nếu có bất kỳ lỗi tồn kho nào, hệ thống lập tức rollback 100% trạng thái kho về ban đầu.
