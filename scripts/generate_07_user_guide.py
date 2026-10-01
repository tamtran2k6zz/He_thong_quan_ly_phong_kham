# -*- coding: utf-8 -*-
"""
Script sinh file 07_GenAI_SoftwareDevelopment_user-guide.docx
Sổ tay Hướng dẫn sử dụng hệ thống CMS-AI cho 4 vai trò (Nhóm 07).
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

def build_user_guide():
    doc = create_base_document()

    add_header_block(
        doc,
        "HƯỚNG DẪN SỬ DỤNG HỆ THỐNG (USER GUIDE)",
        "HỆ THỐNG QUẢN LÝ PHÒNG KHÁM CÓ TÍCH HỢP AI (CMS-AI)"
    )

    add_team_meta(doc)

    # 1. GIỚI THIỆU ỨNG DỤNG
    add_h1(doc, "1. GIỚI THIỆU ỨNG DỤNG")
    add_p(
        doc,
        "Hệ thống quản lý phòng khám đa khoa thông minh CMS-AI là giải pháp phần mềm chuyên biệt phục vụ các cơ sở y tế tư nhân. "
        "Ứng dụng số hóa toàn diện quy trình tiếp đón người bệnh, điều phối lịch hẹn, quản lý hồ sơ bệnh án điện tử EMR, "
        "kê đơn thuốc và thanh toán viện phí không dùng tiền mặt qua mã VietQR chuẩn quốc gia. "
        "Điểm khác biệt của hệ thống nằm ở động cơ Trợ lý AI Hành chính 3 lớp, giúp bác sĩ tóm tắt hồ sơ cũ trong 15 giây, "
        "hỗ trợ người bệnh hỏi đáp quy trình khám tự động và tự động sinh bản dặn dò sau khám theo mẫu y tế chuẩn mực."
    )

    # 2. CẤU HÌNH PHẦN CỨNG - PHẦN MỀM
    add_h1(doc, "2. CẤU HÌNH PHẦN CỨNG - PHẦN MỀM")

    add_h2(doc, "2.1. Cấu hình phần cứng")
    add_p(
        doc,
        "Máy chủ (Server): Bộ vi xử lý Intel Core i5/i7 thế hệ 11 trở lên hoặc AMD Ryzen 5/7; Bộ nhớ RAM tối thiểu 8 GB (khuyến nghị 16 GB); "
        "Ổ cứng thể rắn SSD dung lượng trống tối thiểu 20 GB; Kết nối mạng LAN hoặc Internet tốc độ cao.\n"
        "Máy trạm nhân viên (Client): Máy tính để bàn, máy tính xách tay hoặc máy tính bảng kết nối cùng mạng nội bộ; "
        "Màn hình độ phân giải tối thiểu 1366x768 pixels."
    )

    add_h2(doc, "2.2. Cấu hình phần mềm")
    add_p(
        doc,
        "Phía máy chủ: Hệ điều hành Windows 10/11 Pro hoặc Ubuntu Linux 22.04 LTS; "
        "Nền tảng ảo hóa Docker Desktop 4.x và Docker Compose; Trình quản lý gói Python 3.11 trở lên.\n"
        "Phía máy trạm: Trình duyệt web hiện đại phiên bản mới nhất như Google Chrome, Microsoft Edge hoặc Mozilla Firefox."
    )

    add_h2(doc, "2.3. Hướng dẫn khởi động nhanh hệ thống")
    add_p(
        doc,
        "Người quản trị có thể khởi động toàn bộ hệ thống bằng một trong hai phương thức tiện lợi sau:"
    )

    startup_guide_ascii = """+----------------------------------------------------------------------------------------------------+
|                                 HƯỚNG DẪN KHỞI CHẠY HỆ THỐNG PHÒNG KHÁM                            |
+----------------------------------------------------------------------------------------------------+
  Cách 1: Khởi chạy 1-Click trên Windows (Khuyến nghị cho phòng khám)
  - Bước 1: Mở thư mục chứa mã nguồn dự án.
  - Bước 2: Nhấp đúp chuột vào tệp tin 'run_app.bat' hoặc 'start_demo.bat'.
  - Bước 3: Hệ thống tự động kích hoạt CSDL MySQL, Backend FastAPI và Frontend React.
  - Bước 4: Trình duyệt web tự động mở địa chỉ giao diện: http://localhost:5173

  Cách 2: Khởi chạy qua Docker Compose (Môi trường máy chủ chuyên nghiệp)
  - Lệnh khởi động: docker-compose up -d --build
  - Địa chỉ Frontend: http://localhost:3000 (hoặc http://localhost:5173)
  - Địa chỉ Backend Swagger API: http://localhost:8000/docs
  - Địa chỉ Quản trị CSDL pgAdmin / phpMyAdmin: http://localhost:8080
