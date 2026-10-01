# PROMPT GIAO VIỆC: KIỂM TOÁN MÃ NGUỒN ĐA CHIỀU (CODE REVIEW)
## Giai đoạn SDLC: Giai đoạn 2 & 4 – Code Review & Quality Audit (KT2 & KT4)
### Kỹ năng áp dụng: `.agents/skills/code-review/SKILL.md`

---

## 1. THÔNG TIN NGỮ CẢNH & MỤC TIÊU
* **Dự án:** Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp Trợ lý AI Hành chính (CMS-AI).
* **Đơn vị thực hiện:** Nhóm 07 (Đinh Gia Bảo - Trưởng nhóm, Trần Đặng Công Tâm).
* **Mục tiêu:** Thực hiện quy trình đánh giá và kiểm toán mã nguồn đa chiều (Multi-Dimensional Code Review), rà soát toàn diện codebase Backend và Frontend trên 5 khía cạnh cốt lõi: Tính đúng đắn nghiệp vụ (Correctness), Tuân thủ phân quyền RBAC, Chuẩn mực lập trình (Clean Code & PEP 8), Hiệu năng truy vấn CSDL (N+1 query detection), Xử lý lỗi RFC 7807; phân loại mức độ rủi ro (CRITICAL, HIGH, MEDIUM, LOW) và kích hoạt cổng Human Gate 2.

---

## 2. VAI TRÒ CỦA AI AGENT (PERSONA)
Bạn là **Principal Code Reviewer & Software Quality Auditor Agent (Chuyên gia Kiểm toán Mã nguồn Cấp cao)**, có tiêu chuẩn kỹ thuật cực kỳ khắt khe, am hiểu các lỗ hổng lập trình tinh vi, có khả năng phát hiện lỗi rò rỉ kết nối CSDL, race condition trong đặt lịch hẹn và dead code tồn dư.

---

## 3. RÀNG BUỘC KỸ THUẬT & QUY TẮC CỐT LÕI (GUARDRAILS)
1. **Phân loại Rủi ro Chuẩn mực:**
   - **CRITICAL:** Lỗ hổng bảo mật rò rỉ dữ liệu y tế, bypass phân quyền RBAC, sai lệch số tiền viện phí hoặc âm kho thuốc.
   - **HIGH:** Thiếu transaction CSDL, nguy cơ Race Condition khi 2 người cùng đặt một khung giờ, N+1 queries làm sập API.
   - **MEDIUM:** Thiếu validation kiểu dữ liệu Pydantic, lỗi xử lý exception không đúng chuẩn RFC 7807.
   - **LOW:** Đặt tên biến chưa chuẩn PEP 8, comment thừa hoặc code trùng lặp.
2. **Kích hoạt Human Gate 2:** Nếu phát hiện bất kỳ lỗi CRITICAL hoặc HIGH nào, lập tức chặn quy trình xuất xưởng và yêu cầu Kỹ sư Con người duyệt phương án sửa đổi.
3. **Kiểm tra Dead Code:** Rà soát và loại bỏ các file không còn được sử dụng trong dự án.

---

## 4. NỘI DUNG MASTER PROMPT ĐÃ GIAO CHO AI AGENT

```markdown
Bạn hãy đóng vai trò là Principal Code Reviewer. Hãy thực hiện toàn diện quy trình Kiểm toán Mã nguồn cho dự án CMS-AI của Nhóm 07:

BƯỚC 1: XÂY DỰNG SKILL ĐÁNH GIÁ MÃ NGUỒN (.agents/skills/code-review/SKILL.md)
Tạo file SKILL.md định nghĩa quy chuẩn Code Review: Quy trình kiểm toán 5 bước, bảng phân loại mức độ rủi ro, tiêu chí nghiệm thu chất lượng code và quy trình kích hoạt Human Gate 2.

BƯỚC 2: RÀ SOÁT TOÀN DIỆN MÃ NGUỒN BACKEND VÀ FRONTEND
Kiểm tra chi tiết từng file mã nguồn:
1. `backend/app/core/rbac.py` & `security.py`: Đảm bảo không có backdoor, thuật toán băm bcrypt an toàn, JWT token có thời gian hết hạn rõ ràng.
2. `backend/app/api/v1/appointments.py` & `conflict_checker.py`: Kiểm tra logic chống race condition, kiểm tra giao thoa thời gian đầy đủ.
3. `backend/app/api/v1/invoices.py` & `medical_records.py`: Đảm bảo quy trình lập hóa đơn và trừ kho thuốc nằm trong khối `with db.begin():` nguyên tử.
4. `backend/app/ai/`: Đảm bảo không có hardcoded API keys, bắt buộc gọi qua `PIIAnonymizer` trước khi chuyển tiếp ra ngoài.
5. `frontend/src/services/`: Phát hiện các file dead code không được import trong toàn bộ ứng dụng (phát hiện `authService.js` cũ).

BƯỚC 3: LẬP BÁO CÁO KIỂM TOÁN MÃ NGUỒN CHI TIẾT (docs/code-review.md)
Soạn thảo tài liệu báo cáo gồm:
- Tóm tắt tổng thể chất lượng mã nguồn (Executive Summary).
- Bảng danh mục các vấn đề phát hiện được phân cấp theo CRITICAL, HIGH, MEDIUM, LOW.
- Khuyến nghị chỉnh sửa cụ thể kèm diff mã nguồn minh họa.
- Biên bản nghiệm thu Human Gate 2 có xác nhận của Kỹ sư Trưởng Đinh Gia Bảo.
```

---

## 5. SẢN PHẨM ARTIFACTS KẾT XUẤT
1. [`.agents/skills/code-review/SKILL.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/.agents/skills/code-review/SKILL.md)
2. [`docs/code-review.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/docs/code-review.md)
3. Các chỉnh sửa dọn dẹp dead code (xóa `frontend/src/services/authService.js`, chuyển script sinh tài liệu vào `scripts/`).

---

## 6. KIỂM CHỨNG & HIỆU CHỈNH CỦA CON NGƯỜI (HUMAN GATE 2)
* **Lỗi do AI đề xuất:** Trong file xử lý hóa đơn, AI ban đầu viết logic: cho phép thanh toán hóa đơn ở trạng thái `PAID` thêm một lần nữa mà không kiểm tra trạng thái trước đó, dẫn đến nguy cơ gian lận thu tiền trùng lặp cho một ca khám.
* **Hành động hiệu chỉnh của Kỹ sư Con người:** Kỹ sư Trưởng đã can thiệp, bổ sung điều kiện chặn nghiêm ngặt: `if invoice.payment_status == PaymentStatus.PAID: raise HTTPException(status_code=400, detail="Hóa đơn này đã được thanh toán thành công trước đó")`.
