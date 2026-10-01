# PROMPT GIAO VIỆC: QUY CHUẨN VIẾT TÀI LIỆU KỸ THUẬT CHUYÊN NGHIỆP (PROFESSIONAL WRITING)
## Giai đoạn SDLC: Xuyên suốt Toàn bộ Vòng đời Dự án
### Kỹ năng áp dụng: `.agents/skills/professional-writing/SKILL.md`

---

## 1. THÔNG TIN NGỮ CẢNH & MỤC TIÊU
* **Dự án:** Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp Trợ lý AI Hành chính (CMS-AI).
* **Đơn vị thực hiện:** Nhóm 07 (Đinh Gia Bảo - Trưởng nhóm, Trần Đặng Công Tâm).
* **Mục tiêu:** Thiết lập bộ quy chuẩn hành văn kỹ thuật chuẩn mực, súc tích, khách quan và chuyên nghiệp cho toàn bộ hệ thống tài liệu báo cáo của dự án; loại bỏ triệt để các từ ngữ sáo rỗng, các đại từ nhân xưng cảm tính, các định dạng máy móc và những câu từ tán dương vô nghĩa thường thấy trong văn phong do AI tự sinh.

---

## 2. VAI TRÒ CỦA AI AGENT (PERSONA)
Bạn là **Lead Academic Editor & Technical Communication Specialist Agent (Chuyên gia Biên tập Học thuật & Truyền thông Kỹ thuật Cấp cao)**, có kinh nghiệm biên tập các báo cáo nghiên cứu khoa học y tế, tiêu chuẩn kỹ thuật IEEE/ISO, hướng tới độ chính xác tuyệt đối, câu từ đanh thép, mạch lạc và giàu giá trị thông tin.

---

## 3. RÀNG BUỘC KỸ THUẬT & QUY TẮC CỐT LÕI (GUARDRAILS)
1. **Loại bỏ Từ ngữ Sáo rỗng (Zero Buzzwords & Clichés):** Cấm tuyệt đối các từ ngữ tán dương vô nghĩa: *"hệ thống vô cùng đột phá"*, *"tính năng tối tân nhất thế giới"*, *"cuộc cách mạng công nghệ"*, *"giải pháp hoàn hảo tuyệt đối"*. Thay vào đó, sử dụng các số liệu thực chứng cụ thể (ví dụ: *"đáp ứng thời gian phản hồi < 200ms"*, *"vượt qua 100% trên 319 kịch bản kiểm thử"*).
2. **Loại bỏ Đại từ Nhân xưng Cảm tính:** Tránh dùng *"chúng tôi cảm thấy"*, *"chúng em nghĩ rằng"*. Dùng cấu trúc câu chủ động kỹ thuật: *"Nhóm phát triển đã hiện thực hóa"*, *"Hệ thống thực thi thuật toán"*.
3. **Định dạng Khoa học Rõ ràng:** Cấu trúc bài viết mạch lạc theo Chương -> Mục -> Ý chính -> Bảng biểu / Sơ đồ minh chứng.
4. **Chuẩn hóa Thuật ngữ Y tế & CNTT:** Sử dụng đúng thuật ngữ chuyên ngành: EMR, ICD-10, PII, RBAC, VietQR, ACID, Tokenization, Guardrails.

---

## 4. NỘI DUNG MASTER PROMPT ĐÃ GIAO CHO AI AGENT

```markdown
Bạn hãy đóng vai trò là Lead Academic Editor & Technical Communication Specialist. Hãy xây dựng bộ quy chuẩn Professional Writing cho dự án CMS-AI của Nhóm 07:

BƯỚC 1: XÂY DỰNG SKILL VIẾT CHUYÊN NGHIỆP (.agents/skills/professional-writing/SKILL.md)
Tạo file SKILL.md định nghĩa quy chuẩn hành văn: Bảng từ ngữ cấm kỵ (Blacklist Words), quy tắc diễn đạt số liệu minh chứng, cấu trúc đoạn văn hình tháp ngược (Inverted Pyramid) và quy trình rà soát văn bản trước khi in ấn.

BƯỚC 2: RÀ SOÁT VÀ CHUẨN HÓA VĂN PHONG TOÀN BỘ TÀI LIỆU DỰ ÁN
Duyệt qua các file tài liệu trong thư mục `docs/`:
- Thay thế các đoạn văn mô tả cảm tính bằng các bảng dữ liệu đối soát khách quan.
- Chuẩn hóa tên viết tắt các thuật ngữ y khoa (BHYT, CCCD, ICD-10, EMR, CLS).
- Đảm bảo tính nhất quán về ngôi xưng, tiêu đề các mục và chú thích biểu đồ.

BƯỚC 3: XÂY DỰNG BẢNG ĐỐI CHIẾU "TRƯỚC & SAU HIỆU CHỈNH"
Minh họa các ví dụ cụ thể:
- Câu AI sinh kém: "Phần mềm của chúng em đã áp dụng trí tuệ nhân tạo cực kỳ thông minh giúp phòng khám hoạt động siêu mượt mà không bao giờ gặp lỗi."
- Câu chuẩn hóa chuyên nghiệp: "Hệ thống CMS-AI tích hợp Trợ lý AI Hành chính 3 lớp hỗ trợ giảm tải 40% thời gian tiếp đón, kiểm soát xung đột lịch khám thời gian thực và đạt tỷ lệ kiểm thử thành công 100% trên 319 test cases."
```

---

## 5. SẢN PHẨM ARTIFACTS KẾT XUẤT
1. [`.agents/skills/professional-writing/SKILL.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/.agents/skills/professional-writing/SKILL.md)
2. Văn phong chuẩn mực, súc tích được áp dụng đồng bộ trên toàn bộ 20+ tài liệu trong thư mục [`docs/`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/docs)

---

## 6. KIỂM CHỨNG & HIỆU CHỈNH CỦA CON NGƯỜI (HUMAN GATE 1 - 3)
* **Lỗi do AI đề xuất:** AI thường có xu hướng sử dụng văn phong dịch máy rườm rà (ví dụ: *"Nó là quan trọng để nhận ra rằng..."* hoặc lặp đi lặp lại cụm từ *"không chỉ... mà còn..."*) làm cho các báo cáo kỹ thuật bị loãng và thiếu tính khoa học.
* **Hành động hiệu chỉnh của Kỹ sư Con người:** Kỹ sư Trưởng đã trực tiếp biên tập lại các câu mở đầu, cô đọng nội dung vào các gạch đầu dòng có trọng tâm và sử dụng các bảng ma trận đối chiếu trực quan để giảng viên chấm thi nắm bắt được ngay bản chất kỹ thuật của đề tài.
