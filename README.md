# He_thong_quan_ly_phong_kham

# Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp AI Hành chính
## Clinic Management System with Administrative AI Assistant

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com)
[![React 18](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-5.0+-646CFF.svg)](https://vitejs.dev)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4+-38B2AC.svg)](https://tailwindcss.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com)
[![Tests](https://img.shields.io/badge/tests-223%20passed-brightgreen.svg)](#kiem-thu)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Muc luc

- [Gioi thieu](#gioi-thieu)
- [Kien truc he thong](#kien-truc-he-thong)
- [Tai khoan mac dinh](#tai-khoan-mac-dinh)
- [Huong dan khoi chay](#huong-dan-khoi-chay)
- [Docker Compose](#docker-compose)
- [Tinh nang AI](#tinh-nang-ai)
- [Tai lieu SDLC](#tai-lieu-sdlc)
- [Kiem thu tu dong](#kiem-thu-tu-dong)
- [Giay phep](#giay-phep)

---

## Gioi thieu

**He thong Quan ly Phong kham Da khoa thong minh tich hop AI Hanh chinh** la giai phap phan mem quan tri phong kham toan dien, chuan y te, ket hop giua mo hinh phan quyen nghiem ngat (**RBAC - 4 nhom nguoi dung**) va **Tro ly AI Hanh chinh phan tang bao mat**.

He thong duoc thiet ke theo tieu chuan an toan du lieu y te:

- **Khu dinh danh PII tuyet doi** (Ho ten, CCCD/CMND, So dien thoai, Dia chi, So the BHYT) truoc khi gui toi cac mo hinh AI
- **Fallback Mock Offline 100%** khong phu thuoc internet
- **Tuyen bo mien tru trach nhiem y te** dinh kem bat buoc tren moi ket qua AI
- **Audit Log** day du moi thao tac truy cap ho so benh an

---

## Kien truc he thong

```
                          +-----------------------------------+
                          |   React 18 + Vite + Tailwind SPA  |
                          |  (Admin / Receptionist / Doctor /  |
                          |         Accountant Views)          |
                          +----------------+------------------+
                                           |
                               REST API / JWT Bearer Token
                                           |
                                           v
+------------------------------------------------------------------------------+
|                            FastAPI Backend Engine                             |
|                                                                              |
|  +-----------------+  +-------------------+  +-------------+  +-----------+ |
|  |  RBAC Security  |  | Conflict Detection |  | Clinical    |  | Invoicing | |
|  | (4 Roles JWT)   |  | (Doctor/Room Slot) |  | Flow (EMR)  |  | & Billing | |
|  +-----------------+  +-------------------+  +-------------+  +-----------+ |
|                                                                              |
|  +------------------------------------------------------------------------+  |
|  |              Administrative AI Engine (3-Layer Security)               |  |
|  |  +------------------+  +------------------+  +----------------------+  |  |
|  |  | Layer 1: Privacy |->| Layer 2:         |->| Layer 3: Providers   |  |  |
|  |  | PII De-identify  |  | Medical Guardrail|  | Mock / Ollama / Cloud|  |  |
|  |  +------------------+  +------------------+  +----------------------+  |  |
|  +------------------------------------------------------------------------+  |
|                                        |                                     |
|                          SQLAlchemy 2.0 ORM & Audit Logs                     |
+----------------------------------------+-------------------------------------+
                                         |
                    +--------------------+--------------------+
                    |                                         |
                    v                                         v
     +------------------------------+          +------------------------------+
     |  SQLite (Local / Dev mode)   |          |  MySQL 8.0 (Docker Compose)  |
     +------------------------------+          +------------------------------+
```

---

## Tai khoan mac dinh

He thong cung cap san bo du lieu mau chuan y te Viet Nam voi day du 4 nhom vai tro:

| # | Vai tro | Username | Mat khau | Ho va ten | Quyen han chinh |
|---|---------|----------|----------|-----------|-----------------|
| 1 | **Admin** | `admin` | `admin123` | Quan tri vien He thong | Quan ly nguoi dung, bac si, danh muc thuoc, cau hinh phong, Audit Logs, AI Logs, Thong ke |
| 2 | **Le tan** | `receptionist` | `rec123` | Nguyen Thi Thu Ha | Tiep don benh nhan, tao ho so y te, dat & dieu phoi lich hen, phat so thu tu, FAQ AI |
| 3 | **Ke toan** | `accountant` | `acc123` | Tran Bich Phuong | Thu vien phi, quan ly hoa don, tinh khau tru BHYT, xuat ma VietQR, in hoa don |
| 4 | **Bac si (Tim mach)** | `dr_nam` | `doc123` | BS.CKII Nguyen Van Nam | Kham benh, tom tat ho so AI, ke don thuoc dien tu, sinh dan do xuat vien AI |
| 5 | **Bac si (Tieu hoa)** | `dr_huong` | `doc123` | ThS.BS Le Thu Huong | Kham tieu hoa, chi dinh noi soi, ke don, dan do xuat vien AI |
| 6 | **Bac si (Nhi khoa)** | `dr_minh` | `doc123` | BS.CKI Pham Hoang Minh | Tiep nhan benh nhi, kham lam sang, theo doi sinh hieu |
| 7 | **Bac si (TMH)** | `dr_lan` | `doc123` | BS Vu Mai Lan | Kham TMH, chi dinh can lam sang, ke don dieu tri ngoai tru |

---

## Huong dan khoi chay

### Cach 1: Script Windows 1-click (Khuyen dung cho chay local)

**Yeu cau:** Python 3.10+ va Node.js 18+ da cai dat.

```cmd
# Khoi chay dong thoi Backend + Frontend (2 cua so)
double-click: run_all.bat

# Hoac khoi chay rieng le:
run_backend.bat     # FastAPI tai http://localhost:8000
run_frontend.bat    # React Vite tai http://localhost:5173

# Chay bo test tu dong (223 test cases)
run_tests.bat
```

**Cac dich vu sau khi khoi chay:**

| Dich vu | URL |
|---------|-----|
| Giao dien Web (React SPA) | http://localhost:5173 |
| Backend REST API | http://localhost:8000 |
| Swagger API Docs | http://localhost:8000/docs |

---

## Docker Compose

**Yeu cau:** Docker Desktop da cai dat va dang chay.

```bash
# 1. Sao chep cau hinh moi truong
cp .env.example .env

# 2. Khoi dong toan bo cum container
docker compose up --build -d

# 3. Kiem tra trang thai
docker ps
```

**Cac dich vu Docker:**

| Dich vu | URL / Cong ket noi |
|---------|---------------------|
| Frontend React SPA | http://localhost:3001 |
| Backend FastAPI | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| MySQL Database | 127.0.0.1:3307 (root / root123 / clinic_db) |

> **Ket noi MySQL Workbench:** Host `127.0.0.1`, Port `3307`, User `root`, Password `root123`, Database `clinic_db`

---

## Tinh nang AI

He thong tich hop 3 cong cu AI hanh chinh ho tro bac si va nhan vien y te:

### 1. AI Tom tat Ho so Benh an (Pre-visit Briefing)

- Tu dong trich xuat: Tien su benh, danh sach di ung thuoc nghiem trong, cac dot kham va don thuoc gan nhat
- Giup bac si nam bat tinh trang benh nhan chi trong 30 giay truoc phien kham

### 2. Chatbot Tu van Quy trinh Phong kham (Clinic FAQ Chatbot)

- Tra loi quy trinh hanh chinh: Thu tuc chuyen tuyen BHYT, bang gia dich vu, lich lam viec, quy dinh dat lich
- **Chan moi cau hoi yeu cau chan doan / ke don benh hoc**

### 3. AI Sinh Huong dan Sau kham (Post-visit Discharge Instructions)

- Dua tren ket luan kham va don thuoc cua bac si, AI tu dong tao van ban dan do de hieu cho nguoi benh
- Lich uong thuoc, che do kieng cu dinh duong, dau hieu bat thuong can tai kham khan cap

> **Bao mat AI:** Moi du lieu truoc khi gui AI deu qua module khu dinh danh PII tu dong.
> Moi ket qua AI deu kem nhan **[CANH BAO Y TE]** - khong thay the y kien bac si.

---

## Tai lieu SDLC

Toan bo tai lieu phan tich, dac ta, thiet ke, kiem thu va huong dan van hanh chi tiet tai thu muc `docs/`:

| File | Noi dung |
|------|----------|
| [`docs/SDLC_GiaiDoan1_PhanTich_ThietKe.md`](docs/SDLC_GiaiDoan1_PhanTich_ThietKe.md) | **KT1** - Khao sat bai toan, Phan tich 4 Actor, Bieu do Use Case, ERD 14 bang quan he & Ranh gioi Dao duc AI |
| [`docs/SDLC_GiaiDoan2_ChucNang_QuanLy.md`](docs/SDLC_GiaiDoan2_ChucNang_QuanLy.md) | **KT2** - Kien truc Backend & Frontend, Ma tran Phan quyen RBAC, Thuat toan Kiem tra Xung dot Lich & Dac ta RESTful API |
| [`docs/SDLC_GiaiDoan3_TichHopAI_TestAI.md`](docs/SDLC_GiaiDoan3_TichHopAI_TestAI.md) | **KT3** - Kien truc Phan lop AI, Khu dinh danh PII, Ky thuat Prompt Engineering, Multi-Provider & Ma tran Kiem thu AI |
| [`docs/SDLC_GiaiDoan4_BaoCao_HuongDan_TrienKhai.md`](docs/SDLC_GiaiDoan4_BaoCao_HuongDan_TrienKhai.md) | **Cuoi ky** - Bao cao An toan Bao mat, Huong dan Trien khai Docker, So tay Nguoi dung 4 vai tro & Kich ban Demo 8 buoc cham diem |

---

## Kiem thu tu dong

He thong dat **100% ty le vuot qua (Pass Rate)** tren toan bo 223 test cases:

```bash
# Chay toan bo test suite
pytest backend/tests/ -v

# Cac module kiem thu:
# test_m1_core.py                 : Backend Core, Auth, JWT
# test_m1_adversarial.py          : Adversarial RBAC & JWT attacks
# test_rbac.py                    : Co lap phan quyen 4 vai tro
# test_m2_scheduling_queue_clinical.py : Thuat toan phat hien xung dot lich kham
# test_pii_anonymizer.py          : Khu dinh danh CCCD, SDT, BHYT, Ten
# test_m3_comprehensive.py        : AI Engine, Guardrails, Offline Fallback
# test_ai_features.py             : 3 tinh nang AI hanh chinh
# test_m4_invoicing_and_analytics.py   : Hoa don, thu phi, thong ke
# test_clinical_flow.py           : Chu trinh kham, ke don, thanh toan
# test_e2e_scenarios.py           : Kich ban tich hop End-to-End
# test_adversarial_tier5.py       : Tier 5 Security & Edge cases
```

**Ket qua:** `223 passed in 11.96s`

---

## Cau truc du an

```
He_thong_quan_ly_phong_kham/
├── backend/
│   ├── app/
│   │   ├── ai_engine/          # PII Anonymizer, Guardrails, Mock/Ollama/Cloud Providers
│   │   ├── api/v1/             # 11 RESTful API routers
│   │   ├── core/               # Security, JWT, RBAC, Conflict Detection
│   │   ├── models/             # 14 SQLAlchemy ORM models
│   │   ├── schemas/            # Pydantic validation schemas
│   │   └── seed/               # Seed data loader (10 patients, 4 doctors, 28 medicines)
│   ├── tests/                  # 11 test files, 223 test cases
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/         # Layout, AI widgets, Invoice print modal
│   │   ├── pages/              # 4 role dashboards + Login
│   │   └── services/           # Axios API client & services
│   ├── Dockerfile
│   └── package.json
├── docs/                       # 4 SDLC deliverable documents
├── docker-compose.yml          # MySQL 8.0 + Backend + Frontend
├── run_all.bat                 # 1-click Windows launcher
├── run_backend.bat
├── run_frontend.bat
├── run_tests.bat
└── README.md
```

---

## Giay phep

Du an duoc phat hanh duoi giay phep mo nguon **MIT License**.

Phat trien phuc vu Do an Hoc phan: **Ung dung Tri tue Nhan tao - ICTU 2026-2027**.