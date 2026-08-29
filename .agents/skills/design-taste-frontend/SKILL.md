---
name: design-taste-frontend
description: Clinical precision UI/UX design taste standard, anti-AI-slop philosophy, and high-trust medical ergonomics specification for healthcare web applications.
objective: Establish a rigorous, aesthetic, and functional design standard for healthcare dashboards that eliminates AI visual clutter, ensures 100% WCAG AA accessibility, enforces tabular clinical typography, and delivers responsive tactile interfaces across all 4 clinic roles.
inputs:
  - Role-based user journey specifications (Receptionist, Doctor, Accountant, Admin)
  - Clinical information architecture (Patient queues, Vitals, ICD-10 codes, e-Prescriptions, Invoices, Audit logs)
  - Design tokens (Slate surface scale, Surgical Cerulean brand, Medical Teal accent, Emerald/Amber/Rose semantics)
process:
  - Step 1: Establish 3-tier typography system (Display, Body, Tabular Mono for clinical metrics)
  - Step 2: Configure crisp spatial geometry with 1px tactile borders and subtle surface elevation
  - Step 3: Implement tactile micro-interactions with pressable scales and focus rings
  - Step 4: Construct role-specific medical workflows with high information density
  - Step 5: Embed transparent AI indicators and prominent Medical Disclaimer banners
  - Step 6: Verify WCAG AA color contrast (minimum 4.5:1 ratio) and keyboard navigation accessibility
  - Step 7: Build pixel-perfect CSS print styles for official medical invoices and discharge sheets
rules:
  - Zero AI Slop: strictly forbid saturated neon purple gradients, oversized 32px bubbly cards, and low-contrast grey text
  - All numerical clinical data (Blood pressure, Heart rate, Temp, ICD-10, VNĐ prices) must use tabular monospace fonts
  - Clear visual demarcation between AI-assisted administrative output and physician-signed clinical conclusions
  - High density with visual breathing room: avoid wasted screen space while preserving readability
  - WCAG AA contrast compliance across all interactive elements and text hierarchies
outputs:
  - Production-ready React components with Tailwind CSS utility classes
  - Standardized medical design token dictionary and CSS layers in index.css
  - Responsive dashboards for Receptionist, Doctor, Accountant, and Admin
verification:
  - Lighthouse Accessibility score >= 95 with zero contrast errors
  - Visual inspection ensuring tabular numerals on all tables, vitals, and billing rows
  - Responsive layout validation on 1920x1080 desktop, 1366x768 laptop, and tablet viewports
---

# Quy chuẩn Thiết kế Giao diện Lâm sàng & Gu Thẩm mỹ Y tế (Clinical Precision Frontend Taste Skill)

> **Triết lý Cốt lõi**: Phần mềm y tế là môi trường có tính rủi ro cao và tần suất sử dụng liên tục. Bác sĩ, Lễ tân và Thu ngân làm việc dưới áp lực thời gian và tải nhận thức lớn. Giao diện người dùng phải toát lên **sự tin cậy tuyệt đối, độ chính xác không gian và không có ma sát thị giác (Zero Visual Friction)**. Bài trừ triệt để "AI-Slop" (giao diện cẩu thả do AI tự sinh).

---

## 1. Objective (Mục tiêu Kỹ năng)

1. **Thiết lập Chuẩn Mực Thẩm mỹ Y tế Lâm sàng (Clinical Taste Standard)**: Loại bỏ các mẫu thiết kế sáo rỗng thường thấy của AI (gradient tím neon chói lóa, card bo tròn quá mức làm lãng phí diện tích, chữ xám mờ khó đọc), thay thế bằng phong cách sắc nét, chuyên nghiệp, chuẩn mực y khoa.
2. **Tối ưu Hóa Trình bày Dữ liệu Y khoa & Tài chính (Tabular Figures & High Density)**: Quy chuẩn sử dụng phông chữ đơn cách (Monospace) cho số đo sinh hiệu (Huyết áp, Mạch, Nhiệt độ), mã ICD-10, liều thuốc và số tiền VNĐ nhằm giúp mắt người đọc gióng hàng thẳng cột ngay lập tức.
3. **Trải nghiệm Xúc giác Tinh tế (Tactile Micro-interactions)**: Mang lại cảm giác phản hồi cơ học chính xác khi thao tác trên các nút bấm, ô nhập liệu, danh sách chờ và modal phiếu khám.
4. **Phục vụ Hoàn hảo 4 Luồng Nghiệp vụ Chuyên biệt (Role-Based Workflows)**: Cung cấp bố cục màn hình tối ưu cho 4 nhóm người dùng: Tiếp đón & Lịch hẹn (Lễ tân), Thăm khám & Kê đơn (Bác sĩ), Viện phí & Hóa đơn (Thu ngân), và Quản trị & Giám sát (Admin).
5. **Đạt Chuẩn Tiếp cận Quốc tế (WCAG AA Accessibility)**: Đảm bảo độ tương phản màu sắc >= 4.5:1, hỗ trợ phím tắt và khả năng in ấn hoàn hảo cho tài liệu y tế chính thức.

