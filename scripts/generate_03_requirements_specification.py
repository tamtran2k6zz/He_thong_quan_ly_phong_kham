# -*- coding: utf-8 -*-
"""
Script sinh file 03_GenAI_SoftwareDevelopment_requirements-specification.docx
Tài liệu đặc tả yêu cầu phần mềm (SRS) cho Hệ thống CMS-AI (Nhóm 07).
"""

from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from docx_style_helpers import (
    create_base_document,
    add_header_block,
    add_team_meta,
    add_h1,
    add_h2,
    add_h3,
    add_p,
    add_code_block,
    format_row,
    set_table_borders,
    save_document,
    HEX_HEADER_BG,
    HEX_ROW_ALT
)

def build_srs():
    doc = create_base_document()

    add_header_block(
        doc,
        "ĐẶC TẢ YÊU CẦU PHẦN MỀM (SRS)",
        "HỆ THỐNG QUẢN LÝ PHÒNG KHÁM CÓ TÍCH HỢP AI (CMS-AI)"
    )

    add_team_meta(doc)

    # 1. GIỚI THIỆU CHUNG
    add_h1(doc, "1. GIỚI THIỆU CHUNG")

    add_h2(doc, "1.1. Mục đích")
    add_p(
        doc,
        "Tài liệu mô tả đầy đủ các yêu cầu chức năng, yêu cầu phi chức năng, ranh giới an toàn y tế và các ràng buộc thiết kế "
        "của Hệ thống quản lý phòng khám đa khoa có tích hợp AI (CMS-AI). "
        "Tài liệu là căn cứ pháp lý và kỹ thuật phục vụ việc phát triển, kiểm thử, nghiệm thu và chuyển giao sản phẩm."
    )

    add_h2(doc, "1.2. Phạm vi")
    add_p(
        doc,
        "Hệ thống phục vụ công tác khám chữa bệnh ngoại trú tại phòng khám đa khoa tư nhân quy mô vừa và nhỏ. "
        "Các phân hệ chính gồm Quản lý tiếp đón người bệnh, Đặt lịch khám và chống trùng ca trực, Bàn khám bệnh lâm sàng EMR, "
        "Kê đơn thuốc điện tử, Quản lý viện phí và BHYT, cùng hệ thống Trợ lý AI Hành chính 3 lớp hỗ trợ tóm tắt hồ sơ, "
        "hỏi đáp quy trình khám và sinh hướng dẫn sau khám. "
        "Tài liệu này được sử dụng bởi Ban quản lý phòng khám, Đội ngũ kỹ sư phần mềm, Chuyên viên kiểm thử và Hội đồng đánh giá học phần."
    )

    add_h2(doc, "1.3. Các định nghĩa, thuật ngữ, từ viết tắt")
    terms_data = [
        ("EMR", "Electronic Medical Record", "Hồ sơ bệnh án điện tử ghi nhận thông tin lâm sàng của người bệnh", "Chuẩn Bộ Y tế"),
        ("PII", "Personally Identifiable Information", "Thông tin định danh cá nhân nhạy cảm (CCCD, SĐT, BHYT, Tên)", "Nghị định 13/2023"),
        ("RBAC", "Role-Based Access Control", "Mô hình kiểm soát truy cập dựa trên 4 vai trò của nhân sự phòng khám", "An ninh hệ thống"),
        ("ICD-10", "International Classification of Diseases 10th", "Danh mục phân loại quốc tế về bệnh tật do WHO ban hành", "Mã hóa bệnh"),
        ("VietQR", "Vietnamese Quick Response code", "Chuẩn mã phản hồi nhanh thanh toán liên ngân hàng của NAPAS", "Thanh toán viện phí"),
        ("RAG", "Retrieval-Augmented Generation", "Kỹ thuật truy xuất thông tin từ cơ sở tri thức trước khi sinh phản hồi", "Chatbot FAQ"),
        ("JWT", "JSON Web Token", "Chuẩn mã định danh xác thực phiên làm việc an toàn giữa Client và Backend", "Xác thực API"),
        ("Guardrails", "Medical Safety Guardrails", "Tầng rào chắn an toàn ngăn chặn AI tự động đưa ra kết luận chẩn đoán", "Đạo đức y tế")
    ]

    tbl_terms = doc.add_table(rows=len(terms_data) + 1, cols=4)
    tbl_terms.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_terms.autofit = False
    col_w_terms = [Inches(1.0), Inches(2.2), Inches(2.3), Inches(1.0)]
    for row in tbl_terms.rows:
        for idx, w in enumerate(col_w_terms):
            row.cells[idx].width = w

    headers_terms = ["STT / Từ viết tắt", "Thuật ngữ đầy đủ", "Giải thích ý nghĩa", "Ghi chú"]
    for i, h in enumerate(headers_terms):
        tbl_terms.cell(0, i).text = h
    format_row(tbl_terms.rows[0], HEX_HEADER_BG, RGBColor(255, 255, 255), bold=True, is_header=True)

    for r_idx, (t_short, t_full, t_desc, t_note) in enumerate(terms_data):
        row = tbl_terms.rows[r_idx + 1]
        row.cells[0].text = t_short
        row.cells[1].text = t_full
        row.cells[2].text = t_desc
        row.cells[3].text = t_note
        bg = HEX_ROW_ALT if (r_idx % 2 == 1) else "FFFFFF"
        format_row(row, bg, RGBColor(15, 23, 42), bold=False, is_header=False)
    set_table_borders(tbl_terms)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_h2(doc, "1.4. Tài liệu tham khảo")
    ref_data = [
        ("1", "Đề tài 03: Hệ thống quản lý phòng khám có tích hợp AI", "Khoa CNTT, Trường Đại học CNTT & Truyền thông (ICTU)"),
        ("2", "Nghị định 13/2023/NĐ-CP về Bảo vệ Dữ liệu Cá nhân", "Chính phủ nước Cộng hòa Xã hội Chủ nghĩa Việt Nam"),
        ("3", "Danh mục Bệnh tật Quốc tế ICD-10 và Danh mục Thuốc thiết yếu", "Bộ Y tế Việt Nam và Tổ chức Y tế Thế giới (WHO)"),
        ("4", "OWASP Top 10 API Security Risks và NIST AI Risk Management", "Tổ chức An ninh Ứng dụng Web Mở Quốc tế")
    ]
    tbl_refs = doc.add_table(rows=len(ref_data) + 1, cols=3)
    tbl_refs.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_refs.autofit = False
    col_w_refs = [Inches(0.6), Inches(3.6), Inches(2.3)]
    for row in tbl_refs.rows:
        for idx, w in enumerate(col_w_refs):
            row.cells[idx].width = w
    headers_refs = ["STT", "Tên tài liệu tham khảo", "Cơ quan ban hành / Ghi chú"]
    for i, h in enumerate(headers_refs):
        tbl_refs.cell(0, i).text = h
    format_row(tbl_refs.rows[0], HEX_HEADER_BG, RGBColor(255, 255, 255), bold=True, is_header=True)

    for r_idx, (r_no, r_name, r_auth) in enumerate(ref_data):
        row = tbl_refs.rows[r_idx + 1]
        row.cells[0].text = r_no
        row.cells[1].text = r_name
        row.cells[2].text = r_auth
        bg = HEX_ROW_ALT if (r_idx % 2 == 1) else "FFFFFF"
        format_row(row, bg, RGBColor(15, 23, 42), bold=False, is_header=False)
    set_table_borders(tbl_refs)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 2. MÔ TẢ TỔNG QUAN ỨNG DỤNG
    add_h1(doc, "2. MÔ TẢ TỔNG QUAN ỨNG DỤNG")

    add_h2(doc, "2.1. Mô hình Use Case tổng quát")
    add_p(
        doc,
        "Mô hình Use Case tổng quát thể hiện mối liên kết giữa bốn nhóm tác nhân và các chức năng cốt lõi của hệ thống:"
    )

    uc_model_ascii = """+----------------------------------------------------------------------------------------------------+
|                                    SƠ ĐỒ USE CASE TOÀN HỆ THỐNG CMS-AI                             |
+----------------------------------------------------------------------------------------------------+
  [Tác nhân]                                           [Chức năng / Use Case]

  (Quản trị viên) ────────────┬───────────────────────> (UC001: Đăng nhập & Xác thực RBAC)
                              ├───────────────────────> (UC010: Phân ca làm việc bác sĩ)
                              ├───────────────────────> (UC011: Quản trị danh mục thuốc & dịch vụ)
                              └───────────────────────> (UC012: Giám sát nhật ký Audit & AI logs)

  (Lễ tân)        ────────────┬───────────────────────> (UC002: Tiếp đón & Đăng ký người bệnh)
                              ├───────────────────────> (UC003: Đặt lịch & Kiểm tra trùng lịch)
                              └───────────────────────> (UC008: AI Chatbot hỏi đáp quy trình FAQ)

  (Bác sĩ)        ────────────┬───────────────────────> (UC004: Khám bệnh EMR & Ghi nhận sinh hiệu)
                              ├───────────────────────> (UC005: Kê đơn thuốc & Cảnh báo dị ứng)
                              ├───────────────────────> (UC007: AI Tóm tắt hồ sơ Pre-visit)
                              └───────────────────────> (UC009: AI Sinh hướng dẫn sau khám)

  (Kế toán)       ────────────┬───────────────────────> (UC006: Thanh toán viện phí & VietQR)
                              └───────────────────────> (UC013: Báo cáo tài chính & Doanh thu)
+----------------------------------------------------------------------------------------------------+"""
    add_code_block(doc, uc_model_ascii)

    add_h2(doc, "2.2. Danh sách các tác nhân và mô tả")
    actors_data = [
        ("Quản trị viên (Admin)", "Toàn quyền quản trị tài khoản, phân ca làm việc bác sĩ, quản lý danh mục thuốc, dịch vụ khám và giám sát nhật ký an ninh.", "Nhân sự CNTT phòng khám"),
        ("Lễ tân (Receptionist)", "Tiếp đón người bệnh, tra cứu thông tin hành chính, đăng ký tài khoản bệnh nhân, điều phối lịch hẹn và quản lý hàng đợi.", "Bộ phận Tiền sảnh"),
        ("Bác sĩ (Doctor)", "Khám lâm sàng, ghi nhận sinh hiệu, chẩn đoán bệnh theo mã ICD-10, kê đơn thuốc và sử dụng trợ lý AI tóm tắt bệnh sử.", "Bộ phận Chuyên môn"),
        ("Kế toán (Accountant)", "Tiếp nhận hồ sơ khám hoàn thành, tính toán viện phí, áp dụng mức giảm trừ BHYT, xuất mã VietQR và in biên lai thu tiền.", "Bộ phận Tài chính")
    ]
    tbl_actors = doc.add_table(rows=len(actors_data) + 1, cols=3)
    tbl_actors.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_actors.autofit = False
    col_w_act = [Inches(1.8), Inches(3.7), Inches(1.0)]
    for row in tbl_actors.rows:
        for idx, w in enumerate(col_w_act):
            row.cells[idx].width = w
    headers_act = ["Tác nhân", "Mô tả tác nhân", "Ghi chú"]
    for i, h in enumerate(headers_act):
        tbl_actors.cell(0, i).text = h
    format_row(tbl_actors.rows[0], HEX_HEADER_BG, RGBColor(255, 255, 255), bold=True, is_header=True)

    for r_idx, (a_name, a_desc, a_note) in enumerate(actors_data):
        row = tbl_actors.rows[r_idx + 1]
        row.cells[0].text = a_name
        row.cells[1].text = a_desc
        row.cells[2].text = a_note
        bg = HEX_ROW_ALT if (r_idx % 2 == 1) else "FFFFFF"
        format_row(row, bg, RGBColor(15, 23, 42), bold=False, is_header=False)
    set_table_borders(tbl_actors)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_h2(doc, "2.3. Danh sách Use Case và mô tả")
    uc_list = [
        ("UC001", "Đăng nhập và Phân quyền", "Xác thực người dùng qua JWT và phân quyền theo 4 vai trò", "Quản lý nhân sự", "Bắt buộc"),
        ("UC002", "Quản lý hồ sơ bệnh nhân", "Tạo mới, tìm kiếm CCCD/SĐT, chỉnh sửa thông tin hành chính", "Tiếp đón", "Bắt buộc"),
        ("UC003", "Đặt lịch & Chống trùng lịch", "Tạo lịch hẹn và kiểm tra xung đột thời gian bác sĩ/phòng khám", "Lịch hẹn", "Cốt lõi"),
        ("UC004", "Khám lâm sàng EMR", "Nhập dấu hiệu sinh tồn, tính BMI, chẩn đoán mã ICD-10", "Bàn khám", "Cốt lõi"),
        ("UC005", "Kê đơn & Cảnh báo dị ứng", "Kê thuốc từ danh mục, đối soát dị ứng tiền sử bệnh nhân", "Dược khoa", "Cốt lõi"),
        ("UC006", "Thanh toán & Mã VietQR", "Tính viện phí, giảm trừ BHYT 80-100%, sinh mã thanh toán VietQR", "Viện phí", "Cốt lõi"),
        ("UC007", "AI Tóm tắt hồ sơ khám", "Khử định danh PII và tóm tắt diễn tiến bệnh lý cho bác sĩ", "Trợ lý AI", "Tính năng AI"),
        ("UC008", "AI Chatbot hỏi đáp FAQ", "Hỏi đáp thủ tục khám, bảng giá và BHYT từ cơ sở tri thức RAG", "Trợ lý AI", "Tính năng AI"),
        ("UC009", "AI Dặn dò sau khám", "Sinh hướng dẫn uống thuốc, chế độ ăn và hẹn tái khám theo mẫu", "Trợ lý AI", "Tính năng AI"),
        ("UC010", "Phân ca làm việc bác sĩ", "Phân lịch trực theo tuần và khóa khung giờ ngoài ca trực", "Quản trị", "Bắt buộc"),
        ("UC011", "Quản lý kho dược phẩm", "Thêm mới, cập nhật đơn giá, quản lý số lượng tồn kho thuốc", "Dược khoa", "Bắt buộc"),
        ("UC012", "Giám sát nhật ký hệ thống", "Xem nhật ký kiểm toán thao tác nhạy cảm và nhật ký gọi AI", "An ninh", "Tuân thủ")
    ]
    tbl_uclist = doc.add_table(rows=len(uc_list) + 1, cols=5)
    tbl_uclist.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_uclist.autofit = False
    col_w_uclist = [Inches(0.8), Inches(1.8), Inches(2.2), Inches(1.0), Inches(0.7)]
    for row in tbl_uclist.rows:
        for idx, w in enumerate(col_w_uclist):
            row.cells[idx].width = w
    headers_uclist = ["ID", "Tên Use case", "Mô tả ngắn gọn Use case", "Chức năng", "Ghi chú"]
    for i, h in enumerate(headers_uclist):
        tbl_uclist.cell(0, i).text = h
    format_row(tbl_uclist.rows[0], HEX_HEADER_BG, RGBColor(255, 255, 255), bold=True, is_header=True)

    for r_idx, (u_id, u_name, u_desc, u_fn, u_note) in enumerate(uc_list):
        row = tbl_uclist.rows[r_idx + 1]
        row.cells[0].text = u_id
        row.cells[1].text = u_name
        row.cells[2].text = u_desc
        row.cells[3].text = u_fn
        row.cells[4].text = u_note
        bg = HEX_ROW_ALT if (r_idx % 2 == 1) else "FFFFFF"
        format_row(row, bg, RGBColor(15, 23, 42), bold=False, is_header=False)
    set_table_borders(tbl_uclist)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_h2(doc, "2.4. Các điều kiện phụ thuộc kỹ thuật")
    add_p(
        doc,
        "Hệ thống vận hành trên môi trường mạng nội bộ phòng khám hoặc đám mây với các yêu cầu kỹ thuật: "
        "Máy chủ chạy hệ điều hành Linux/Windows hỗ trợ Docker Compose; "
        "Cơ sở dữ liệu quan hệ MySQL phiên bản 8.0; "
        "Hậu tầng Backend xây dựng bằng ngôn ngữ Python với framework FastAPI và thư viện SQLAlchemy ORM; "
        "Giao diện Frontend xây dựng bằng thư viện React 18, Vite và Tailwind CSS; "
        "Kết nối mạng Internet băng thông tối thiểu 10 Mbps để giao tiếp với dịch vụ Google Gemini Live API; "
        "Môi trường kiểm thử tự động sử dụng Pytest 8.3 và FastAPI TestClient."
    )

    # 3. ĐẶC TẢ CHI TIẾT CÁC YÊU CẦU CHỨC NĂNG
    add_h1(doc, "3. ĐẶC TẢ CÁC YÊU CẦU CHỨC NĂNG (FUNCTIONAL)")

    use_cases_detailed = [
        {
            "id": "UC003",
            "name": "Đặt lịch khám và Kiểm tra trùng lịch",
            "goal": "Cho phép lễ tân hoặc người bệnh đặt lịch hẹn khám mà không bị trùng khung giờ của bác sĩ hoặc phòng khám.",
            "desc": "Hệ thống kiểm tra tính khả dụng của bác sĩ và phòng khám dựa trên thuật toán giao thoa khoảng thời gian trước khi xác nhận lưu lịch hẹn.",
            "actor": "Lễ tân, Quản trị viên",
            "pre": "Người bệnh đã có hồ sơ trong hệ thống; Bác sĩ có ca trực hợp lệ trong ngày cần đặt.",
            "post": "Lịch hẹn mới được ghi nhận vào CSDL với trạng thái 'confirmed', hiển thị trên lịch trực của bác sĩ.",
            "basic_flow": "1. Lễ tân chọn người bệnh từ danh bạ hoặc nhập mã định danh bệnh nhân.\n"
                          "2. Lễ tân chọn chuyên khoa, bác sĩ phụ trách, phòng khám và khung giờ mong muốn (VD: 08:30 - 09:00).\n"
                          "3. Hệ thống kích hoạt ConflictChecker kiểm tra điều kiện [S1, E1) giao [S2, E2) trên CSDL.\n"
                          "4. Hệ thống xác nhận không có xung đột lịch của bác sĩ và phòng khám.\n"
                          "5. Lễ tân nhấn 'Xác nhận đặt lịch'.\n"
                          "6. Hệ thống lưu bản ghi lịch hẹn và cập nhật lịch làm việc.",
            "alt_flow": "3a. Bác sĩ đã có lịch hẹn khác giao nhau về thời gian: Hệ thống thông báo lỗi trùng lịch và gợi ý khung giờ trống gần nhất.\n"
                        "3b. Phòng khám đang có ca khám khác: Hệ thống thông báo phòng bận và đề xuất phòng khám thay thế.\n"
                        "3c. Thời gian đặt nằm ngoài ca trực của bác sĩ: Hệ thống từ chối và yêu cầu chọn lại trong ca trực.",
            "diagram_type": "Sequence Diagram",
            "diagram": """sequenceDiagram
    autonumber
    actor Receptionist as Lễ tân
    participant UI as Giao diện Web
    participant API as Appointments API
    participant Engine as ConflictChecker
    participant DB as CSDL MySQL

    Receptionist->>UI: Nhập thông tin lịch hẹn (BN, Bác sĩ, Khung giờ)
    UI->>API: POST /api/v1/appointments/ (payload)
    API->>Engine: check_conflict(doctor_id, room_id, start_time, end_time)
    Engine->>DB: Query các lịch hẹn trùng khung giờ
    DB-->>Engine: Trả về 0 bản ghi xung đột
    Engine-->>API: ConflictStatus: VALID (Không xung đột)
    API->>DB: INSERT INTO appointments (...)
    DB-->>API: appointment_id = 105, status='confirmed'
    API-->>UI: 201 Created (Chi tiết lịch hẹn)
    UI-->>Receptionist: Hiển thị thông báo đặt lịch thành công"""
        },
        {
            "id": "UC004",
            "name": "Khám lâm sàng EMR và Kê đơn thuốc có cảnh báo dị ứng",
            "goal": "Ghi nhận toàn diện kết quả thăm khám lâm sàng, chỉ số sinh hiệu và kê đơn thuốc an toàn cho người bệnh.",
            "desc": "Bác sĩ nhập triệu chứng, chỉ số sinh tồn (HA, mạch, SpO2, BMI), chẩn đoán mã ICD-10 và kê đơn thuốc có đối soát dị ứng.",
            "actor": "Bác sĩ",
            "pre": "Bác sĩ đã đăng nhập thành công; Người bệnh đang ở trạng thái 'in_progress' trong hàng đợi khám.",
            "post": "Hồ sơ bệnh án điện tử EMR và đơn thuốc được lưu trữ, chuyển trạng thái sang chờ thanh toán viện phí.",
            "basic_flow": "1. Bác sĩ mở hồ sơ bệnh án của bệnh nhân từ danh sách chờ khám.\n"
                          "2. Bác sĩ nhập triệu chứng ban đầu và các chỉ số sinh hiệu (Huyết áp, Mạch, Nhiệt độ, SpO2, Chiều cao, Cân nặng).\n"
                          "3. Hệ thống tự động tính chỉ số BMI và hiển thị đánh giá thể trạng.\n"
                          "4. Bác sĩ tìm kiếm và chọn mã bệnh theo danh mục chuẩn quốc tế ICD-10.\n"
                          "5. Bác sĩ thêm danh mục thuốc, nhập số lượng, đường dùng và liều lượng uống.\n"
                          "6. Hệ thống đối soát thành phần hoạt chất thuốc với tiền sử dị ứng đã lưu của người bệnh.\n"
                          "7. Hệ thống xác nhận an toàn dị ứng thuốc.\n"
                          "8. Bác sĩ bấm 'Lưu và hoàn thành ca khám'.",
            "alt_flow": "6a. Phát hiện thành phần thuốc trùng tiền sử dị ứng: Hệ thống hiển thị cảnh báo đỏ nổi bật, yêu cầu bác sĩ đổi thuốc hoặc nhập lý do chuyên môn bắt buộc để tiếp tục.\n"
                        "5a. Số lượng thuốc trong kho không đủ: Hệ thống cảnh báo tồn kho và yêu cầu điều chỉnh số lượng.",
            "diagram_type": "Activity Diagram",
            "diagram": """flowchart TD
    Start([Bắt đầu ca khám]) --> OpenEMR[Mở hồ sơ bệnh án EMR]
    OpenEMR --> InputVitals[Nhập sinh hiệu: HA, Mạch, SpO2, Cân nặng, Chiều cao]
    InputVitals --> CalcBMI[Hệ thống tự động tính BMI và cảnh báo thể trạng]
    CalcBMI --> SelectICD[Tra cứu và chọn mã chẩn đoán ICD-10]
    SelectICD --> AddMedicine[Chọn thuốc từ kho dược và nhập liều dùng]
    AddMedicine --> CheckAllergy{Đối soát tiền sử dị ứng thuốc?}
    CheckAllergy -- Trùng dị ứng --> WarnAlert[Cảnh báo nguy cơ dị ứng thuốc]
    WarnAlert --> ChangeMed[Bác sĩ đổi thuốc khác an toàn]
    ChangeMed --> AddMedicine
    CheckAllergy -- An toàn --> SaveRecord[Lưu bệnh án EMR và đơn thuốc]
    SaveRecord --> End([Chuyển hồ sơ sang thu viện phí])"""
        },
        {
            "id": "UC006",
            "name": "Thanh toán viện phí và Sinh mã VietQR động",
            "goal": "Tính toán viện phí chính xác, áp dụng giảm trừ BHYT và hỗ trợ người bệnh thanh toán chuyển khoản nhanh qua VietQR.",
            "desc": "Kế toán tổng hợp viện phí, hệ thống tính toán phần BHYT chi trả và tạo mã VietQR chuẩn NAPAS chứa chính xác số tiền cần thu.",
            "actor": "Kế toán",
            "pre": "Hồ sơ khám bệnh và đơn thuốc đã được bác sĩ hoàn thành và chuyển sang phân hệ kế toán.",
            "post": "Hóa đơn chuyển trạng thái 'paid', biên lai thu tiền được in ra và lưu vết nhật ký tài chính.",
            "basic_flow": "1. Kế toán mở danh sách hồ sơ chờ thu phí và chọn hồ sơ của bệnh nhân.\n"
                          "2. Hệ thống tổng hợp chi phí tiền khám, xét nghiệm và danh mục thuốc trong đơn.\n"
                          "3. Hệ thống kiểm tra mã thẻ BHYT và áp dụng tỷ lệ chi trả (80% hoặc 100%), tính số tiền người bệnh phải thanh toán.\n"
                          "4. Kế toán chọn phương thức 'Chuyển khoản VietQR'.\n"
                          "5. Hệ thống sinh mã VietQR động chứa số tiền, mã hóa đơn và số tài khoản phòng khám.\n"
                          "6. Người bệnh quét mã QR bằng ứng dụng ngân hàng và hoàn tất chuyển tiền.\n"
                          "7. Kế toán bấm 'Xác nhận thanh toán' và in hóa đơn viện phí bàn giao cho người bệnh.",
            "alt_flow": "4a. Người bệnh thanh toán tiền mặt: Kế toán chọn 'Tiền mặt', nhập số tiền nhận, hệ thống tính tiền thừa thối lại.\n"
                        "3a. Bệnh nhân không có BHYT: Tỷ lệ chi trả BHYT tính bằng 0%, người bệnh thanh toán toàn bộ 100% viện phí.",
            "diagram_type": "Sequence Diagram",
            "diagram": """sequenceDiagram
    autonumber
    actor Accountant as Kế toán
    participant UI as Giao diện Kế toán
    participant API as Billing API
    participant QR as VietQR Service
    participant DB as CSDL MySQL

    Accountant->>UI: Chọn hồ sơ bệnh nhân cần thanh toán
    UI->>API: GET /api/v1/invoices/preview/{record_id}
    API->>DB: Lấy tiền khám, tiền thuốc, thông tin BHYT
    DB-->>API: Dữ liệu viện phí
    API-->>UI: Hiển thị bảng kê (Tổng tiền, Giảm trừ BHYT, Cần thu)
    Accountant->>UI: Chọn phương thức "VietQR"
    UI->>API: POST /api/v1/invoices/generate-vietqr
    API->>QR: Tạo payload chuẩn NAPAS (Số tiền, Mã HĐ)
    QR-->>API: Chuỗi URL ảnh VietQR
    API-->>UI: Hiển thị mã QR động trên màn hình
    Accountant->>UI: Xác nhận đã nhận tiền -> Nhấn "Hoàn thành"
    UI->>API: POST /api/v1/invoices/{id}/pay
    API->>DB: UPDATE invoices SET status='paid', paid_at=NOW()
    DB-->>API: Cập nhật thành công
    API-->>UI: 200 OK -> Mở cửa sổ in biên lai"""
        },
        {
            "id": "UC007",
            "name": "AI Tóm tắt hồ sơ tiền sử bệnh án (Pre-visit Briefing)",
            "goal": "Hỗ trợ bác sĩ nắm bắt diễn tiến bệnh và tiền sử dị ứng của người bệnh trong thời gian dưới 15 giây trước khi bắt đầu khám.",
            "desc": "Trích xuất lịch sử khám cũ, lọc bỏ toàn bộ thông tin định danh nhạy cảm PII, gọi mô hình AI sinh bản tóm tắt súc tích.",
            "actor": "Bác sĩ",
            "pre": "Bác sĩ đang mở bệnh án của người bệnh có lịch sử khám trước đó; Trợ lý AI đang hoạt động.",
            "post": "Bản tóm tắt bệnh sử hiển thị trên thẻ AI Pre-visit Card với đầy đủ nhãn cảnh báo miễn trừ y tế.",
            "basic_flow": "1. Bác sĩ bấm nút 'Xem tóm tắt AI' trên giao diện bàn khám EMR.\n"
                          "2. Backend truy xuất các hồ sơ khám cũ, đơn thuốc cũ và kết quả sinh hiệu của bệnh nhân.\n"
                          "3. Module PIIAnonymizer che giấu họ tên, số điện thoại, số CCCD thành các nhãn an toàn.\n"
                          "4. MedicalGuardrails kiểm tra tính an toàn của prompt trước khi gọi AI.\n"
                          "5. AIService gửi prompt đã khử định danh sang Google Gemini Live API.\n"
                          "6. Mô hình AI trả về bản tóm tắt gồm: Tiền sử bệnh, Dị ứng thuốc, Thuốc đang dùng, Diễn tiến lần khám gần nhất.\n"
                          "7. Hệ thống gắn nhãn Disclaimer y tế và hiển thị kết quả cho bác sĩ xem.",
            "alt_flow": "2a. Người bệnh khám lần đầu (chưa có lịch sử cũ): Hệ thống thông báo 'Bệnh nhân khám lần đầu, chưa có dữ liệu tiền sử để tóm tắt'.\n"
                        "5a. Mất kết nối Internet: Hệ thống tự động chuyển sang MockFallbackProvider sinh tóm tắt quy tắc cục bộ.",
            "diagram_type": "Sequence Diagram",
            "diagram": """sequenceDiagram
    autonumber
    actor Doctor as Bác sĩ
    participant UI as Bàn khám EMR
    participant API as AI Engine API
    participant PII as PII Sanitizer
    participant AI as Google Gemini Live
    participant DB as CSDL MySQL

    Doctor->>UI: Nhấn "Xem tóm tắt AI"
    UI->>API: POST /api/v1/ai/pre-visit-summary (patient_id)
    API->>DB: Lấy lịch sử 3 lần khám gần nhất
    DB-->>API: Dữ liệu hồ sơ bệnh án
    API->>PII: sanitize(medical_history)
    PII-->>API: Dữ liệu đã khử CCCD, SĐT, Tên ([ID_REDACTED])
    API->>AI: generate_summary(sanitized_text, prompt_template)
    AI-->>API: Chuỗi tóm tắt tiền sử bệnh học
    API->>API: Thêm cảnh báo miễn trừ trách nhiệm y tế
    API->>DB: Ghi log gọi AI (AuditLog, latency_ms)
    API-->>UI: 200 OK (Bản tóm tắt an toàn)
    UI-->>Doctor: Hiển thị thẻ tóm tắt Pre-visit Card"""
        }
    ]

    for uc in use_cases_detailed:
        add_h2(doc, f"3.{use_cases_detailed.index(uc) + 1}. Đặc tả Use Case {uc['id']}: {uc['name']}")

        tbl_uc = doc.add_table(rows=8, cols=2)
        tbl_uc.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl_uc.autofit = False
        tbl_uc.columns[0].width = Inches(2.0)
        tbl_uc.columns[1].width = Inches(4.5)

        uc_fields = [
            (f"Use case: {uc['id']}_{uc['name']}", None),
            ("Mục đích:", uc["goal"]),
            ("Mô tả:", uc["desc"]),
            ("Tác nhân tác động:", uc["actor"]),
            ("Điều kiện trước:", uc["pre"]),
            ("Điều kiện sau:", uc["post"]),
            ("Luồng sự kiện chính (Basic flows):", uc["basic_flow"]),
            ("Luồng sự kiện phụ (Alternative flows):", uc["alt_flow"])
        ]

        for r_i, (f_label, f_val) in enumerate(uc_fields):
            row = tbl_uc.rows[r_i]
            if f_val is None:
                # Dòng tiêu đề gộp ô
                cell_a = row.cells[0]
                cell_b = row.cells[1]
                cell_a.merge(cell_b)
                cell_a.text = f_label
                format_row(row, HEX_HEADER_BG, RGBColor(255, 255, 255), bold=True, is_header=True)
            else:
                row.cells[0].text = f_label
                row.cells[1].text = f_val
                bg = HEX_ROW_ALT if (r_i % 2 == 1) else "FFFFFF"
                format_row(row, bg, RGBColor(15, 23, 42), bold=False, is_header=False)
                row.cells[0].paragraphs[0].runs[0].font.bold = True

        set_table_borders(tbl_uc)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

        add_h3(doc, f"Biểu đồ nghiệp vụ ({uc['diagram_type']}) cho {uc['id']}:")
        add_code_block(doc, uc["diagram"])

    # 4. CÁC THÔNG TIN HỖ TRỢ KHÁC
    add_h1(doc, "4. CÁC THÔNG TIN HỖ TRỢ KHÁC")

    add_h2(doc, "4.1. Ma trận truy vết yêu cầu (Traceability Matrix)")
    add_p(
        doc,
        "Ma trận truy vết bảo đảm tính liên kết hai chiều giữa các câu hỏi khảo sát, tài liệu User Stories và các Use Case chức năng:"
    )

    trace_data = [
        ("UC001", "US-AUTH-01, US-AUTH-02", "Q10, Q11, Q12", "backend/app/api/v1/auth.py", "100%"),
        ("UC002", "US-REC-01, US-REC-02", "Q1, Q2", "backend/app/api/v1/patients.py", "100%"),
        ("UC003", "US-SCHED-01, US-SCHED-02", "Q3, Q4", "backend/app/core/conflict_checker.py", "100%"),
        ("UC004", "US-DOC-01, US-DOC-02", "Q5, Q6", "backend/app/api/v1/medical_records.py", "100%"),
        ("UC005", "US-DOC-03, US-DOC-04", "Q7", "backend/app/api/v1/prescriptions.py", "100%"),
        ("UC006", "US-ACC-01, US-ACC-02", "Q8, Q9", "backend/app/api/v1/invoices.py", "100%"),
        ("UC007", "US-AI-01, US-AI-02", "Q13, Q17, Q18", "backend/app/ai_engine/anonymizer.py", "100%"),
        ("UC008", "US-AI-03, US-AI-04", "Q15", "backend/app/ai_engine/knowledge_base.py", "100%"),
        ("UC009", "US-AI-05, US-AI-06", "Q16", "backend/app/ai_engine/guardrails.py", "100%")
    ]
    tbl_trace = doc.add_table(rows=len(trace_data) + 1, cols=5)
    tbl_trace.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_trace.autofit = False
    col_w_trace = [Inches(1.0), Inches(1.5), Inches(1.0), Inches(2.3), Inches(0.7)]
    for row in tbl_trace.rows:
        for idx, w in enumerate(col_w_trace):
            row.cells[idx].width = w
    headers_trace = ["Mã UC", "Mã User Story", "Nguồn Q&A", "Tệp mã nguồn thực thi", "Tỷ lệ"]
    for i, h in enumerate(headers_trace):
        tbl_trace.cell(0, i).text = h
    format_row(tbl_trace.rows[0], HEX_HEADER_BG, RGBColor(255, 255, 255), bold=True, is_header=True)

    for r_idx, (m_uc, m_us, m_qa, m_code, m_rate) in enumerate(trace_data):
        row = tbl_trace.rows[r_idx + 1]
        row.cells[0].text = m_uc
        row.cells[1].text = m_us
        row.cells[2].text = m_qa
        row.cells[3].text = m_code
        row.cells[4].text = m_rate
        bg = HEX_ROW_ALT if (r_idx % 2 == 1) else "FFFFFF"
        format_row(row, bg, RGBColor(15, 23, 42), bold=False, is_header=False)
    set_table_borders(tbl_trace)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_h2(doc, "4.2. Ranh giới đạo đức AI và Tuyên bố miễn trừ y tế")
    add_p(
        doc,
        "Các chức năng tích hợp trí tuệ nhân tạo trong hệ thống CMS-AI tuân thủ nghiêm ngặt nguyên tắc đạo đức y tế: "
        "Trợ lý AI chỉ xử lý tác vụ hành chính, sắp xếp thông tin và hỗ trợ tra cứu quy trình; "
        "Mô hình AI bị cấm đưa ra kết luận chẩn đoán bệnh học hoặc tự ý kê đơn thuốc điều trị; "
        "Mọi kết quả do AI sinh ra bắt buộc phải có bác sĩ chuyên khoa hoặc nhân viên y tế có thẩm quyền kiểm tra và phê duyệt; "
        "Toàn bộ màn hình hiển thị nội dung AI đều đính kèm thông báo miễn trừ: "
        "'LƯU Ý Y TẾ: Nội dung do Trợ lý AI Hành chính tạo ra chỉ mang tính chất tham khảo quy trình, không thay thế cho quyết định chẩn đoán và điều trị của Bác sĩ chuyên khoa.'"
    )

    save_document(doc, "03_GenAI_SoftwareDevelopment_requirements-specification.docx")

if __name__ == "__main__":
    build_srs()