+----------------------------------------------------------------------------------------------------+"""
    add_code_block(doc, startup_guide_ascii)

    add_h2(doc, "2.4. Danh mục tài khoản thử nghiệm theo vai trò")
    tbl_acc = doc.add_table(rows=5, cols=4)
    tbl_acc.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_acc.autofit = False
    col_w_acc = [Inches(1.8), Inches(1.5), Inches(1.4), Inches(1.8)]
    for row in tbl_acc.rows:
        for idx, w in enumerate(col_w_acc):
            row.cells[idx].width = w

    headers_acc = ["Vai trò người dùng", "Tên đăng nhập", "Mật khẩu mặc định", "Phạm vi quyền hạn"]
    for i, h in enumerate(headers_acc):
        tbl_acc.cell(0, i).text = h
    format_row(tbl_acc.rows[0], HEX_HEADER_BG, RGBColor(255, 255, 255), bold=True, is_header=True)

    acc_data = [
        ("Quản trị viên (Admin)", "admin", "Admin@123", "Toàn quyền quản trị hệ thống, ca trực, kho dược"),
        ("Lễ tân (Receptionist)", "receptionist", "Recep@123", "Tiếp đón người bệnh, đặt lịch hẹn, điều phối hàng đợi"),
        ("Bác sĩ (Doctor)", "doctor", "Doctor@123", "Bàn khám EMR, xem tóm tắt AI, chẩn đoán ICD-10, kê đơn"),
        ("Kế toán (Accountant)", "accountant", "Acc@123", "Quản lý hóa đơn viện phí, BHYT, thanh toán VietQR")
    ]
    for r_idx, (a_role, a_user, a_pass, a_perm) in enumerate(acc_data):
        row = tbl_acc.rows[r_idx + 1]
        row.cells[0].text = a_role
        row.cells[1].text = a_user
        row.cells[2].text = a_pass
        row.cells[3].text = a_perm
        bg = HEX_ROW_ALT if (r_idx % 2 == 1) else "FFFFFF"
        format_row(row, bg, RGBColor(15, 23, 42), bold=False, is_header=False)
    set_table_borders(tbl_acc)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 3. CÁC CHỨC NĂNG CHÍNH THEO 4 VAI TRÒ
    add_h1(doc, "3. CÁC CHỨC NĂNG CHÍNH")
    add_p(doc, "Các chức năng chính được phân chia theo 4 nhóm tác nhân (Actors) đã xác định trong tài liệu SRS:")

    add_h2(doc, "3.1. Chức năng của Lễ tân (Receptionist)")
    rec_steps = [
        ("Bước 1: Đăng nhập hệ thống: ", "Truy cập màn hình đăng nhập, nhập tài khoản 'receptionist' và mật khẩu. Giao diện chuyển hướng vào Receptionist Dashboard."),
        ("Bước 2: Tiếp đón và Tìm kiếm bệnh nhân: ", "Nhập số CCCD hoặc SĐT của người bệnh vào ô tìm kiếm nhanh. Nếu người bệnh đã có hồ sơ, thông tin hiển thị ngay lập tức. Nếu là bệnh nhân mới, nhấn nút 'Đăng ký bệnh nhân', điền đầy đủ họ tên, ngày sinh, địa chỉ, mã thẻ BHYT và ghi nhận tiền sử dị ứng thuốc nếu có."),
        ("Bước 3: Đặt lịch khám bệnh: ", "Vào mục 'Lịch hẹn' -> Nhấn 'Tạo lịch hẹn mới'. Chọn người bệnh, chọn bác sĩ chuyên khoa và chọn khung giờ khám. Hệ thống tự động kiểm tra ca trực và báo động đỏ nếu bác sĩ hoặc phòng khám đã có lịch hẹn trùng giờ. Nếu hợp lệ, nhấn 'Lưu lịch hẹn'."),
        ("Bước 4: Quản lý hàng đợi phòng khám: ", "Khi người bệnh có mặt tại phòng khám, lễ tân chuyển trạng thái từ 'Đã hẹn' sang 'Đang chờ khám', hệ thống tự động xếp số thứ tự vào hàng đợi của bác sĩ tương ứng.")
    ]
    for title, desc in rec_steps:
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

    add_h2(doc, "3.2. Chức năng của Bác sĩ (Doctor)")
    doc_steps = [
        ("Bước 1: Tiếp nhận ca khám từ hàng đợi: ", "Bác sĩ đăng nhập tài khoản 'doctor', xem danh sách người bệnh đang chờ khám tại phòng của mình. Nhấn nút 'Tiến hành khám' trên hàng đợi."),
        ("Bước 2: Xem tóm tắt bệnh án từ Trợ lý AI (Pre-visit Briefing): ", "Nhấn nút 'Xem tóm tắt AI' trên giao diện EMR. Trợ lý AI tự động trích xuất các lần khám cũ, hiển thị thẻ tóm tắt súc tích về diễn tiến bệnh, thuốc đã dùng và dị ứng thuốc trong thời gian dưới 15 giây."),
        ("Bước 3: Ghi nhận sinh hiệu lâm sàng: ", "Đo và nhập huyết áp, mạch, nhiệt độ, SpO2, chiều cao, cân nặng. Hệ thống tự động tính chỉ số khối cơ thể (BMI) và hiển thị phân loại thể trạng."),
        ("Bước 4: Chẩn đoán bệnh theo mã ICD-10: ", "Gõ tên bệnh lý hoặc triệu chứng vào ô chẩn đoán (VD: Viêm phế quản), hệ thống gợi ý danh sách mã ICD-10 chuẩn quốc tế để bác sĩ lựa chọn."),
        ("Bước 5: Kê đơn thuốc điện tử và Cảnh báo dị ứng: ", "Tìm và thêm thuốc từ kho dược phòng khám, nhập số lượng và liều dùng. Nếu bác sĩ vô tình kê loại thuốc có hoạt chất trùng tiền sử dị ứng của người bệnh, hệ thống lập tức hiển thị cảnh báo đỏ nguy hiểm để ngăn chặn sai sót."),
        ("Bước 6: Sinh hướng dẫn sau khám và Hoàn tất ca khám: ", "Nhấn nút 'Tạo dặn dò AI', hệ thống sinh lịch uống thuốc chi tiết theo buổi (sáng, trưa, tối) và lời khuyên ăn uống. Bác sĩ kiểm tra, chỉnh sửa nếu cần và bấm 'Hoàn thành ca khám'. Hồ sơ tự động chuyển sang phân hệ kế toán.")
    ]
    for title, desc in doc_steps:
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

    add_h2(doc, "3.3. Chức năng của Kế toán (Accountant)")
    acc_steps = [
        ("Bước 1: Tiếp nhận hồ sơ chờ thanh toán: ", "Kế toán đăng nhập tài khoản 'accountant', mở danh sách hồ sơ khám đã hoàn thành cần thu tiền."),
        ("Bước 2: Kiểm tra bảng kê chi phí và BHYT: ", "Mở chi tiết phiếu khám. Hệ thống tự động tổng hợp tiền công khám và tiền thuốc trong đơn. Dựa trên mã thẻ BHYT, hệ thống tự động khấu trừ 80% hoặc 100% chi phí được bảo hiểm chi trả, hiển thị rõ ràng số tiền người bệnh phải nộp."),
        ("Bước 3: Thu tiền và Thanh toán VietQR: ", "Nếu người bệnh thanh toán chuyển khoản, kế toán bấm 'Tạo mã VietQR'. Màn hình hiển thị mã QR động chuẩn NAPAS chứa chính xác số tiền cần thu. Người bệnh dùng ứng dụng ngân hàng quét mã."),
        ("Bước 4: Xác nhận thanh toán và In biên lai: ", "Sau khi tiền vào tài khoản phòng khám, kế toán nhấn 'Xác nhận thanh toán', hóa đơn chuyển trạng thái 'Đã thanh toán'. Nhấn 'In hóa đơn' để in biên lai viện phí bàn giao cho người bệnh.")
    ]
    for title, desc in acc_steps:
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

    add_h2(doc, "3.4. Chức năng của Quản trị viên (Admin)")
    adm_steps = [
        ("Quản lý tài khoản và phân quyền: ", "Tạo tài khoản nhân sự mới, gán đúng vai trò theo ma trận RBAC, đặt lại mật khẩu và khóa tài khoản khi có biến động nhân sự."),
        ("Phân ca làm việc bác sĩ: ", "Xếp lịch trực cho từng bác sĩ theo các ca sáng, chiều, tối trong tuần và phân bổ phòng khám chuyên khoa tương ứng."),
        ("Quản lý danh mục kho dược: ", "Nhập kho thuốc mới, điều chỉnh đơn giá niêm yết, theo dõi số lượng tồn kho và thiết lập hạn mức cảnh báo sắp hết thuốc."),
        ("Báo cáo thống kê quản trị: ", "Theo dõi biểu đồ doanh thu theo ngày/tháng, số lượt người bệnh đến khám, tỷ lệ chi trả BHYT và năng suất làm việc của đội ngũ bác sĩ."),
        ("Giám sát nhật ký an ninh (Audit Logs): ", "Tra cứu lịch sử truy cập hồ sơ bệnh án nhạy cảm và nhật ký gọi API trợ lý AI để bảo đảm an toàn dữ liệu theo Nghị định 13/2023/NĐ-CP.")
    ]
    for title, desc in adm_steps:
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

    # 4. KỊCH BẢN DEMO 8 BƯỚC ĐÁNH GIÁ ĐỒ ÁN
    add_h1(doc, "4. KỊCH BẢN DEMO 8 BƯỚC ĐÁNH GIÁ ĐỒ ÁN (THỜI LƯỢNG 10 - 15 PHÚT)")
    add_p(
        doc,
        "Kịch bản trình diễn luồng nghiệp vụ khép kín từ tiếp đón đến báo cáo doanh thu phục vụ Hội đồng đánh giá chấm điểm:"
    )

    demo_steps = [
        ("Bước 1 (1 phút): Khởi chạy và Giới thiệu tổng quan", "Khởi động ứng dụng từ script 'run_app.bat'. Giới thiệu kiến trúc phân tầng FastAPI + React Vite và 4 phân hệ tương ứng 4 vai trò."),
        ("Bước 2 (2 phút): Phân hệ Lễ tân - Đăng ký bệnh nhân", "Đăng nhập tài khoản 'receptionist'. Tiếp đón người bệnh Trần Văn Bình (CCCD: 001099012345). Ghi nhận tiền sử dị ứng thuốc Penicillin."),
        ("Bước 3 (2 phút): Trình diễn thuật toán chống trùng lịch", "Đặt lịch khám vào lúc 08:30 cho Bác sĩ Lê Văn Cường. Thử đặt thêm một lịch hẹn khác cùng thời điểm 08:30 để chứng minh hệ thống phát hiện xung đột và từ chối lưu lịch."),
        ("Bước 4 (3 phút): Phân hệ Bác sĩ - Bàn khám EMR và Thẻ AI Pre-visit", "Đăng nhập tài khoản 'doctor'. Mở hồ sơ bệnh nhân từ hàng đợi. Bấm nút 'Xem tóm tắt AI' để hiển thị bản tóm tắt hồ sơ cũ không để lộ PII kèm cảnh báo y tế."),
        ("Bước 5 (2 phút): Nhập sinh hiệu và Cảnh báo dị ứng thuốc", "Nhập dấu hiệu sinh tồn (HA: 130/85, Mạch: 80, SpO2: 98%), hệ thống tự tính BMI. Nhập chẩn đoán ICD-10 'J02.9'. Thử kê thuốc Amoxicillin, hệ thống hiển thị cảnh báo đỏ dị ứng Penicillin. Đổi sang thuốc an toàn."),
        ("Bước 6 (1 phút): AI Dặn dò xuất viện", "Nhấn nút 'Tạo dặn dò sau khám', AI tự động tạo lịch uống thuốc và chế độ ăn uống. Bác sĩ hoàn thành ca khám."),
        ("Bước 7 (2 phút): Phân hệ Kế toán - Viện phí và Thanh toán VietQR", "Đăng nhập tài khoản 'accountant'. Mở hóa đơn, kiểm tra mức khấu trừ BHYT 80%. Bấm hiển thị mã thanh toán VietQR động NAPAS. Xác nhận thanh toán và in biên lai thu tiền."),
        ("Bước 8 (2 phút): Phân hệ Admin - Thống kê và Nhật ký Audit Logs", "Đăng nhập tài khoản 'admin'. Xem biểu đồ doanh thu cập nhật tức thời. Mở trang Audit Logs minh chứng toàn bộ thao tác vừa thực hiện đã được ghi vết an toàn.")
    ]

    for title, desc in demo_steps:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(f"• {title}: ")
        r1.font.bold = True
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(10.5)
        r2 = p.add_run(desc)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(10.5)

    save_document(doc, "07_GenAI_SoftwareDevelopment_user-guide.docx")

if __name__ == "__main__":
    build_user_guide()
