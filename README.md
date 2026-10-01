# 🏥 Hệ Thống Quản Lý Phòng Khám Đa Khoa Thông Minh Tích Hợp AI Hành Chính
### 🌟 *Smart Clinic Management System with Administrative AI Assistant (AI-Augmented SDLC)*

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React" />
  <img src="https://img.shields.io/badge/TailwindCSS-3.4+-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind" />
  <img src="https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL" />
  <img src="https://img.shields.io/badge/Google_Gemini-Live_3.6-8E75B2?style=for-the-badge&logo=google&logoColor=white" alt="Gemini" />
  <img src="https://img.shields.io/badge/Tests-319_Passed_100%25-22C55E?style=for-the-badge&logo=pytest&logoColor=white" alt="Pytest" />
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
</p>

---

## 👥 Nhóm Thực Hiện Đề Tài: Nhóm 07
* 👨‍💻 **Đinh Gia Bảo** – **Trưởng nhóm** ([@dtc245220019-create](https://github.com/dtc245220019-create))
* 👨‍💻 **Trần Đặng Công Tâm** – Thành viên ([@tamtran2k6zz](https://github.com/tamtran2k6zz))
* 🎓 **Học phần:** Ứng dụng Trí tuệ Nhân tạo trong Kỹ thuật Phần mềm (ICTU 2026-2027)
* ⏱️ **Thời gian thực hiện:** 27/07/2026 – 27/09/2026 (9 tuần)

---

## 📖 Lời Giới Thiệu

Chào mừng bạn đến với **Hệ thống Quản lý Phòng khám Đa khoa Thông minh (Smart Clinic CMS-AI)**! 

Trong bối cảnh các phòng khám tư nhân thường gặp khó khăn vì quy trình tiếp đón rời rạc, dễ xảy ra tình trạng trùng lịch bác sĩ, mất thời gian tra cứu bệnh sử cũ và quá tải thủ tục hành chính, dự án này ra đời như một **giải pháp số hóa toàn diện, chuẩn y tế và an toàn tuyệt đối**.

Hệ thống kết hợp hài hòa giữa:
1. **Nghiệp vụ phòng khám chuẩn mực**: Quản lý bệnh nhân, điều phối lịch hẹn thông minh (thuật toán kiểm tra giao thoa thời gian thực chống trùng lịch 100%), bàn khám điện tử EMR, kê đơn thuốc và thanh toán viện phí tích hợp BHYT / VietQR động Napas247.
2. **Trợ lý AI Hành chính 3 lớp bảo vệ**: Ứng dụng mô hình ngôn ngữ lớn thời gian thực (**Google Gemini 3.6 Flash / OpenAI / Ollama**) để giải đáp quy trình, tóm tắt hồ sơ bệnh án 10 giây và sinh dặn dò sau khám — **tuyệt đối không tự ý chẩn đoán bệnh học hay thay thế bác sĩ**.
3. **Mô hình thực hành AI-Augmented SDLC**: Toàn bộ quá trình phát triển được điều phối qua **15 bộ Kỹ năng (Skills)**, **Tools**, **MCP**, hệ thống **16 Master Prompts** cho AI Agent (`prompt_agents/`) và các cổng kiểm soát chất lượng của con người (**Human Gates 1, 2, 3**).

---

## 🌈 Điểm Nổi Bật Của Hệ Thống

```
                     +-------------------------------------------------------------+
                     |                PHÒNG KHÁM ĐA KHOA THÔNG MINH                |
                     +------------------------------+------------------------------+
                                                    |
       +--------------------+-----------------------+-----------------------+--------------------+
       |                    |                                               |                    |
+------v------+      +------v------+                                 +------v------+      +------v------+
|   LỄ TÂN    |      |   BÁC SĨ    |                                 |   KẾ TOÁN   |      |  QUẢN TRỊ   |
| Tiếp đón    |      | Hàng đợi EMR|                                 | Viện phí    |      | Báo cáo thu |
| Hẹn khám    |      | Khám bệnh   |                                 | Khấu trừ    |      | Phân ca trực|
| Chống trùng |      | Kê đơn điện |                                 | BHYT        |      | Danh mục    |
| lịch 100%   |      | tử & Cảnh   |                                 | VietQR động |      | Audit Logs  |
| Chatbot FAQ |      | báo dị ứng  |                                 | In hóa đơn  |      | AI Logs     |
+------+------+      +------+------+                                 +------+------+      +------+------+
       |                    |                                               |                    |
       +--------------------+-----------------------+-----------------------+--------------------+
                                                    |
                                  +-----------------v-----------------+
                                  | 🛡️ ADMINISTRATIVE AI ENGINE       |
                                  | 1. Khử PII: CCCD, SĐT, BHYT, Tên  |
                                  | 2. Medical Guardrails & Cảnh báo  |
                                  | 3. Multi-Provider & Mock Fallback |
                                  +-----------------------------------+
```

### 1. 🗓️ Đặt Lịch Hẹn & Thuật Toán Chống Trùng Lịch Tuyệt Đối
- Giao diện lịch biểu trực quan theo ngày/tuần (Calendar View).
- Tự động phát hiện và chặn đứng xung đột thời gian của bác sĩ và phòng khám trước khi lưu vào cơ sở dữ liệu theo công thức toán học: `(Start_A < End_B) and (End_A > Start_B)`.
- Hỗ trợ bệnh nhân đăng ký tài khoản trực tuyến và đặt lịch hẹn khám từ xa.

### 2. 🩺 Bàn Khám Bệnh EMR Lâm Sàng Dành Cho Bác Sĩ
- **Hàng đợi bệnh nhân trực quan**: Theo dõi thời gian thực ai đang chờ, ai đang khám.
- **Thước đo sinh hiệu & Tính BMI tự động**: Tự động tính chỉ số khối cơ thể và cảnh báo theo chuẩn người Châu Á.
- **Tra cứu danh mục ICD-10**: Tìm kiếm mã bệnh quốc tế nhanh chóng theo nhóm bệnh.
- **Kê đơn thuốc thông minh**: Tự động kiểm tra số lượng tồn kho và **cảnh báo đỏ ngay lập tức nếu thuốc trùng với tiền sử dị ứng** của người bệnh.

### 3. 🤖 Bộ 3 Trợ Lý AI Hành Chính (Google Gemini 3.6 Flash / Offline Mock)
- 📋 **AI Tóm tắt bệnh án (Pre-visit Briefing)**: Trích xuất nhanh các lần khám trước, bệnh nền và cảnh báo dị ứng giúp Bác sĩ nắm bắt bệnh sử chỉ trong 10 giây.
- 💬 **Chatbot tư vấn quy trình (Clinic FAQ)**: Hướng dẫn người bệnh về bảng giá, giờ làm việc, thủ tục BHYT. Tích hợp bộ lọc kiên quyết từ chối chẩn đoán bệnh học hoặc kê đơn thuốc.
- 💊 **AI Sinh hướng dẫn sau khám (Discharge Generator)**: Tự động tạo bản dặn dò dễ hiểu: bảng phân chia lịch uống thuốc 4 bữa, chế độ ăn uống kiêng cữ, dấu hiệu nguy hiểm cần tái khám ngay.
- 🔌 **Cơ chế Fallback Ngoại tuyến**: Tích hợp sẵn `DeterministicMockAIService` cho phép toàn bộ tính năng AI hoạt động 100% mượt mà ngay cả khi mất kết nối mạng.

### 4. 💳 Quản Lý Viện Phí, BHYT & Thanh Toán VietQR
- Tự động tổng hợp chi phí khám, xét nghiệm cận lâm sàng và tiền thuốc.
- Hỗ trợ khấu trừ BHYT đúng tuyến/trái tuyến (80% - 100%).
- Tạo mã **VietQR động** có sẵn số tiền và nội dung chuyển khoản Napas247; hỗ trợ in hóa đơn chuẩn y tế.

### 5. 🔒 An Toàn Dữ Liệu Y Tế & Khử Định Danh PII (Nghị định 13/2023/NĐ-CP)
- Tự động ẩn danh hóa các thông tin nhạy cảm (Họ tên, CCCD/CMND, Số điện thoại, Địa chỉ, Thẻ BHYT) trước khi gửi đến mô hình AI.
- Mọi kết quả từ AI đều được gắn kèm **Tuyên bố miễn trừ trách nhiệm y tế** (`Medical Disclaimer`).
- Lưu trữ đầy đủ **Audit Log** (nhật ký truy cập bệnh án) và **AI Invocation Log** (lịch sử gọi AI, độ trễ, prompt đã khử PII).

---

## 🏗️ Kiến Trúc Công Nghệ Hiện Đại

| Tầng Ứng Dụng | Công Nghệ Sử Dụng | Mục Đích & Vai Trò |
| :--- | :--- | :--- |
| **Giao Diện (Frontend)** | React 18 SPA, Vite 5, Tailwind CSS 3, Lucide Icons | Giao diện công thái học lâm sàng chuẩn **Taste-Skill**, font chữ 3 tầng (*Plus Jakarta Sans / Inter / JetBrains Mono*), bảng số liệu Tabular Figures rõ nét. |
| **Dịch Vụ (Backend)** | Python 3.10+, FastAPI, Pydantic v2, SQLAlchemy 2.0 | Xử lý bất đồng bộ (Async), hiệu năng cao, tài liệu API tự động qua Swagger UI, xử lý lỗi chuẩn RFC 7807 Problem Details. |
| **Cơ Sở Dữ Liệu** | MySQL 8.0 (Docker Port 3307) / SQLite Fallback | Thiết kế 14 bảng quan hệ chuẩn hóa 3NF, ràng buộc khóa ngoại chặt chẽ, đánh chỉ mục Composite Index tối ưu truy vấn xung đột lịch hẹn. |
| **Mô Hình AI** | Google Gemini Live (`gemini-3.6-flash`), OpenAI, Ollama, Mock | Phản hồi thông minh thời gian thực bằng tiếng Việt tự nhiên, có chế độ Mock Offline dự phòng khi mất mạng. |
| **Đóng Gói & Môi Trường** | Docker, Docker Compose, Nginx Alpine | Triển khai 1 câu lệnh toàn bộ hệ sinh thái dịch vụ. |

---

## ⚡ Hướng Dẫn Cài Đặt & Khởi Chạy Nhanh

Bạn có thể lựa chọn 1 trong 2 cách khởi chạy dưới đây tùy theo môi trường máy của mình:

### Cách 1: Khởi chạy bằng Docker Compose (Khuyên dùng - Nhanh nhất)

> **Yêu cầu:** Đã cài đặt [Docker Desktop](https://www.docker.com/products/docker-desktop/) và đang bật Docker Engine.

```bash
# 1. Clone dự án về máy
git clone https://github.com/tamtran2k6zz/He_thong_quan_ly_phong_kham.git
cd He_thong_quan_ly_phong_kham

# 2. Khởi chạy toàn bộ hệ thống bằng 1 lệnh duy nhất
docker compose up -d --build
```

Sau khi khởi chạy thành công, bạn mở trình duyệt và truy cập:
- 🌐 **Giao diện Web Phòng khám:** **[http://localhost:3001](http://localhost:3001)** hoặc **[http://localhost:5173](http://localhost:5173)**
- 📚 **Tài liệu Backend API (Swagger UI):** **[http://localhost:8000/docs](http://localhost:8000/docs)**
- 🗄️ **Cơ sở dữ liệu MySQL:** `127.0.0.1:3307` (User: `clinic_user` | Pass: `clinic_password123` | DB: `clinic_db`)

---

### Cách 2: Khởi chạy cục bộ trên Windows (Local Development)

> **Yêu cầu:** Đã cài đặt [Python 3.10+](https://www.python.org/) và [Node.js 18+](https://nodejs.org/).

Chỉ cần nhấp đúp chuột vào file batch script có sẵn trong thư mục dự án:
```cmd
# Cách tiện lợi nhất: Khởi động cả Backend & Frontend trong 2 cửa sổ
double-click: run_all.bat

# Hoặc khởi chạy từng phần riêng biệt:
run_backend.bat     # Khởi chạy FastAPI Backend tại http://localhost:8000
run_frontend.bat    # Khởi chạy React Vite Frontend tại http://localhost:3001 hoặc http://localhost:5173
run_tests.bat       # Chạy toàn bộ 319+ bài kiểm thử tự động
```

---

## 👥 Danh Sách Tài Khoản Trải Nghiệm 4 Vai Trò

Hệ thống đã nạp sẵn bộ dữ liệu mẫu y tế đầy đủ. Bạn có thể đăng nhập bằng các tài khoản sau để trải nghiệm từng góc nhìn nghiệp vụ:

| Vai Trò | Tên Đăng Nhập | Mật Khẩu | Họ Và Tên | Trải Nghiệm Nghiệp Vụ Chính |
| :--- | :--- | :--- | :--- | :--- |
| 👑 **Quản Trị Viên (Admin)** | `admin` | `admin123` | Quản trị viên Hệ thống | Xem bảng thống kê doanh thu, phân ca trực bác sĩ, quản lý danh mục thuốc, xem Audit Logs & nhật ký AI. |
| 👩‍💼 **Lễ Tân (Receptionist)** | `receptionist` | `rec123` | Nguyễn Thị Thu Hà | Đón tiếp bệnh nhân, cấp mã hồ sơ y tế, đặt & đổi lịch hẹn khám (kiểm tra trùng lịch), tra cứu Chatbot AI. |
| 👨‍⚕️ **Bác Sĩ (Doctor)** | `dr_nam` | `doc123` | BS.CKII Nguyễn Văn Nam | Xem tóm tắt bệnh sử AI 10 giây, khám lâm sàng, chọn ICD-10, kê đơn thuốc cảnh báo dị ứng và sinh dặn dò AI. |
| 👨‍⚕️ **Bác Sĩ Nhi Khoa** | `dr_huong` | `doc123` | ThS.BS Lê Thu Hương | Khám chuyên khoa nhi, kê đơn thuốc và theo dõi bệnh nhi. |
| 💰 **Kế Toán / Thu Ngân** | `accountant` | `acc123` | Trần Bích Phương | Quản lý danh sách viện phí, khấu trừ BHYT, tạo mã VietQR thanh toán tự động, xuất & in phiếu thu. |

> 💡 **Khách hàng / Bệnh nhân mới:** Có thể trực tiếp bấm nút **"Đăng ký tài khoản"** trên màn hình đăng nhập để tạo hồ sơ khám bệnh cá nhân và đặt lịch hẹn khám trực tuyến.

---

## 🎯 Kịch Bản 8 Bước Trải Nghiệm Hệ Thống (Demo Flow)

Để có cái nhìn tổng thể và liền mạch nhất về hệ thống, bạn có thể thực hiện theo quy trình khám chữa bệnh thực tế:

```
[Bước 1: Tiếp đón]  --> [Bước 2: Đặt lịch] --> [Bước 3: Điều phối] --> [Bước 4: Xem AI Pre-visit]
(Lễ tân đăng ký)       (Chọn bác sĩ & giờ)   (Đưa vào hàng đợi)      (Bác sĩ đọc tóm tắt)
                                                                               |
[Bước 8: Báo cáo]   <-- [Bước 7: Thu tiền] <-- [Bước 6: AI Dặn dò] <-- [Bước 5: Khám & Kê đơn]
(Admin xem thống kê)    (Kế toán quét QR)     (Sinh phiếu dặn dò)    (Chẩn đoán ICD-10)
```

1. **Bước 1 (Lễ tân):** Đăng nhập tài khoản `receptionist` / `rec123`, tiếp đón bệnh nhân mới hoặc tìm kiếm hồ sơ bệnh nhân cũ theo SĐT / CCCD.
2. **Bước 2 (Lễ tân):** Đặt lịch khám tại chuyên khoa Tim mạch cho BS. Nguyễn Văn Nam (thử chọn giờ trùng ca khác để thấy hệ thống lập tức cảnh báo đỏ 409 Conflict).
3. **Bước 3 (Lễ tân):** Bấm nút Check-in để chuyển trạng thái bệnh nhân sang hàng đợi khám bệnh của bác sĩ.
4. **Bước 4 (Bác sĩ):** Đăng nhập tài khoản `dr_nam` / `doc123`, mở bàn khám và đọc thẻ **AI Pre-visit Briefing** để nắm nhanh tiền sử dị ứng thuốc và bệnh lý nền chỉ trong 10 giây.
5. **Bước 5 (Bác sĩ):** Nhập sinh hiệu (huyết áp, nhịp tim, thân nhiệt - hệ thống tự tính BMI), chọn chẩn đoán ICD-10 (`J06.9`), chỉ định xét nghiệm và kê đơn thuốc (thử chọn thuốc nhóm Penicillin để kiểm tra cảnh báo dị ứng thời gian thực).
6. **Bước 6 (Bác sĩ):** Bấm nút **"Sinh hướng dẫn sau khám bằng AI"** để tự động tạo bảng phân chia lịch uống thuốc 4 bữa và chế độ dinh dưỡng dặn dò người bệnh. Hoàn tất phiếu khám.
7. **Bước 7 (Kế toán):** Đăng nhập tài khoản `accountant` / `acc123`, mở hóa đơn vừa được chuyển sang, áp dụng mức hưởng BHYT (80%), hiển thị mã **VietQR** động và in phiếu thu viện phí.
8. **Bước 8 (Admin):** Đăng nhập tài khoản `admin` / `admin123`, xem biểu đồ phân tích lượt khám, doanh thu theo chuyên khoa và kiểm tra **Audit Logs** cùng **AI Invocation Logs**.

---

## 🧩 Hệ Sinh Thái 15 Skills Chuẩn AI-Augmented SDLC

Dự án được xây dựng và quản trị theo triết lý **AI-Augmented SDLC**, biến AI từ một công cụ sinh code thông thường thành một **AI Agent có quy trình, tiêu chuẩn và kiểm soát chặt chẽ**:

```text
.agents/skills/
├── 📘 requirements-analysis/SKILL.md   # Phân tích yêu cầu nghiệp vụ y tế & 27 User Stories
├── 🏛️ architecture-design/SKILL.md     # Thiết kế kiến trúc phân tầng & Vành đai AI 3 lớp
├── 🗄️ database-design/SKILL.md         # Thiết kế CSDL 14 bảng quan hệ 3NF & Composite Indexes
├── 📊 diagram-design/SKILL.md          # Thiết kế biểu đồ UML (Use Case, Class, Sequence, Activity, State)
├── 💻 implementation/SKILL.md          # Quy chuẩn Clean Code, PEP 8, Pydantic v2 & RFC 7807
├── 🧪 testing/SKILL.md                 # Chiến lược kiểm thử đa tầng (319+ test cases pass 100%)
├── 🔍 code-review/SKILL.md             # Kiểm toán chất lượng mã nguồn & phân quyền RBAC
├── 🛡️ security-review/SKILL.md         # Kiểm toán an ninh dữ liệu y tế OWASP & Nghị định 13
├── 📝 documentation/SKILL.md           # Quy chuẩn biên soạn tài liệu SDLC 4 giai đoạn
├── 🔒 pii-deidentification/SKILL.md    # Khử định danh CCCD, SĐT, BHYT, Tên người bệnh
├── 📋 pre-visit-briefing/SKILL.md      # Tóm tắt tiền sử bệnh án 10 giây và cảnh báo dị ứng thuốc
├── 💬 clinic-faq-rag/SKILL.md          # Chatbot hỏi đáp thủ tục phòng khám & Guardrail y tế
├── 💊 discharge-instructions/SKILL.md  # Sinh hướng dẫn dặn dò sau khám & bảng lịch uống thuốc
├── 🎨 design-taste-frontend/SKILL.md   # Chuẩn thiết kế giao diện lâm sàng công thái học chống AI-slop
└── ✍️ professional-writing/SKILL.md    # Chuẩn hóa văn phong kỹ thuật học thuật, loại bỏ từ ngữ sáo rỗng
```

---

## 🤖 Thư Mục Master Prompts Giao Việc Cho AI Agent (`prompt_agents/`)

Đáp ứng **Tiêu chí Đánh giá số 2 (Prompt/task đã giao cho Codex/AI Agent)** trong mô hình thực hành AI-Augmented SDLC, thư mục [`prompt_agents/`](prompt_agents/) lưu trữ trọn bộ 16 file prompt chuẩn mực:

| File Prompt | Nội Dung Nhiệm Vụ Giao Cho AI Agent | Giai Đoạn SDLC & Human Gate |
| :--- | :--- | :---: |
| [`00_README_PROMPT_AGENTS_INDEX.md`](prompt_agents/00_README_PROMPT_AGENTS_INDEX.md) | Tổng mục lục hệ thống prompts, mô hình 4 trụ cột và ma trận ánh xạ | Tổng quan |
| [`01_prompt_requirements_analysis.md`](prompt_agents/01_prompt_requirements_analysis.md) | Phân tích 5 điểm nghẽn, đặc tả 38 FR, 10 NFR, 27 User Stories | KT1 / Human Gate 1 |
| [`02_prompt_architecture_design.md`](prompt_agents/02_prompt_architecture_design.md) | Thiết kế kiến trúc 5 tầng, Vành đai AI 3 lớp, 5 hồ sơ ADR | KT1 / Human Gate 2 |
| [`03_prompt_database_design.md`](prompt_agents/03_prompt_database_design.md) | Thiết kế CSDL 14 bảng quan hệ 3NF, Composite Indexes xung đột lịch | KT1 / Human Gate 2 |
| [`04_prompt_diagram_design.md`](prompt_agents/04_prompt_diagram_design.md) | Mô hình hóa UML 2.5: Use Case, Class OOD 10 lớp, 5 Sequence, Activity | KT1 & KT2 |
| [`05_prompt_implementation_fullstack.md`](prompt_agents/05_prompt_implementation_fullstack.md) | Hiện thực hóa FastAPI Backend, React SPA Frontend, Seed data, Docker | KT2 / Human Gate 2 |
| [`06_prompt_pii_deidentification.md`](prompt_agents/06_prompt_pii_deidentification.md) | Xây dựng module `PIIAnonymizer` khử sạch CCCD, SĐT, BHYT theo Nghị định 13 | KT3 / Human Gate 3 |
| [`07_prompt_pre_visit_briefing.md`](prompt_agents/07_prompt_pre_visit_briefing.md) | Phát triển tính năng tóm tắt bệnh án 10 giây, làm nổi bật cảnh báo dị ứng | KT3 / Human Gate 3 |
| [`08_prompt_clinic_faq_rag.md`](prompt_agents/08_prompt_clinic_faq_rag.md) | Xây dựng FAQ Chatbot RAG, bộ lọc Guardrails chặn câu hỏi chẩn đoán | KT3 / Human Gate 1 & 3 |
| [`09_prompt_discharge_instructions.md`](prompt_agents/09_prompt_discharge_instructions.md) | Phát triển tính năng sinh dặn dò xuất viện, bảng lịch uống thuốc 4 bữa | KT3 / Human Gate 3 |
| [`10_prompt_design_taste_frontend.md`](prompt_agents/10_prompt_design_taste_frontend.md) | Thiết kế Design Tokens lâm sàng, Typography Tabular figures, Anti-AI-slop | KT2 / Human Gate 2 |
| [`11_prompt_testing_automation.md`](prompt_agents/11_prompt_testing_automation.md) | Thiết kế Test Plan, Test Report và bộ 319+ test cases Pytest pass 100% | KT4 / Human Gate 2 |
| [`12_prompt_code_review.md`](prompt_agents/12_prompt_code_review.md) | Kiểm toán mã nguồn đa chiều, phân loại rủi ro CRITICAL/HIGH/MEDIUM/LOW | KT2 & KT4 |
| [`13_prompt_security_review.md`](prompt_agents/13_prompt_security_review.md) | Kiểm toán an ninh thông tin OWASP Top 10 và thử nghiệm AI Red Teaming | KT4 / Human Gate 2 & 3 |
| [`14_prompt_documentation_sdlc_reports.md`](prompt_agents/14_prompt_documentation_sdlc_reports.md) | Biên soạn bộ tài liệu minh chứng 4 giai đoạn SDLC và báo cáo tổng kết AI | KT4 / Human Gate 1..3 |
| [`15_prompt_professional_writing.md`](prompt_agents/15_prompt_professional_writing.md) | Quy chuẩn viết tài liệu kỹ thuật chuyên nghiệp, loại bỏ từ ngữ sáo rỗng | Xuyên suốt |

---

## 📁 Trọn Bộ Hồ Sơ Minh Chứng Kỹ Thuật (`docs/`)

Toàn bộ các tài liệu phân tích, đặc tả, thiết kế, báo cáo kiểm thử và sổ tay vận hành được lưu trữ chuyên nghiệp trong thư mục `docs/`:

| STT | Tài Liệu Kỹ Thuật | Nội Dung & Mục Đích Minh Chứng |
| :---: | :--- | :--- |
| 1 | [`docs/customer-requirement.md`](docs/customer-requirement.md) | Yêu cầu bài toán ban đầu từ góc nhìn khách hàng và chủ phòng khám. |
| 2 | [`docs/requirements.md`](docs/requirements.md) | Đặc tả yêu cầu phần mềm chi tiết (SRS) gồm 38 FR và 10 NFR. |
| 3 | [`docs/user-stories.md`](docs/user-stories.md) | 27 User Stories hoàn chỉnh phân loại theo 4 vai trò kèm thang đo MoSCoW. |
| 4 | [`docs/acceptance-criteria.md`](docs/acceptance-criteria.md) | Tiêu chí chấp nhận chuẩn Gherkin (*Given - When - Then*) cho từng chức năng. |
| 5 | [`docs/requirements-issues.md`](docs/requirements-issues.md) | Nhật ký ghi nhận và xử lý các vấn đề yêu cầu/xung đột phát sinh (Human Gate 1). |
| 6 | [`docs/architecture.md`](docs/architecture.md) | Đặc tả kiến trúc hệ thống phân tầng, luồng dữ liệu y tế và mô hình AI 3 lớp. |
| 7 | [`docs/architecture-decisions.md`](docs/architecture-decisions.md) | 8 Quyết định kiến trúc công nghệ quan trọng (ADR-001 đến ADR-008). |
| 8 | [`docs/database-design.md`](docs/database-design.md) | Thiết kế 14 bảng quan hệ 3NF, sơ đồ Mermaid ERD và từ điển dữ liệu Data Dictionary. |
| 9 | [`docs/thiet-ke-huong-doi-tuong-class-diagram.md`](docs/thiet-ke-huong-doi-tuong-class-diagram.md) | Đặc tả thiết kế hướng đối tượng (OOD) chi tiết 10 lớp nghiệp vụ cốt lõi. |
| 10 | [`docs/test-plan.md`](docs/test-plan.md) | Kế hoạch kiểm thử tự động toàn diện từ Unit, Integration đến AI Security. |
| 11 | [`docs/test-report.md`](docs/test-report.md) | Báo cáo kết quả kiểm thử tự động: **319 / 319 passed (100% Pass Rate)**. |
| 12 | [`docs/code-review.md`](docs/code-review.md) | Biên bản kiểm toán mã nguồn đa chiều, đánh giá RBAC và xử lý lỗi RFC 7807. |
| 13 | [`docs/security-review.md`](docs/security-review.md) | Báo cáo an toàn thông tin theo chuẩn OWASP Top 10 và Nghị định 13/2023/NĐ-CP. |
| 14 | [`docs/deployment.md`](docs/deployment.md) | Sổ tay hướng dẫn triển khai Docker Compose và thiết lập biến môi trường. |
| 15 | [`docs/user-guide.md`](docs/user-guide.md) | Hướng dẫn vận hành chi tiết cho 4 vai trò người dùng kèm kịch bản demo chấm điểm. |
| 16 | [`docs/Reports/AI-Augmented-SDLC-Report.md`](docs/Reports/AI-Augmented-SDLC-Report.md) | **Báo cáo tổng kết phương pháp luận AI SDLC**, các điểm kiểm soát Human Gates 1-3, danh mục phát hiện lỗi AI và các hiệu chỉnh thực tế của con người. |
| 17 | **4 Báo Cáo Học Phần (KT1 - KT4)** | [`SDLC_GiaiDoan1_PhanTich_ThietKe.md`](docs/Reports/SDLC_GiaiDoan1_PhanTich_ThietKe.md), [`SDLC_GiaiDoan2_ChucNang_QuanLy.md`](docs/Reports/SDLC_GiaiDoan2_ChucNang_QuanLy.md), [`SDLC_GiaiDoan3_TichHopAI_TestAI.md`](docs/Reports/SDLC_GiaiDoan3_TichHopAI_TestAI.md), [`SDLC_GiaiDoan4_BaoCao_HuongDan_TrienKhai.md`](docs/Reports/SDLC_GiaiDoan4_BaoCao_HuongDan_TrienKhai.md). |
| 18 | [`docs/Reports/phan-chia-cong-viec.md`](docs/Reports/phan-chia-cong-viec.md) | Bảng phân công nhiệm vụ và tỷ lệ đóng góp chi tiết giữa 2 thành viên nhóm (50% - 50%). |
| 19 | **Bộ 7 Tài Liệu Hoàn Thiện (.docx)** | Lưu trữ tại thư mục `docs/7_Giai_Doan_Hoan_Thien/` phục vụ nộp báo cáo hoàn chỉnh. |

---

## 🧪 Kết Quả Kiểm Thử Tự Động (Automated Testing)

Hệ thống duy trì tỷ lệ vượt qua **100% (319/319 passed, 4 xfailed)** trên toàn bộ test suite:

```bash
# Chạy toàn bộ test suite kiểm thử tự động
pytest backend/tests/ -v

# ============================== 319 passed, 4 xfailed in 14.82s ==============================
```

- ✅ **Test RBAC & Phân Quyền**: Chặn đứng 100% hành vi truy cập trái phép qua API giữa các vai trò.
- ✅ **Test Chống Trùng Lịch**: Kiểm thử toàn diện 15 kịch bản giao thoa khung giờ của bác sĩ và phòng khám.
- ✅ **Test Khử Định Danh PII**: Xác minh việc che số CCCD, SĐT, BHYT, Tên bệnh nhân chính xác tuyệt đối mà không che nhầm thông số sinh hiệu lâm sàng.
- ✅ **Test AI Guardrails**: Kiểm thử khả năng chống Prompt Injection, chống Jailbreak và từ chối tự chẩn đoán bệnh học.
- ✅ **Test E2E Clinical Flow**: Chu trình khép kín Tiếp đón ➔ Khám bệnh ➔ Kê đơn ➔ Xuất hóa đơn ➔ Báo cáo.

---

## 📜 Giấy Phép & Đóng Góp

- Dự án được phát hành mã nguồn mở dưới giấy phép **[MIT License](LICENSE)**.
- Sản phẩm được nghiên cứu và phát triển phục vụ Đồ án Học phần: **Ứng dụng Trí tuệ Nhân tạo - ICTU 2026-2027**.
- Tác giả: **Nhóm 07** – **Đinh Gia Bảo (Trưởng nhóm)** và **Trần Đặng Công Tâm** ([@dtc245220019-create](https://github.com/dtc245220019-create) & [@tamtran2k6zz](https://github.com/tamtran2k6zz)).

---

<p align="center">
  <b>Smart Clinic CMS-AI</b> — <i>Nâng cao hiệu suất y tế bằng Trí tuệ Nhân tạo có trách nhiệm và nhân văn.</i> ❤️
</p>
