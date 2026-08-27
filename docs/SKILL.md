---
name: clinic-taste-skill
description: Anti-slop design taste, UI/UX aesthetics, and robust backend engineering specifications for Healthcare & Clinic Management Systems with AI Integration.
version: 2.0.0
author: Leonxlnx / Taste-Skill Adapted for Healthcare Architecture
---

# 🏥 Clinic Taste-Skill: Anti-Slop Design & Architecture Specification
> *Aesthetic Excellence, High-Trust Medical Ergonomics, and Resilient Fullstack AI Architecture.*

---

## 🧭 I. The Taste Axioms (Anti-Slop Manifesto for Healthcare)

### 1. The Core Philosophy
Healthcare software is **high-stakes and high-frequency**. Doctors, receptionists, and accountants use these interfaces under cognitive load. The UI must convey **unwavering clinical trust, spatial precision, and zero visual friction**.

AI agents often default to **"AI Slop"**:
- ❌ **Saturated purple/neon blue gradient meshes** everywhere.
- ❌ **Oversized bubbly cards** (`rounded-3xl p-12`) with massive wasted whitespace.
- ❌ **Generic centered hero sections** with icons trapped in colorful pastel circles.
- ❌ **Low-contrast gray-on-gray text** that strains clinicians' eyes.
- ❌ **Gimmicky "Magic Wand AI" animations** that distract from clinical workflows.

### 2. The Medical Precision Standard
- ✅ **High Information Density with Visual Breathing Room**: Data-dense tables and queues without clutter.
- ✅ **Tactile 1px Boundaries**: Clean `border border-slate-200/80` or `ring-1 ring-black/5` instead of muddy 20px drop shadows.
- ✅ **Typography as Interface**: Clear contrast, tabular numerals for doses/prices, and monospace accents for ICD-10 codes.
- ✅ **Subtle Atmospheric Depth**: Crisp neutral backdrops (`#F8FAFC`, `#0F172A`), backdrop-blur glass panels (`backdrop-blur-md bg-white/90`), and refined surface elevation.
- ✅ **Ethical & Transparent AI**: Clear provenance, prominent Medical Disclaimers, and explicit PII de-identification badges.

---

## 🎨 II. Frontend Design System (Medical Precision & Tactile UI)

### 1. Typography & Hierarchy System
| Role | Font Family | Weight / Tracking | Use Case |
|---|---|---|---|
| **Display / Headings** | *Plus Jakarta Sans* / *Inter* | `font-bold tracking-tight` | Module titles, Doctor name headers, Stat figures |
| **Body & UI Controls** | *Inter* / *system-ui* | `font-medium leading-relaxed` | Patient details, medical notes, form inputs, buttons |
| **Clinical & Financial Data** | *JetBrains Mono* / *Monospace* | `font-semibold tabular-nums` | ICD-10 codes, Drug dosages, Timestamps, Currency (VNĐ), CCCD/BHYT IDs |
| **Eyebrow / Status Labels** | *Inter* | `uppercase tracking-wider text-[10px] font-bold` | Category chips, Table headers, Audit tags |

#### Typography Rules:
- **No pure black text**: Use `text-slate-900` (`#0F172A`) for primary headers and `text-slate-600` for secondary descriptions.
- **Tabular figures**: Always apply `tabular-nums font-mono` to numbers in tables, prices, and vitals (`140/90 mmHg`, `37.2 °C`, `185,000 đ`).
- **Contrast**: Maintain a minimum 4.5:1 contrast ratio for all medical information.

---

### 2. Color Palette & Semantic Intent

```
Clinical Surface Tokens:
  Canvas (Light):     #F8FAFC (Slate-50)
  Surface (Card):     #FFFFFF with border #E2E8F0 (Slate-200)
  Sidebar / Topbar:   #0F172A (Deep Slate-900) or #FFFFFF with backdrop blur
  Text Primary:       #0F172A (Slate-900)
  Text Muted:         #64748B (Slate-500)

Semantic Medical Accents:
  Primary Brand:      #0284C7 (Sky-600) -> Surgical Cerulean (Trust, Modernity)
  Secondary Accent:   #0D9488 (Teal-600) -> Medical Clinical Green (Health, Vitality)
  Success / Paid:     #10B981 (Emerald-500) -> Verified, Completed, Normal Vitals
  Warning / Waiting:  #F59E0B (Amber-500) -> In Queue, Pending Payment, Moderate Risk
  Critical / Allergy: #EF4444 (Rose-500) -> Drug Allergies, Emergency, Severe Vitals
  AI Administrative:  #6366F1 (Indigo-500) -> AI Briefing, Chatbot, De-identification
```

---

### 3. Spatial Geometry & Surface Elevation
- **Border Radius Discipline**: 
  - Standard cards & modals: `rounded-2xl` (`16px`) or `rounded-xl` (`12px`).
  - Small tags, chips & inputs: `rounded-lg` (`8px`).
  - Circular avatars & status dots: `rounded-full`.
  - Avoid cartoonish `rounded-[32px]` on enterprise dashboards.
- **Surface Elevation**:
  - Base layer: `bg-slate-50/50`.
  - Card layer: `bg-white border border-slate-200/80 shadow-sm hover:shadow transition-shadow duration-200`.
  - Floating Popover / Modal: `bg-white/95 backdrop-blur-xl border border-slate-200/80 shadow-2xl shadow-slate-900/10`.
- **Inner Rim Light (Subtle Highlight)**:
  - Add a 1px top highlight for cards: `ring-1 ring-black/[0.04]`.

---

### 4. Component Design Patterns