---

## 2. Terminology & Conceptual Model (Phân định Khái niệm)

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. CODEX (AI Autonomous Agent / Developer)                             │
│    - Lập trình viên AI tuân thủ nghiêm ngặt bảng quy tắc thiết kế      │
│    - Không tự ý thêm thắt các hiệu ứng màu mè làm giảm tính nghiêm túc│
├────────────────────────────────────────────────────────────────────────┤
│ 2. SKILL (Quy trình & Tiêu chuẩn Thủ tục - File này)                   │
│    - Định nghĩa hệ thống Typography 3 tầng, Bảng mã màu Semantic,      │
│      Kích thước hình học (Geometry), Token viền (1px rim) và CSS print │
├────────────────────────────────────────────────────────────────────────┤
│ 3. TOOL (Công cụ Xây dựng & Style Engine)                              │
│    - Tailwind CSS 3.4+, PostCSS, Lucide React Icons, Vite              │
│    - File cấu hình `frontend/tailwind.config.js` & `frontend/index.css`│
├────────────────────────────────────────────────────────────────────────┤
│ 4. MCP / Component Library (Thư viện Thành phần)                       │
│    - Shared Components: `AIPreVisitCard`, `MedicalDisclaimerBadge`,    │
│      `InvoicePrintModal`, `Navbar`, `Sidebar`, `AIChatWidget`          │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Inputs & Prerequisites (Dữ liệu Đầu vào & Điều kiện Tiên quyết)

### 3.1. Dữ liệu Đầu vào
- Các màn hình chức năng thuộc 4 vai trò người dùng trong `frontend/src/pages/`.
- Cấu trúc dữ liệu JSON từ REST API Backend (`/api/v1/...`).
- Danh mục màu sắc và biến thể trong Tailwind CSS.

### 3.2. Tiêu chuẩn Thiết kế Tối thiểu
- Trình duyệt mục tiêu: Chrome, Edge, Safari, Firefox phiên bản hiện đại.
- Độ phân giải tối ưu: Màn hình Desktop phòng khám 1920x1080, Laptop 1366x768, và Tablet 1024x768.

---

## 4. Execution Process (Hệ Quy chuẩn Chi tiết)

### 4.1. Hệ thống Typography 3 Tầng (3-Tier Typography Hierarchy)

| Tầng Phông | Họ Phông (Font Family) | Thuộc tính / Tracking | Trường hợp Sử dụng Cụ thể |
|---|---|---|---|
| **1. Display & Headings** | *Plus Jakarta Sans* / *Inter* | `font-bold tracking-tight` | Tiêu đề phân hệ, Tên phòng khám, Tên bác sĩ, Con số KPI tổng quan |
| **2. Body & Controls** | *Inter* / *system-ui* | `font-medium leading-relaxed` | Nội dung mô tả bệnh án, lời dặn bác sĩ, form nhập liệu, nhãn nút bấm |
| **3. Clinical & Financial Data** | *JetBrains Mono* / *Monospace* | `font-semibold tabular-nums` | **Huyết áp (`120/80 mmHg`)**, **Nhiệt độ (`37.2 °C`)**, **Mã ICD-10 (`J02.9`)**, **Tiền tệ (`150.000 đ`)**, **Số CCCD**, **Mã BHYT** |

```html
<!-- Ví dụ Áp dụng Tabular Numbers trên Sinh hiệu & Viện phí -->
<span class="font-mono font-bold tabular-nums text-slate-900">135/85</span>
<span class="text-xs text-slate-500 ml-1">mmHg</span>

<span class="font-mono font-extrabold tabular-nums text-emerald-600">350.000 ₫</span>
```

### 4.2. Bảng Màu Ngữ nghĩa Y tế (Semantic Medical Palette)

