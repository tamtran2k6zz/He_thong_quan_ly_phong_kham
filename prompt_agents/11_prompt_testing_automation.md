# PROMPT GIAO VIỆC: CHIẾN LƯỢC KIỂM THỬ ĐA TẦNG & TỰ ĐỘNG HÓA TEST SUITE
## Giai đoạn SDLC: Giai đoạn 4 – Testing & Quality Assurance (KT4)
### Kỹ năng áp dụng: `.agents/skills/testing/SKILL.md`

---

## 1. THÔNG TIN NGỮ CẢNH & MỤC TIÊU
* **Dự án:** Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp Trợ lý AI Hành chính (CMS-AI).
* **Đơn vị thực hiện:** Nhóm 07 (Đinh Gia Bảo - Trưởng nhóm, Trần Đặng Công Tâm).
* **Mục tiêu:** Xây dựng Kế hoạch Kiểm thử Toàn diện (Test Plan), Báo cáo Kết quả Kiểm thử (Test Report) và bộ kiểm thử tự động đa tầng (Multi-tier Automated Test Suite) với hơn **319+ test cases Pytest** vượt qua 100%, bao gồm: Unit Test, Integration Test, RBAC Security Test, Xung đột lịch khám, Khử PII và Adversarial Prompt Injection Test.

---

## 2. VAI TRÒ CỦA AI AGENT (PERSONA)
Bạn là **Lead QA Automation Engineer & Security Test Specialist Agent (Kỹ sư Trưởng Kiểm thử Tự động & Bảo mật)**, chuyên gia viết kịch bản kiểm thử Pytest, TestClient FastAPI, giả lập dữ liệu y tế (Mocking/Fixtures) và kiểm thử các kịch bản biên phá hoại (Adversarial Security Testing).

---

## 3. RÀNG BUỘC KỸ THUẬT & QUY TẮC CỐT LÕI (GUARDRAILS)
1. **Tỷ lệ Đạt 100% (Zero Flaky Tests):** Toàn bộ test suite phải chạy độc lập, cô lập bằng SQLite in-memory hoặc test database, không phụ thuộc vào kết nối mạng bên ngoài, đảm bảo vượt qua 100% trên mọi môi trường CI/CD.
2. **Kiểm thử Phân quyền RBAC Chặt chẽ:** Mọi endpoint phải được kiểm tra quyền hạn của cả 4 vai trò (Admin, Receptionist, Doctor, Accountant), xác nhận trả về đúng mã lỗi `401 Unauthorized` hoặc `403 Forbidden` khi truy cập trái quyền.
3. **Kiểm thử Thuật toán Trùng lịch Khám:** Kiểm thử toàn bộ các trường hợp biên giao thoa thời gian (Trùng đầu ca, trùng cuối ca, bao trọn khung giờ, nằm lọt trong khung giờ, ngoài giờ làm việc).
4. **Kiểm thử Adversarial AI:** Kiểm tra khả năng chống chịu của Chatbot trước các câu prompt cố tình lừa đảo yêu cầu chẩn đoán hoặc kê đơn thuốc độc hại.

---

## 4. NỘI DUNG MASTER PROMPT ĐÃ GIAO CHO AI AGENT

```markdown
Bạn hãy đóng vai trò là Lead QA Automation Engineer. Hãy thực hiện toàn diện quy trình Kiểm thử Phần mềm Tự động cho dự án CMS-AI của Nhóm 07:

BƯỚC 1: XÂY DỰNG SKILL KIỂM THỬ PHẦN MỀM (.agents/skills/testing/SKILL.md)
Tạo file SKILL.md định nghĩa quy chuẩn kiểm thử đa tầng: Tháp kiểm thử y tế (Unit -> Integration -> Security -> Adversarial AI), cấu trúc thư mục `backend/tests/`, quy chuẩn đặt tên test fixture và tiêu chuẩn nghiệm thu trước khi xuất xưởng.

BƯỚC 2: BIÊN SOẠN KẾ HOẠCH KIỂM THỬ TEST PLAN (docs/test-plan.md)
Xác định:
- Phạm vi kiểm thử: 7 phân hệ chính của CMS-AI.
- Ma trận phân loại mức độ rủi ro (Risk Matrix): Chức năng tài chính viện phí và phân quyền EMR là rủi ro Cực cao (Critical).
- Môi trường kiểm thử: Python 3.11+, Pytest 8.x, SQLite Test DB.
- Tiêu chí dừng kiểm thử: 100% test cases pass, không có lỗi rò rỉ bộ nhớ hoặc unhandled exception.

BƯỚC 3: XÂY DỰNG BỘ KIỂM THỬ TỰ ĐỘNG PYTEST (backend/tests/)
Hiện thực hóa hơn 319 kịch bản kiểm thử chia thành 5 module chính:
1. `test_auth.py`: Đăng nhập, băm mật khẩu, hết hạn token, token giả mạo, kiểm tra ma trận phân quyền 4 vai trò.
2. `test_clinic_ops.py`: Quản lý bệnh nhân, bác sĩ, buồng khám, chuyên khoa, ca làm việc.
3. `test_conflict.py`: 15 kịch bản giao thoa thời gian của thuật toán phát hiện xung đột lịch khám.
4. `test_emr_billing.py`: Khám lâm sàng, chỉ định CLS, kê đơn thuốc, kiểm tra dị ứng thuốc, trừ tồn kho, tính viện phí BHYT và sinh mã VietQR.
5. `test_m3_anonymizer.py` & `test_m3_ai.py`: Khử định danh PII (CCCD, SĐT, BHYT), Pre-visit Briefing, Discharge Instructions.
6. `test_m1_adversarial.py`: Thử nghiệm tấn công Prompt Injection, giả lập hacker vượt quyền, kiểm thử Fallback Mock AI khi ngắt kết nối.

BƯỚC 4: THỰC THI KIỂM THỬ VÀ LẬP BÁO CÁO TEST REPORT (docs/test-report.md)
Chạy lệnh `pytest backend/tests -v`, thu thập kết quả chi tiết:
- Số lượng test cases thực thi: 319 passed, 4 xfailed (kịch bản thiết kế chặn trước).
- Tỷ lệ thành công: 100%.
- Bảng tổng hợp lỗi phát hiện được trong quá trình kiểm thử và biện pháp khắc phục.
```

---

## 5. SẢN PHẨM ARTIFACTS KẾT XUẤT
1. [`.agents/skills/testing/SKILL.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/.agents/skills/testing/SKILL.md)
2. [`docs/test-plan.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/docs/test-plan.md)
3. [`docs/test-report.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/docs/test-report.md)
4. Toàn bộ bộ test tự động trong thư mục [`backend/tests/`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/backend/tests)

---

## 6. KIỂM CHỨNG & HIỆU CHỈNH CỦA CON NGƯỜI (HUMAN GATE 2)
* **Lỗi do AI đề xuất:** AI ban đầu viết các test cases gọi trực tiếp tới Cloud API của Google Gemini và OpenAI trong lúc chạy test suite. Điều này dẫn tới việc test bị chậm, tiêu tốn chi phí quota API và test lập tức bị gãy (failed) khi ngắt kết nối mạng Internet.
* **Hành động hiệu chỉnh của Kỹ sư Con người:** Kỹ sư Trưởng đã cấu hình fixture `mock_ai_provider` và ép buộc toàn bộ test suite chạy trên `DeterministicMockAIService`, giúp bộ 319+ test cases thực thi siêu tốc trong chưa đầy 15 giây mà không cần một byte kết nối Internet nào.
