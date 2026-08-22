# Project: Clinic Management System with Administrative AI Assistant
# (Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp AI Hành chính)

## Architecture Overview
The system is built as a production-grade, secure, role-based Clinic Management System (CMS) augmented with an Administrative AI Assistant. It strictly follows medical data privacy standards (de-identification of PII before any AI interaction), deterministic offline fallback capabilities, and strict RBAC isolation across 4 distinct staff roles.

### Technology Stack
- **Backend**: Python 3.10+ / FastAPI, SQLAlchemy 2.0 (ORM), Pydantic v2 (Validation & Schemas), Passlib (Bcrypt hashing), PyJWT (Authentication).
- **Database**: SQLite (default zero-config local engine for instant verification) and PostgreSQL (production-ready via SQLAlchemy connection strings).
- **AI Engine**: Layered privacy & provider architecture:
  - *Layer 1 (Privacy)*: Regex & rule-based PII De-identification Engine (`re` patterns for Vietnamese CCCD, Phone, BHYT, Patient Names, Addresses).
  - *Layer 2 (Guardrails)*: System prompt guardrails prohibiting diagnostic/prescriptive AI behavior + Vietnamese Medical Disclaimer injection (`TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y TẾ`).
  - *Layer 3 (Provider Abstraction)*: `AIProvider` base class with implementations for:
    1. `MockDeterministicAIProvider` (100% offline, zero internet dependency, test-resilient rule engine).
    2. `OllamaAIProvider` (Local LLM via `http://localhost:11434`).
    3. `GeminiOpenAIAIProvider` (Cloud API via environment keys).
- **Frontend**: Modern SPA with React 18+, Vite, Tailwind CSS (Medical color palette: Slate, Emerald, Blue, Rose), Lucide Icons, React Router v6, Axios with JWT interceptors.
- **Testing & QA**: Pytest, pytest-asyncio, HTTPX TestClient, multi-tier automated test suites.
- **DevOps & Packaging**: Dockerfile, Docker Compose (`backend`, `frontend`, `postgres`, `pgadmin`), Windows batch scripts (`run_backend.bat`, `run_frontend.bat`, `run_all.bat`, `run_tests.bat`).

---

