# Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp AI Hành chính
## (Clinic Management System with Administrative AI Assistant)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com)
[![React 18](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-5.0+-646CFF.svg)](https://vitejs.dev)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4+-38B2AC.svg)](https://tailwindcss.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🏥 Giới thiệu tổng quan (Project Overview)

**Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp AI Hành chính (CMS)** là giải pháp phần mềm quản trị phòng khám toàn diện, chuẩn y tế, kết hợp giữa mô hình phân quyền nghiêm ngặt (**RBAC - 4 nhóm người dùng**) và **Trợ lý AI Hành chính phân tầng bảo mật**.

Hệ thống được thiết kế theo tiêu chuẩn an toàn dữ liệu y tế: **Khử định danh PII tuyệt đối** (Họ tên, CCCD/CMND, Số điện thoại, Địa chỉ, Số thẻ BHYT) trước khi gửi tới các mô hình AI, có cơ chế **Fallback Mock Offline 100%** không phụ thuộc internet, và luôn đính kèm **Tuyên bố miễn trừ trách nhiệm y tế** theo quy định.

---

## 🏗️ Kiến trúc Hệ thống (System Architecture)

```
                                  +---------------------------------------+
                                  |     React 18 + Vite + Tailwind SPA    |
                                  |  (Role-based UI: Admin, Rec, Doc, Acc)|
                                  +-------------------+-------------------+
                                                      |
                                           REST API / JWT Token
                                                      |
                                                      v
+---------------------------------------------------------------------------------------------------+
|                                     FastAPI Backend Engine                                         |
|                                                                                                   |
|  +--------------------+  +--------------------+  +--------------------+  +--------------------+   |
|  |    RBAC Security   |  | Conflict Detection |  |   Clinical Flow    |  | Invoicing & Billing|   |
|  |  (4 Roles Isolation|  | (Doctor/Room Slot) |  | (Queue, EMR, Rx)   |  | (BHYT, QR, Receipt)|   |
|  +--------------------+  +--------------------+  +--------------------+  +--------------------+   |
|                                                                                                   |
|  +---------------------------------------------------------------------------------------------+  |
|  |                            Administrative AI Engine (Layered Security)                      |  |
|  |  +---------------------+   +---------------------+   +------------------------------------+ |  |
|  |  | Layer 1: Privacy    |-->| Layer 2: Guardrails |-->| Layer 3: Multi-Provider           | |  |
|  |  | (PII De-ident Regex)|   | (Disclaimer & Block)|   | (Mock Fallback / Ollama / Cloud)   | |  |
|  |  +---------------------+   +---------------------+   +------------------------------------+ |  |
|  +---------------------------------------------------------------------------------------------+  |
|                                                      |                                            |
|                                       SQLAlchemy 2.0 ORM & Audit Logs                             |
+------------------------------------------------------+--------------------------------------------+
                                                       |
                             +-------------------------+-------------------------+
                             |                                                   |
                             v                                                   v
             +-------------------------------+                   +-------------------------------+
             | SQLite (Local / Rapid Testing)|                   | PostgreSQL 16 (Docker Prod)   |
             +-------------------------------+                   +-------------------------------+
```

---

## 🔑 Danh sách Tài khoản & Phân quyền (Default User Credentials)

Hệ thống cung cấp sẵn bộ dữ liệu mẫu chuẩn y tế Việt Nam với đầy đủ 4 nhóm vai trò:

| # | Nhóm vai trò (Role) | Username | Mật khẩu mặc định | Họ và tên người dùng | Quyền hạn chính |
|---|---------------------|----------|-------------------|----------------------|-----------------|
| 1 | **Quản trị viên (Admin)** | `admin` | `admin123` | Quản trị viên Hệ thống | Quản lý người dùng, bác sĩ, danh mục thuốc, cấu hình phòng, Audit Logs, AI Logs, Thống kê |
| 2 | **Lễ tân (Receptionist)** | `receptionist` | `rec123` | Nguyễn Thị Thu Hà | Tiếp đón bệnh nhân, tạo hồ sơ y tế, đặt & điều phối lịch hẹn, phát số thứ tự, Tra cứu FAQ AI |
| 3 | **Kế toán (Accountant)** | `accountant` | `acc123` | Trần Bích Phương | Thu viện phí, quản lý hóa đơn, tính khấu trừ BHYT, xuất mã VietQR thanh toán, in hóa đơn |
| 4 | **Bác sĩ (Doctor - Tim mạch)** | `dr_nam` | `doc123` | BS.CKII Nguyễn Văn Nam | Khám bệnh, xem tóm tắt hồ sơ AI, kê đơn thuốc điện tử, sinh dặn dò xuất viện AI |
| 5 | **Bác sĩ (Doctor - Tiêu hóa)** | `dr_huong` | `doc123` | ThS.BS Lê Thu Hương | Khám tiêu hóa, chỉ định nội soi, kê đơn thuốc, sinh dặn dò xuất viện AI |
| 6 | **Bác sĩ (Doctor - Nhi khoa)** | `dr_minh` | `doc123` | BS.CKI Phạm Hoàng Minh | Tiếp nhận bệnh nhi, khám lâm sàng, theo dõi sinh hiệu, hướng dẫn chăm sóc |
| 7 | **Bác sĩ (Doctor - Tai Mũi Họng)** | `dr_lan` | `doc123` | BS Vũ Mai Lan | Khám TMH, chỉ định cận lâm sàng, kê đơn điều trị ngoại trú |

---

## ⚡ Hướng dẫn Khởi chạy nhanh (Quickstart Guide)

### Cách 1: Khởi chạy Cục bộ qua Script Windows (.bat) - Khuyên dùng

Yêu cầu: Đã cài đặt **Python 3.10+** và **Node.js 18+**.

1. **Khởi chạy toàn bộ hệ thống (Cả Backend & Frontend trong 2 cửa sổ):**
   ```cmd
   double-click vào file: run_all.bat
   ```
2. **Hoặc khởi chạy riêng lẻ từng dịch vụ:**
   - Chạy Backend (FastAPI tại `http://localhost:8000`):
     ```cmd
     run_backend.bat
     ```
   - Chạy Frontend (React Vite tại `http://localhost:5173`):
     ```cmd
     run_frontend.bat
     ```
   - Chạy toàn bộ Test Suite tự động (Pytest):
     ```cmd
     run_tests.bat
     ```

---

### Cách 2: Triển khai bằng Docker Compose (Production-ready)

Yêu cầu: Đã cài đặt **Docker Desktop** và **Docker Compose**.

1. **Sao chép cấu hình môi trường:**
   ```bash
   cp .env.example .env
   ```
2. **Khởi chạy toàn bộ cụm Container (Backend + Frontend + PostgreSQL + pgAdmin):**
   ```bash
   docker compose up --build -d
   ```
3. **Truy cập các dịch vụ:**
   - 🌐 **Frontend Web SPA**: [http://localhost:3000](http://localhost:3000)
   - 🔌 **Backend REST API**: [http://localhost:8000](http://localhost:8000)
   - 📖 **Swagger API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - 🐘 **pgAdmin 4 GUI**: [http://localhost:5050](http://localhost:5050) *(Tài khoản: `admin@phongkham.vn` / Mật khẩu: `admin123`)*

---

## 🧠 Tính năng Trợ lý AI Hành chính (Administrative AI Suite)

Hệ thống tích hợp 3 công cụ AI hành chính hỗ trợ bác sĩ và nhân viên y tế:

1. **AI Tóm tắt Hồ sơ Bệnh án (Pre-visit Briefing):**
   - Tự động trích xuất các thông tin then chốt: Tiền sử bệnh, danh sách dị ứng thuốc nghiêm trọng, các đợt khám và đơn thuốc gần nhất.
   - Giúp bác sĩ nắm bắt tình trạng bệnh nhân chỉ trong 30 giây trước khi bắt đầu phiên khám.

2. **Chatbot Tư vấn Quy trình Phòng khám (Clinic Workflow FAQ Chatbot):**
   - Trả lời nhanh chóng và chính xác các quy trình hành chính: Thủ tục chuyển tuyến BHYT, bảng giá dịch vụ, lịch làm việc, quy định đặt lịch.
   - Tự động phát hiện và **chặn mọi câu hỏi yêu cầu chẩn đoán/kê đơn bệnh học**.

3. **AI Sinh Hướng dẫn Sau khám & Nhắc Tái khám (Post-visit Discharge Instructions):**
   - Dựa trên kết luận khám và đơn thuốc của bác sĩ, AI tự động tạo văn bản dặn dò song ngữ/dễ hiểu cho người bệnh về: Lịch uống thuốc, chế độ kiêng cữ dinh dưỡng, dấu hiệu bất thường cần tái khám khẩn cấp.

---

## 📚 Tài liệu Minh chứng 4 Giai đoạn SDLC (SDLC Deliverables)

Toàn bộ tài liệu phân tích, đặc tả, thiết kế, kiểm thử và hướng dẫn vận hành chi tiết được lưu trữ tại thư mục `docs/`:

- 📄 [`docs/SDLC_GiaiDoan1_PhanTich_ThietKe.md`](docs/SDLC_GiaiDoan1_PhanTich_ThietKe.md): **KT1 - Khảo sát bài toán, Phân tích 4 Actor, Biểu đồ Use Case, ERD 14 bảng quan hệ & Ranh giới Đạo đức AI**.
- 📄 [`docs/SDLC_GiaiDoan2_ChucNang_QuanLy.md`](docs/SDLC_GiaiDoan2_ChucNang_QuanLy.md): **KT2 - Kiến trúc Backend & Frontend, Ma trận Phân quyền RBAC, Thuật toán Kiểm tra Xung đột Lịch & Đặc tả RESTful API**.
- 📄 [`docs/SDLC_GiaiDoan3_TichHopAI_TestAI.md`](docs/SDLC_GiaiDoan3_TichHopAI_TestAI.md): **KT3 - Kiến trúc Phân lớp AI, Khử định danh PII (Regex/Token), Kỹ thuật Prompt Engineering, Multi-Provider & Ma trận Kiểm thử AI**.
- 📄 [`docs/SDLC_GiaiDoan4_BaoCao_HuongDan_TrienKhai.md`](docs/SDLC_GiaiDoan4_BaoCao_HuongDan_TrienKhai.md): **Cuối kỳ - Báo cáo An toàn Bảo mật, Hướng dẫn Triển khai Docker, Sổ tay Người dùng 4 vai trò & Kịch bản Demo 8 bước chấm điểm**.

---

## 🧪 Kiểm thử Tự động (Automated Pytest Suite)

Hệ thống đạt **100% tỷ lệ vượt qua (Pass Rate)** trên toàn bộ các bộ kiểm thử:

```bash
# Chạy toàn bộ test suite
pytest backend/tests -v

# Kết quả kiểm thử các module:
# - test_rbac.py             : Kiểm tra cô lập phân quyền 4 vai trò
# - test_appointments.py     : Kiểm tra thuật toán phát hiện xung đột lịch khám
# - test_pii_anonymizer.py   : Kiểm tra khử định danh CCCD, SĐT, BHYT, Tên
# - test_ai_features.py      : Kiểm tra 3 tính năng AI, Guardrails, Fallback
# - test_clinical_flow.py    : Kiểm tra chu trình khám, kê đơn, thanh toán
# - test_e2e_scenarios.py    : Kịch bản tích hợp liên phòng ban End-to-End
```

---

## 📜 Giấy phép & Bản quyền (License)

Dự án được phát hành dưới giấy phép mã nguồn mở **MIT License**.
Phát triển phục vụ Đồ án Học phần: **Ứng dụng Trí tuệ Nhân tạo - ICTU 2026-2027**.
#   H e _ t h o n g _ q u a n _ l y _ p h o n g _ k h a m  
 