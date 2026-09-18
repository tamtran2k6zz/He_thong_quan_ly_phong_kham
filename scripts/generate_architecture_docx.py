# -*- coding: utf-8 -*-
"""
Script tạo file Word (.docx) Tài Liệu Thiết Kế Kiến Trúc Hệ Thống Toàn Diện
cho Nhóm 07 - Hệ thống quản lý phòng khám có tích hợp AI (CMS-AI).
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    """Đặt màu nền cho ô trong bảng"""
    tc_pr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tc_pr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    """Đặt lề trong cho ô của bảng"""
    tc_pr = cell._element.get_or_add_tcPr()
    tc_mar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tc_mar.append(node)
    tc_pr.append(tc_mar)

def format_row(row, bg_hex, text_color, bold=False, is_header=False):
    """Định dạng cho toàn bộ hàng trong bảng"""
    for cell in row.cells:
        set_cell_background(cell, bg_hex)
        set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        for p in cell.paragraphs:
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.color.rgb = text_color
                run.font.bold = bold
                if is_header:
                    run.font.size = Pt(10)
                    run.font.bold = True
                else:
                    run.font.size = Pt(9.5)

def add_code_block(doc, text):
    """Thêm một khối code hoặc sơ đồ kiến trúc với nền xám nhạt"""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F1F5F9")  # Slate 100
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_h1(doc, text):
    h = doc.add_heading(level=1)
    h.paragraph_format.space_before = Pt(16)
    h.paragraph_format.space_after = Pt(6)
    r = h.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(13, 148, 136) # Teal 600
    return h

def add_h2(doc, text):
    h = doc.add_heading(level=2)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    r = h.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
    return h

def add_h3(doc, text):
    h = doc.add_heading(level=3)
    h.paragraph_format.space_before = Pt(8)
    h.paragraph_format.space_after = Pt(2)
    r = h.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(30, 41, 59) # Slate 800
    return h

def build_docx():
    doc = docx.Document()

    # Thiết lập lề 1.0 inch (2.54 cm)
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
        # Header & Footer
        footer = s.footer
        p_ft = footer.paragraphs[0]
        p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_ft = p_ft.add_run("TÀI LIỆU THIẾT KẾ KIẾN TRÚC HỆ THỐNG — NHÓM 07 — ĐINH GIA BẢO & TRẦN ĐẶNG CÔNG TÂM")
        r_ft.font.name = "Times New Roman"
        r_ft.font.size = Pt(8.5)
        r_ft.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # TRANG BÌA VÀ THÔNG TIN DỰ ÁN
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO — TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ TRUYỀN THÔNG\nKHOA CÔNG NGHỆ THÔNG TIN")
    r_inst.font.name = "Times New Roman"
    r_inst.font.size = Pt(11)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(71, 85, 105)
    p_inst.paragraph_format.space_after = Pt(24)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_title.add_run("TÀI LIỆU THIẾT KẾ KIẾN TRÚC HỆ THỐNG (ARCHITECTURE SPECIFICATION)\n")
    r_t1.font.name = "Times New Roman"
    r_t1.font.size = Pt(16)
    r_t1.font.bold = True
    r_t1.font.color.rgb = RGBColor(13, 148, 136) # Teal 600

    r_t2 = p_title.add_run("HỆ THỐNG QUẢN LÝ PHÒNG KHÁM CÓ TÍCH HỢP AI (CMS-AI)")
    r_t2.font.name = "Times New Roman"
    r_t2.font.size = Pt(17)
    r_t2.font.bold = True
    r_t2.font.color.rgb = RGBColor(15, 23, 42)
    p_title.paragraph_format.space_after = Pt(20)

    # Bảng thông tin nhóm và thời gian thực hiện
    info_table = doc.add_table(rows=4, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_table.autofit = False
    info_table.columns[0].width = Inches(2.2)
    info_table.columns[1].width = Inches(4.3)
    
    rows_data = [
        ("Nhóm thực hiện:", "Nhóm 07"),
        ("Thành viên nhóm:", "1. Đinh Gia Bảo (Trưởng nhóm — Architecture & AI Lead)\n2. Trần Đặng Công Tâm (Thành viên — Fullstack Dev & QA Lead)"),
        ("Tên ứng dụng:", "Hệ thống quản lý phòng khám có tích hợp AI (CMS-AI)"),
        ("Thời gian thực hiện:", "Từ 27/07/2026 đến 27/09/2026 (9 tuần)")
    ]
    for idx, (label, val) in enumerate(rows_data):
        row = info_table.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        set_cell_background(cell_lbl, "F8FAFC")
        set_cell_background(cell_val, "FFFFFF")
        set_cell_margins(cell_lbl, 80, 80, 120, 120)
        set_cell_margins(cell_val, 80, 80, 120, 120)
        
        p1 = cell_lbl.paragraphs[0]
        r1 = p1.add_run(label)
        r1.font.name = "Times New Roman"
        r1.font.bold = True
        r1.font.size = Pt(10)
        
        p2 = cell_val.paragraphs[0]
        r2 = p2.add_run(val)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(10)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(20)

    # =========================================================================
    # PHẦN 1: TỔNG QUAN KIẾN TRÚC PHÂN TẦNG (SYSTEM LAYERED ARCHITECTURE)
    # =========================================================================
    add_h1(doc, "1. KIẾN TRÚC PHÂN TẦNG TỔNG THỂ (SYSTEM LAYERED ARCHITECTURE)")
    p = doc.add_paragraph()
    p.add_run("Hệ thống CMS-AI được xây dựng theo mô hình ")
    p.add_run("Kiến trúc Phân tầng Hướng Dịch vụ (Service-Oriented Layered Architecture)").font.bold = True
    p.add_run(", phân tách độc lập giữa Tầng Trình diễn (Client Presentation), Cổng API & Bảo mật (API Gateway), Nghiệp vụ Lâm sàng (Core Business Services), Trợ lý AI Hành chính 3 Lớp (AI Engine) và Lưu trữ CSDL (Persistence Layer).")

    add_code_block(doc,
"""+---------------------------------------------------------------------------------------------------+
|                           MÔ HÌNH KIẾN TRÚC PHÂN TẦNG HỆ THỐNG CMS-AI                            |
+---------------------------------------------------------------------------------------------------+
  [TẦNG CLIENT - React 18 SPA + Vite + Tailwind CSS]
    ├── Receptionist Dashboard (Tiếp đón, Đặt lịch, Xếp hàng)
    ├── Doctor Workspace (Bàn khám EMR, Sinh hiệu, ICD-10, Kê đơn)
    ├── Accountant Portal (Viện phí, Khấu trừ BHYT, VietQR Napas247)
    ├── Admin Governance (Quản trị người dùng, Kho dược, Audit Logs)
    └── Patient Chatbot (Hỏi đáp quy trình, BHYT, Bảng giá)
           │
           │ HTTPS / REST API / JSON Payload / Bearer JWT Token
           ▼
  [TẦNG CỔNG API & BẢO MẬT - FastAPI ASGI Gateway]
    ├── CORS Policy Middleware (Kiểm soát nguồn gốc tin cậy)
    ├── Security & JWT Token Validator (Giải mã chữ ký HS256)
    ├── RBAC RoleChecker Middleware (Admin, Receptionist, Doctor, Accountant)
    └── FastAPI v1 REST Routers (Pydantic v2 Strict Validation)
           │
           ▼
  [TẦNG DỊCH VỤ NGHIỆP VỤ LÂM SÀNG - Core Business Services]
    ├── Authentication & User Service (Băm bcrypt salt 12 vòng)
    ├── Appointment & Shift Service (Quản lý lịch hẹn ca trực)
    ├── Conflict Detection Engine (Thuật toán toán học Interval Overlap O(1))
    ├── Consultation & EMR Service (Bệnh án điện tử, Tự động tính BMI)
    ├── e-Prescription & Pharmacy Service (Kê đơn, Cảnh báo dị ứng, Trừ tồn kho)
    └── Billing & VietQR Service (Tổng hợp chi phí, Giảm trừ BHYT, QR động)
           │                                          │
           │ Gọi trợ lý hỗ trợ                        │ Truy xuất dữ liệu
           ▼                                          ▼
  [TẦNG TRỢ LÝ AI HÀNH CHÍNH 3 LỚP]          [TẦNG DỮ LIỆU CSDL]
    ├── Lớp 1: PII Anonymizer (Regex Masking)  ├── SQLAlchemy 2.0 ORM Engine
    ├── Lớp 2: Medical Guardrails & Disclaimer ├── MySQL 8.0 (14 Bảng 3NF, B-Tree)
    ├── Lớp 3: Gemini Live & Offline Mock      └── Audit Logs & AI Invocation Logs
    └── Lớp 4: AI Invocation Logger
