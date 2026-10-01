# -*- coding: utf-8 -*-
"""
Script sinh file 06_GenAI_SoftwareDevelopment_screenflow_db.docx
Screen Flow và Tài liệu thiết kế Cơ sở dữ liệu hệ thống CMS-AI (Nhóm 07).
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
        "Cấu trúc này bảo đảm tính công thái học trong vận hành y tế và tính toàn vẹn của dữ liệu bệnh nhân."
    )

    # 1. SCREEN FLOW: PHÂN LUỒNG MÀN HÌNH CỦA ỨNG DỤNG
    add_h1(doc, "1. Screen Flow: Phân luồng màn hình của ứng dụng")

    add_h2(doc, "1.1. Sơ đồ điều hướng tổng quát (Application Screen Map)")
    add_p(
        doc,
        "Hệ thống phân tách điều hướng độc lập ngay sau bước xác thực đăng nhập dựa trên trường vai trò trong mã token JWT:"
    )

    app_flow_ascii = """+----------------------------------------------------------------------------------------------------+
|                                    SƠ ĐỒ ĐIỀU HƯỚNG TỔNG QUÁT HỆ THỐNG                             |
+----------------------------------------------------------------------------------------------------+
                                      [Màn hình Đăng nhập (Login)]
                                                   |
                             +---------------------+---------------------+
                             | (Xác thực JWT Role) |                     |
                             v                     v                     v
     [Lễ tân Dashboard]             [Bác sĩ Dashboard]          [Kế toán Dashboard]          [Admin Dashboard]
             |                              |                           |                            |
    +--------+--------+            +--------+--------+         +--------+--------+          +--------+--------+
    |                 |            |                 |         |                 |          |        |        |
    v                 v            v                 v         v                 v          v        v        v
[Tiếp đón BN]   [Đặt lịch &    [Hàng đợi EMR]  [Bàn khám    [DS Hóa đơn]   [Thu tiền &    [Phân ca [QL Thuốc [Audit
                 Hàng đợi]                      lâm sàng]                   VietQR]        bác sĩ]  & Giá]    Logs]
                                                     |
                                            +--------+--------+
                                            |                 |
                                            v                 v
                                     [AI Pre-visit]    [AI Dặn dò]
+----------------------------------------------------------------------------------------------------+"""
    add_code_block(doc, app_flow_ascii)

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

    add_h2(doc, "2.1. Cơ sở dữ liệu quan hệ (Relational Database Design)")
    add_p(
        doc,
        "Cơ sở dữ liệu của Hệ thống CMS-AI gồm 14 bảng quan hệ được chuẩn hóa đạt chuẩn 3NF, "
        "bảo đảm không có dữ liệu dư thừa bất thường và duy trì tính toàn vẹn tham chiếu:"
    )

    erd_ascii = """+----------------------------------------------------------------------------------------------------+
|                                    SƠ ĐỒ THỰC THỂ QUAN HỆ (ERD 14 BẢNG)                            |
+----------------------------------------------------------------------------------------------------+
  [roles] 1 ────── 0..* [users] 1 ────── 0..1 [doctors] 1 ────── 0..* [doctor_shifts]
                           │                      │
                           │ 1                    │ 1
                           │                      ▼
                           │ 0..*              [appointments] 0..* ────── 1 [clinics] 0..* ────── 1 [specialties]
                           ▼                      ▲
                        [audit_logs]              │ 0..*
                                                  │
                                               [patients] 1 ────── 0..* [appointments]
                                                  │
                                                  ├────────────────────────┐
                                                  ▼ 0..*                   ▼ 0..*
                                           [medical_records] 1 ────── 0..1 [invoices] 1 ────── 0..* [invoice_items]
                                                  │
                                                  ▼ 1
                                           [prescriptions] 1 ────── 0..* [prescription_items] 0..* ────── 1 [medicines]

  [knowledge_base] (Độc lập, lưu trữ dữ liệu quy trình phục vụ Trợ lý AI FAQ Chatbot RAG)
  [ai_invocation_logs] (Lưu trữ nhật ký prompt đã khử PII, thời gian phản hồi latency và mô hình phục vụ)
