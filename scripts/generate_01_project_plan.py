# -*- coding: utf-8 -*-
"""
Script sinh file 01_GenAI_SoftwareDevelopment_project-plan.docx
Kế hoạch thực hiện dự án 9 tuần cho Nhóm 07 (Đinh Gia Bảo, Trần Đặng Công Tâm).
"""

import sys
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from docx_style_helpers import (
    create_base_document,
    add_header_block,
    add_team_meta,
    add_h1,
    add_p,
    format_row,
    set_table_borders,
    save_document,
    HEX_HEADER_BG,
    HEX_ROW_ALT
)

def build_project_plan():
    doc = create_base_document()

    add_header_block(
        doc,
        "KẾ HOẠCH THỰC HIỆN, PHÁT TRIỂN ỨNG DỤNG CHUYÊN SÂU",
        "HỌC PHẦN: ỨNG DỤNG TRÍ TUỆ NHÂN TẠO"
    )

    add_team_meta(doc)

    add_h1(doc, "Kế hoạch chi tiết thực hiện dự án")
    add_p(
        doc,
        "Dự án triển khai trong thời gian 9 tuần từ ngày 27/07/2026 đến ngày 27/09/2026. "
        "Hai thành viên phối hợp chặt chẽ qua bốn giai đoạn SDLC (KT1, KT2, KT3, KT4) để xây dựng hệ thống quản lý phòng khám đa khoa CMS-AI."
    )

    # Dữ liệu 46 công việc chi tiết chia cho 9 tuần (khớp 47 hàng gồm cả tiêu đề)
    tasks_data = [
        # Tuần 1: Khảo sát bài toán & xác định phạm vi
        ("Tuần 01 (Từ: 27/07/2026 Đến: 02/08/2026)", "Khảo sát thực trạng quy trình tiếp đón và quản lý hồ sơ tại phòng khám đa khoa tư nhân", "Đinh Gia Bảo", "Hoàn thành phỏng vấn sơ bộ"),
        ("Tuần 01 (Từ: 27/07/2026 Đến: 02/08/2026)", "Phân tích năm điểm nghẽn nghiệp vụ gồm ùn tắc tiếp đón, trùng lịch khám, sai sót đơn thuốc, thất thoát viện phí, rò rỉ dữ liệu", "Trần Đặng Công Tâm", "Báo cáo thực trạng"),
        ("Tuần 01 (Từ: 27/07/2026 Đến: 02/08/2026)", "Nghiên cứu văn bản quy định pháp lý về bảo vệ dữ liệu cá nhân y tế theo Nghị định 13/2023/NĐ-CP", "Đinh Gia Bảo", "Cơ sở an toàn thông tin"),
        ("Tuần 01 (Từ: 27/07/2026 Đến: 02/08/2026)", "Xác định mục tiêu đề tài và phạm vi ứng dụng Trợ lý AI Hành chính hỗ trợ quy trình khám", "Đinh Gia Bảo", "Đề cương kỹ thuật"),
        ("Tuần 01 (Từ: 27/07/2026 Đến: 02/08/2026)", "Lập kế hoạch làm việc nhóm, phân chia trách nhiệm và thiết lập kho lưu trữ Git của dự án", "Trần Đặng Công Tâm", "Khởi tạo repository"),

        # Tuần 2: Thu thập & làm rõ yêu cầu
        ("Tuần 02 (Từ: 03/08/2026 Đến: 09/08/2026)", "Xây dựng bảng 20 câu hỏi phỏng vấn làm rõ yêu cầu nghiệp vụ phòng khám (Requirements Q&A)", "Đinh Gia Bảo", "Tài liệu Q&A"),
        ("Tuần 02 (Từ: 03/08/2026 Đến: 09/08/2026)", "Mô hình hóa bốn tác nhân chính gồm Quản trị viên, Lễ tân, Bác sĩ, Kế toán và phân định quyền hạn", "Trần Đặng Công Tâm", "Phân vai hệ thống"),
        ("Tuần 02 (Từ: 03/08/2026 Đến: 09/08/2026)", "Thiết lập danh mục yêu cầu chức năng (FR) cho nghiệp vụ tiếp đón, khám bệnh, kê đơn, viện phí và AI", "Đinh Gia Bảo", "Đặc tả chức năng"),
        ("Tuần 02 (Từ: 03/08/2026 Đến: 09/08/2026)", "Thiết lập danh mục yêu cầu phi chức năng (NFR) về hiệu năng truy vấn, thời gian phản hồi AI, bảo mật", "Trần Đặng Công Tâm", "Đặc tả phi chức năng"),
        ("Tuần 02 (Từ: 03/08/2026 Đến: 09/08/2026)", "Vẽ sơ đồ phân cấp chức năng hệ thống (Functional Decomposition Diagram)", "Đinh Gia Bảo", "Sơ đồ FDD"),

        # Tuần 3: Đặc tả yêu cầu SRS & Human Gate 1
        ("Tuần 03 (Từ: 10/08/2026 Đến: 16/08/2026)", "Soạn thảo tài liệu đặc tả yêu cầu phần mềm (SRS) theo cấu trúc chuẩn môn học", "Đinh Gia Bảo", "Tài liệu SRS"),
        ("Tuần 03 (Từ: 10/08/2026 Đến: 16/08/2026)", "Xây dựng danh mục 27 User Stories theo phương pháp MoSCoW kèm tiêu chí chấp nhận Acceptance Criteria", "Trần Đặng Công Tâm", "Danh sách User Stories"),
        ("Tuần 03 (Từ: 10/08/2026 Đến: 16/08/2026)", "Đặc tả chi tiết 12 Use Case cốt lõi từ UC001 đến UC012 kèm luồng chính và luồng ngoại lệ", "Trần Đặng Công Tâm", "Bảng đặc tả Use Case"),
        ("Tuần 03 (Từ: 10/08/2026 Đến: 16/08/2026)", "Vẽ biểu đồ Activity Diagram và Sequence Diagram cho các ca khám lâm sàng và đặt lịch", "Đinh Gia Bảo", "Sơ đồ UML"),
        ("Tuần 03 (Từ: 10/08/2026 Đến: 16/08/2026)", "Đánh giá, đối soát và kích hoạt cổng phê duyệt Human Gate 1 (Yêu cầu & Phạm vi)", "Đinh Gia Bảo, Trần Đặng Công Tâm", "Nghiệm thu Human Gate 1"),

        # Tuần 4: Thiết kế kiến trúc & CSDL quan hệ
        ("Tuần 04 (Từ: 17/08/2026 Đến: 23/08/2026)", "Thiết kế kiến trúc hệ thống phân tầng (FastAPI Backend, React Vite Frontend, CSDL MySQL 8.0)", "Đinh Gia Bảo", "Tài liệu Kiến trúc"),
        ("Tuần 04 (Từ: 17/08/2026 Đến: 23/08/2026)", "Thiết kế mô hình CSDL quan hệ 14 bảng đạt chuẩn chuẩn hóa 3NF", "Trần Đặng Công Tâm", "Sơ đồ quan hệ ERD"),
        ("Tuần 04 (Từ: 17/08/2026 Đến: 23/08/2026)", "Xây dựng từ điển dữ liệu chi tiết, xác định kiểu dữ liệu, khóa chính PK và khóa ngoại FK", "Trần Đặng Công Tâm", "Từ điển dữ liệu"),
        ("Tuần 04 (Từ: 17/08/2026 Đến: 23/08/2026)", "Thiết kế kiến trúc động cơ Trợ lý AI Hành chính 3 lớp (Khử PII, Guardrails, Multi-Provider)", "Đinh Gia Bảo", "Mô hình AI 3 lớp"),
        ("Tuần 04 (Từ: 17/08/2026 Đến: 23/08/2026)", "Hoàn thiện và nộp báo cáo cột mốc Giai đoạn 1 (Bài kiểm tra KT1)", "Đinh Gia Bảo, Trần Đặng Công Tâm", "Báo cáo KT1"),

        # Tuần 5: Thiết kế hướng đối tượng & Khởi tạo dự án
        ("Tuần 05 (Từ: 24/08/2026 Đến: 30/08/2026)", "Xây dựng biểu đồ lớp (Class Diagram) tổng thể cho các Domain Entities và Core Services", "Đinh Gia Bảo", "Sơ đồ Class Diagram"),
        ("Tuần 05 (Từ: 24/08/2026 Đến: 30/08/2026)", "Đặc tả chi tiết thuộc tính, phương thức, luồng xử lý và tiền điều kiện của hơn 20 lớp nghiệp vụ", "Đinh Gia Bảo", "Đặc tả OOP"),
        ("Tuần 05 (Từ: 24/08/2026 Đến: 30/08/2026)", "Khởi tạo dự án Backend FastAPI, thiết lập kết nối SQLAlchemy ORM và di chuyển lược đồ CSDL", "Trần Đặng Công Tâm", "Backend Core"),
        ("Tuần 05 (Từ: 24/08/2026 Đến: 30/08/2026)", "Khởi tạo giao diện Frontend React Vite, cấu hình Tailwind CSS theo phong cách Taste-Skill", "Trần Đặng Công Tâm", "Frontend Boilerplate"),
        ("Tuần 05 (Từ: 24/08/2026 Đến: 30/08/2026)", "Viết kịch bản sinh dữ liệu mẫu (seed_data.py) chuẩn y tế Việt Nam phục vụ phát triển", "Đinh Gia Bảo", "Kịch bản nạp dữ liệu"),

        # Tuần 6: Phát triển chức năng quản lý cốt lõi
        ("Tuần 06 (Từ: 31/08/2026 Đến: 06/09/2026)", "Xây dựng module xác thực JWT, cơ chế băm mật khẩu Bcrypt và bộ kiểm tra phân quyền RoleChecker", "Đinh Gia Bảo", "API Phân quyền RBAC"),
        ("Tuần 06 (Từ: 31/08/2026 Đến: 06/09/2026)", "Lập trình thuật toán phát hiện xung đột lịch khám bác sĩ và phòng khám dựa trên giao thoa khoảng thời gian", "Đinh Gia Bảo", "ConflictChecker Engine"),
        ("Tuần 06 (Từ: 31/08/2026 Đến: 06/09/2026)", "Phát triển giao diện phân hệ Lễ tân (Tiếp đón người bệnh, quản lý lịch hẹn, điều phối hàng đợi)", "Trần Đặng Công Tâm", "Màn hình Lễ tân"),
        ("Tuần 06 (Từ: 31/08/2026 Đến: 06/09/2026)", "Phát triển giao diện phân hệ Bác sĩ (Bàn khám EMR, ghi nhận sinh hiệu, tính chỉ số BMI)", "Trần Đặng Công Tâm", "Bàn khám bác sĩ"),
        ("Tuần 06 (Từ: 31/08/2026 Đến: 06/09/2026)", "Hoàn thành và nghiệm thu Báo cáo cột mốc Giai đoạn 2 (Bài kiểm tra KT2)", "Đinh Gia Bảo, Trần Đặng Công Tâm", "Báo cáo KT2"),

        # Tuần 7: Tích hợp AI Hành chính & Bảo mật PII
        ("Tuần 07 (Từ: 07/09/2026 Đến: 13/09/2026)", "Xây dựng module PII Anonymizer khử số CCCD, số điện thoại, mã thẻ BHYT trước khi gọi mô hình", "Đinh Gia Bảo", "Module khử PII"),
        ("Tuần 07 (Từ: 07/09/2026 Đến: 13/09/2026)", "Thiết lập rào chắn an toàn Medical Guardrails ngăn Prompt Injection và từ chối tự động chẩn đoán bệnh", "Đinh Gia Bảo", "Rào chắn an toàn AI"),
        ("Tuần 07 (Từ: 07/09/2026 Đến: 13/09/2026)", "Tích hợp Google Gemini Live API và xây dựng cơ chế Mock Fallback khi gián đoạn kết nối mạng", "Đinh Gia Bảo", "Bộ điều phối AI"),
        ("Tuần 07 (Từ: 07/09/2026 Đến: 13/09/2026)", "Xây dựng ba tính năng AI gồm Tóm tắt tiền sử (Pre-visit), Chatbot FAQ (RAG), Hướng dẫn xuất viện", "Đinh Gia Bảo, Trần Đặng Công Tâm", "Bộ ba trợ lý AI"),
        ("Tuần 07 (Từ: 07/09/2026 Đến: 13/09/2026)", "Phát triển phân hệ Viện phí (Khấu trừ quyền lợi BHYT 80% hoặc 100%, sinh mã thanh toán VietQR động)", "Trần Đặng Công Tâm", "Màn hình Viện phí"),

        # Tuần 8: Kiểm thử đa tầng & Rà soát an ninh
        ("Tuần 08 (Từ: 14/09/2026 Đến: 20/09/2026)", "Viết bộ kiểm thử tự động Pytest bao phủ 13 tệp test suite với 323 ca kiểm thử đạt tỷ lệ 100%", "Trần Đặng Công Tâm", "Bộ test 323 ca kiểm thử"),
        ("Tuần 08 (Từ: 14/09/2026 Đến: 20/09/2026)", "Thực hiện kiểm thử an ninh tấn công mô hình AI (Adversarial Security Test) và phòng chống Jailbreak", "Đinh Gia Bảo", "Kiểm thử bảo mật AI"),
        ("Tuần 08 (Từ: 14/09/2026 Đến: 20/09/2026)", "Kiểm toán an toàn thông tin y tế theo mô hình STRIDE và tiêu chuẩn OWASP Top 10", "Đinh Gia Bảo", "Báo cáo an ninh y tế"),
        ("Tuần 08 (Từ: 14/09/2026 Đến: 20/09/2026)", "Đánh giá chất lượng mã nguồn đa chiều và kích hoạt cổng phê duyệt Human Gate 2 (Chất lượng mã)", "Trần Đặng Công Tâm, Đinh Gia Bảo", "Nghiệm thu Human Gate 2"),
        ("Tuần 08 (Từ: 14/09/2026 Đến: 20/09/2026)", "Hoàn thành và nghiệm thu Báo cáo cột mốc Giai đoạn 3 (Bài kiểm tra KT3)", "Đinh Gia Bảo, Trần Đặng Công Tâm", "Báo cáo KT3"),

        # Tuần 9: Đóng gói Docker, Hướng dẫn sử dụng & Nghiệm thu
        ("Tuần 09 (Từ: 21/09/2026 Đến: 27/09/2026)", "Đóng gói hệ thống bằng Docker Compose với ba dịch vụ gồm clinic_mysql, clinic_backend, clinic_frontend", "Đinh Gia Bảo", "Docker Compose"),
        ("Tuần 09 (Từ: 21/09/2026 Đến: 27/09/2026)", "Soạn thảo Sổ tay Hướng dẫn sử dụng chi tiết cho bốn vai trò người dùng kèm tài khoản thử nghiệm", "Trần Đặng Công Tâm", "User Guide 4 vai trò"),
        ("Tuần 09 (Từ: 21/09/2026 Đến: 27/09/2026)", "Xây dựng kịch bản trình diễn hệ thống 8 bước khép kín phục vụ hội đồng đánh giá chấm điểm", "Trần Đặng Công Tâm", "Kịch bản Demo chấm điểm"),
        ("Tuần 09 (Từ: 21/09/2026 Đến: 27/09/2026)", "Biên soạn báo cáo tổng kết thực hành AI-Augmented SDLC ghi nhận tương tác giữa con người và AI", "Đinh Gia Bảo", "Báo cáo AI SDLC"),
        ("Tuần 09 (Từ: 21/09/2026 Đến: 27/09/2026)", "Đánh giá nghiệm thu tổng thể dự án và kích hoạt cổng Human Gate 3 (Bảo vệ đồ án cuối kỳ)", "Đinh Gia Bảo, Trần Đặng Công Tâm", "Nghiệm thu cuối kỳ")
    ]

    # Tạo bảng
    table = doc.add_table(rows=len(tasks_data) + 1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    col_widths = [Inches(1.8), Inches(2.7), Inches(1.0), Inches(1.0)]
    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    # Hàng tiêu đề
    headers = ["Thời gian / Tuần", "Công việc thực hiện", "Thành viên", "Ghi chú"]
    for i, h_text in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h_text
    format_row(table.rows[0], HEX_HEADER_BG, RGBColor(255, 255, 255), bold=True, is_header=True)

    # Các hàng dữ liệu
    for r_idx, data in enumerate(tasks_data):
        row = table.rows[r_idx + 1]
        for c_idx, val in enumerate(data):
            row.cells[c_idx].text = val
        bg = HEX_ROW_ALT if (r_idx % 2 == 1) else "FFFFFF"
        format_row(row, bg, RGBColor(15, 23, 42), bold=False, is_header=False)

    set_table_borders(table)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Chữ ký xác nhận
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(16)
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sign = p_sign.add_run("Thái Nguyên, ngày 27 tháng 09 năm 2026\nĐẠI DIỆN NHÓM THỰC HIỆN\n\n\n\nĐinh Gia Bảo (Trưởng nhóm) và Trần Đặng Công Tâm")
    r_sign.font.name = "Times New Roman"
    r_sign.font.size = Pt(10)
    r_sign.font.bold = True

    save_document(doc, "01_GenAI_SoftwareDevelopment_project-plan.docx")

if __name__ == "__main__":
    build_project_plan()