+---------------------------------------------------------------------------------------------------+""")

    # =========================================================================
    # PHẦN 2: KIẾN TRÚC TRIỂN KHAI HẠ TẦNG DOCKER (DEPLOYMENT ARCHITECTURE)
    # =========================================================================
    add_h1(doc, "2. KIẾN TRÚC TRIỂN KHAI HẠ TẦNG DOCKER (DEPLOYMENT & INFRASTRUCTURE)")
    p = doc.add_paragraph()
    p.add_run("Toàn bộ giải pháp được đóng gói thành hệ sinh thái các Container Docker độc lập thông qua file ")
    p.add_run("docker-compose.yml").font.bold = True
    p.add_run(", vận hành trên mạng ảo bridge cách ly an toàn (`clinic_net`):")

    add_code_block(doc,
"""+---------------------------------------------------------------------------------------------------+
|                        MÔ HÌNH TRIỂN KHAI CONTAINER DOCKER (DOCKER-COMPOSE)                       |
+---------------------------------------------------------------------------------------------------+
  [Người Dùng Trình Duyệt Web]                     [Quản Trị Viên MySQL Workbench]
             │ Port 3001, 5173 / HTTP                            │ Port 3307 / TCP
             ▼                                                   ▼
  +─────────────────────────+                         +─────────────────────────+
  | Container: clinic_frontend |                         | Container: clinic_mysql |
  | - Image: Nginx Alpine   |                         | - Image: MySQL 8.0      |
  | - Port nội bộ: 3000     |                         | - Port nội bộ: 3306     |
  | - SPA Static Assets     |                         | - Volume: mysql_data    |
  +─────────────────────────+                         | - Database: clinic_db   |
             │                                        +─────────────────────────+
             │ Gọi REST API nội bộ                               ▲
             ▼ Port 8000 / HTTP                                  │ Kết nối ORM
  +──────────────────────────────────────────────────────────────┴──────+
  | Container: clinic_backend (FastAPI + Uvicorn Python 3.10+)          |
  | - REST API Endpoints v1                                             |
  | - Conflict Detection Algorithm                                      |
  | - Offline Deterministic Mock AI Engine                              |
  +─────────────────────────────────────────────────────────────────────+
             │                                        │
             │ HTTPS TLS 1.3 / Port 443               │ HTTP CDN / Port 443
             ▼ Payload đã Khử 100% PII                ▼
  [Cloud: Google Gemini Live API]             [Cloud: VietQR Napas247 CDN]
