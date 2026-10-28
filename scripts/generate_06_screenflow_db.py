# -*- coding: utf-8 -*-
"""
Script sinh file 06_GenAI_SoftwareDevelopment_screenflow_db.docx
Screen Flow và Tài liệu thiết kế Cơ sở dữ liệu hệ thống CMS-AI (Nhóm 03).
Bổ sung:
- Sơ đồ Screen Flow điều hướng 4 vai trò (diagram_ui_flows_role.png)
- Sơ đồ thực thể quan hệ CSDL 14 bảng chuẩn 3NF (diagram_database_erd.png)
- Từ điển dữ liệu chuẩn hóa chi tiết 14 bảng CSDL quan hệ (Data Dictionary)
- Ràng buộc toàn vẹn dữ liệu và an toàn thông tin
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

def build_screenflow_db():
    doc = create_base_document()

    add_header_block(
        doc,
        "SCREEN FLOW & TÀI LIỆU THIẾT KẾ CƠ SỞ DỮ LIỆU",
        "HỆ THỐNG QUẢN LÝ PHÒNG KHÁM CÓ TÍCH HỢP AI (CMS-AI)"
    )

    add_team_meta(doc)

    add_p(
        doc,
        "Tài liệu mô tả chi tiết luồng chuyển màn hình (Screen Flow) theo từng vai trò người dùng "
        "và thiết kế cơ sở dữ liệu quan hệ 14 bảng đạt chuẩn chuẩn hóa 3NF của Hệ thống CMS-AI. "
        "Cấu trúc này bảo đảm tính công thái học trong vận hành y tế, khả năng đáp ứng cao và tính toàn vẹn tuyệt đối của dữ liệu bệnh nhân."
    )

    # 1. SCREEN FLOW: PHÂN LUỒNG MÀN HÌNH CỦA ỨNG DỤNG
    add_h1(doc, "1. Screen Flow: Phân luồng màn hình của ứng dụng")

    add_h2(doc, "1.1. Sơ đồ điều hướng tổng quát (Application Screen Map)")
    add_p(
        doc,
        "Hệ thống phân tách điều hướng độc lập ngay sau bước xác thực đăng nhập dựa trên trường vai trò trong mã token JWT. "
        "Dưới đây là sơ đồ tương tác và luồng chuyển màn hình trực quan cho 4 vai trò người dùng trong hệ thống CMS-AI:"
    )

    # Chèn sơ đồ Screen Flow 4 vai trò
    sf_img = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "generated_diagrams", "diagram_ui_flows_role.png"))
    add_diagram(doc, sf_img, "Hình 1.1: Sơ đồ tương tác luồng giao diện (Screen Flow) theo 4 vai trò người dùng (300 DPI)", width=Inches(6.4))

    add_h2(doc, "1.2. Phân luồng màn hình chi tiết theo 4 vai trò")

    flows_detailed = [
        (
            "Phân hệ Lễ tân (Receptionist Flow):",
            "1. Màn hình Đăng nhập -> Nhập tài khoản lễ tân -> Chuyển đến ReceptionistDashboard.\n"
            "2. Màn hình Tiếp đón bệnh nhân: Tìm kiếm bệnh nhân theo số CCCD hoặc SĐT. Nếu chưa có, mở biểu mẫu 'Đăng ký bệnh nhân mới', nhập thông tin nhân khẩu và mã thẻ BHYT.\n"
            "3. Màn hình Đặt lịch khám: Chọn bệnh nhân, chuyên khoa, bác sĩ và khung giờ. Hệ thống hiển thị trạng thái phòng khám và cảnh báo trùng lịch tức thời.\n"
            "4. Màn hình Hàng đợi (Queue Management): Xem danh sách bệnh nhân đang chờ tại các phòng khám, điều phối số thứ tự và chuyển bệnh nhân vào phòng khám."
        ),
        (
            "Phân hệ Bác sĩ (Doctor Flow):",
            "1. Màn hình Bác sĩ Dashboard: Xem lịch trực hôm nay, danh sách bệnh nhân đang đợi trước cửa phòng khám.\n"
            "2. Màn hình Bàn khám lâm sàng EMR: Chọn bệnh nhân, mở hồ sơ. Nhấn nút 'Xem tóm tắt AI' để mở thẻ AI Pre-visit Briefing hiển thị diễn tiến bệnh cũ.\n"
            "3. Nhập triệu chứng và sinh hiệu: Điền huyết áp, mạch, nhiệt độ, SpO2, chiều cao, cân nặng. Hệ thống tự động tính chỉ số BMI.\n"
            "4. Chẩn đoán và Kê đơn: Chọn mã bệnh ICD-10. Thêm danh mục thuốc từ kho dược. Hệ thống đối soát tiền sử dị ứng và hiển thị cảnh báo đỏ nếu phát hiện trùng dị ứng.\n"
            "5. Màn hình AI Dặn dò xuất viện: Nhấn nút tạo dặn dò, AI tự động sinh bảng nhắc lịch uống thuốc và chế độ ăn. Bác sĩ nhấn 'Hoàn tất khám'."
        ),
        (
            "Phân hệ Kế toán (Accountant Flow):",
            "1. Màn hình Kế toán Dashboard: Xem tổng doanh thu trong ngày, số hóa đơn đã thu và danh sách hồ sơ chờ thanh toán.\n"
            "2. Màn hình Chi tiết hóa đơn: Mở hồ sơ của người bệnh vừa khám xong. Hệ thống tự động liệt kê tiền khám, tiền thuốc và mức giảm trừ BHYT (80% hoặc 100%).\n"
            "3. Màn hình Thanh toán VietQR: Chọn phương thức chuyển khoản, hệ thống hiển thị mã VietQR động NAPAS chứa đúng số tiền đồng chi trả.\n"
            "4. Xác nhận thanh toán & In hóa đơn: Khi người bệnh thanh toán thành công, kế toán bấm 'Xác nhận', hệ thống mở bản in biên lai thu tiền hợp lệ."
        ),
        (
            "Phân hệ Quản trị viên (Admin Flow):",
            "1. Màn hình Admin Dashboard: Xem biểu đồ doanh thu theo tuần/tháng, số lượt khám theo chuyên khoa và hiệu suất làm việc của bác sĩ.\n"
            "2. Màn hình Phân ca làm việc: Thiết lập lịch trực theo tuần cho từng bác sĩ (Ca sáng, chiều, tối) và gán phòng khám tương ứng.\n"
            "3. Màn hình Quản lý kho dược & Dịch vụ: Thêm mới thuốc, cập nhật giá bán, kiểm tra số lượng tồn kho và thiết lập cảnh báo thuốc sắp hết.\n"
            "4. Màn hình Quản trị người dùng & Phân quyền: Tạo tài khoản nhân sự mới, gán vai trò RBAC và khóa tài khoản vi phạm.\n"
            "5. Màn hình Nhật ký kiểm toán (Audit Logs) & AI Logs: Giám sát toàn bộ thao tác thêm/sửa/xóa hồ sơ bệnh án và lịch sử gọi API trí tuệ nhân tạo."
        )
    ]

    for title, desc in flows_detailed:
        add_h3(doc, title)
        add_p(doc, desc)

    # 2. CƠ SỞ DỮ LIỆU
    add_h1(doc, "2. Cơ sở dữ liệu")

    add_h2(doc, "2.1. Sơ đồ thực thể quan hệ (Entity Relationship Diagram - ERD)")
    add_p(
        doc,
        "Cơ sở dữ liệu của Hệ thống CMS-AI gồm 14 bảng quan hệ được thiết kế chuẩn hóa đạt chuẩn 3NF, "
        "bảo đảm không có dữ liệu dư thừa bất thường, duy trì tính toàn vẹn tham chiếu và tối ưu hóa hiệu năng truy vấn:"
    )

    # Chèn sơ đồ ERD 14 bảng 3NF chất lượng cao
    erd_img = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "generated_diagrams", "diagram_database_erd.png"))
    add_diagram(doc, erd_img, "Hình 2.1: Sơ đồ thực thể quan hệ CSDL 14 bảng chuẩn 3NF của Hệ thống CMS-AI (300 DPI)", width=Inches(6.4))

    add_h2(doc, "2.2. Từ điển dữ liệu chi tiết 14 bảng cơ sở dữ liệu quan hệ (Data Dictionary)")
    add_p(
        doc,
        "Đặc tả cấu trúc chi tiết từng cột, kiểu dữ liệu, ràng buộc khóa chính (PK), khóa ngoại (FK) và mục đích sử dụng cho toàn bộ 14 bảng trong hệ thống:"
    )

    # Helper vẽ bảng lược đồ
    def render_schema_table(doc, table_name, desc_text, columns):
        add_h3(doc, f"Bảng: {table_name}")
        p_desc = doc.add_paragraph()
        p_desc.paragraph_format.space_before = Pt(2)
        p_desc.paragraph_format.space_after = Pt(4)
        r = p_desc.add_run(f"Mô tả: {desc_text}")
        r.font.name = "Times New Roman"
        r.font.italic = True
        r.font.size = Pt(10)

        tbl = doc.add_table(rows=len(columns) + 1, cols=4)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        tbl.columns[0].width = Inches(1.5)
        tbl.columns[1].width = Inches(1.2)
        tbl.columns[2].width = Inches(1.3)
        tbl.columns[3].width = Inches(2.5)

        headers = ["Tên cột (Column)", "Kiểu dữ liệu", "Ràng buộc (Constraints)", "Ý nghĩa nghiệp vụ"]
        for idx, h in enumerate(headers):
            tbl.cell(0, idx).text = h
        format_row(tbl.rows[0], HEX_HEADER_BG, RGBColor(255, 255, 255), bold=True, is_header=True)

        for r_i, (c_name, c_type, c_const, c_note) in enumerate(columns):
            row = tbl.rows[r_i + 1]
            row.cells[0].text = c_name
            row.cells[1].text = c_type
            row.cells[2].text = c_const
            row.cells[3].text = c_note
            bg = HEX_ROW_ALT if (r_i % 2 == 1) else "FFFFFF"
            format_row(row, bg, RGBColor(15, 23, 42), bold=False, is_header=False)
            row.cells[0].paragraphs[0].runs[0].font.name = "Consolas"
            row.cells[0].paragraphs[0].runs[0].font.bold = True
            row.cells[0].paragraphs[0].runs[0].font.size = Pt(9)

        set_table_borders(tbl)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 1. users
    render_schema_table(doc, "users", "Quản lý danh sách tài khoản người dùng và xác thực nhân viên phòng khám.", [
        ("id", "INTEGER", "PRIMARY KEY, AUTO_INCREMENT", "Mã định danh duy nhất người dùng"),
        ("username", "VARCHAR(50)", "NOT NULL, UNIQUE", "Tên tài khoản đăng nhập hệ thống"),
        ("email", "VARCHAR(100)", "NOT NULL, UNIQUE", "Địa chỉ thư điện tử liên hệ"),
        ("full_name", "VARCHAR(100)", "NOT NULL", "Họ và tên đầy đủ của nhân sự"),
        ("hashed_password", "VARCHAR(255)", "NOT NULL", "Chuỗi mật khẩu đã băm bằng thuật toán Bcrypt"),
        ("role", "VARCHAR(20)", "NOT NULL", "Vai trò: admin, receptionist, doctor, accountant"),
        ("is_active", "BOOLEAN", "NOT NULL, DEFAULT TRUE", "Trạng thái kích hoạt tài khoản"),
        ("created_at", "DATETIME", "NOT NULL, DEFAULT CURRENT_TIMESTAMP", "Thời điểm khởi tạo tài khoản")
    ])

    # 2. patients
    render_schema_table(doc, "patients", "Lưu trữ hồ sơ nhân khẩu, định danh cá nhân và tiền sử y tế bệnh nhân.", [
        ("id", "INTEGER", "PRIMARY KEY, AUTO_INCREMENT", "Khóa chính hồ sơ bệnh nhân"),
        ("medical_code", "VARCHAR(20)", "NOT NULL, UNIQUE", "Mã số định danh y tế (VD: BN-2026-0001)"),
        ("full_name", "VARCHAR(100)", "NOT NULL", "Họ và tên bệnh nhân"),
        ("date_of_birth", "DATE", "NOT NULL", "Ngày tháng năm sinh"),
        ("gender", "VARCHAR(10)", "NOT NULL", "Giới tính (MALE, FEMALE, OTHER)"),
        ("phone", "VARCHAR(20)", "NOT NULL, INDEX", "Số điện thoại liên hệ chính"),
        ("identity_card", "VARCHAR(20)", "UNIQUE", "Số CCCD/CMND 12 chữ số"),
        ("address", "VARCHAR(255)", "NULL", "Địa chỉ cư trú thường trú"),
        ("insurance_number", "VARCHAR(20)", "NULL, INDEX", "Mã số thẻ Bảo hiểm Y tế (BHYT) 15 ký tự"),
        ("medical_history", "TEXT", "NULL", "Tóm tắt tiền sử bệnh mãn tính, phẫu thuật cũ"),
        ("drug_allergies", "TEXT", "NULL", "Danh mục hoạt chất thuốc bị dị ứng"),
        ("emergency_contact", "VARCHAR(100)", "NULL", "Tên và SĐT người thân liên hệ khẩn cấp"),
        ("created_at", "DATETIME", "DEFAULT CURRENT_TIMESTAMP", "Thời điểm đăng ký hồ sơ")
    ])

    # 3. specialties
    render_schema_table(doc, "specialties", "Danh mục các chuyên khoa y tế phục vụ khám bệnh.", [
        ("id", "INTEGER", "PRIMARY KEY, AUTO_INCREMENT", "Mã định danh chuyên khoa"),
        ("name", "VARCHAR(100)", "NOT NULL, UNIQUE", "Tên chuyên khoa (Nội khoa, Ngoại khoa, Nhi...)"),
        ("description", "VARCHAR(255)", "NULL", "Mô tả phạm vi chuyên môn tiếp nhận"),
        ("is_active", "BOOLEAN", "DEFAULT TRUE", "Trạng thái hoạt động của chuyên khoa"),
        ("created_at", "DATETIME", "DEFAULT CURRENT_TIMESTAMP", "Thời điểm tạo")
    ])

    # 4. clinics
    render_schema_table(doc, "clinics", "Quản lý buồng khám vật lý tại cơ sở y tế.", [
        ("id", "INTEGER", "PRIMARY KEY, AUTO_INCREMENT", "Mã định danh buồng khám"),
        ("name", "VARCHAR(100)", "NOT NULL", "Tên hiển thị (VD: Phòng khám Nội 101)"),
        ("room_number", "VARCHAR(20)", "NOT NULL, UNIQUE", "Số phòng trên thực địa"),
        ("specialty_id", "INTEGER", "NOT NULL, FK -> specialties.id", "Chuyên khoa của buồng khám"),
        ("is_active", "BOOLEAN", "DEFAULT TRUE", "Trạng thái buồng khám sẵn sàng")
    ])

    # 5. doctors
    render_schema_table(doc, "doctors", "Thông tin chuyên môn, chứng chỉ hành nghề của bác sĩ.", [
        ("id", "INTEGER", "PRIMARY KEY, AUTO_INCREMENT", "Mã định danh bác sĩ"),
        ("user_id", "INTEGER", "NOT NULL, UNIQUE, FK -> users.id", "Liên kết tài khoản người dùng"),
        ("specialty_id", "INTEGER", "NOT NULL, FK -> specialties.id", "Chuyên khoa chuyên môn"),
        ("clinic_id", "INTEGER", "NULL, FK -> clinics.id", "Buồng khám làm việc chính"),
        ("license_number", "VARCHAR(50)", "NOT NULL, UNIQUE", "Số chứng chỉ hành nghề y"),
        ("title", "VARCHAR(50)", "NULL", "Học hàm, học vị (BS.CKI, ThS.BS, PGS.TS)"),
        ("bio", "TEXT", "NULL", "Tóm tắt kinh nghiệm công tác"),
        ("phone", "VARCHAR(20)", "NULL", "Số điện thoại liên hệ nghiệp vụ"),
        ("max_patients_per_shift", "INTEGER", "DEFAULT 20", "Số lượt khám tối đa trong 1 ca trực"),
        ("is_active", "BOOLEAN", "DEFAULT TRUE", "Trạng thái đang công tác")
    ])

    # 6. doctor_shifts
    render_schema_table(doc, "doctor_shifts", "Lịch trực theo ca của bác sĩ làm căn cứ kiểm tra xung đột.", [
        ("id", "INTEGER", "PRIMARY KEY, AUTO_INCREMENT", "Mã định danh ca trực"),
        ("doctor_id", "INTEGER", "NOT NULL, FK -> doctors.id", "Bác sĩ phụ trách"),
        ("clinic_id", "INTEGER", "NOT NULL, FK -> clinics.id", "Buồng khám phân công"),
        ("shift_date", "DATE", "NOT NULL, INDEX", "Ngày làm việc của ca"),
        ("start_time", "TIME", "NOT NULL", "Giờ bắt đầu ca trực (VD: 08:00:00)"),
        ("end_time", "TIME", "NOT NULL", "Giờ kết thúc ca trực (VD: 12:00:00)"),
        ("max_patients", "INTEGER", "DEFAULT 20", "Giới hạn số bệnh nhân tiếp nhận"),
        ("status", "VARCHAR(20)", "DEFAULT 'SCHEDULED'", "Trạng thái: SCHEDULED, ACTIVE, COMPLETED")
    ])

    # 7. appointments
    render_schema_table(doc, "appointments", "Lịch hẹn khám bệnh và dữ liệu quản lý hàng đợi tiếp đón.", [
        ("id", "INTEGER", "PRIMARY KEY, AUTO_INCREMENT", "Mã định danh lịch hẹn"),
        ("appointment_code", "VARCHAR(20)", "NOT NULL, UNIQUE", "Mã phiếu hẹn (VD: APT-2026-0001)"),
        ("patient_id", "INTEGER", "NOT NULL, FK -> patients.id", "Bệnh nhân đặt khám"),
        ("doctor_id", "INTEGER", "NOT NULL, FK -> doctors.id", "Bác sĩ chỉ định"),
        ("clinic_id", "INTEGER", "NOT NULL, FK -> clinics.id", "Buồng khám chỉ định"),
        ("appointment_date", "DATE", "NOT NULL, INDEX", "Ngày hẹn khám"),
        ("start_time", "TIME", "NOT NULL", "Giờ hẹn bắt đầu"),
        ("end_time", "TIME", "NOT NULL", "Giờ hẹn kết thúc"),
        ("status", "VARCHAR(20)", "NOT NULL, DEFAULT 'PENDING'", "PENDING, CONFIRMED, COMPLETED, CANCELLED"),
        ("reason", "VARCHAR(255)", "NULL", "Lý do khám bệnh ban đầu"),
        ("notes", "TEXT", "NULL", "Ghi chú điều phối lễ tân")
    ])

    # 8. medical_records
    render_schema_table(doc, "medical_records", "Hồ sơ bệnh án điện tử EMR ghi nhận kết quả khám và chỉ số sinh hiệu.", [
        ("id", "INTEGER", "PRIMARY KEY, AUTO_INCREMENT", "Mã định danh bệnh án EMR"),
        ("record_code", "VARCHAR(20)", "NOT NULL, UNIQUE", "Mã phiếu khám bệnh"),
        ("appointment_id", "INTEGER", "NULL, UNIQUE, FK -> appointments.id", "Lịch hẹn liên kết"),
        ("patient_id", "INTEGER", "NOT NULL, FK -> patients.id", "Bệnh nhân được khám"),
        ("doctor_id", "INTEGER", "NOT NULL, FK -> doctors.id", "Bác sĩ trực tiếp khám"),
        ("pulse", "INTEGER", "NULL", "Nhịp tim (lần/phút)"),
        ("blood_pressure", "VARCHAR(20)", "NULL", "Huyết áp tâm thu/tâm trương (mmHg)"),
        ("temperature", "DECIMAL(4,1)", "NULL", "Nhiệt độ cơ thể (độ C)"),
        ("spo2", "INTEGER", "NULL", "Độ bão hòa oxy trong máu (%)"),
        ("height", "DECIMAL(5,1)", "NULL", "Chiều cao bệnh nhân (cm)"),
        ("weight", "DECIMAL(5,1)", "NULL", "Cân nặng bệnh nhân (kg)"),
        ("bmi", "DECIMAL(4,2)", "NULL", "Chỉ số khối cơ thể tính tự động"),
        ("symptoms", "TEXT", "NOT NULL", "Triệu chứng cơ năng và lý do vào viện"),
        ("icd10_code", "VARCHAR(20)", "NULL, INDEX", "Mã chẩn đoán chuẩn quốc tế ICD-10"),
        ("diagnosis", "TEXT", "NOT NULL", "Kết luận chẩn đoán xác định bệnh"),
        ("status", "VARCHAR(20)", "NOT NULL, DEFAULT 'DRAFT'", "DRAFT, COMPLETED, CANCELLED")
    ])

    # 9. service_orders
    render_schema_table(doc, "service_orders", "Chỉ định cận lâm sàng, xét nghiệm và kỹ thuật y khoa.", [
        ("id", "INTEGER", "PRIMARY KEY, AUTO_INCREMENT", "Mã chỉ định dịch vụ"),
        ("medical_record_id", "INTEGER", "NOT NULL, FK -> medical_records.id", "Hồ sơ bệnh án liên kết"),
        ("service_name", "VARCHAR(100)", "NOT NULL", "Tên dịch vụ kỹ thuật"),
        ("unit_price", "DECIMAL(12,2)", "NOT NULL", "Đơn giá niêm yết"),
        ("quantity", "INTEGER", "DEFAULT 1", "Số lượng chỉ định"),
        ("status", "VARCHAR(20)", "DEFAULT 'PENDING'", "PENDING, COMPLETED, CANCELLED"),
        ("result_summary", "TEXT", "NULL", "Tóm tắt kết luận kỹ thuật cận lâm sàng")
    ])

    # 10. prescriptions
    render_schema_table(doc, "prescriptions", "Đơn thuốc điện tử do bác sĩ kê trong phiên khám.", [
        ("id", "INTEGER", "PRIMARY KEY, AUTO_INCREMENT", "Mã định danh đơn thuốc"),
        ("prescription_code", "VARCHAR(20)", "NOT NULL, UNIQUE", "Mã đơn thuốc điện tử"),
        ("medical_record_id", "INTEGER", "NOT NULL, UNIQUE, FK -> medical_records.id", "Bệnh án tương ứng"),
        ("doctor_id", "INTEGER", "NOT NULL, FK -> doctors.id", "Bác sĩ kê đơn"),
        ("usage_instructions", "TEXT", "NULL", "Lời dặn dò chung về chế độ dùng thuốc"),
        ("created_at", "DATETIME", "DEFAULT CURRENT_TIMESTAMP", "Thời điểm kê đơn")
    ])

    # 11. prescription_items
    render_schema_table(doc, "prescription_items", "Chi tiết từng loại thuốc, liều dùng và cách dùng trong đơn.", [
        ("id", "INTEGER", "PRIMARY KEY, AUTO_INCREMENT", "Mã chi tiết đơn thuốc"),
        ("prescription_id", "INTEGER", "NOT NULL, FK -> prescriptions.id", "Đơn thuốc chứa mục này"),
        ("medicine_id", "INTEGER", "NOT NULL, FK -> medicines.id", "Loại thuốc được cấp"),
        ("quantity", "INTEGER", "NOT NULL", "Tổng số lượng viên/gói"),
        ("dosage", "VARCHAR(100)", "NOT NULL", "Liều lượng mỗi lần dùng"),
        ("morning", "INTEGER", "DEFAULT 0", "Số lượng uống buổi sáng"),
        ("noon", "INTEGER", "DEFAULT 0", "Số lượng uống buổi trưa"),
        ("afternoon", "INTEGER", "DEFAULT 0", "Số lượng uống buổi chiều"),
        ("evening", "INTEGER", "DEFAULT 0", "Số lượng uống buổi tối"),
        ("notes", "VARCHAR(255)", "NULL", "Lời dặn riêng (uống trước/sau ăn)")
    ])

    # 12. medicines
    render_schema_table(doc, "medicines", "Quản lý danh mục dược phẩm và theo dõi tồn kho thuốc.", [
        ("id", "INTEGER", "PRIMARY KEY, AUTO_INCREMENT", "Mã định danh dược phẩm"),
        ("medicine_code", "VARCHAR(20)", "NOT NULL, UNIQUE", "Mã thuốc theo quy chuẩn"),
        ("name", "VARCHAR(100)", "NOT NULL", "Tên thương mại của thuốc"),
        ("active_ingredient", "VARCHAR(100)", "NOT NULL", "Tên hoạt chất chính phục vụ kiểm tra dị ứng"),
        ("unit", "VARCHAR(20)", "NOT NULL", "Đơn vị tính (Viên, Gói, Chai, Hộp)"),
        ("unit_price", "DECIMAL(12,2)", "NOT NULL", "Đơn giá bán niêm yết (VNĐ)"),
        ("stock_quantity", "INTEGER", "NOT NULL, DEFAULT 0", "Số lượng hiện có trong kho"),
        ("min_stock_alert", "INTEGER", "DEFAULT 10", "Ngưỡng cảnh báo sắp hết hàng"),
        ("is_active", "BOOLEAN", "DEFAULT TRUE", "Trạng thái còn lưu hành")
    ])

    # 13. invoices
    render_schema_table(doc, "invoices", "Quản lý hóa đơn viện phí, khấu trừ BHYT và giao dịch VietQR.", [
        ("id", "INTEGER", "PRIMARY KEY, AUTO_INCREMENT", "Mã định danh hóa đơn"),
        ("invoice_code", "VARCHAR(20)", "NOT NULL, UNIQUE", "Mã hóa đơn tài chính (INV-2026-XXXX)"),
        ("medical_record_id", "INTEGER", "NOT NULL, UNIQUE, FK -> medical_records.id", "Bệnh án tương ứng"),
        ("patient_id", "INTEGER", "NOT NULL, FK -> patients.id", "Bệnh nhân thanh toán"),
        ("total_amount", "DECIMAL(12,2)", "NOT NULL", "Tổng chi phí trước giảm trừ"),
        ("insurance_deduction", "DECIMAL(12,2)", "NOT NULL, DEFAULT 0", "Số tiền BHYT chi trả"),
        ("patient_pay_amount", "DECIMAL(12,2)", "NOT NULL", "Số tiền bệnh nhân phải đồng chi trả"),
        ("payment_method", "VARCHAR(20)", "NULL", "CASH, BANK_TRANSFER, VIETQR"),
        ("payment_status", "VARCHAR(20)", "NOT NULL, DEFAULT 'UNPAID'", "UNPAID, PAID, CANCELLED"),
        ("vietqr_url", "TEXT", "NULL", "Đường dẫn mã QR thanh toán động NAPAS"),
        ("paid_at", "DATETIME", "NULL", "Thời điểm hoàn tất giao dịch")
    ])

    # 14. audit_logs
    render_schema_table(doc, "audit_logs", "Lưu vết bất biến mọi thao tác an ninh và nhật ký kiểm toán hệ thống.", [
        ("id", "INTEGER", "PRIMARY KEY, AUTO_INCREMENT", "Mã bản ghi kiểm toán"),
        ("user_id", "INTEGER", "NULL, FK -> users.id", "Người dùng thực hiện hành động"),
        ("action", "VARCHAR(50)", "NOT NULL", "Hành động (LOGIN, EMR_VIEW, AI_CALL, PAY)"),
        ("resource", "VARCHAR(100)", "NOT NULL", "Đối tượng tác động (Patient, Invoice...)"),
        ("resource_id", "INTEGER", "NULL", "Mã của đối tượng bị tác động"),
        ("ip_address", "VARCHAR(45)", "NOT NULL", "Địa chỉ IPv4/IPv6 máy Client"),
        ("details", "TEXT", "NULL", "Thông tin bổ sung chi tiết về thay đổi"),
        ("payload_hash", "VARCHAR(64)", "NULL", "Mã băm SHA-256 bảo đảm tính toàn vẹn"),
        ("created_at", "DATETIME", "DEFAULT CURRENT_TIMESTAMP", "Thời điểm ghi nhận sự kiện")
    ])

    add_h2(doc, "2.3. Các ràng buộc toàn vẹn trong CSDL (Database Integrity Constraints)")

    integrity_rules = [
        ("1. Ràng buộc thực thể (Entity Integrity): ", "Mỗi bảng đều có một khóa chính (PK) duy nhất kiểu số nguyên tự tăng hoặc UUID không mang giá trị NULL, bảo đảm tính định danh xác thực."),
        ("2. Ràng buộc tham chiếu (Referential Integrity): ", "Các khóa ngoại (FK) liên kết chính xác giữa các bảng. Áp dụng quy tắc ON DELETE RESTRICT cho bảng bệnh nhân và bác sĩ (không cho phép xóa người bệnh khi đã có lịch sử khám bệnh). Áp dụng ON DELETE CASCADE cho chi tiết đơn thuốc và chi tiết hóa đơn."),
        ("3. Ràng buộc duy nhất (Unique Constraints): ", "Số CCCD (identity_card) gồm 12 số là duy nhất trong toàn hệ thống. Mã thẻ BHYT (insurance_number) 15 ký tự là duy nhất. Tên đăng nhập (username) và mã thuốc (medicine_code) không được trùng lặp."),
        ("4. Ràng buộc kiểm tra miền giá trị (Check Constraints): ", "Số lượng thuốc (quantity > 0), đơn giá dược phẩm (unit_price >= 0), chỉ số SpO2 trong khoảng 0 đến 100%, huyết áp và mạch mang giá trị số dương hợp lý. Trạng thái lịch hẹn chỉ nhận các giá trị: 'pending', 'confirmed', 'in_progress', 'completed', 'cancelled'."),
        ("5. Ràng buộc toàn vẹn thời gian chống trùng lịch (Temporal Integrity): ", "Ràng buộc không giao thoa thời gian đối với bác sĩ và phòng khám. Hai lịch hẹn của cùng một bác sĩ hoặc cùng một phòng khám phải thỏa mãn điều kiện thời gian kết thúc của lịch trước nhỏ hơn hoặc bằng thời gian bắt đầu của lịch sau: E1 <= S2 hoặc E2 <= S1.")
    ]

    for title, desc in integrity_rules:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(title)
        r1.font.bold = True
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        r2 = p.add_run(desc)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11)

    save_document(doc, "06_GenAI_SoftwareDevelopment_screenflow_db.docx")

if __name__ == "__main__":
    build_screenflow_db()