```
Nền & Bề mặt (Surface Tokens):
  Canvas Nền:        #F8FAFC (Slate-50) kèm họa tiết vi chấm tinh tế (Radial dots 30px)
  Card Mặt phẳng:    #FFFFFF kèm viền sắc nét border-slate-200/80 và đổ bóng shadow-sm
  Thanh điều hướng:  #0F172A (Deep Slate-900) tạo độ tương phản cao với vùng làm việc
  Chữ Tiêu đề:       #0F172A (Slate-900) - Tuyệt đối không dùng #000000 đen tuyền
  Chữ Nội dung:      #334155 (Slate-700) và #64748B (Slate-500)

Màu Ngữ nghĩa Chức năng (Semantic Accents):
  Primary Brand:     #0284C7 (Sky-600) -> Xanh Cerulean Phẫu thuật (Tin cậy, Chuyên môn)
  Secondary Accent:  #0D9488 (Teal-600) -> Xanh Lâm sàng (Sức khỏe, Sức sống)
  Success / Paid:    #10B981 (Emerald-500) -> Đã thanh toán, Sinh hiệu bình thường
  Warning / Waiting: #F59E0B (Amber-500) -> Đang chờ khám, Chờ thanh toán
  Critical / Danger: #EF4444 (Rose-500) -> Cảnh báo dị ứng thuốc, Sinh hiệu nguy kịch
  AI Administrative: #6366F1 (Indigo-500) -> Trợ lý AI, Khử định danh PII, Chatbot
```

### 4.3. Cấu trúc Hình học & Độ nổi Bề mặt (Geometry & Elevation)
- **Bo góc (Border Radius)**:
  - Khung Card nghiệp vụ & Modal: `rounded-2xl` (`16px`) hoặc `rounded-xl` (`12px`).
  - Nút bấm, Input, Tag trạng thái: `rounded-lg` (`8px`) hoặc `rounded-md` (`6px`).
  - Avatar, Đèn trạng thái: `rounded-full`.
  - **CẤM**: Dùng `rounded-3xl` hoặc `rounded-[32px]` làm loãng không gian.
- **Viền nổi 1px (1px Inner Rim Light)**:
  - Áp dụng lớp viền phản xạ ánh sáng: `box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.8), 0 1px 2px 0 rgba(15, 23, 42, 0.05)`.
- **Hiệu ứng Kính Mờ (Tactile Glass)**:
  - Header & Modal dùng `backdrop-blur-md bg-white/90 border border-slate-200/80`.

### 4.4. Tương tác Xúc giác Nút bấm (Tactile Micro-interactions)
```jsx
// Nút bấm Tiêu chuẩn Thao tác Lâm sàng
<button 
  className="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-xl text-xs font-bold text-white bg-gradient-to-b from-sky-500 to-sky-600 hover:from-sky-600 hover:to-sky-700 shadow-sm shadow-sky-500/20 active:scale-[0.98] transition-all duration-150 border border-sky-400/30 select-none focus:outline-none focus:ring-2 focus:ring-sky-500/40"
>
  <Stethoscope className="w-4 h-4" />
  Tiếp nhận Khám bệnh
</button>
```

---

## 5. Human-in-the-loop Governance (Kiểm soát Con người & Minh bạch AI)

| Nguyên tắc UI/UX | Quy định Bắt buộc trên Giao diện |
|---|---|
| **Minh bạch AI (AI Provenance)** | Bất kỳ nội dung nào do AI sinh ra (Tóm tắt tiền sử, Dặn dò sau khám, FAQ) đều phải có Huy hiệu `AI-ASSISTED` màu chàm (Indigo) và viền phân biệt rõ ràng với nội dung do người nhập. |
| **Bắt buộc Medical Disclaimer** | Khối cảnh báo `MedicalDisclaimerBadge.jsx` phải luôn hiển thị dưới chân các card AI với nền vàng nhạt `bg-amber-50/80` và biểu tượng `ShieldAlert`. |
| **Xác nhận Trước khi Thực hiện** | Các thao tác quan trọng (Hủy lịch khám, Xóa thuốc khỏi đơn, Xác nhận thanh toán hóa đơn, Hoàn tất ca khám) bắt buộc phải có Modal xác nhận 2 bước. |

---

## 6. Business & Compliance Rules (Ma trận Giao diện theo 4 Vai trò)

