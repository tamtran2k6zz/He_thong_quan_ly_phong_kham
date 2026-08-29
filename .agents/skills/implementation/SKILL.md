---
name: implementation
description: Quy chuẩn lập trình sạch (Clean Fullstack Implementation), tuân thủ PEP 8, Pydantic v2 validation, RFC 7807 Error Handling và triết lý thiết kế UI/UX y tế Taste-Skill cho FastAPI & React SPA.
objective: Định hình các chuẩn mực lập trình chuẩn y tế cho Kỹ sư và AI Codex, đảm bảo mã nguồn tinh gọn, an toàn, dễ bảo trì, xử lý ngoại lệ đồng nhất và giao diện lâm sàng công thái học cao.
inputs:
  - Tài liệu đặc tả kiến trúc (docs/architecture.md)
  - Thiết kế CSDL và ORM Models (docs/database-design.md)
  - Quy chuẩn thiết kế giao diện lâm sàng (docs/SKILL.md - Taste-Skill)
  - Danh mục API endpoints và hợp đồng giao tiếp (Interface Contracts)
process:
  - 1. Thiết lập cấu trúc dự án và môi trường thực thi chuẩn hóa
  - 2. Triển khai tầng Backend FastAPI theo Clean Architecture và PEP 8
  - 3. Triển khai tầng Schemas Pydantic v2 với cấu hình from_attributes và validation chặt chẽ
  - 4. Triển khai hệ thống xử lý lỗi tập trung chuẩn RFC 7807 Problem Details
  - 5. Triển khai tầng Frontend React SPA tuân thủ Taste-Skill và Medical Ergonomics
  - 6. Triển khai Axios Interceptors và cơ chế xác thực JWT đồng bộ
  - 7. Triển khai Mock Deterministic AI Provider và Fallback Pipeline
rules:
  - Tuyệt đối không hardcode API Keys, Database Passwords hay JWT Secrets trong mã nguồn
  - Không bao giờ trả về raw ORM entities trực tiếp ở API; bắt buộc qua Pydantic Response Schema
  - Xử lý lỗi không được để lộ stack trace nội bộ ra client; phải trả về mã lỗi và thông báo tiếng Việt
  - Giao diện người dùng phải tuân thủ chuẩn Taste-Skill: Tabular numbers, contrast cao, không AI-slop
outputs:
  - Mã nguồn Backend hoàn chỉnh trong thư mục backend/app/
  - Mã nguồn Frontend hoàn chỉnh trong thư mục frontend/src/
  - Script nạp dữ liệu mẫu backend/app/seed/seed_data.py
verification:
  - Biên dịch Frontend bằng Vite build thành công không lỗi cú pháp hoặc cảnh báo nghiêm trọng
  - Khởi động Backend FastAPI ở chế độ kiểm tra dependencies thành công
  - Xác nhận 100% endpoints có validation Pydantic v2 và bảo vệ bằng RoleChecker
  - Kiểm tra giao diện tuân thủ bảng màu và typography lâm sàng
---

# Kỹ năng Triển khai Mã nguồn Chuẩn Y tế (Implementation Skill)

## 1. Objective (Mục tiêu Kỹ năng)

Kỹ năng này quy định toàn bộ các tiêu chuẩn kỹ thuật, phong cách lập trình (Code Style), mẫu cấu trúc (Design Patterns) và hướng dẫn triển khai mã nguồn cho **Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp Trợ lý AI Hành chính (CMS-AI)**.

Mục tiêu cốt lõi:
1. Đảm bảo mã nguồn Backend (FastAPI + SQLAlchemy 2.0 + Pydantic v2) đạt chuẩn **Clean Architecture**, tuân thủ nghiêm ngặt **PEP 8**, phân tách rõ ràng giữa Schemas, Models, Services và Routers.
2. Đảm bảo mã nguồn Frontend (React 18 + Vite + Tailwind CSS) tuân thủ triết lý **Clinical Taste-Skill**: Tương phản cao, thiết kế bảng dữ liệu tối ưu cho phòng khám, số liệu dùng `tabular-nums font-mono`, loại bỏ hoàn toàn các thành phần đồ họa AI-slop thừa thãi.
3. Chuẩn hóa cơ chế xử lý lỗi theo chuẩn quốc tế **RFC 7807 Problem Details**, cung cấp thông điệp tiếng Việt thân thiện cho người dùng lâm sàng.
4. Triệt tiêu 100% rủi ro hardcode thông tin nhạy cảm (Zero Hardcoded Secrets).

---

## 2. Terminology & Conceptual Model (Mô hình Khái niệm)

Trong không gian Triển khai Mã nguồn:

```
+-----------------------------------------------------------------------------------------------+
|                                    MÔ HÌNH KHÁI NIỆM TRIỂN KHAI                               |
+-----------------------------------------------------------------------------------------------+
|  1. CODEX (AI Agent)         : Kỹ sư Lập trình Fullstack (Fullstack Developer Agent). Thực thi|
|                                viết mã, refactor, tuân thủ Clean Architecture và Taste-Skill. |
|  2. SKILL (Procedural Standard): Quy chuẩn lập trình sạch, cấu trúc thư mục, quy tắc Pydantic,|
|                                xử lý ngoại lệ RFC 7807 và tiêu chuẩn UI y tế (Skill này).      |
|  3. TOOL (Environment Action): Công cụ biên dịch `vite build`, `pytest`, chỉnh sửa file mã    |
|                                nguồn `replace_file_content` / `write_to_file`.                |
|  4. MCP (Model Context Protocol): Giao thức đồng bộ cấu hình môi trường và tài nguyên mã nguồn.|
+-----------------------------------------------------------------------------------------------+
```

---

## 3. Inputs & Prerequisites (Đầu vào & Điều kiện Tiên quyết)

1. **Tài liệu Kiến trúc & CSDL**: `docs/architecture.md` và `docs/database-design.md`.
2. **Quy chuẩn Giao diện Clinical Taste-Skill**: `docs/SKILL.md`.
3. **Môi trường Phát triển**:
   - Python 3.10+ với các thư viện: `fastapi`, `uvicorn`, `sqlalchemy>=2.0`, `pydantic>=2.0`, `passlib[bcrypt]`, `pyjwt`, `httpx`.
   - Node.js 18+ với: `react`, `react-dom`, `react-router-dom`, `vite`, `tailwindcss`, `lucide-react`, `axios`.

---

## 4. Execution Process (Quy trình Thực thi Từng bước)

```
[Bước 1: Cấu trúc Dự án] ---> [Bước 2: Backend Clean Layer] ---> [Bước 3: Pydantic v2 Schemas]
                                                                                |
[Bước 6: Tích hợp API]    <--- [Bước 5: Frontend Taste-Skill]  <--- [Bước 4: Xử lý Lỗi RFC 7807]
           |
           v
[Bước 7: Deterministic Mock AI Provider & Seeding Data]
```

### Bước 1: Thiết lập Cấu trúc Dự án Chuẩn hóa
Tổ chức mã nguồn theo mô hình phân lớp rõ ràng:

```
d:/ICTU/Nam 3/ICTU_2026-2027/Ứng dụng trí tuệ nhân tạo - Project/He_thong_quan_ly_phong_kham/
├── backend/
│   ├── app/
│   │   ├── main.py                  # Entry point, middlewares, exception handlers
│   │   ├── config.py                # Pydantic BaseSettings (.env loading)
│   │   ├── database.py              # Engine, SessionLocal, Base
│   │   ├── models/                  # 14 SQLAlchemy Declarative Models
│   │   ├── schemas/                 # Pydantic v2 In/Out/Filter DTOs
│   │   ├── core/                    # Security, RBAC, Conflict checker
│   │   ├── ai_engine/               # Anonymizer, Guardrails, Providers, Services
│   │   ├── api/v1/                  # REST API Routers per domain
│   │   └── seed/                    # Seed dataset loader
├── frontend/
│   ├── src/
│   │   ├── components/              # Shared Clinical UI components
│   │   ├── context/                 # AuthContext, ToastContext
│   │   ├── pages/                   # Role-based pages (receptionist, doctor, accountant, admin)
│   │   ├── services/                # Axios API services
│   │   └── utils/                   # Formatters (VND, Dates, Vitals)
```

### Bước 2: Triển khai Tầng Backend FastAPI theo Clean Architecture & PEP 8
1. **Dependency Injection**: Tách biệt việc quản lý DB Session và xác thực người dùng:
   ```python
   # backend/app/api/deps.py
   def get_db() -> Generator[Session, None, None]:
       db = SessionLocal()
       try:
           yield db
       finally:
           db.close()
   ```
2. **Kiểm soát Phân quyền RBAC tại Endpoint**:
   ```python
   @router.post("", response_model=MedicalRecordResponse, status_code=status.HTTP_201_CREATED)
   def create_medical_record(
       record_in: MedicalRecordCreate,
       db: Session = Depends(get_db),
       current_user: User = Depends(RoleChecker(["doctor", "admin"]))
   ):
       # Business logic implementation
       return service.create_record(db, record_in, current_user)
   ```

### Bước 3: Triển khai Schemas Pydantic v2 Chuẩn hóa
1. Luôn sử dụng `model_config = ConfigDict(from_attributes=True)` thay cho `class Config: orm_mode = True` cũ.
2. Xác thực định dạng số điện thoại, CCCD và mã BHYT bằng Pydantic `@field_validator`:
   ```python
   from pydantic import BaseModel, Field, field_validator, ConfigDict

   class PatientCreate(BaseModel):
       full_name: str = Field(..., min_length=2, max_length=100)
       phone: str = Field(..., pattern=r'^(?:\+84|0)\d{9,10}$')
       cccd: Optional[str] = Field(None, pattern=r'^\d{9}|\d{12}$')
       bhyt: Optional[str] = Field(None, pattern=r'^[A-Z]{2}\d{13}$')
       date_of_birth: date
       gender: str = Field(..., pattern=r'^(male|female|other)$')
       address: Optional[str] = None
       allergies: Optional[str] = None
       medical_history: Optional[str] = None

       model_config = ConfigDict(from_attributes=True)
   ```