+---------------------------------------------------------------------------------------------------+""")

    p_net = doc.add_paragraph()
    p_net.add_run("Bảng phân bổ cổng mạng và cấu hình dịch vụ trong hệ sinh thái Docker:")
    p_net.runs[0].font.italic = True

    port_table_data = [
        ("Dịch vụ Container", "Hình ảnh Image", "Cổng Máy Chủ (Host)", "Cổng Nội Bộ (Container)", "Giao thức"),
        ("clinic_frontend", "nginx:alpine", "3001, 5173", "3000", "HTTP / Web SPA"),
        ("clinic_backend", "FastAPI Python 3.10+", "8000", "8000", "HTTP / REST API"),
        ("clinic_mysql", "mysql:8.0", "3307", "3306", "TCP / MySQL Protocol"),
        ("Google Gemini API", "Cloud Endpoint", "443 (Outbound)", "443", "HTTPS / TLS 1.3"),
        ("VietQR Gateway", "Cloud CDN", "443 (Outbound)", "443", "HTTPS / REST")
    ]
    tbl_p = doc.add_table(rows=len(port_table_data), cols=5)
    tbl_p.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_p.columns[0].width = Inches(1.5)
    tbl_p.columns[1].width = Inches(1.5)
    tbl_p.columns[2].width = Inches(1.3)
    tbl_p.columns[3].width = Inches(1.3)
    tbl_p.columns[4].width = Inches(0.9)
    for idx, (c1, c2, c3, c4, c5) in enumerate(port_table_data):
        row = tbl_p.rows[idx]
        row.cells[0].text, row.cells[1].text, row.cells[2].text, row.cells[3].text, row.cells[4].text = c1, c2, c3, c4, c5
        if idx == 0:
            format_row(row, "0D9488", RGBColor(255, 255, 255), is_header=True)
        else:
            format_row(row, "FFFFFF" if idx % 2 == 1 else "F8FAFC", RGBColor(30, 41, 59))
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # =========================================================================
    # PHẦN 3: KIẾN TRÚC TRỢ LÝ AI HÀNH CHÍNH 3 LỚP (AI ENGINE ARCHITECTURE)
    # =========================================================================
    add_h1(doc, "3. KIẾN TRÚC ĐỘNG CƠ TRỢ LÝ AI HÀNH CHÍNH 3 LỚP (AI ENGINE ARCHITECTURE)")
    p = doc.add_paragraph()
    p.add_run("Để đảm bảo tuân thủ nghiêm ngặt ")
    p.add_run("Nghị định 13/2023/NĐ-CP").font.bold = True
    p.add_run(" về bảo vệ dữ liệu cá nhân y tế và quy chuẩn đạo đức y tế, động cơ AI được thiết kế theo mô hình 3 lớp khép kín với cơ chế phòng vệ chuyên sâu:")

    add_code_block(doc,
"""+---------------------------------------------------------------------------------------------------+
|                        MÔ HÌNH ĐỘNG CƠ TRỢ LÝ AI HÀNH CHÍNH 3 LỚP BẢO VỆ                         |
+---------------------------------------------------------------------------------------------------+
  Yêu cầu từ Bác sĩ / Tiếp đón / Bệnh nhân
    │
    ▼
  [LỚP 1: BẢO VỆ DỮ LIỆU & KHỬ ĐỊNH DANH - PII ANONYMIZATION]
    ├── Quét biểu thức chính quy Regex 12 chữ số: CCCD -> [CCCD_REDACTED]
    ├── Quét biểu thức chính quy Regex 10 chữ số: Số điện thoại -> [PHONE_REDACTED]
    ├── Quét biểu thức chính quy Regex 15 ký tự: Thẻ BHYT -> [BHYT_REDACTED]
    └── Lưu bảng ánh xạ tạm thời trên bộ nhớ RAM (Token Mapping Cache)
    │
    ▼
  [LỚP 2: BỘ LỌC ĐẠO ĐỨC Y TẾ & GUARDRAILS BẢO MẬT]
    ├── Chặn yêu cầu tự chẩn đoán bệnh học: "Tôi bị bệnh gì", "Kê đơn cho tôi" -> Từ chối lập tức
    ├── Chặn tấn công Prompt Injection / System Prompt Jailbreak -> Ghi nhận cảnh báo bảo mật
    └── Kiểm tra phạm vi dữ liệu: Chỉ cho phép xử lý quy trình, tóm tắt và hướng dẫn dặn dò
    │
    ▼
  [LỚP 3: ĐIỀU PHỐI ĐA NHÀ CUNG CẤP & DỰ PHÒNG NGOẠI TUYẾN - MULTI-PROVIDER]
    ├── Khi Online & Có API Key: Kết nối Google Gemini 3.6 Flash Live API (Hiệu năng cao)
    └── Khi Offline / Mất kết nối: Tự động Fallback sang Deterministic Rule-Based Mock Engine
    │
    ▼
  [LỚP 4: KIỂM TOÁN VÀ CHUẨN HÓA KẾT QUẢ - OUTPUT SANITIZATION]
    ├── Gắn Tuyên bố Miễn trừ Trách nhiệm Y tế bắt buộc (Medical Disclaimer)
    ├── Khôi phục lại ngữ cảnh hiển thị nội bộ cho bác sĩ (Deanonymize từ RAM)
    └── Ghi nhật ký kiểm toán vĩnh viễn vào bảng ai_invocation_logs
