# HƯỚNG DẪN TRIỂN KHAI VÀ VẬN HÀNH HỆ THỐNG (DEPLOYMENT & OPERATIONS MANUAL)
## DỰ ÁN: HỆ THỐNG QUẢN LÝ PHÒNG KHÁM ĐA KHOA THÔNG MINH TÍCH HỢP TRỢ LÝ AI HÀNH CHÍNH
### (Clinic Management System with Administrative AI Assistant - CMS-AI)

---

## 1. TỔNG QUAN KIẾN TRÚC TRIỂN KHAI (DEPLOYMENT TOPOLOGY)

Hệ thống **CMS-AI** được đóng gói hoàn chỉnh, hỗ trợ hai phương thức triển khai chính:
1. **Triển khai Production / Server qua Docker Compose (Khuyên dùng):** Đóng gói thành cụm 4 container mạng nội bộ cô lập.
2. **Triển khai Cục bộ Windows Native (Dành cho Dev & Chấm điểm Lab):** Khởi chạy bằng các file kịch bản `.bat` tự động.

```mermaid
graph TD
    subgraph CLIENTS [TRÌNH DUYỆT NGƯỜI DÙNG]
        B1[Lễ tân - Trình duyệt Edge/Chrome]
        B2[Bác sĩ - Máy tính Khám bệnh]
        B3[Thu ngân - Máy in Hóa đơn]
        B4[Admin - Máy trạm Quản trị]
    end

    subgraph DOCKER_CONTAINERS [CỤM DOCKER COMPOSE MẠNG NỘI BỘ]
        NGINX[clinic_frontend : Port 3000 / Nginx React SPA]
        FASTAPI[clinic_backend : Port 8000 / Uvicorn ASGI]
        POSTGRES[(clinic_postgres : Port 5432 / PostgreSQL 16)]
        PGADMIN[clinic_pgadmin : Port 5050 / Quản trị DB GUI]
    end

    CLIENTS -->|HTTP / Cổng 3000| NGINX
    NGINX -->|REST API / Cổng 8000| FASTAPI
    FASTAPI -->|TCP / Cổng 5432| POSTGRES
    PGADMIN -->|TCP / Cổng 5432| POSTGRES
```

---

## 2. PHƯƠNG THỨC 1: TRIỂN KHAI BẰNG DOCKER COMPOSE

### 2.1. Yêu cầu Cấu hình Máy chủ (System Prerequisites)
- **Hệ điều hành:** Linux (Ubuntu 22.04 LTS+, Debian 12+) hoặc Windows Server 2022 / Windows 11 có Docker Desktop.
- **CPU:** Tối thiểu 2 Cores (Khuyến nghị 4 Cores).
- **RAM:** Tối thiểu 4 GB (Khuyến nghị 8 GB nếu chạy kèm Ollama Local LLM).
- **Ổ cứng:** Dung lượng trống tối thiểu 20 GB SSD.
- **Phần mềm:** Docker Engine 24.0+ và Docker Compose v2.20+.

### 2.2. Danh mục 4 Dịch vụ Container trong `docker-compose.yml`
| Tên Container | Hình ảnh (Base Image) | Cổng Host : Container | Chức năng |
|---|---|:---:|---|
| `clinic_backend` | `python:3.10-slim` | `8000:8000` | FastAPI REST API, SQLAlchemy ORM & AI Engine |
| `clinic_frontend`| `nginx:alpine` (Sau Vite build) | `3000:80` | Single Page Application, giao diện người dùng |
| `clinic_postgres`| `postgres:16-alpine` | `5432:5432` | CSDL Quan hệ lưu trữ hồ sơ y tế |
| `clinic_pgadmin` | `dpage/pgadmin4:latest` | `5050:80` | Giao diện Web quản trị CSDL trực quan |

### 2.3. Quy trình Triển khai 4 Bước Chi tiết

```bash
# Bước 1: Di chuyển vào thư mục dự án
cd "d:/ICTU/Nam 3/ICTU_2026-2027/Ứng dụng trí tuệ nhân tạo - Project/He_thong_quan_ly_phong_kham"

# Bước 2: Chuẩn bị tệp cấu hình môi trường (.env)
# (Sao chép từ tệp mẫu .env.example)
copy .env.example .env

# Bước 3: Khởi dựng và đóng gói toàn bộ hệ thống
docker compose up --build -d

# Bước 4: Kiểm tra trạng thái toàn bộ Container
docker compose ps
```

### 2.4. Truy cập các Dịch vụ sau khi Triển khai
- **Giao diện Ứng dụng Quản lý (Frontend):** `http://localhost:3000` (hoặc IP máy chủ: `http://192.168.1.100:3000`)
- **Tài liệu API Swagger UI (Backend):** `http://localhost:8000/docs`
- **Quản trị Cơ sở Dữ liệu pgAdmin:** `http://localhost:5050`
  - Tài khoản mặc định: `admin@clinic.local` / `admin123`