### 6.1. Bố cục Màn hình Chuyên biệt cho 4 Vai trò

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. LỄ TÂN (Receptionist Portal):                                       │
│    - Thanh tìm kiếm bệnh nhân nhanh theo CCCD / SĐT / Mã BN            │
│    - Lịch làm việc trực quan (Calendar Grid) hiển thị ca trực bác sĩ   │
│    - Bảng danh sách bệnh nhân chờ tiếp đón trong ngày                  │
├────────────────────────────────────────────────────────────────────────┤
│ 2. BÁC SĨ (Doctor Clinical Workspace):                                 │
│    - Hàng đợi bệnh nhân (Queue list) với thời gian chờ tính theo phút  │
│    - AI Pre-visit Briefing Card với cảnh báo dị ứng thuốc đỏ rực       │
│    - Form ghi sinh hiệu (Huyết áp, Mạch, SpO2) dạng Tabular Numerals   │
│    - Bộ gõ đơn thuốc nhanh với tính toán tổng tiền tự động             │
├────────────────────────────────────────────────────────────────────────┤
│ 3. KẾ TOÁN / THU NGÂN (Accountant Cashier Portal):                     │
│    - Danh sách hóa đơn chờ thu viện phí phân biệt màu sắc              │
│    - Khung tính toán BHYT (Chi phí gốc, BHYT thanh toán, Đồng chi trả) │
│    - Modal tạo mã VietQR tự động kèm nút In Hóa đơn chuyên dụng        │
├────────────────────────────────────────────────────────────────────────┤
│ 4. QUẢN TRỊ VIÊN (Admin Governance & Analytics):                       │
│    - Bảng số liệu KPI doanh thu, lượt khám theo biểu đồ phân tích      │
│    - Bảng điều khiển phân quyền người dùng và ca làm việc bác sĩ      │
│    - Bảng tra cứu Audit Log và AI Invocation Log chi tiết              │
└────────────────────────────────────────────────────────────────────────┘
```

### 6.2. Bảng Đối chiếu Anti-Slop (Những điều CẤM vs BẮT BUỘC)

| Hạng mục | ❌ KIỂU CẨU THẢ (AI-Slop) | ✅ CHUẨN MỰC LÂM SÀNG (Clinic Taste) |
|---|---|---|
| **Nút bấm** | Nút bo tròn hình viên thuốc màu tím neon phát sáng | Nút có viền 1px trên, màu Cerulean/Teal sắc nét, hiệu ứng nhấn lún `active:scale-[0.98]` |
| **Thẻ (Card)** | Thẻ khổng lồ `rounded-3xl p-12` ngập tràn khoảng trắng vô nghĩa | Thẻ `rounded-xl p-5 border border-slate-200/80` mật độ thông tin cao, dễ quét mắt |
| **Bảng dữ liệu** | Bảng không viền, chữ xám mờ trên nền trắng trơn | Bảng có thanh tiêu đề dính (sticky header), số liệu đơn cách `tabular-nums`, hiệu ứng hover hàng |
| **Sinh hiệu y tế** | Viết dạng text thường `Huyết áp: 120/80` | Card đo sinh hiệu chuyên dụng, số lớn in đậm `font-mono`, có icon nhịp tim/nhiệt kế |
| **Cảnh báo AI** | Không ghi chú nguồn gốc hoặc để chữ bé xíu mờ nhạt | Hộp cảnh báo màu hổ phách trang trọng kèm huy hiệu `ADMINISTRATIVE-ONLY` |

---

## 7. Expected Outputs & Deliverables (Sản phẩm Đầu ra)

1. **Bộ CSS Cơ sở & Tiện ích trong `frontend/src/index.css`**:
   - Lớp `.glass-panel`, `.border-rim`, `.btn-tactile`.
   - Cấu hình `@media print` cho bản in hóa đơn y tế và bản dặn dò sau khám.
2. **Hệ thống Component Tương tác Y tế**:
   - `AIPreVisitCard.jsx`: Card tóm tắt bệnh án cho Bác sĩ.
   - `MedicalDisclaimerBadge.jsx`: Huy hiệu cảnh báo y tế chuẩn mực.
   - `InvoicePrintModal.jsx`: Modal xuất hóa đơn viện phí sắc nét.
   - `AIChatWidget.jsx`: Khung chat hỗ trợ thủ tục hành chính thông minh.
3. **Bộ Màn hình Dashboard 4 Vai trò**:
   - `ReceptionistDashboard.jsx`, `DoctorDashboard.jsx`, `AccountantDashboard.jsx`, `AdminDashboard.jsx`.

---

## 8. Verification & Quality Acceptance Criteria (Tiêu chí Nghiệm thu)

### 8.1. Kiểm tra Bản Build Frontend
```bash
cd frontend && npm run build
```

### 8.2. Tiêu chí Chấp thuận (Acceptance Criteria)
- [x] **Không Có Lỗi Build & Warning**: Vite build thành công gói production không có lỗi cú pháp hoặc xung đột Tailwind.
- [x] **100% Tabular Numerals cho Dữ liệu Số**: Toàn bộ chỉ số sinh hiệu, giá tiền VNĐ, mã ICD-10 và thời gian đều áp dụng `tabular-nums font-mono`.
- [x] **Độ Tương Phản WCAG AA**: Mọi văn bản chính đều dùng `text-slate-900` hoặc `text-slate-700`, đạt tỷ lệ tương phản >= 4.5:1 so với nền `#F8FAFC` và `#FFFFFF`.
- [x] **Phản Hồi Xúc Giác Nút Bấm**: Các nút bấm có hiệu ứng lún cơ học mượt mà (`active:scale-[0.98]`).
- [x] **Chế Độ In Ấn Hoàn Hảo**: Khi kích hoạt lệnh in (`window.print()`), chỉ có nội dung phiếu thu/hóa đơn hoặc hướng dẫn sau khám hiển thị, toàn bộ thanh sidebar và navbar tự động ẩn đi.
