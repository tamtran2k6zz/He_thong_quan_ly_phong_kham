# E2E Test Infra: Clinic Management System with Administrative AI Assistant

## Test Philosophy
- Opaque-box, requirement-driven, medical privacy and RBAC security oriented.
- Zero external network dependencies (powered by Pytest, SQLite in-memory/file test fixture, and Deterministic Offline Mock AI Provider).
- Methodology: Category-Partition + Boundary Value Analysis (BVA) + Pairwise Combinatorial Testing + Real-World Workload Testing.

## Feature Inventory Coverage Matrix
| # | Feature | Requirement Source | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|---------|-------------------|:------:|:------:|:------:|:------:|
| 1 | JWT Auth & Session | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 2 | RBAC Permissions (4 Roles) | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 3 | User Management | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 4 | Specialty & Room Management | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 5 | Doctor & Shift Schedules | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 6 | Patient Profile & Medical ID | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 7 | Seed Dataset Loading | ORIGINAL_REQUEST §R4 | 5 | 5 | ✓ | ✓ |
| 8 | Appointment Booking | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 9 | Time Conflict Detection Engine | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 10 | Appointment Status Lifecycle | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 11 | Reception Queue Management | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 12 | Clinical Encounter & Vitals | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 13 | Service & Lab Orders | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 14 | Medicine Catalog & Stock | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 15 | e-Prescription & Stock Decrement | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 16 | PII Anonymizer (CCCD, Phone, BHYT) | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 17 | Pre-visit Briefing AI Tool | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 18 | Clinic FAQ Chatbot | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 19 | Post-visit Discharge AI | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 20 | Medical Disclaimer Enforcement | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 21 | AI Diagnostic Guardrail | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 22 | Offline Mock AI Fallback | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 23 | External AI Provider Adapter | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 24 | Audit Logging Engine | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 25 | AI Request Logging | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 26 | Medical Invoice Calculation | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 27 | BHYT Co-pay Deduction | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 28 | Multi-channel Payment Processing | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 29 | Printable Receipt Data | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 30 | Clinic Analytics & Reporting | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |

## Test Architecture
- **Framework**: `pytest`, `pytest-asyncio`, `httpx.AsyncClient` / `fastapi.testclient.TestClient`.
- **Test Database**: Isolated SQLite test instance (`test_clinic.db` or memory fixture) seeded with reference staff and catalog data.
- **Execution Command**: `pytest backend/tests -v --tb=short` or `run_tests.bat`.
- **Directory Layout**:
  - `backend/tests/conftest.py`: Database fixtures, auth headers for 4 roles, test data generators.
  - `backend/tests/test_rbac.py`: Tier 1 & 2 tests for JWT and 4-role access restrictions.
  - `backend/tests/test_appointments.py`: Tier 1 & 2 tests for appointment booking, 4-factor conflict detection, time intervals.
  - `backend/tests/test_pii_anonymizer.py`: Tier 1 & 2 tests for Vietnamese phone numbers, 12-digit CCCD, 15-char BHYT, patient names.
  - `backend/tests/test_ai_features.py`: Tier 1, 2, 4 tests for AI Pre-visit summary, FAQ chatbot, Discharge instructions, prompt injection guardrails, disclaimers.
  - `backend/tests/test_clinical_flow.py`: Tier 3 cross-feature clinical workflow (Reception -> Queue -> Consultation -> Prescription -> Invoice -> Payment -> Audit).
  - `backend/tests/test_e2e_scenarios.py`: Tier 4 real-world full clinic operations scenarios.

## Coverage Thresholds
- **Tier 1 (Feature Coverage)**: >= 150 test cases (>= 5 per feature).
- **Tier 2 (Boundary & Corner Cases)**: >= 150 test cases (boundary overlap, negative stock, malformed PII, prompt injections).
- **Tier 3 (Cross-Feature Combinations)**: >= 30 cross-module interaction scenarios.
- **Tier 4 (Real-World Application Scenarios)**: >= 15 end-to-end full patient journeys and security drills.