---

## 3. PHƯƠNG THỨC 2: KHỞI CHẠY CỤC BỘ WINDOWS BẰNG FILE SCRIPT (.BAT)

Dành cho môi trường kiểm thử lab, máy chấm bài hoặc lập trình viên phát triển cục bộ:

```
+---------------------------------------------------------------------------------------------------+
|                        DANH MỤC CÁC TỆP SCRIPT KHỞI CHẠY TRÊN WINDOWS                             |
+---------------------------------------------------------------------------------------------------+
| 1. `run_all.bat`      | Khởi chạy song song toàn bộ Backend (8000) và Frontend (5173)              |
| 2. `run_backend.bat`  | Tự động tạo venv, cài dependencies, nạp seed data và chạy FastAPI Uvicorn |
| 3. `run_frontend.bat` | Cài đặt npm packages và khởi chạy máy chủ Vite Development Server         |
| 4. `run_tests.bat`    | Kích hoạt môi trường test và chạy toàn bộ 223+ Pytest test cases          |
+---------------------------------------------------------------------------------------------------+
```

### Hướng dẫn Thao tác Nhanh:
1. Nhấp đúp chuột vào file `run_all.bat`.
2. Hệ thống sẽ tự động mở 2 cửa sổ dòng lệnh độc lập:
   - Cửa sổ 1: Khởi động Backend tại `http://localhost:8000`.
   - Cửa sổ 2: Khởi động Frontend tại `http://localhost:5173`.
3. Mở trình duyệt Web (Chrome, Edge) và truy cập `http://localhost:5173` để sử dụng ngay.

---

## 4. ĐẶC TẢ BIẾN MÔI TRƯỜNG (.ENV CONFIGURATION SPECIFICATION)

```ini
# ==============================================================================
# HỆ THỐNG CẤU HÌNH BIẾN MÔI TRƯỜNG CMS-AI (.env)
# ==============================================================================

# 1. Cấu hình Ứng dụng & Mạng
PROJECT_NAME="Clinic Management System with Administrative AI Assistant"
API_V1_STR="/api/v1"
DEBUG=False
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173","http://127.0.0.1:5173"]

# 2. Cấu hình Xác thực & Bảo mật (JWT & Bcrypt)
SECRET_KEY="clinic_super_secure_secret_key_change_in_production_min_32_chars!"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60

# 3. Cấu hình Cơ sở Dữ liệu (Database URL)
# Môi trường Dev/Test (SQLite cục bộ):
DATABASE_URL="sqlite:///./clinic_system.db"
# Môi trường Production (PostgreSQL Docker):
# DATABASE_URL="postgresql://postgres:postgres123@clinic_postgres:5432/clinic_db"

# 4. Cấu hình Trợ lý AI Phân tầng (AI Provider Settings)
# Lựa chọn Provider: "mock" (Offline), "ollama" (Local LLM), "gemini" (Cloud API)
DEFAULT_AI_PROVIDER="mock"
OLLAMA_BASE_URL="http://localhost:11434"
OLLAMA_MODEL="llama3"
GEMINI_API_KEY=""
```

---

## 5. CHIẾN LƯỢC SAO LƯU & PHỤC HỒI DỮ LIỆU Y TẾ (BACKUP & DISASTER RECOVERY)

### 5.1. Sao lưu Tự động Định kỳ (Automated Backup Schedule)
- **Tần suất:** Sao lưu toàn bộ (Full Backup) vào 01:00 sáng hàng ngày; Sao lưu gia tăng (Incremental Backup) mỗi 4 giờ.
- **Kịch bản lệnh sao lưu PostgreSQL:**
  ```bash
  # Lệnh tạo bản sao lưu nén gzip có gắn dấu thời gian
  pg_dump -U postgres -h localhost -d clinic_db | gzip > /backups/clinic_db_$(date +%Y%m%d_%H%M%S).sql.gz
  ```
- **Lưu trữ an toàn:** Lưu trữ 3 bản sao tại 3 vị trí khác nhau (Local Server, Ổ cứng mạng NAS nội bộ, Cloud Object Storage mã hóa).

### 5.2. Quy trình Phục hồi Dữ liệu khi Gặp Sự cố (Disaster Recovery Runbook)
1. **Dừng dịch vụ Backend:** `docker compose stop clinic_backend`
2. **Khởi tạo lại cơ sở dữ liệu trống:**
   ```bash
   dropdb -U postgres clinic_db
   createdb -U postgres clinic_db
   ```
3. **Phục hồi từ bản sao lưu gần nhất:**
   ```bash
   gunzip -c /backups/clinic_db_20260829_010000.sql.gz | psql -U postgres -d clinic_db
   ```
4. **Khởi động lại toàn bộ hệ thống:** `docker compose start clinic_backend`
5. **Xác minh toàn vẹn:** Đăng nhập và kiểm tra bản ghi phiếu khám gần nhất.
