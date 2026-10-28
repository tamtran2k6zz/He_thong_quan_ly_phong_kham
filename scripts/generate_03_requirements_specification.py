# -*- coding: utf-8 -*-
"""
Script sinh file 03_GenAI_SoftwareDevelopment_requirements-specification.docx
Tài liệu đặc tả yêu cầu phần mềm (SRS) cho Hệ thống CMS-AI (Nhóm 03).
Bổ sung đầy đủ sơ đồ Use Case tổng quát, Sơ đồ Activity luồng nghiệp vụ khép kín,
đặc tả chi tiết toàn bộ 12 Use Case cốt lõi, ma trận truy vết và ranh giới đạo đức AI.
"""

import os
import sys
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
    add_diagram,
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
        "Mô hình Use Case tổng quát thể hiện mối liên kết giữa bốn nhóm tác nhân người dùng, một tác nhân dịch vụ ngoài (Google Gemini Live API) "
        "và 13 Use Case cốt lõi phân tầng thuộc 5 phân hệ nghiệp vụ chính của phòng khám:"
    )

    # Chèn sơ đồ Use Case tổng quát chất lượng cao
    uc_img = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "generated_diagrams", "diagram_usecase_general.png"))
    add_diagram(doc, uc_img, "Hình 2.1: Sơ đồ Use Case tổng quát Hệ thống quản lý phòng khám CMS-AI (UML Use Case)")

    add_p(
        doc,
        "Bên cạnh sơ đồ chức năng tĩnh, luồng vận hành nghiệp vụ lâm sàng khép kín (End-to-End Activity Flow) "
        "từ khi bệnh nhân bước vào phòng khám cho đến khi ra về và uống thuốc tại nhà được thể hiện trực quan dưới đây:"
    )

    # Chèn sơ đồ Activity Diagram luồng nghiệp vụ
    flow_img = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "generated_diagrams", "diagram_business_activity_flow.png"))
    add_diagram(doc, flow_img, "Hình 2.2: Sơ đồ luồng hoạt động nghiệp vụ lâm sàng khép kín (End-to-End Activity Flowchart)")

    add_h2(doc, "2.2. Danh sách các tác nhân và mô tả")
    actors_data = [
        ("Quản trị viên (Admin)", "Toàn quyền quản trị tài khoản, phân ca làm việc bác sĩ, quản lý danh mục thuốc, dịch vụ khám và giám sát nhật ký an ninh.", "Nhân sự CNTT phòng khám"),
        ("Lễ tân (Receptionist)", "Tiếp đón người bệnh, tra cứu thông tin hành chính, đăng ký tài khoản bệnh nhân, điều phối lịch hẹn và quản lý hàng đợi.", "Bộ phận Tiền sảnh"),
        ("Bác sĩ (Doctor)", "Khám lâm sàng, ghi nhận sinh hiệu, chẩn đoán bệnh theo mã ICD-10, kê đơn thuốc và sử dụng trợ lý AI tóm tắt bệnh sử.", "Bộ phận Chuyên môn"),
        ("Kế toán (Accountant)", "Tiếp nhận hồ sơ khám hoàn thành, tính toán viện phí, áp dụng mức giảm trừ BHYT, xuất mã VietQR và in biên lai thu tiền.", "Bộ phận Tài chính"),
        ("Gemini Live API (External)", "Dịch vụ trí tuệ nhân tạo đám mây hỗ trợ xử lý ngôn ngữ tự nhiên: tóm tắt bệnh sử, hỏi đáp FAQ và sinh hướng dẫn sau khám.", "Nhà cung cấp ngoại vi")
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
        ("UC001", "Đăng nhập & Phân quyền RBAC", "Xác thực người dùng qua JWT và phân quyền theo 4 vai trò", "Quản lý nhân sự", "Bắt buộc"),
        ("UC002", "Quản lý hồ sơ bệnh nhân", "Tạo mới, tìm kiếm CCCD/SĐT, chỉnh sửa thông tin hành chính", "Tiếp đón", "Bắt buộc"),
        ("UC003", "Đặt lịch & Chống trùng lịch", "Tạo lịch hẹn và kiểm tra xung đột thời gian bác sĩ/phòng khám", "Lịch hẹn", "Cốt lõi"),
        ("UC004", "Khám lâm sàng EMR", "Nhập dấu hiệu sinh tồn, tính BMI, chẩn đoán mã ICD-10", "Bàn khám", "Cốt lõi"),
        ("UC005", "Kê đơn & Cảnh báo dị ứng", "Kê thuốc từ danh mục, đối soát dị ứng tiền sử bệnh nhân", "Dược khoa", "Cốt lõi"),
        ("UC006", "Thanh toán & Mã VietQR", "Tính viện phí, giảm trừ BHYT 80-100%, sinh mã thanh toán VietQR", "Viện phí", "Cốt lõi"),
        ("UC007", "AI Tóm tắt hồ sơ Pre-visit", "Khử định danh PII và tóm tắt diễn tiến bệnh lý cho bác sĩ", "Trợ lý AI", "Tính năng AI"),
        ("UC008", "AI Chatbot hỏi đáp FAQ RAG", "Hỏi đáp thủ tục khám, bảng giá và BHYT từ cơ sở tri thức RAG", "Trợ lý AI", "Tính năng AI"),
        ("UC009", "AI Dặn dò sau khám", "Sinh hướng dẫn uống thuốc, chế độ ăn và hẹn tái khám theo mẫu", "Trợ lý AI", "Tính năng AI"),
        ("UC010", "Phân ca làm việc bác sĩ", "Phân lịch trực theo tuần và khóa khung giờ ngoài ca trực", "Quản trị", "Bắt buộc"),
        ("UC011", "Quản trị danh mục dược phẩm", "Thêm mới, cập nhật đơn giá, quản lý số lượng tồn kho thuốc", "Dược khoa", "Bắt buộc"),
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
        "Cơ sở dữ liệu quan hệ MySQL phiên bản 8.0 / PostgreSQL 15; "
        "Hậu tầng Backend xây dựng bằng ngôn ngữ Python với framework FastAPI và thư viện SQLAlchemy ORM; "
        "Giao diện Frontend xây dựng bằng thư viện React 18, Vite và Tailwind CSS; "
        "Kết nối mạng Internet băng thông tối thiểu 10 Mbps để giao tiếp với dịch vụ Google Gemini Live API; "
        "Môi trường kiểm thử tự động sử dụng Pytest 8.3 và FastAPI TestClient với 323 ca kiểm thử đạt tỷ lệ pass 100%."
    )

    # 3. ĐẶC TẢ CHI TIẾT CÁC YÊU CẦU CHỨC NĂNG
    add_h1(doc, "3. ĐẶC TẢ CÁC YÊU CẦU CHỨC NĂNG (FUNCTIONAL)")

    use_cases_detailed = [
        {
            "id": "UC001",
            "name": "Đăng nhập và Phân quyền người dùng (RBAC)",
            "goal": "Xác thực danh tính nhân sự y tế và cấp quyền truy cập theo đúng vai trò.",
            "desc": "Người dùng đăng nhập bằng tài khoản được cấp. Hệ thống xác thực bằng Bcrypt băm mật khẩu, sinh JWT Token chứa vai trò (Admin, Receptionist, Doctor, Accountant).",
            "actor": "Quản trị viên, Lễ tân, Bác sĩ, Kế toán",
            "pre": "Người dùng đã có tài khoản kích hoạt trong CSDL.",
            "post": "Hệ thống cấp Access Token JWT có thời hạn 60 phút, chuyển hướng vào đúng bảng điều khiển theo vai trò.",
            "basic_flow": "1. Người dùng mở trang đăng nhập hệ thống (/login).\n"
                          "2. Người dùng nhập Tên đăng nhập (username) và Mật khẩu (password).\n"
                          "3. Người dùng nhấn nút 'Đăng nhập'.\n"
                          "4. Hệ thống kiểm tra tài khoản, xác thực mật khẩu băm Bcrypt qua hàm verify_password().\n"
                          "5. Hệ thống sinh mã JWT Token chứa thông tin user_id và role.\n"
                          "6. Trình duyệt lưu Token vào LocalStorage và chuyển hướng vào Dashboard theo quyền hạn.",
            "alt_flow": "4a. Sai tên đăng nhập hoặc mật khẩu: Hệ thống trả về mã lỗi 401 Unauthorized kèm thông báo 'Thông tin đăng nhập không chính xác'.\n"
                        "4b. Tài khoản bị vô hiệu hóa: Hệ thống trả về mã lỗi 403 Forbidden kèm thông báo 'Tài khoản đã bị khóa bởi Quản trị viên'.\n"
                        "5a. Token hết hạn: Khi thực hiện yêu cầu mới, hệ thống tự động đăng xuất và yêu cầu đăng nhập lại.",
            "diagram_type": "Sequence Diagram",
            "diagram": """sequenceDiagram
    autonumber
    actor User as Nhân sự phòng khám
    participant UI as Giao diện Login
    participant API as Auth API (/api/v1/auth)
    participant Sec as Security Engine (Bcrypt)
    participant DB as CSDL MySQL

    User->>UI: Nhập username và password
    UI->>API: POST /api/v1/auth/login
    API->>DB: Query thông tin user theo username
    DB-->>API: Trả về hashed_password, role, is_active
    API->>Sec: verify_password(plain, hashed)
    Sec-->>API: Mật khẩu chính xác (True)
    API->>API: create_access_token(user_id, role, exp=60m)
    API-->>UI: 200 OK {access_token, token_type: "bearer", role}
    UI-->>User: Điều hướng tới Dashboard chuyên trách"""
        },
        {
            "id": "UC002",
            "name": "Tiếp đón và Quản lý hồ sơ bệnh nhân",
            "goal": "Tìm kiếm, đăng ký mới và quản lý thông tin hành chính, tiền sử dị ứng của người bệnh.",
            "desc": "Lễ tân tra cứu nhanh hồ sơ bệnh nhân theo số điện thoại hoặc CCCD. Nếu chưa có, tạo mới hồ sơ bệnh nhân kèm số thẻ BHYT và ghi nhận tiền sử dị ứng thuốc.",
            "actor": "Lễ tân, Bác sĩ",
            "pre": "Lễ tân đã đăng nhập vào hệ thống với vai trò Receptionist hoặc Admin.",
            "post": "Hồ sơ bệnh nhân được lưu trữ trong CSDL, mã y tế duy nhất (medical_code) được cấp phát tự động.",
            "basic_flow": "1. Lễ tân vào phân hệ Tiếp đón bệnh nhân.\n"
                          "2. Nhập số CCCD hoặc Số điện thoại vào ô tìm kiếm nhanh.\n"
                          "3. Nếu bệnh nhân đã có hồ sơ cũ: Hệ thống hiển thị thông tin để đối chiếu và mở ca khám mới.\n"
                          "4. Nếu bệnh nhân mới: Lễ tân nhấn 'Đăng ký bệnh nhân mới', nhập họ tên, ngày sinh, giới tính, địa chỉ, số CCCD, số BHYT và tiền sử dị ứng thuốc.\n"
                          "5. Lễ tân nhấn 'Lưu hồ sơ'.\n"
                          "6. Hệ thống kiểm tra tính duy nhất của CCCD/SĐT, sinh mã BN tự động và thêm vào hàng đợi.",
            "alt_flow": "4a. Số CCCD hoặc Số BHYT đã tồn tại trong hệ thống: Hệ thống thông báo trùng lặp và mở hồ sơ đã có để kiểm tra.\n"
                        "4b. Dữ liệu ngày sinh không hợp lệ: Hệ thống cảnh báo đỏ và yêu cầu sửa lại trước khi lưu.",
            "diagram_type": "Activity Diagram",
            "diagram": """flowchart TD
    Start([Bắt đầu tiếp đón]) --> Search[Tra cứu CCCD hoặc Số điện thoại]
    Search --> Found{Bệnh nhân đã có hồ sơ?}
    Found -- Có --> ConfirmInfo[Đối chiếu thông tin cá nhân]
    ConfirmInfo --> CreateQueue[Đưa vào hàng đợi chờ khám]
    Found -- Chưa --> InputForm[Nhập thông tin hành chính, BHYT, Dị ứng]
    InputForm --> Validate[Kiểm tra định dạng và tính hợp lệ]
    Validate --> Valid{Dữ liệu hợp lệ?}
    Valid -- Không --> AlertErr[Báo lỗi định dạng và yêu cầu nhập lại]
    AlertErr --> InputForm
    Valid -- Có --> SaveDB[Lưu vào CSDL và sinh mã BN tự động]
    SaveDB --> CreateQueue
    CreateQueue --> End([Hoàn thành tiếp đón và in số thứ tự])"""
        },
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
            "name": "Khám lâm sàng EMR và Ghi nhận sinh hiệu",
            "goal": "Ghi nhận toàn diện kết quả thăm khám lâm sàng, chỉ số sinh hiệu và kết luận chẩn đoán mã ICD-10.",
            "desc": "Bác sĩ nhập triệu chứng, chỉ số sinh tồn (HA, mạch, SpO2, BMI), chẩn đoán mã bệnh theo chuẩn quốc tế ICD-10.",
            "actor": "Bác sĩ",
            "pre": "Bác sĩ đã đăng nhập thành công; Người bệnh đang ở trạng thái 'in_progress' trong hàng đợi khám.",
            "post": "Hồ sơ bệnh án điện tử EMR được lưu trữ hoàn tất, sẵn sàng chuyển sang kê đơn hoặc chỉ định cận lâm sàng.",
            "basic_flow": "1. Bác sĩ mở hồ sơ bệnh án của bệnh nhân từ danh sách chờ khám.\n"
                          "2. Bác sĩ nhập triệu chứng ban đầu và các chỉ số sinh hiệu (Huyết áp, Mạch, Nhiệt độ, SpO2, Chiều cao, Cân nặng).\n"
                          "3. Hệ thống tự động tính chỉ số BMI và hiển thị đánh giá thể trạng.\n"
                          "4. Bác sĩ tìm kiếm và chọn mã bệnh theo danh mục chuẩn quốc tế ICD-10.\n"
                          "5. Bác sĩ nhập tóm tắt kết luận lâm sàng và hướng điều trị.\n"
                          "6. Bác sĩ bấm 'Lưu kết quả khám'.",
            "alt_flow": "2a. Chỉ số huyết áp hoặc nhịp tim ngoài ngưỡng an toàn sinh lý: Hệ thống hiển thị cảnh báo viền đỏ nổi bật nhắc bác sĩ kiểm tra lại.\n"
                        "4a. Mã ICD-10 không tồn tại: Hệ thống gợi ý tìm kiếm theo từ khóa triệu chứng tiếng Việt tương đương.",
            "diagram_type": "Activity Diagram",
            "diagram": """flowchart TD
    Start([Bắt đầu ca khám]) --> OpenEMR[Mở hồ sơ bệnh án EMR]
    OpenEMR --> InputVitals[Nhập sinh hiệu: HA, Mạch, SpO2, Cân nặng, Chiều cao]
    InputVitals --> CalcBMI[Hệ thống tự động tính BMI và cảnh báo thể trạng]
    CalcBMI --> SelectICD[Tra cứu và chọn mã chẩn đoán ICD-10]
    SelectICD --> SaveRecord[Lưu bệnh án EMR hoàn tất]
    SaveRecord --> End([Chuyển tiếp kê đơn thuốc])"""
        },
        {
            "id": "UC005",
            "name": "Kê đơn thuốc điện tử và Cảnh báo tương tác dị ứng",
            "goal": "Hỗ trợ bác sĩ lập đơn thuốc điện tử an toàn, đối soát tự động thành phần thuốc với tiền sử dị ứng của người bệnh.",
            "desc": "Bác sĩ chọn thuốc từ kho dược, chỉ định liều lượng, số lượng và tần suất uống. Hệ thống kiểm tra đối soát với tiền sử dị ứng đã lưu của bệnh nhân.",
            "actor": "Bác sĩ",
            "pre": "Ca khám bệnh án EMR đã hoàn thành bước chẩn đoán xác định bệnh.",
            "post": "Đơn thuốc được tạo thành công, số lượng thuốc tồn kho được giữ chỗ tạm thời.",
            "basic_flow": "1. Bác sĩ nhấn nút 'Kê đơn thuốc' trên màn hình EMR.\n"
                          "2. Bác sĩ gõ tên thuốc hoặc hoạt chất, hệ thống hiển thị danh mục thuốc có sẵn trong kho.\n"
                          "3. Bác sĩ chọn thuốc, nhập số lượng, số lần uống trong ngày (Sáng, Trưa, Chiều, Tối), số ngày dùng.\n"
                          "4. Hệ thống tự động kích hoạt hàm check_drug_allergy(medicine_name) đối chiếu tiền sử dị ứng của bệnh nhân.\n"
                          "5. Hệ thống xác nhận an toàn không có xung đột dị ứng.\n"
                          "6. Bác sĩ nhấn 'Ký đơn thuốc và chuyển thu ngân'.",
            "alt_flow": "4a. Phát hiện thành phần hoạt chất trùng với tiền sử dị ứng: Hệ thống hiển thị hộp cảnh báo màu đỏ kèm thông tin dị ứng cụ thể, yêu cầu bác sĩ đổi thuốc khác.\n"
                        "3a. Số lượng thuốc yêu cầu vượt quá số lượng tồn kho: Hệ thống hiển thị cảnh báo hết thuốc và đề xuất số lượng tối đa hiện có.",
            "diagram_type": "Sequence Diagram",
            "diagram": """sequenceDiagram
    autonumber
    actor Doctor as Bác sĩ
    participant UI as Bàn khám EMR
    participant API as Prescription API
    participant Checker as AllergyChecker
    participant DB as CSDL MySQL

    Doctor->>UI: Thêm thuốc (Paracetamol 500mg, SL: 20 viên)
    UI->>API: POST /api/v1/prescriptions/check-item
    API->>Checker: check_allergy(patient_id=104, medicine="Paracetamol")
    Checker->>DB: Query patient.drug_allergies
    DB-->>Checker: drug_allergies = "Aspirin, Penicillin"
    Checker-->>API: Safe: Không trùng hoạt chất dị ứng
    API-->>UI: 200 OK (Thuốc an toàn)
    Doctor->>UI: Bấm "Lưu và Ký đơn thuốc"
    UI->>API: POST /api/v1/prescriptions/
    API->>DB: INSERT INTO prescriptions & prescription_items
    DB-->>API: prescription_id = 88
    API-->>UI: Hoàn thành đơn thuốc thành công"""
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
        },
        {
            "id": "UC008",
            "name": "AI Chatbot hỏi đáp thủ tục FAQ và BHYT (RAG)",
            "goal": "Giải đáp tự động các thắc mắc về thủ tục đăng ký, bảng giá dịch vụ và chính sách BHYT 24/7.",
            "desc": "Người bệnh hoặc nhân viên gửi câu hỏi. Hệ thống kiểm tra an toàn Guardrails, truy vấn kho tri thức RAG và gọi Gemini API để phản hồi chính xác kèm cảnh báo y tế.",
            "actor": "Lễ tân, Bệnh nhân, Quản trị viên",
            "pre": "Hệ thống cơ sở tri thức phòng khám (FAQ Knowledge Base) đã được nạp dữ liệu.",
            "post": "Câu trả lời được hiển thị trong khung chat, không chứa nội dung chẩn đoán bệnh học.",
            "basic_flow": "1. Người dùng mở hộp thoại Trợ lý ảo AI Chatbot trên giao diện web.\n"
                          "2. Người dùng nhập câu hỏi (VD: 'Thủ tục khám BHYT cần mang theo giấy tờ gì?').\n"
                          "3. Hệ thống gửi câu hỏi qua bộ kiểm tra MedicalGuardrails.is_medical_diagnosis_query().\n"
                          "4. Hệ thống xác nhận câu hỏi thuộc phạm vi hành chính, kích hoạt cơ chế RAG tìm kiếm tài liệu liên quan.\n"
                          "5. Ghép ngữ cảnh tri thức phòng khám vào prompt gửi đến Google Gemini API.\n"
                          "6. Mô hình sinh câu trả lời súc tích, đầy đủ và đính kèm lời nhắc bảo mật.\n"
                          "7. Hệ thống hiển thị câu trả lời trên khung chat trong thời gian dưới 2 giây.",
            "alt_flow": "3a. Người dùng hỏi câu hỏi chẩn đoán hoặc kê đơn bệnh tật (VD: 'Tôi bị đau ngực khó thở uống thuốc gì?'): Guardrails lập tức chặn lại và trả về thông báo an toàn: 'Trợ lý AI chỉ giải đáp thủ tục hành chính, không có chức năng khám bệnh. Vui lòng đến ngay phòng khám hoặc bệnh viện gần nhất để được bác sĩ tư vấn'.",
            "diagram_type": "Sequence Diagram",
            "diagram": """sequenceDiagram
    autonumber
    actor User as Bệnh nhân / Lễ tân
    participant Chat as Widget Chatbot
    participant API as Chatbot API (/api/v1/ai/chat)
    participant Guard as MedicalGuardrails
    participant RAG as KnowledgeBase (FAQ)
    participant AI as Google Gemini Live

    User->>Chat: Gửi câu hỏi thủ tục khám BHYT
    Chat->>API: POST /api/v1/ai/chat {message: "..."}
    API->>Guard: is_medical_diagnosis_query(message)
    Guard-->>API: False (Câu hỏi hành chính an toàn)
    API->>RAG: search_knowledge(query="thủ tục BHYT")
    RAG-->>API: Trả về điều khoản quy định thẻ BHYT
    API->>AI: Gửi Prompt (Context FAQ + Question)
    AI-->>API: Trả về câu trả lời đã biên tập
    API-->>Chat: 200 OK {response: "...", disclaimer: "..."}
    Chat-->>User: Hiển thị phản hồi thân thiện và chính xác"""
        },
        {
            "id": "UC009",
            "name": "AI Sinh hướng dẫn dặn dò sau khám (Discharge Instructions)",
            "goal": "Tự động tổng hợp và sinh bảng dặn dò sinh hoạt, lịch uống thuốc và dấu hiệu cấp cứu sau khi khám.",
            "desc": "Trích xuất chẩn đoán và đơn thuốc đã kê, sinh bản hướng dẫn cá nhân hóa phân chia lịch uống thuốc (Sáng - Trưa - Chiều - Tối) và chế độ ăn kiêng cho bệnh nhân.",
            "actor": "Bác sĩ",
            "pre": "Hồ sơ bệnh án EMR và đơn thuốc của bệnh nhân đã hoàn thành.",
            "post": "Tờ hướng dẫn sau khám trực quan được tạo ra, cho phép bác sĩ chỉnh sửa trước khi in phát cho người bệnh.",
            "basic_flow": "1. Bác sĩ nhấn nút 'Tạo dặn dò sau khám AI' trên màn hình hoàn tất bệnh án.\n"
                          "2. Hệ thống tổng hợp mã chẩn đoán ICD-10 và danh mục các loại thuốc vừa kê.\n"
                          "3. Module AI sinh văn bản hướng dẫn gồm: Bảng lịch uống thuốc, Chế độ ăn uống sinh hoạt kiêng cữ, và Dấu hiệu cảnh báo nguy hiểm cần tái khám khẩn cấp.\n"
                          "4. Bản thảo hiển thị trong cửa sổ biên tập để bác sĩ xem lại.\n"
                          "5. Bác sĩ duyệt và nhấn 'In tờ dặn dò kèm đơn thuốc'.",
            "alt_flow": "3a. Mất kết nối API bên ngoài: Hệ thống tự động kích hoạt bộ mẫu dặn dò chuẩn theo từng nhóm bệnh ICD-10 có sẵn trong cơ sở dữ liệu nội bộ.",
            "diagram_type": "Activity Diagram",
            "diagram": """flowchart TD
    Start([Hoàn thành khám và kê đơn]) --> ReqGen[Bác sĩ bấm 'Sinh dặn dò sau khám AI']
    ReqGen --> ExtractData[Trích xuất chẩn đoán và đơn thuốc]
    ExtractData --> CallAI[Gọi AI phân chia lịch uống và chế độ ăn]
    CallAI --> ReviewDraft[Hiển thị bản thảo cho bác sĩ duyệt]
    ReviewDraft --> NeedEdit{Bác sĩ cần sửa đổi?}
    NeedEdit -- Có --> EditContent[Bác sĩ chỉnh sửa văn bản]
    EditContent --> Approve[Xác nhận bản hoàn chỉnh]
    NeedEdit -- Không --> Approve
    Approve --> PrintDoc[In phiếu dặn dò bàn giao bệnh nhân]
    PrintDoc --> End([Hoàn tất quy trình sau khám])"""
        },
        {
            "id": "UC010",
            "name": "Phân ca làm việc bác sĩ và Khóa khung giờ trực",
            "goal": "Quản lý và thiết lập lịch làm việc hàng tuần cho bác sĩ theo phòng khám, bảo đảm dữ liệu đầu vào cho bộ kiểm tra xung đột.",
            "desc": "Quản trị viên tạo lịch trực theo ca (Sáng: 08:00 - 12:00, Chiều: 13:30 - 17:30) cho từng bác sĩ tại buồng khám chỉ định.",
            "actor": "Quản trị viên",
            "pre": "Quản trị viên đã đăng nhập thành công với vai trò Admin; Danh sách bác sĩ và phòng khám đã có trong hệ thống.",
            "post": "Bản ghi ca trực (DoctorShift) được lưu trữ, hệ thống tự động khóa không cho đặt lịch ngoài khung giờ này.",
            "basic_flow": "1. Quản trị viên vào phân hệ 'Quản trị ca trực bác sĩ'.\n"
                          "2. Chọn bác sĩ, chọn phòng khám và chọn ngày làm việc trong tuần.\n"
                          "3. Chọn ca làm việc (Ca sáng hoặc Ca chiều) và số lượng bệnh nhân tối đa tiếp nhận trong ca.\n"
                          "4. Nhấn 'Lưu ca trực'.\n"
                          "5. Hệ thống xác thực không có xung đột bác sĩ trực 2 phòng cùng lúc và cập nhật lịch làm việc.",
            "alt_flow": "5a. Bác sĩ đã được phân ca tại phòng khám khác cùng khung giờ: Hệ thống cảnh báo trùng ca trực và từ chối lưu.",
            "diagram_type": "Activity Diagram",
            "diagram": """flowchart TD
    Start([Bắt đầu xếp ca]) --> SelectDoc[Chọn bác sĩ và phòng khám]
    SelectDoc --> SelectDate[Chọn ngày và khung giờ trực]
    SelectDate --> CheckConflict{Kiểm tra trùng ca trực bác sĩ?}
    CheckConflict -- Trùng lịch --> WarnErr[Báo lỗi trùng ca trực cùng giờ]
    WarnErr --> SelectDate
    CheckConflict -- Hợp lệ --> SaveShift[Lưu ca trực vào CSDL]
    SaveShift --> UpdateCalendar[Cập nhật bảng lịch làm việc tuần]
    UpdateCalendar --> End([Hoàn tất xếp ca])"""
        },
        {
            "id": "UC011",
            "name": "Quản trị danh mục dược phẩm và Tồn kho thuốc",
            "goal": "Theo dõi số lượng tồn kho, giá bán, hoạt chất và cảnh báo khi thuốc sắp hết hàng trong tủ thuốc phòng khám.",
            "desc": "Quản trị viên hoặc Dược sĩ thêm mới thuốc, cập nhật giá bán, theo dõi lượng thuốc xuất theo đơn và nhập kho bổ sung.",
            "actor": "Quản trị viên, Kế toán",
            "pre": "Người dùng đăng nhập với quyền Admin hoặc Accountant.",
            "post": "Dữ liệu kho thuốc được cập nhật chính xác theo thời gian thực.",
            "basic_flow": "1. Người dùng mở phân hệ 'Quản lý kho thuốc'.\n"
                          "2. Xem danh sách tồn kho, lọc theo thuốc sắp hết hàng (tồn < 10 đơn vị).\n"
                          "3. Thêm mới thuốc: Nhập tên thuốc, hoạt chất, quy cách đóng gói, đơn giá và số lượng ban đầu.\n"
                          "4. Nhấn 'Lưu danh mục'.\n"
                          "5. Hệ thống cập nhật bảng dữ liệu thuốc cho toàn phòng khám.",
            "alt_flow": "3a. Tên thuốc đã tồn tại: Hệ thống hiển thị tùy chọn cập nhật số lượng nhập kho thay vì tạo mới.",
            "diagram_type": "Activity Diagram",
            "diagram": """flowchart TD
    Start([Mở quản lý kho]) --> ViewStock[Xem danh sách tồn kho]
    ViewStock --> CheckLow{Thuốc tồn dưới ngưỡng tối thiểu?}
    CheckLow -- Đúng --> WarnLow[Hiển thị cảnh báo màu vàng cần nhập hàng]
    CheckLow -- Không --> Normal[Hiển thị số lượng bình thường]
    Normal --> UpdateAction[Nhập thêm thuốc hoặc sửa đơn giá]
    WarnLow --> UpdateAction
    UpdateAction --> SaveDB[Cập nhật CSDL kho dược]
    SaveDB --> End([Hoàn tất cập nhật tồn kho])"""
        },
        {
            "id": "UC012",
            "name": "Giám sát nhật ký kiểm toán hệ thống và AI Call Logs",
            "goal": "Lưu vết và giám sát toàn bộ các thao tác nhạy cảm, đăng nhập và lượt gọi mô hình AI theo tiêu chuẩn Nghị định 13/2023/NĐ-CP.",
            "desc": "Hệ thống tự động ghi nhật ký AuditLog với địa chỉ IP, User ID, hành động và thời gian thực. Cung cấp màn hình theo dõi số lượng token và độ trễ gọi AI.",
            "actor": "Quản trị viên",
            "pre": "Quản trị viên đã đăng nhập với vai trò Admin.",
            "post": "Báo cáo kiểm toán bảo mật và hiệu năng AI được hiển thị đầy đủ, không cho phép xóa sửa log.",
            "basic_flow": "1. Quản trị viên truy cập mục 'Nhật ký kiểm toán an ninh'.\n"
                          "2. Hệ thống hiển thị danh sách các sự kiện bảo mật: Đăng nhập thành công/thất bại, Thao tác sửa bệnh án, Xuất đơn thuốc.\n"
                          "3. Quản trị viên chuyển sang tab 'Nhật ký AI': Xem độ trễ phản hồi (latency), số lượng token tiêu thụ, tỷ lệ thành công của mô hình.\n"
                          "4. Quản trị viên lọc sự kiện theo ngày hoặc theo người dùng để kiểm tra bất thường.",
            "alt_flow": "2a. Phát hiện nhiều lần đăng nhập thất bại liên tiếp từ một IP: Hệ thống đánh dấu cờ cảnh báo an ninh (Security Alert).",
            "diagram_type": "Sequence Diagram",
            "diagram": """sequenceDiagram
    autonumber
    actor Admin as Quản trị viên
    participant UI as Màn hình Audit Logs
    participant API as Audit API (/api/v1/audit)
    participant DB as CSDL MySQL

    Admin->>UI: Mở tab Giám sát an ninh & AI Logs
    UI->>API: GET /api/v1/audit/logs?limit=50
    API->>DB: Query bảng audit_logs sắp xếp giảm dần theo thời gian
    DB-->>API: Trả về danh sách sự kiện (IP, user, action, latency)
    API-->>UI: 200 OK (Dữ liệu nhật ký chuẩn)
    UI-->>Admin: Hiển thị bảng kiểm toán và biểu đồ độ trễ AI"""
        }
    ]

    for idx, uc in enumerate(use_cases_detailed):
        add_h2(doc, f"3.{idx + 1}. Đặc tả Use Case {uc['id']}: {uc['name']}")

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
        ("UC009", "US-AI-05, US-AI-06", "Q16", "backend/app/ai_engine/guardrails.py", "100%"),
        ("UC010", "US-ADM-01, US-ADM-02", "Q19", "backend/app/api/v1/doctor_shifts.py", "100%"),
        ("UC011", "US-MED-01, US-MED-02", "Q20", "backend/app/api/v1/medicines.py", "100%"),
        ("UC012", "US-SEC-01, US-SEC-02", "Q14", "backend/app/api/v1/audit_logs.py", "100%")
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