#### A. The Clinical Stat Card (Stat Card)
```jsx
<div className="group relative overflow-hidden rounded-2xl bg-white p-5 border border-slate-200/80 shadow-sm hover:shadow-md transition-all duration-200">
  <div className="flex items-center justify-between">
    <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Hôm nay</span>
    <span className="p-2 rounded-xl bg-sky-50 text-sky-600 group-hover:scale-110 transition-transform">
      <Users className="w-4 h-4" />
    </span>
  </div>
  <div className="mt-3">
    <div className="text-2xl font-extrabold text-slate-900 font-display tabular-nums tracking-tight">
      128 <span className="text-xs font-medium text-slate-400">lượt</span>
    </div>
    <div className="mt-1 flex items-center gap-1.5 text-xs text-emerald-600 font-semibold">
      <TrendingUp className="w-3.5 h-3.5" /> +14.2% so với hôm qua
    </div>
  </div>
</div>
```

#### B. The Medical Disclaimer & AI Badge
```jsx
<div className="rounded-xl border border-amber-200/80 bg-amber-50/70 p-3.5 text-xs text-amber-900 flex items-start gap-3 backdrop-blur-sm">
  <ShieldAlert className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
  <div className="space-y-0.5">
    <div className="font-bold flex items-center gap-1.5">
      CẢNH BÁO AN TOÀN Y TẾ & GIỚI HẠN AI
      <span className="px-1.5 py-0.5 rounded text-[10px] bg-amber-200/80 font-mono font-bold text-amber-900">
        ADMINISTRATIVE-ONLY
      </span>
    </div>
    <p className="text-[11px] text-amber-800 leading-relaxed">
      Nội dung do Trợ lý AI tổng hợp mang tính chất hỗ trợ hành chính và đối chiếu hồ sơ. AI không thay thế chẩn đoán chuyên môn của bác sĩ phụ trách.
    </p>
  </div>
</div>
```

#### C. Tactile Button Micro-interactions
```jsx
<button className="relative inline-flex items-center justify-center gap-2 px-4 py-2 rounded-xl text-xs font-bold text-white bg-gradient-to-b from-sky-500 to-sky-600 hover:from-sky-600 hover:to-sky-700 shadow-sm shadow-sky-500/20 active:scale-[0.98] transition-all duration-150 border border-sky-400/30">
  <Stethoscope className="w-4 h-4" />
  Bắt đầu khám bệnh
</button>
```

---

## ⚙️ III. Backend Architecture Taste & Standards (FastAPI + SQLAlchemy)

### 1. RESTful Domain Hierarchy & Clean Layering
```
backend/app/
├── api/v1/          # Pure HTTP Layer: Route definitions, input validation, status codes
├── core/            # Security (JWT, bcrypt), RBAC dependencies, Conflict Detection engine
├── models/          # SQLAlchemy Declarative Models (Relations, ForeignKeys, Indexes)
├── schemas/         # Pydantic V2 Models (Separation: Request vs Response vs InDB)
├── services/        # Domain Business Logic & AI Multi-Provider Service Layer
└── seed/            # Seed data loader with deterministic medical data
```

### 2. The 5 Backend Architectural Axioms
1. **Explicit Schemas Everywhere**: Never return raw ORM entities directly. Always use typed `response_model=List[PatientResponse]` with `model_config = ConfigDict(from_attributes=True)`.
2. **Zero Naked Exceptions**: Catch domain errors cleanly and return RFC 7807 structured HTTP responses with actionable Vietnamese error messages.
3. **RBAC at Endpoint Level**: Enforce role checks at the dependency injection level (`dependencies=[Depends(require_role(["doctor", "admin"]))]`).
4. **Data Redaction Pipeline Before AI**:
   - All AI calls must pass through `PIIAnonymizer.anonymize_text()`.
   - Strip Name, Phone, National ID (CCCD), Address, Health Insurance numbers.
5. **Deterministic Offline Fallback**:
   - Every AI service must support `MockProvider` so test suites and local demos work 100% offline without external API keys.

---

## 📋 IV. Agent Execution Checklist (What to Do vs What NOT to Do)

| Domain | ❌ What AI Agents Must STOP Doing (Slop) | ✅ What AI Agents MUST ALWAYS Do (Taste) |
|---|---|---|
| **Buttons** | Flat purple pill with blurry gradient glow | Crisp 1px top border, solid high-contrast fill, tactile active press scale |
| **Cards** | Giant `rounded-3xl` cards with empty white space | Compact `rounded-2xl` cards with crisp border, micro-header, and tabular figures |
| **Tables** | Unbordered plain text with standard scrollbars | Sticky header, hover row highlight, subtle alternating tint, mono font on IDs/prices |
| **Navigation** | Clunky desktop navigation with text links only | Clean sidebar with active indicator pill, role badge, icon + label pairing, breadcrumb |
| **Modals** | Plain white box with hard shadow | Backdrop blur (`backdrop-blur-md bg-slate-900/40`), smooth entrance animation, clear header/footer separation |
| **AI Output** | Raw unformatted markdown dump | Structured cards with badge tags, key-value grids, and embedded medical safety disclaimer |
| **Forms** | Huge spaced out inputs with floating labels | Grouped fieldsets, clear label with optional subtext, subtle focus ring, inline error state |

---

## 🎯 V. How to Use this Skill

When modifying or generating code in this repository:
1. **For Frontend**: Follow the Typography, Color Tokens, and Tactile Component recipes outlined in Section II.
2. **For Backend**: Adhere to the Pydantic separation, RBAC guards, and PII anonymization pipeline defined in Section III.
3. **For Testing**: Ensure all 223+ test cases pass and new features maintain 100% test coverage and audit logging.
