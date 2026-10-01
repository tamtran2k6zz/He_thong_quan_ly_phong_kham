# PROMPT GIAO VIỆC: BIÊN SOẠN TÀI LIỆU MINH CHỨNG 4 GIAI ĐOẠN SDLC & BÁO CÁO TỔNG KẾT
## Giai đoạn SDLC: Giai đoạn 4 – Final Deliverables & Master Synthesis (KT4 / Cuối kỳ)
### Kỹ năng áp dụng: `.agents/skills/documentation/SKILL.md`

---

## 1. THÔNG TIN NGỮ CẢNH & MỤC TIÊU
* **Dự án:** Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp Trợ lý AI Hành chính (CMS-AI).
* **Đơn vị thực hiện:** Nhóm 07 (Đinh Gia Bảo - Trưởng nhóm, Trần Đặng Công Tâm).
* **Mục tiêu:** Biên soạn toàn bộ hệ thống tài liệu minh chứng học phần cho 4 giai đoạn phát triển phần mềm (KT1, KT2, KT3, KT4), xây dựng Báo cáo Tổng kết Phương pháp luận AI-Augmented SDLC (Master Synthesis Report) phản ánh rõ 3 Cổng Kiểm soát Con người (Human Gates 1 - 3), Bảng theo dõi lỗi do AI tạo ra và các hiệu chỉnh thực tế của con người, cùng Hướng dẫn Triển khai (Deployment Guide) và Hướng dẫn Sử dụng (User Guide) theo từng vai trò.

---

## 2. VAI TRÒ CỦA AI AGENT (PERSONA)
Bạn là **Lead Technical Writer & SDLC Methodologist Agent (Trưởng nhóm Biên tập Tài liệu Kỹ thuật & Phương pháp luận SDLC)**, am hiểu sâu sắc quy chuẩn học phần Công nghệ Phần mềm và Ứng dụng Trí tuệ Nhân tạo, có kỹ năng tổng hợp dữ liệu xuất sắc, hành văn mạch lạc, chặt chẽ và chuẩn xác.

---

## 3. RÀNG BUỘC KỸ THUẬT & QUY TẮC CỐT LÕI (GUARDRAILS)
1. **Minh bạch Quá trình Đồng sáng tạo (Human-AI Collaboration):** Báo cáo không được che giấu các sai sót của AI, mà phải làm nổi bật năng lực phát hiện và hiệu chỉnh của Kỹ sư Con người (Human-in-the-Loop) tại 3 cổng kiểm soát: Human Gate 1 (Yêu cầu & Đạo đức), Human Gate 2 (Kiến trúc & Mã nguồn), Human Gate 3 (An toàn lâm sàng & Quyền riêng tư).
2. **Khớp nối 100% với Dữ liệu Thực tế:** Toàn bộ số liệu trong báo cáo (319+ test cases, 14 bảng CSDL, 4 vai trò RBAC, 3 tính năng AI) phải khớp chính xác với mã nguồn thực tế trong kho lưu trữ Git.
3. **Phân định rõ 9 Hạng mục Đánh giá:** SKILL.md, Prompts, Artifacts, Test Evidence, Review Report, Security Report, AI Errors Detected, Human Corrections, Git History.

---

## 4. NỘI DUNG MASTER PROMPT ĐÃ GIAO CHO AI AGENT