+---------------------------------------------------------------------------------------------------+""")

    # =========================================================================
    # PHẦN 4: KIẾN TRÚC LUỒNG DỮ LIỆU LÂM SÀNG END-TO-END (CLINICAL WORKFLOW)
    # =========================================================================
    add_h1(doc, "4. KIẾN TRÚC LUỒNG DỮ LIỆU LÂM SÀNG END-TO-END (CLINICAL WORKFLOW)")
    p = doc.add_paragraph()
    p.add_run("Biểu đồ trình tự (Sequence Flow) mô tả quy trình nghiệp vụ lâm sàng khép kín từ lúc người bệnh đến tiếp đón, vào phòng khám của bác sĩ, kê đơn, thanh toán viện phí đến khi nhận hướng dẫn dặn dò xuất viện:")

    add_code_block(doc,
"""+---------------------------------------------------------------------------------------------------+
|                        QUY TRÌNH NGHIỆP VỤ LÂM SÀNG KHÉP KÍN (END-TO-END)                         |
+---------------------------------------------------------------------------------------------------+
  (1) GIAI ĐOẠN TIẾP ĐÓN & ĐẶT LỊCH:
      Bệnh nhân -> Lễ tân -> Frontend -> POST /api/v1/appointments
      FastAPI kích hoạt ConflictChecker kiểm tra trùng lịch (Start_A < End_B && End_A > Start_B):
      - Nếu trùng lịch bác sĩ / phòng khám -> Báo lỗi 409 Conflict, gợi ý khung giờ khác.
      - Nếu hợp lệ -> Ghi CSDL bảng appointments (status='CHECKED_IN'), cấp số hàng đợi.

  (2) GIAI ĐOẠN KHÁM BỆNH & TỔNG HỢP EMR:
      Bác sĩ mở ca khám -> Frontend gọi GET /api/v1/ai/pre-visit-summary/{patient_id}
      Backend lấy lịch sử khám cũ -> Khử PII -> AI Engine tóm tắt trong 10 giây & cảnh báo dị ứng.
      Bác sĩ nhập sinh hiệu (Tự tính BMI) -> Chẩn đoán mã ICD-10 -> Kê đơn thuốc (Kiểm tra kho).
      Bác sĩ bấm "Hoàn thành ca khám" -> Cập nhật medical_records (COMPLETED), trừ tồn kho,
      tự động tạo hóa đơn viện phí bảng invoices (payment_status='PENDING').

  (3) GIAI ĐOẠN THANH TOÁN VIỆN PHÍ VIETQR:
      Kế toán mở hóa đơn -> Hệ thống tổng hợp: Tiền khám + Cận lâm sàng + Thuốc - Giảm trừ BHYT.
      Frontend sinh mã VietQR Napas247 động với số tiền chính xác -> Bệnh nhân quét mã chuyển khoản.
      Thu ngân bấm "Xác nhận thanh toán" -> Cập nhật invoices (payment_status='PAID'), in biên lai.

  (4) GIAI ĐOẠN HƯỚNG DẪN SAU KHÁM (AI DISCHARGE):
      Bác sĩ gọi POST /api/v1/ai/discharge-instructions -> AI tự động sinh bảng chia lịch uống thuốc
      (Sáng/Trưa/Chiều/Tối), chế độ dinh dưỡng, dấu hiệu cấp cứu cần tái khám kèm Medical Disclaimer.
      Bác sĩ duyệt nội dung trên màn hình và in phát cho bệnh nhân.
