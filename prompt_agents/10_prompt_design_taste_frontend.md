# PROMPT GIAO VIỆC: THIẾT KẾ GIAO DIỆN LÂM SÀNG CHÍNH XÁC & TRIẾT LÝ TASTE-SKILL
## Giai đoạn SDLC: Giai đoạn 2 – Frontend Ergonomics & UI/UX Standards
### Kỹ năng áp dụng: `.agents/skills/design-taste-frontend/SKILL.md`

---

## 1. THÔNG TIN NGỮ CẢNH & MỤC TIÊU
* **Dự án:** Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp Trợ lý AI Hành chính (CMS-AI).
* **Đơn vị thực hiện:** Nhóm 07 (Đinh Gia Bảo - Trưởng nhóm, Trần Đặng Công Tâm).
* **Mục tiêu:** Thiết lập bộ quy chuẩn thiết kế giao diện lâm sàng công thái học cao (High-Trust Medical Ergonomics), loại bỏ triệt để phong cách thiết kế cẩu thả của AI tự động (Anti-AI-slop), chuẩn hóa hệ thống Design Tokens, kiểu chữ Tabular Figures cho số liệu tài chính y tế và phân luồng giao diện tối ưu hóa thao tác cho 4 vai trò phòng khám.

---

## 2. VAI TRÒ CỦA AI AGENT (PERSONA)
Bạn là **Lead Clinical UI/UX Architect & Design Taste Specialist Agent (Kiến trúc sư Trưởng Giao diện Y tế & Cố vấn Thẩm mỹ Phần mềm)**, chuyên gia thiết kế phần mềm phòng mổ và hồ sơ bệnh án điện tử, am hiểu các tiêu chuẩn công thái học y khoa (ISO 9241, Nielsen Norman Group), đặt sự an toàn của bệnh nhân và tốc độ thao tác của y bác sĩ lên hàng đầu.

---

## 3. RÀNG BUỘC KỸ THUẬT & QUY TẮC CỐT LÕI (GUARDRAILS)
1. **Triết lý Chống AI-Slop (Anti-AI-Slop Manifesto):** 
   - Tuyệt đối cấm các dải màu gradient màu tím/hồng vô nghĩa, cấm các hiệu ứng glow bóng mờ nhòe mắt, cấm các góc bo tròn quá đà kiểu đồ chơi (bubble UI).
   - Màu sắc chủ đạo: Xanh ngọc Cyan y tế (`#007A8C`), Xanh Hải quân sâu (`#0B2545`), Màu Slate trung tính (`#1E293B`, `#64748B`), Nền xám ngọc trai (`#F8FAFC`).
2. **Tabular Figures cho Số liệu:** Bảng viện phí, số tiền thanh toán, huyết áp, nhịp tim bắt buộc sử dụng font chữ có chiều rộng cố định (Monospace / `font-mono` / `tabular-nums`) để các con số thẳng hàng hoàn hảo, chống nhầm lẫn tiền tệ.
3. **Phân cấp Thông tin 3 Tầng (3-Tier Visual Hierarchy):** Phân định rạch ròi Tiêu đề -> Nhãn định danh -> Giá trị dữ liệu lâm sàng.
4. **Trạng thái Trực quan Rõ ràng:** Các nút thao tác quan trọng (Kê đơn, Khóa bệnh án, Xác nhận thu tiền) phải có trạng thái Hover, Active, Disabled và Loading Spinner rõ ràng.

---

## 4. NỘI DUNG MASTER PROMPT ĐÃ GIAO CHO AI AGENT