## Code Layout
```
d:/ICTU/Nam 3/ICTU_2026-2027/Ứng dụng trí tuệ nhân tạo - Project/He_thong_quan_ly_phong_kham/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI application entry & middleware
│   │   ├── config.py                # Pydantic Settings & environment config
│   │   ├── database.py              # SQLAlchemy engine, SessionLocal, Base
│   │   ├── models/                  # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # User, Role enum
│   │   │   ├── clinic.py            # Specialty, Clinic (Room), Doctor, Shift
│   │   │   ├── patient.py           # Patient (Medical Code, PII, Insurance, Allergies)
│   │   │   ├── appointment.py       # Appointment, AppointmentStatus enum
│   │   │   ├── medical_record.py    # MedicalRecord / Encounter, Queue
│   │   │   ├── prescription.py      # Prescription, PrescriptionItem, Medicine
│   │   │   ├── invoice.py           # Invoice, PaymentStatus, PaymentMethod
│   │   │   └── audit.py             # AuditLog, AIInvocationLog
│   │   ├── schemas/                 # Pydantic v2 validation models
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── clinic.py
│   │   │   ├── patient.py
│   │   │   ├── appointment.py
│   │   │   ├── medical_record.py
│   │   │   ├── prescription.py
│   │   │   ├── invoice.py
│   │   │   ├── ai.py
│   │   │   └── stats.py
│   │   ├── core/                    # Core security & utilities
│   │   │   ├── __init__.py
│   │   │   ├── security.py          # Password hashing, JWT creation & decoding
│   │   │   ├── rbac.py              # RoleChecker, get_current_user, permission gates
│   │   │   └── conflict_checker.py  # Time interval & doctor/room conflict detection
│   │   ├── ai_engine/               # Administrative AI Module
│   │   │   ├── __init__.py
│   │   │   ├── anonymizer.py        # PII De-identification regex engine
│   │   │   ├── guardrails.py        # Prompt injection filters & medical disclaimer
│   │   │   ├── providers/           # AI Provider implementations
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py          # Abstract AIProvider interface
│   │   │   │   ├── mock_provider.py # 100% offline deterministic rule engine
│   │   │   │   ├── ollama_provider.py
│   │   │   │   └── cloud_provider.py
│   │   │   ├── service.py           # Pre-visit summary, FAQ Chatbot, Discharge instructions
│   │   │   └── knowledge_base.py    # FAQ data & clinic guidelines
│   │   ├── api/                     # REST API Routers
│   │   │   ├── __init__.py
│   │   │   ├── deps.py              # Dependency injections (db, current_user)
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   ├── clinics.py
│   │   │   │   ├── patients.py
│   │   │   │   ├── appointments.py
│   │   │   │   ├── medical_records.py
│   │   │   │   ├── prescriptions.py
│   │   │   │   ├── medicines.py
│   │   │   │   ├── invoices.py
│   │   │   │   ├── ai.py
│   │   │   │   ├── audit.py
│   │   │   │   └── stats.py
│   │   └── seed/
│   │       ├── __init__.py
│   │       └── seed_data.py         # Full realistic Vietnamese clinic dataset
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py              # Pytest fixtures, test client, test DB
│   │   ├── test_rbac.py             # Multi-role access control tests
│   │   ├── test_appointments.py     # Conflict detection & scheduling tests
│   │   ├── test_pii_anonymizer.py   # PII masking & regex tests
│   │   ├── test_ai_features.py      # AI pre-visit, FAQ chatbot, discharge & guardrails
│   │   ├── test_clinical_flow.py    # End-to-end clinical encounter & invoice lifecycle
│   │   └── test_e2e_scenarios.py    # Full 4-tier application scenarios
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/              # Shared UI components (Modals, Tables, Badges, Disclaimers)
│   │   │   ├── Navbar.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── MedicalDisclaimerBadge.jsx
│   │   │   ├── InvoicePrintModal.jsx
│   │   │   ├── AIPreVisitCard.jsx
│   │   │   └── AIChatWidget.jsx
│   │   ├── context/                 # AuthContext, ToastContext
│   │   │   ├── AuthContext.jsx
│   │   │   └── ToastContext.jsx
│   │   ├── pages/                   # Role-based views & dashboards
│   │   │   ├── LoginPage.jsx
│   │   │   ├── UnauthorizedPage.jsx
│   │   │   ├── receptionist/
│   │   │   │   ├── ReceptionistDashboard.jsx
│   │   │   │   ├── PatientRegistrationPage.jsx
│   │   │   │   └── AppointmentCalendarPage.jsx
│   │   │   ├── doctor/
│   │   │   │   ├── DoctorDashboard.jsx
│   │   │   │   ├── PatientQueuePage.jsx
│   │   │   │   └── ConsultationFormPage.jsx
│   │   │   ├── accountant/
│   │   │   │   ├── AccountantDashboard.jsx
│   │   │   │   └── InvoicePaymentPage.jsx
│   │   │   └── admin/
│   │   │       ├── AdminDashboard.jsx
│   │   │       ├── UserManagementPage.jsx
│   │   │       ├── DoctorShiftPage.jsx
│   │   │       ├── MedicineCatalogPage.jsx
│   │   │       ├── AuditLogPage.jsx
│   │   │       └── AILogPage.jsx
│   │   ├── services/                # Axios API client & endpoints
│   │   │   ├── api.js
│   │   │   ├── authService.js
│   │   │   ├── clinicService.js
│   │   │   ├── patientService.js
│   │   │   ├── appointmentService.js
│   │   │   ├── consultationService.js
│   │   │   ├── invoiceService.js
│   │   │   └── aiService.js
│   │   ├── utils/                   # Formatters (VND currency, date, status badges)
│   │   │   └── formatters.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── Dockerfile
├── docs/
│   ├── SDLC_GiaiDoan1_PhanTich_ThietKe.md
│   ├── SDLC_GiaiDoan2_ChucNang_QuanLy.md
│   ├── SDLC_GiaiDoan3_TichHopAI_TestAI.md
│   └── SDLC_GiaiDoan4_BaoCao_HuongDan_TrienKhai.md
├── docker-compose.yml
├── run_backend.bat
├── run_frontend.bat
├── run_all.bat
├── run_tests.bat
├── README.md
└── PROJECT.md
```