+----------------------------------------------------------------------------------------------------+"""
    add_code_block(doc, erd_ascii)

    add_h3(doc, "Bảng đặc tả cấu trúc chi tiết 14 bảng cơ sở dữ liệu quan hệ:")

    tables_schema = [
        ("1. users", "Lưu trữ tài khoản nhân sự phòng khám (id, role_id, username, hashed_password, full_name, email, is_active, created_at). PK: id, FK: role_id -> roles.id."),
        ("2. roles", "Danh mục 4 vai trò hệ thống gồm admin, receptionist, doctor, accountant (id, name, description). PK: id."),
        ("3. patients", "Hồ sơ thông tin người bệnh (id, patient_code, full_name, dob, gender, national_id, phone, address, insurance_code, allergy_history, created_at). PK: id, Unique: patient_code, national_id."),
        ("4. doctors", "Thông tin chuyên môn bác sĩ (id, user_id, specialty_id, room_id, license_number, qualification, is_active). PK: id, FK: user_id -> users.id, specialty_id -> specialties.id."),
        ("5. doctor_shifts", "Ca trực theo tuần của bác sĩ (id, doctor_id, room_id, shift_date, start_time, end_time, status). PK: id, FK: doctor_id -> doctors.id."),
        ("6. appointments", "Lịch hẹn khám bệnh (id, appointment_code, patient_id, doctor_id, room_id, appointment_date, start_time, end_time, status, notes). PK: id, FK: patient_id, doctor_id."),
        ("7. medical_records", "Hồ sơ bệnh án điện tử EMR (id, record_code, appointment_id, patient_id, doctor_id, symptoms, blood_pressure, pulse, temperature, spo2, height, weight, bmi, icd10_code, diagnosis, status, created_at). PK: id."),
        ("8. prescriptions", "Đơn thuốc điện tử (id, record_id, doctor_id, notes, created_at). PK: id, FK: record_id -> medical_records.id."),
        ("9. prescription_items", "Chi tiết từng loại thuốc trong đơn (id, prescription_id, medicine_id, quantity, dosage, instruction). PK: id, FK: prescription_id, medicine_id."),
        ("10. medicines", "Danh mục dược phẩm kho thuốc (id, medicine_code, medicine_name, active_ingredient, unit, unit_price, stock_quantity, is_active). PK: id, Unique: medicine_code."),
        ("11. invoices", "Hóa đơn viện phí (id, invoice_code, record_id, patient_id, total_amount, insurance_amount, patient_amount, payment_method, status, vietqr_url, paid_at). PK: id."),
        ("12. invoice_items", "Chi tiết các hạng mục thu phí (id, invoice_id, item_name, item_type, quantity, unit_price, amount). PK: id, FK: invoice_id -> invoices.id."),
        ("13. audit_logs", "Nhật ký kiểm toán an ninh (id, user_id, action, resource, resource_id, ip_address, details, created_at). PK: id."),
        ("14. knowledge_base", "Cơ sở tri thức FAQ phòng khám (id, category, question, answer, keywords, is_active). PK: id.")
    ]

    for t_name, t_desc in tables_schema:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(f"• {t_name}: ")
        r1.font.bold = True
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(10.5)
        r2 = p.add_run(t_desc)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(10.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_h2(doc, "2.2. Các ràng buộc toàn vẹn trong CSDL (Database Integrity Constraints)")

    integrity_rules = [
        ("1. Ràng buộc thực thể (Entity Integrity): ", "Mỗi bảng đều có một khóa chính (PK) duy nhất kiểu số nguyên tự tăng hoặc UUID không mang giá trị NULL, bảo đảm tính định danh xác thực."),
        ("2. Ràng buộc tham chiếu (Referential Integrity): ", "Các khóa ngoại (FK) liên kết chính xác giữa các bảng. Áp dụng quy tắc ON DELETE RESTRICT cho bảng bệnh nhân và bác sĩ (không cho phép xóa người bệnh khi đã có lịch sử khám bệnh). Áp dụng ON DELETE CASCADE cho chi tiết đơn thuốc và chi tiết hóa đơn."),
        ("3. Ràng buộc duy nhất (Unique Constraints): ", "Số CCCD (national_id) gồm 12 số là duy nhất trong toàn hệ thống. Mã thẻ BHYT (insurance_code) 15 ký tự là duy nhất. Tên đăng nhập (username) và mã thuốc (medicine_code) không được trùng lặp."),
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