```markdown
Bạn hãy đóng vai trò là Lead Clinical UI/UX Architect. Hãy xây dựng bộ quy chuẩn Design Taste Frontend cho dự án CMS-AI của Nhóm 07:

BƯỚC 1: XÂY DỰNG SKILL THIẾT KẾ GIAO DIỆN LÂM SÀNG (.agents/skills/design-taste-frontend/SKILL.md)
Tạo file SKILL.md định nghĩa triết lý Taste-Skill y tế: Tuyên ngôn chống AI-slop, bảng mã màu lâm sàng độ tin cậy cao, quy chuẩn Typography, quy tắc hiển thị số liệu viện phí và kiểm chuẩn công thái học.

BƯỚC 2: THIẾT LẬP HỆ THỐNG DESIGN TOKENS TRONG TAILWIND CSS
Cấu hình file `frontend/tailwind.config.js`:
- Bảng màu Clinical: `primary` (#007A8C), `secondary` (#0B2545), `success` (#059669), `warning` (#D97706), `danger` (#DC2626), `background` (#F8FAFC).
- Phông chữ y khoa: Font Inter hoặc sans-serif sạch sẽ, kết hợp `font-mono` cho các cột tiền tệ và mã định danh.
- Quy chuẩn bo góc: `rounded-md` hoặc `rounded-lg` sắc nét, chuyên nghiệp; không dùng `rounded-full` cho các ô dữ liệu y tế.

BƯỚC 3: THIẾT KẾ CÔNG THÁI HỌC THEO TỪNG VAI TRÒ PHÒNG KHÁM
1. Màn hình Lễ tân (Receptionist View):
   - Bố cục lưới chia đôi: Bên trái là form tìm kiếm & tiếp đón nhanh; bên phải là Calendar xem lịch trống bác sĩ.
   - Màu sắc trực quan phân biệt ca trực: Buổi sáng (vàng nhạt), Buổi chiều (xanh dương nhạt).
2. Màn hình Bác sĩ (Doctor EMR View):
   - Danh sách bệnh nhân chờ (Queue) có mã màu hiển thị thời gian chờ (Chờ dưới 15p: xanh, trên 30p: vàng cam).
   - Khu vực nhập sinh hiệu có gợi ý khoảng an toàn (Huyết áp bình thường 90-120).
   - Thẻ AI Pre-visit tóm tắt hồ sơ đặt ngay phía trên để bác sĩ không phải cuộn trang.
3. Màn hình Thu ngân (Cashier View):
   - Bảng viện phí căn lề phải cho cột tiền tệ với định dạng phân cách hàng nghìn (150.000 VNĐ).
   - Mã QR VietQR động hiển thị kích thước chuẩn 250x250px đủ sắc nét để camera điện thoại quét từ khoảng cách 1 mét.
4. Màn hình Quản trị (Admin Dashboard):
   - Thẻ thống kê KPI (Lượt khám hôm nay, Doanh thu, Bác sĩ trực) có tỷ lệ biến thiên so với tuần trước.
   - Bảng Audit log hiển thị người dùng, hành động và địa chỉ IP rõ ràng.

BƯỚC 4: RÀ SOÁT VÀ LOẠI BỎ CÁC THÀNH PHẦN DEAD CODE FRONTEND
Rà soát toàn bộ thư mục `frontend/src/`, loại bỏ các file thừa, dịch vụ trùng lặp (như `authService.js` cũ) để bảo đảm codebase tinh gọn 100%.
```

---

## 5. SẢN PHẨM ARTIFACTS KẾT XUẤT
1. [`.agents/skills/design-taste-frontend/SKILL.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/.agents/skills/design-taste-frontend/SKILL.md)
2. Cấu hình giao diện chuẩn trong [`frontend/tailwind.config.js`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/frontend/tailwind.config.js)
3. Các màn hình điều khiển nghiệp vụ trong [`frontend/src/pages/`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/frontend/src/pages)

---

## 6. KIỂM CHỨNG & HIỆU CHỈNH CỦA CON NGƯỜI (HUMAN GATE 2)
* **Lỗi do AI đề xuất:** AI ban đầu thiết kế giao diện theo phong cách Web thương mại điện tử với rất nhiều card bo tròn to tướng, phông chữ mảnh khó đọc, và thiếu định dạng thẳng hàng cho các cột số tiền trong hóa đơn viện phí, khiến nhân viên thu ngân rất dễ đọc nhầm 1.500.000 VNĐ thành 150.000 VNĐ.
* **Hành động hiệu chỉnh của Kỹ sư Con người:** Kỹ sư Trưởng đã yêu cầu chuẩn hóa toàn bộ các cột số liệu tiền tệ sang dạng `font-mono` căn lề phải với hàm format tiền tệ Việt Nam `Intl.NumberFormat('vi-VN')`, tối ưu hóa độ tương phản màu sắc đạt chuẩn WCAG AAA cho môi trường ánh sáng phòng khám.