### Bước 4: Triển khai Hệ thống Xử lý Lỗi chuẩn RFC 7807 Problem Details
Định dạng mọi lỗi HTTP trả về thống nhất:
```python
# RFC 7807 Error Response Format
{
  "type": "https://clinic.local/errors/appointment-conflict",
  "title": "Xung đột lịch khám",
  "status": 400,
  "detail": "Bác sĩ Nguyễn Văn A đã có lịch khám trong khoảng thời gian này.",
  "instance": "/api/v1/appointments",
  "timestamp": "2026-08-29T14:00:00Z"
}
```

### Bước 5: Triển khai Tầng Frontend SPA tuân thủ Taste-Skill
1. **Typography 3 Tầng**:
   - Tiêu đề: `font-bold tracking-tight text-slate-900`.
   - Nội dung form/nhãn: `font-medium text-slate-700`.
   - Số liệu y tế, giờ khám, giá tiền VNĐ: `tabular-nums font-mono font-semibold text-slate-900`.
2. **Medical Disclaimer Component (`MedicalDisclaimerBadge.jsx`)**:
   - Luôn hiển thị trên mọi kết quả sinh ra bởi Trợ lý AI với màu hổ phách cảnh báo (`amber-500`), icon `ShieldAlert` rõ ràng.
3. **Tactile Micro-interactions**:
   - Nút bấm có hiệu ứng viền 1px (`ring-1 ring-black/5`), đổ bóng nhẹ (`shadow-sm`), scale khi click (`active:scale-[0.98]`).

### Bước 6: Triển khai Axios Client & Token Management
```javascript
// frontend/src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

### Bước 7: Triển khai Deterministic Mock AI Provider & Seeding Data
1. `MockDeterministicAIProvider` cung cấp kết quả phản hồi quy chuẩn, tức thì, hỗ trợ 100% kịch bản kiểm thử không cần internet.
2. `seed_data.py` nạp đầy đủ danh mục: 5 chuyên khoa, 6 bác sĩ, 15 ca làm việc, 20 danh mục thuốc phổ biến, và 10 hồ sơ bệnh nhân mẫu chuẩn Việt Nam.

---

## 5. Human-in-the-loop Governance (Cơ chế Kiểm soát Con người)

### 5.1. Cổng Kiểm soát Human Gate 2 (Code Review Gate)
Trước khi hợp nhất (merge) bất kỳ thay đổi mã nguồn nào vào nhánh chính:
- Kỹ sư Trưởng (Tech Lead) phải rà soát để đảm bảo không vi phạm: Zero Hardcoded Secrets, Zero Naked Exceptions, và PII Redaction Pipeline.

### 5.2. Danh mục Kiểm tra Thẩm định
- [ ] 1. Toàn bộ mã nguồn Python tuân thủ PEP 8 (được format bằng `black` hoặc `flake8`).
- [ ] 2. Không có biến môi trường hoặc khóa bí mật nào bị gán cứng trong code.
- [ ] 3. Frontend biên dịch `npm run build` không lỗi và không có console warning nghiêm trọng.
- [ ] 4. Tất cả các endpoint đều có phản hồi lỗi định dạng rõ ràng, không trả về raw traceback.

---

## 6. Business & Compliance Rules (Quy tắc Nghiệp vụ & Tuân thủ)

1. **Bảo toàn Transaction Database**: Mọi thao tác ghi nhận khám bệnh kèm kê đơn thuốc và tạo hóa đơn phải nằm trong cùng một Database Transaction. Nếu một bước thất bại, toàn bộ giao dịch phải được `rollback()`.
2. **Khử PII trước khi gọi AI**: Tuyệt đối không được gọi `AIProvider.generate()` với chuỗi text thô chưa chạy qua `PIIAnonymizer.anonymize()`.

---

## 7. Expected Outputs & Deliverables (Tài liệu & Mã nguồn Đầu ra)

1. Toàn bộ mã nguồn Backend trong `backend/app/` (FastAPI, Models, Schemas, Core, AI Engine, API Routers).
2. Toàn bộ mã nguồn Frontend trong `frontend/src/` (Components, Pages, Services, Contexts, Utils).
3. Bộ script nạp dữ liệu mẫu `backend/app/seed/seed_data.py`.

---

## 8. Verification & Quality Acceptance Criteria (Tiêu chí Nghiệm thu Chất lượng)

- **Biên dịch & Khởi chạy (Build & Run)**: Backend khởi động sạch sẽ trên cổng 8000; Frontend Vite đóng gói production thành công ra thư mục `frontend/dist/`.
- **Độ bao phủ Schemas**: 100% Request Payload và Response Body được định kiểu chặt chẽ bằng Pydantic v2.
- **Tính Thẩm mỹ Lâm sàng (Clinical Aesthetics)**: Đạt chuẩn Taste-Skill, hiển thị số liệu y tế rõ nét, có Medical Disclaimer Badge đầy đủ.
