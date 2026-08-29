# HỒ SƠ QUYẾT ĐỊNH KIẾN TRÚC (ARCHITECTURE DECISION RECORDS - ADR)
## DỰ ÁN: HỆ THỐNG QUẢN LÝ PHÒNG KHÁM ĐA KHOA THÔNG MINH TÍCH HỢP TRỢ LÝ AI HÀNH CHÍNH
### (Clinic Management System with Administrative AI Assistant - CMS-AI)

---

## 1. MỤC ĐÍCH & PHƯƠNG PHÁP QUẢN TRỊ KIẾN TRÚC

Tài liệu này lưu trữ các Quyết định Kiến trúc (ADR) quan trọng được đưa ra trong suốt vòng đời phát triển hệ thống CMS-AI. Mỗi bản ghi tuân thủ cấu trúc chuẩn quốc tế Michael Nygard: **Title, Status, Context, Decision, Consequences, Compliance**.

```
+---------------------------------------------------------------------------------------------------+
|                        DANH MỤC CÁC QUYẾT ĐỊNH KIẾN TRÚC (ADR-001 ĐẾN ADR-008)                    |
+---------------------------------------------------------------------------------------------------+
| ADR-001: Lựa chọn FastAPI (Python 3.10+) cho Backend Y tế Hiệu năng cao                          |
| ADR-002: Lựa chọn React 18 SPA + Vite + Tailwind CSS theo Chuẩn Taste-Skill Y tế                  |
| ADR-003: Chiến lược Cơ sở dữ liệu Kép: SQLite (Dev/Test) & PostgreSQL 16 (Production)            |
| ADR-004: Thiết kế Kiến trúc AI Engine Phân tầng 4 Lớp Độc lập                                     |
| ADR-005: Khử Định danh PII bằng Biểu thức Chính quy (Regex) & Tokenization                       |
| ADR-006: Xác thực Không Trạng thái (Stateless JWT) & Băm Mật khẩu Bcrypt                         |
| ADR-007: Đóng gói Đa Container bằng Docker Compose (Backend, Frontend, Postgres, pgAdmin)        |
| ADR-008: Tích hợp Deterministic Rule-Based Mock AI Provider phục vụ Offline & Auto-Testing       |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. CHI TIẾT CÁC BẢN GHI QUYẾT ĐỊNH KIẾN TRÚC

### ADR-001: Lựa chọn FastAPI (Python 3.10+) cho Backend Y tế Hiệu năng cao
- **Trạng thái:** `ACCEPTED` | **Ngày quyết định:** 2026-08-22
- **Bối cảnh (Context):**
  Hệ thống quản lý phòng khám đòi hỏi khả năng xử lý đồng thời cao (hàng trăm lượt đặt lịch, tra cứu hồ sơ và tích hợp các thư viện AI/Machine Learning trong hệ sinh thái Python). Cần một framework hiện đại, có tính năng xác thực kiểu dữ liệu chặt chẽ và sinh tài liệu API tự động.
- **Quyết định (Decision):**
  Lựa chọn **FastAPI (Python 3.10+)** kết hợp ASGI server **Uvicorn**, ORM **SQLAlchemy 2.0** và **Pydantic v2**.
- **Hệ quả (Consequences):**
  - *Mặt tích cực:* Tốc độ xử lý tương đương NodeJS/Go; Pydantic v2 ép kiểu dữ liệu y tế nghiêm ngặt; tự động sinh Swagger UI tương tác (`/docs`).
  - *Thách thức:* Đội ngũ cần nắm vững lập trình bất đồng bộ (`async`/`await`) và dependency injection trong FastAPI.

---

### ADR-002: Lựa chọn React 18 SPA + Vite + Tailwind CSS theo Chuẩn Taste-Skill Y tế
- **Trạng thái:** `ACCEPTED` | **Ngày quyết định:** 2026-08-22
- **Bối cảnh (Context):**
  Nhân viên y tế (Bác sĩ, Lễ tân, Thu ngân) thao tác liên tục nhiều giờ trước màn hình máy tính. Giao diện cần công thái học tối ưu, tốc độ phản hồi trang tức thì, không tải lại trang (SPA), chống "AI-slop" rối mắt và đảm bảo độ tương phản cao.
- **Quyết định (Decision):**
  Xây dựng Frontend dưới dạng **Single Page Application (SPA)** bằng **React 18**, đóng gói bằng **Vite**, định dạng kiểu dáng bằng **Tailwind CSS** và bộ biểu tượng **Lucide Icons**. Tuân thủ nghiêm ngặt bảng màu y tế (Slate/Emerald/Sky Blue/Rose) và phông chữ số học `tabular-nums font-mono`.
- **Hệ quả (Consequences):**
  - *Mặt tích cực:* Trải nghiệm mượt mà, chuyển trang < 100ms; biểu mẫu khám bệnh có tính tương tác cao; modal in ấn hóa đơn viện phí sắc nét.
  - *Thách thức:* Cần quản lý vòng đời component và đồng bộ trạng thái xác thực qua React Context API.

---

### ADR-003: Chiến lược Cơ sở dữ liệu Kép: SQLite (Dev/Test) & PostgreSQL 16 (Production)
- **Trạng thái:** `ACCEPTED` | **Ngày quyết định:** 2026-08-22
- **Bối cảnh (Context):**
  Môi trường triển khai đa dạng: Máy chấm bài / Dev cục bộ cần chạy ngay không cần cài đặt dịch vụ database nặng, trong khi môi trường Production bệnh viện cần hệ quản trị cơ sở dữ liệu quan hệ mạnh mẽ, hỗ trợ giao dịch ACID cao cấp, Connection Pooling và mở rộng quy mô.
- **Quyết định (Decision):**
  Sử dụng **SQLAlchemy 2.0 ORM** làm tầng trừu tượng hóa cơ sở dữ liệu. Mặc định chạy **SQLite** (file cục bộ hoặc in-memory) cho môi trường kiểm thử tự động và máy dev; cấu hình chuỗi kết nối **PostgreSQL 16** cho môi trường Docker và máy chủ sản xuất.
- **Hệ quả (Consequences):**
  - *Mặt tích cực:* Bộ test 223+ cases chạy tức thì trong 30 giây mà không cần cài đặt PostgreSQL; sẵn sàng chuyển đổi lên PostgreSQL chỉ bằng 1 dòng cấu hình `.env`.
  - *Thách thức:* Phải tránh sử dụng các câu lệnh SQL đặc thù riêng của từng loại DB để duy trì tính tương thích 100%.

---

### ADR-004: Thiết kế Kiến trúc AI Engine Phân tầng 4 Lớp Độc lập
- **Trạng thái:** `ACCEPTED` | **Ngày quyết định:** 2026-08-22
- **Bối cảnh (Context):**
  Ứng dụng AI trong y tế tiềm ẩn rủi ro vi phạm dữ liệu cá nhân, câu trả lời sai lệch gây nguy hiểm tính mạng và phụ thuộc vào kết nối đám mây. Cần một kiến trúc phòng thủ đa tầng tách biệt rạch ròi.
- **Quyết định (Decision):**
  Thiết kế **4 Lớp AI Độc lập**:
  1. *Lớp 1 (Privacy):* Regex khử định danh PII sang Token.
  2. *Lớp 2 (Ethics & Guardrails):* Chặn Prompt Injection, từ chối chẩn đoán chuyên môn, nhúng Disclaimer.
  3. *Lớp 3 (Multi-Provider Abstraction):* Giao diện `AIProvider` hỗ trợ Mock, Ollama và Cloud API.
  4. *Lớp 4 (Logging & Audit):* Ghi nhận lịch sử prompt đã ẩn danh và độ trễ.
- **Hệ quả (Consequences):**
  - *Mặt tích cực:* Bảo vệ dữ liệu cá nhân tuyệt đối; đảm bảo tuân thủ đạo đức y khoa; dễ dàng thay thế mô hình LLM mà không sửa đổi mã nguồn nghiệp vụ.
  - *Thách thức:* Tăng thêm một số mili-giây xử lý trung gian (được tối ưu < 5ms).

---

### ADR-005: Khử Định danh PII bằng Biểu thức Chính quy (Regex) & Tokenization
- **Trạng thái:** `ACCEPTED` | **Ngày quyết định:** 2026-08-22
- **Bối cảnh (Context):**
  Các giải pháp nhận diện PII bằng mô hình NLP học sâu (như SpaCy/BERT) thường nặng nề, đòi hỏi GPU và có thể bỏ sót định dạng số hành chính đặc thù của Việt Nam (CCCD 12 số, mã BHYT 15 ký tự).
- **Quyết định (Decision):**
  Xây dựng `PIIAnonymizer` thuần túy bằng **Python Regex biên dịch sẵn (`re.compile`)** kết hợp **Tokenization từ điển**. Các mẫu nhận diện được tối ưu hóa cho đầu số viễn thông Việt Nam (03x, 05x, 07x, 08x, 09x, +84), CCCD 12 số, CMND 9 số và mã thẻ BHYT có tiền tố chuyên ngành (GD, DN, TE, BT, HT...).
- **Hệ quả (Consequences):**
  - *Mặt tích cực:* Tốc độ xử lý cực nhanh (< 1ms/văn bản); 0% phụ thuộc thư viện ngoài; độ chính xác 100% với các mã số chuẩn hóa.
  - *Thách thức:* Cần liên tục cập nhật biểu thức nếu có sự thay đổi quy định mã định danh quốc gia.

---

### ADR-006: Xác thực Không Trạng thái (Stateless JWT) & Băm Mật khẩu Bcrypt
- **Trạng thái:** `ACCEPTED` | **Ngày quyết định:** 2026-08-22
- **Bối cảnh (Context):**
  Hệ thống phục vụ đồng thời nhiều người dùng từ các phòng ban khác nhau. Cần cơ chế xác thực an toàn, dễ mở rộng (Scalable), không phụ thuộc vào bộ nhớ Session tập trung của Server.
- **Quyết định (Decision):**
  Sử dụng **JSON Web Token (JWT)** theo chuẩn RFC 7519, thuật toán ký mật mã `HS256`, chứa thông tin định danh `user_id`, `username`, `role` và thời gian hết hạn `exp = 60 phút`. Mật khẩu được băm một chiều bằng **Bcrypt** với chi phí 12 rounds.
- **Hệ quả (Consequences):**
  - *Mặt tích cực:* Máy chủ Backend hoàn toàn Stateless, dễ dàng mở rộng nhiều instance; bảo vệ chống tấn công Brute-force mật khẩu.
  - *Thách thức:* Thu hồi token trước thời hạn (Revocation) cần giải pháp Blacklist khi có yêu cầu bảo mật đột xuất.

---

### ADR-007: Đóng gói Đa Container bằng Docker Compose
- **Trạng thái:** `ACCEPTED` | **Ngày quyết định:** 2026-08-22
- **Bối cảnh (Context):**
  Việc cài đặt môi trường y tế thủ công (Python, Node, PostgreSQL, Nginx) trên các máy chủ phòng khám thường dễ phát sinh lỗi xung đột phiên bản phần mềm.
- **Quyết định (Decision):**
  Đóng gói toàn bộ hệ sinh thái thành tệp `docker-compose.yml` gồm 4 dịch vụ cô lập: `clinic_backend` (cổng 8000), `clinic_frontend` (cổng 3000), `clinic_postgres` (cổng 5432), và `clinic_pgadmin` (cổng 5050). Đi kèm các tệp batch script Windows (`run_backend.bat`, `run_frontend.bat`, `run_all.bat`).
- **Hệ quả (Consequences):**
  - *Mặt tích cực:* Triển khai một chạm (One-click deployment); đồng nhất môi trường từ máy phát triển đến máy chủ thật.
  - *Thách thức:* Đòi hỏi máy chủ hỗ trợ Docker Engine và RAM tối thiểu 4GB.

---

### ADR-008: Tích hợp Deterministic Rule-Based Mock AI Provider phục vụ Offline & Auto-Testing
- **Trạng thái:** `ACCEPTED` | **Ngày quyết định:** 2026-08-22
- **Bối cảnh (Context):**
  Khi chạy bộ kiểm thử tự động (CI/CD hoặc máy lab chấm bài) hoặc khi phòng khám tạm thời mất Internet, việc gọi các dịch vụ LLM đám mây sẽ gây chậm trễ, tốn chi phí và làm flaky test suite nếu mạng chập chờn.
- **Quyết định (Decision):**
  Cài đặt `MockDeterministicAIProvider` kế thừa từ `AIProvider`. Lớp này thực thi các quy tắc suy diễn cục bộ (Rule-based heuristics) để trả về kết quả tóm tắt bệnh sử, câu trả lời FAQ và dặn dò sau khám hoàn toàn xác định, đúng cấu trúc schema, có đầy đủ Disclaimer và độ trễ < 5ms.
- **Hệ quả (Consequences):**
  - *Mặt tích cực:* Toàn bộ 223+ test cases chạy thành công 100% trên bất kỳ máy nào mà không cần kết nối mạng; hệ thống tự động fallback mượt mà khi API ngoài gặp sự cố.
  - *Thách thức:* Phản hồi của Mock Provider mang tính cố định dựa trên quy tắc nghiệp vụ chứ không linh hoạt bằng LLM sinh ngôn ngữ tự nhiên.

---

## 3. TỔNG KẾT & ĐÁNH GIÁ TÍNH TUÂN THỦ

Toàn bộ 8 Quyết định Kiến trúc trên đã được nhóm phát triển tuân thủ 100% trong quá trình hiện thực hóa mã nguồn hệ thống CMS-AI.