---

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | JWT Authentication & Session | Login, password hashing (bcrypt), token issuance, profile endpoint | M1 | Survey R1 |
| 2 | Role-Based Access Control (RBAC) | 4 roles: Admin, Receptionist, Doctor, Accountant; route guards & permission matrices | M1 | Survey R1 |
| 3 | User & Staff Management | CRUD users, assign roles, activate/deactivate accounts | M1 | Survey R1 |
| 4 | Specialty & Clinic Room Management | Manage medical specialties, consultation rooms, equipment | M1 | Survey R1 |
| 5 | Doctor Profiles & Shift Management | Doctor profiles, qualifications, working shifts (morning/afternoon/night) | M1 | Survey R1 |
| 6 | Patient Profile & Medical Code | Auto-generation of unique medical ID (`BN-YYYYMMDD-XXXX`), PII, BHYT, drug allergies | M1 | Survey R1 |
| 7 | Seed Dataset Loading | Population of specialties, doctors, shifts, medicines, sample patients & history | M1 | Survey R4 |
| 8 | Appointment Booking Engine | Booking appointments with doctor, specialty, time slot, symptoms | M2 | Survey R1 |
| 9 | Time Conflict Detection Algorithm | Proactive overlap prevention for doctor & clinic room; slot availability check | M2 | Survey R1 |
| 10 | Appointment Status Lifecycle | Reschedule, confirm, check-in, cancel, complete lifecycle tracking | M2 | Survey R1 |
| 11 | Reception Queue Management | Daily queue number generation, check-in counter, assigned doctor dispatch | M2 | Survey R1 |
| 12 | Clinical Examination Record | Recording vitals (BP, HR, SpO2, Temp, BMI), ICD-10 diagnosis, clinical notes | M2 | Survey R1 |
| 13 | Service & Lab Order Management | Ordering ultrasound, blood tests, X-rays with price calculation | M2 | Survey R1 |
| 14 | Medicine Catalog & Stock Management | Catalog with active ingredients, dosage forms, unit prices, stock tracking | M2 | Survey R1 |
| 15 | Electronic Prescription (e-Prescription) | Prescribing medicines, dosage, usage instructions, inventory decrement | M2 | Survey R1 |
| 16 | PII De-identification Engine | Regex masking of Vietnamese CCCD, Phone, BHYT, Names, Addresses before AI calls | M3 | Survey R2 |
| 17 | Pre-visit Briefing AI Tool | Rapid medical history summary, allergy warning, chronic condition alerts for doctors | M3 | Survey R2 |
| 18 | Clinic FAQ Chatbot | RAG/FAQ-based guidance on clinic procedures, insurance, pricing, opening hours | M3 | Survey R2 |
| 19 | Post-visit Discharge AI Generator | Auto-generating patient care instructions, medication schedule, follow-up date | M3 | Survey R2 |
| 20 | Mandatory Medical Disclaimer | Injection of legal disclaimer on all AI outputs (`TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM`) | M3 | Survey R2 |
| 21 | AI Diagnostic Guardrail & Filter | System prompt guardrails refusing diagnostic or clinical treatment commands | M3 | Survey R2 |
| 22 | Deterministic Offline Mock AI Provider | 100% reliable offline mock engine providing realistic responses with zero latency | M3 | Survey R2 |
| 23 | External AI Provider Adapter | Pluggable Ollama local LLM and Gemini/OpenAI cloud API adapter | M3 | Survey R2 |
| 24 | Audit Logging Engine | Recording read/write actions on patient medical records (user, time, action, IP) | M3 | Survey R2 |
| 25 | AI Invocation Logging | Logging all AI requests: anonymized prompt, response, model, latency, timestamp | M3 | Survey R2 |
| 26 | Medical Invoice Generation | Aggregating consultation fees, lab orders, prescribed medicine costs | M4 | Survey R1 |
| 27 | BHYT & Insurance Co-pay Calculation | Applying BHYT discount rates (80%, 100%) and patient co-pay calculations | M4 | Survey R1 |
| 28 | Multi-channel Payment Processing | Cash, Bank Transfer / VietQR generation, insurance settlement | M4 | Survey R1 |
| 29 | Printable Receipt / Invoice View | Formatted HTML/CSS print template with clinic header, itemized breakdown | M4 | Survey R1 |
| 30 | Operational & Financial Reporting | Daily/Monthly revenue charts, patient volume by specialty, doctor performance | M4 | Survey R1 |
| 31 | Receptionist Dashboard & Calendar UI | Fast registration, interactive calendar view, queue list, FAQ assistant | M5 | Survey R3 |
| 32 | Doctor Consultation & AI Workspace UI | Patient queue, AI pre-visit briefing card, examination form, prescription builder | M5 | Survey R3 |
| 33 | Accountant Billing & Cashier UI | Invoice queue, payment modal, VietQR code display, invoice printing | M5 | Survey R3 |
| 34 | Admin Analytics & Governance UI | Analytics charts, user/doctor management, audit log viewer, AI log inspector | M5 | Survey R3 |
| 35 | Docker Containerization & Scripts | Docker Compose (`backend`, `frontend`, `db`, `pgadmin`), `.bat` startup scripts | M6 | Survey R4 |
| 36 | 4 SDLC Milestone Documents | Complete professional Vietnamese SDLC documentation for Stages 1, 2, 3, 4 | M6 | Survey R4 |
| 37 | Automated Multi-Tier Pytest Suite | Pytest suite covering RBAC, conflict detection, PII de-id, AI tools, E2E flows | M0 | Survey R4 |
| 38 | Final Acceptance & Adversarial Hardening | Verification of 100% E2E test pass, stress testing, prompt injection resistance | M-Final | Survey R4 |