```markdown
Bạn hãy đóng vai trò là Lead Technical Writer & SDLC Methodologist. Hãy tổng hợp và biên soạn toàn bộ hệ thống tài liệu học phần cho dự án CMS-AI của Nhóm 07:

BƯỚC 1: XÂY DỰNG SKILL BIÊN SOẠN TÀI LIỆU (.agents/skills/documentation/SKILL.md)
Tạo file SKILL.md quy định quy chuẩn viết tài liệu kỹ thuật: Cấu trúc 4 giai đoạn SDLC, quy chuẩn bảng biểu, sơ đồ Mermaid và danh mục tài liệu xuất xưởng bắt buộc.

BƯỚC 2: TỔNG HỢP BÁO CÁO MASTER AI-AUGMENTED SDLC (docs/Reports/AI-Augmented-SDLC-Report.md)
Soạn thảo báo cáo tổng thể gồm 4 chương trọng tâm:
1. Tổng quan phương pháp luận AI-Augmented SDLC và mô hình vận hành 4 trụ cột (Codex, Skill, Tool, MCP).
2. Chuỗi công cụ AI (AI Toolchain) tương ứng với 4 giai đoạn phát triển phần mềm.
3. Hiện thực hóa 3 Cổng Kiểm soát Con người (Human Gates 1 - 3):
   - Human Gate 1: Bác bỏ đề xuất AI tự chẩn đoán bệnh tật, xác lập ranh giới đạo đức y khoa.
   - Human Gate 2: Tái cấu trúc giao dịch CSDL viện phí nguyên tử, bổ sung kiểm tra xung đột phòng khám 2 chiều.
   - Human Gate 3: Khắc phục lỗi Regex che nhầm thông số sinh hiệu lâm sàng, bắt buộc đính kèm Medical Disclaimer.
4. Bảng theo dõi chi tiết 4 lỗi do AI tạo ra (AI Hallucinations), nguy cơ tiềm ẩn và hành động hiệu chỉnh cụ thể của con người.

BƯỚC 3: BIÊN SOẠN BỘ 4 TÀI LIỆU MINH CHỨNG 4 GIAI ĐOẠN SDLC (docs/Reports/)
1. `SDLC_GiaiDoan1_PhanTich_ThietKe.md`: Khảo sát hiện trạng, 4 Actor, 38 FR, 10 NFR, ranh giới đạo đức AI.
2. `SDLC_GiaiDoan2_ChucNang_QuanLy.md`: Hiện thực hóa nghiệp vụ tiếp đón, thuật toán xung đột, khám bệnh, kê đơn và viện phí.
3. `SDLC_GiaiDoan3_TichHopAI_TestAI.md`: Module khử định danh PII, Pre-visit Briefing, FAQ Chatbot, Discharge Instructions, cơ chế Mock AI Fallback.
4. `SDLC_GiaiDoan4_BaoCao_HuongDan_TrienKhai.md`: Báo cáo an toàn thông tin, kết quả kiểm thử 319+ test cases, kịch bản demo chấm điểm theo 4 vai trò.

BƯỚC 4: XÂY DỰNG HƯỚNG DẪN TRIỂN KHAI VÀ SỬ DỤNG
- `docs/deployment.md`: Hướng dẫn khởi chạy bằng Docker Compose và chạy local với các file batch (.bat), cấu hình biến môi trường `.env`.
- `docs/user-guide.md`: Cẩm nang hướng dẫn sử dụng chi tiết bằng hình ảnh và từng bước thao tác cho Lễ tân, Bác sĩ, Thu ngân và Quản trị viên.
- `docs/Reports/phan-chia-cong-viec.md`: Bảng phân công nhiệm vụ và tỷ lệ đóng góp chi tiết giữa Đinh Gia Bảo (Trưởng nhóm - 50%) và Trần Đặng Công Tâm (50%).
```

---

## 5. SẢN PHẨM ARTIFACTS KẾT XUẤT
1. [`.agents/skills/documentation/SKILL.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/.agents/skills/documentation/SKILL.md)
2. Báo cáo tổng thể [`docs/Reports/AI-Augmented-SDLC-Report.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/docs/Reports/AI-Augmented-SDLC-Report.md)
3. Bộ 4 tài liệu minh chứng SDLC trong [`docs/Reports/`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/docs/Reports)
4. [`docs/deployment.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/docs/deployment.md) & [`docs/user-guide.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/docs/user-guide.md)
5. Bảng phân chia công việc [`docs/Reports/phan-chia-cong-viec.md`](file:///d:/ICTU/Nam%203/ICTU_2026-2027/%E1%BB%A8ng%20d%E1%BB%A5ng%20tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20-%20Project/He_thong_quan_ly_phong_kham/docs/Reports/phan-chia-cong-viec.md)

---

## 6. KIỂM CHỨNG & HIỆU CHỈNH CỦA CON NGƯỜI (HUMAN GATE 1 - 3)
* **Lỗi do AI đề xuất:** AI ban đầu sinh các bản báo cáo theo mẫu chung chung của phần mềm thương mại điện tử, trích dẫn sai số lượng test cases (ghi 50 tests thay vì 319 tests) và tự ý bổ sung các thư viện không có thực trong mã nguồn.
* **Hành động hiệu chỉnh của Kỹ sư Con người:** Kỹ sư Trưởng đã rà soát và đối soát trực tiếp từng mục trong báo cáo với mã nguồn thực tế, cập nhật chính xác số liệu 319 passed tests, 14 bảng quan hệ, bảo đảm 100% tính chân thực và tính minh chứng cao nhất trước Hội đồng chấm điểm.