+---------------------------------------------------------------------------------------------------+""")

    # =========================================================================
    # PHẦN 5: BỘ QUYẾT ĐỊNH KIẾN TRÚC ADR (ARCHITECTURE DECISION RECORDS)
    # =========================================================================
    add_h1(doc, "5. BỘ HỒ SƠ QUYẾT ĐỊNH KIẾN TRÚC (ARCHITECTURE DECISION RECORDS - ADR)")
    p = doc.add_paragraph()
    p.add_run("Các quyết định kỹ thuật then chốt đã được phê duyệt và lưu vết tại tài liệu ")
    p.add_run("docs/architecture-decisions.md").font.bold = True
    p.add_run(":")

    adrs_data = [
        ("Mã ADR", "Tiêu đề Quyết định", "Lựa chọn Kỹ thuật", "Lý do & Đánh đổi Kiến trúc"),
        ("ADR-001", "Kiến trúc Phân tầng Backend", "FastAPI + Clean Architecture", "Độ trễ thấp < 15ms, sinh tài liệu Swagger UI tự động, phân tách nghiệp vụ độc lập."),
        ("ADR-002", "Mô hình Phân quyền RBAC", "Role-Based Access Control (4 Roles)", "Admin, Lễ tân, Bác sĩ, Kế toán; kiểm soát truy cập nghiêm ngặt tại cấp Router/API."),
        ("ADR-003", "Giải thuật Chống trùng lịch", "Interval Overlap Algorithm", "Phát hiện chồng lấn thời gian hai chiều (Bác sĩ & Phòng khám) độ phức tạp O(1)."),
        ("ADR-004", "Bảo vệ Quyền riêng tư PII", "In-Memory Regex De-identification", "Khử 100% CCCD, SĐT, BHYT trước khi gửi ra Cloud; tuân thủ Nghị định 13/2023/NĐ-CP."),
        ("ADR-005", "Kiến trúc AI Ngoại tuyến", "Deterministic Mock Fallback", "Tự động kích hoạt khi mất internet; đảm bảo phòng khám vận hành 100% không gián đoạn."),
        ("ADR-006", "Thiết kế Giao diện Lâm sàng", "React 18 + Tailwind Taste-Skill", "Thiết kế công thái học y tế: phông chữ 3 tầng, tabular-nums sinh hiệu, không AI-slop."),
        ("ADR-007", "Thanh toán Viện phí Động", "Chuẩn VietQR Napas247", "Sinh mã QR chuyển khoản ngân hàng chính xác số tiền và nội dung hóa đơn trong 1 giây."),
        ("ADR-008", "Đóng gói Triển khai", "Docker Compose Multi-Container", "Đóng gói 4 container đồng bộ: Frontend Nginx, Backend Uvicorn, CSDL MySQL 8.0.")
    ]
    tbl_a = doc.add_table(rows=len(adrs_data), cols=4)
    tbl_a.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_a.columns[0].width = Inches(1.1)
    tbl_a.columns[1].width = Inches(1.8)
    tbl_a.columns[2].width = Inches(1.8)
    tbl_a.columns[3].width = Inches(1.8)
    for idx, (c1, c2, c3, c4) in enumerate(adrs_data):
        row = tbl_a.rows[idx]
        row.cells[0].text, row.cells[1].text, row.cells[2].text, row.cells[3].text = c1, c2, c3, c4
        if idx == 0:
            format_row(row, "0D9488", RGBColor(255, 255, 255), is_header=True)
        else:
            format_row(row, "FFFFFF" if idx % 2 == 1 else "F8FAFC", RGBColor(30, 41, 59))
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # =========================================================================
    # KÝ TÊN VÀ XÁC NHẬN CỦA NHÓM 07
    # =========================================================================
    doc.add_paragraph().paragraph_format.space_after = Pt(20)
    sign_table = doc.add_table(rows=2, cols=2)
    sign_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sign_table.columns[0].width = Inches(3.2)
    sign_table.columns[1].width = Inches(3.3)
    
    c_left = sign_table.cell(0, 0)
    c_right = sign_table.cell(0, 1)
    
    p_l = c_left.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l.add_run("THÀNH VIÊN NHÓM 07\n(Ký và ghi rõ họ tên)\n\n\n\n").font.bold = True
    p_l.add_run("Trần Đặng Công Tâm\n(Fullstack Dev & QA Lead)").font.italic = True
    
    p_r = c_right.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r.add_run("TRƯỞNG NHÓM 07\n(Ký và ghi rõ họ tên)\n\n\n\n").font.bold = True
    p_r.add_run("Đinh Gia Bảo\n(Architecture & AI Lead)").font.italic = True

    # Lưu tài liệu vào các thư mục docs/ và docs/Reports/
    out_paths = [
        r"d:\ICTU\Nam 3\ICTU_2026-2027\Ứng dụng trí tuệ nhân tạo - Project\He_thong_quan_ly_phong_kham\docs\Tai_Lieu_Thiet_Ke_Kien_Truc_Nhom_07.docx",
        r"d:\ICTU\Nam 3\ICTU_2026-2027\Ứng dụng trí tuệ nhân tạo - Project\He_thong_quan_ly_phong_kham\docs\Reports\Tai_Lieu_Thiet_Ke_Kien_Truc_Nhom_07.docx",
        r"d:\ICTU\Nam 3\ICTU_2026-2027\Ứng dụng trí tuệ nhân tạo - Project\He_thong_quan_ly_phong_kham\Tai_Lieu_Thiet_Ke_Kien_Truc_Nhom_07.docx"
    ]
    
    for p in out_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        doc.save(p)
    print("Successfully generated all architecture docx files!")

if __name__ == "__main__":
    build_docx()