---

## Milestones & Execution Plan

| # | Milestone Name | Scope & Deliverables | Dependencies | Status |
|---|----------------|----------------------|--------------|--------|
| **M0** | E2E Testing Suite & Infra | Pytest test framework, fixtures, 4-tier test suites (Tiers 1-4), validation runner | None | DONE |
| **M1** | Backend Base, RBAC & Core Models | FastAPI setup, SQLAlchemy models, JWT auth, RBAC permissions, Seed dataset | None | DONE |
| **M2** | Scheduling, Queue & Clinical Flow | Conflict detection engine, appointment booking, queue, medical records, prescriptions | M1 | DONE |
| **M3** | Administrative AI & Privacy Engine | PII anonymizer, 3 AI tools, Mock/Ollama/Gemini providers, Guardrails, Audit/AI logs | M1, M2 | DONE |
| **M4** | Invoicing, Billing & Analytics | Invoice generation, BHYT co-pay, payment handling, printable receipts, analytics APIs | M1, M2 | DONE |
| **M5** | Modern Frontend SPA | Vite + React + Tailwind + Lucide Icons, 4 role-based portals, AI widgets, print modals | M1, M2, M3, M4 | DONE |
| **M6** | Docker, Scripts & 4 SDLC Docs | Docker Compose, bat scripts, SDLC Stage 1-4 comprehensive markdown reports | M1, M2, M3, M4, M5 | DONE |
| **M-Final** | 100% E2E Pass & Adversarial Hardening | Run all E2E tests, execute Tier 5 adversarial checks, finalize project handoff | M0-M6 | DONE |

---

## Interface Contracts

### 1. Authentication & RBAC
- **Token Format**: Bearer JWT in `Authorization` header.
- **Payload**: `{"sub": user_id, "username": str, "role": "admin"|"receptionist"|"doctor"|"accountant", "exp": timestamp}`.
- **Role Enforcement**:
  - `Admin`: Full access to `/api/v1/users`, `/api/v1/clinics`, `/api/v1/medicines`, `/api/v1/audit`, `/api/v1/stats`.
  - `Receptionist`: Access to `/api/v1/patients`, `/api/v1/appointments`, `/api/v1/queue`, `/api/v1/ai/faq`.
  - `Doctor`: Access to assigned `/api/v1/medical_records`, `/api/v1/prescriptions`, `/api/v1/ai/pre-visit-summary`, `/api/v1/ai/discharge-instructions`.
  - `Accountant`: Access to `/api/v1/invoices`, `/api/v1/payments`, `/api/v1/stats/revenue`.

### 2. Appointment Conflict Detection Contract
```python
def check_appointment_conflict(
    db: Session,
    doctor_id: int,
    clinic_id: int,
    start_time: datetime,
    end_time: datetime,
    exclude_appointment_id: Optional[int] = None
) -> Tuple[bool, Optional[str]]:
    """
    Returns (True, None) if slot is valid and free of conflict.
    Returns (False, "Conflict reason...") if doctor or clinic is already booked.
    """
```

### 3. PII De-identification Engine Contract
```python
class PIIAnonymizer:
    def anonymize(self, text: str, patient_name: Optional[str] = None) -> Tuple[str, Dict[str, str]]:
        """
        Masks Vietnamese phone numbers, 12-digit CCCD/CMND, 15-character BHYT,
        and patient names into tokens like [PHONE_REDACTED], [CCCD_REDACTED], [PATIENT_NAME_REDACTED].
        Returns (anonymized_text, token_mapping).
        """
```

### 4. Administrative AI Service Contract
```python
class AdminAIService:
    def generate_pre_visit_summary(self, patient_history: dict) -> AIResponseSchema:
        """Returns structured summary with allergies, past treatments, and disclaimer."""
    
    def answer_faq(self, query: str) -> AIResponseSchema:
        """Returns workflow guidelines or politely refuses medical diagnosis with disclaimer."""
        
    def generate_discharge_instructions(self, encounter_data: dict) -> AIResponseSchema:
        """Returns medication schedule, home care instructions, follow-up notice and disclaimer."""
```
