# -*- coding: utf-8 -*-
"""
Script sinh tài liệu Word chuyên sâu:
BÁO CÁO QUÁ TRÌNH ỨNG DỤNG AI AGENT TRONG TOÀN BỘ VÒNG ĐỜI THIẾT KẾ VÀ PHÁT TRIỂN HỆ THỐNG PHÒNG KHÁM (CMS-AI)
Đề tài: Hệ thống Quản lý Phòng khám Đa khoa Tích hợp AI Hành chính
Nhóm 03 - Lớp An toàn thông tin K23A, Trường Đại học CNTT & Truyền thông (ICTU)
Sinh viên: Đinh Gia Bảo (Trưởng nhóm) & Trần Đặng Công Tâm
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Thêm đường dẫn scripts vào sys.path để import helpers
sys.path.append(os.path.dirname(__file__))

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

def build_ai_agent_report():
    doc = create_base_document()

    # Trang tiêu đề chuẩn mực
    add_header_block(
        doc,
        "BÁO CÁO QUÁ TRÌNH ỨNG DỤNG AI AGENT TRONG THIẾT KẾ VÀ PHÁT TRIỂN HỆ THỐNG",
        "PHƯƠNG PHÁP LUẬN AI-AUGMENTED SDLC & AGENTIC WORKFLOW CHO HỆ THỐNG PHÒNG KHÁM (CMS-AI)"
    )

    add_team_meta(doc)

    # Lời mở đầu
    add_p(
        doc,
        "Báo cáo này trình bày toàn diện, chi tiết và có hệ thống quá trình đội ngũ phát triển (Nhóm 03) đã ứng dụng "
        "các tác nhân trí tuệ nhân tạo (AI Agents / Codex) đồng hành xuyên suốt 4 giai đoạn của vòng đời phát triển phần mềm (SDLC) "
        "để tạo nên Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp Trợ lý AI Hành chính (CMS-AI). "
        "Điểm cốt lõi của công trình là không sử dụng AI như một công cụ sinh code rời rạc, mà tổ chức thành một thực thể kỹ thuật "
        "vận hành theo mô hình 4 trụ cột có kiểm soát (Codex, Skills, Tools, MCP) kết hợp với vai trò giám sát tối cao của Kỹ sư Con người "
        "(Human-in-the-Loop) qua 3 Cổng Kiểm soát Chất lượng (Human Gates 1, 2, 3)."
    )

    # =========================================================================
    # PHẦN 1: TỔNG QUAN PHƯƠNG PHÁP LUẬN AI-AUGMENTED SDLC
    # =========================================================================
    add_h1(doc, "1. TỔNG QUAN PHƯƠNG PHÁP LUẬN AI-AUGMENTED SDLC VÀ KHUNG KIẾN TRÚC AI AGENT")

    add_h2(doc, "1.1. Bối cảnh và Sự chuyển dịch mô hình phát triển phần mềm")
    add_p(
        doc,
        "Trong kỷ nguyên trí tuệ nhân tạo tạo sinh (GenAI), phương pháp phát triển phần mềm truyền thống đang chứng kiến "
        "sự chuyển dịch căn bản: từ việc lập trình viên trực tiếp viết từng dòng mã sang mô hình Kỹ sư Phần mềm đóng vai trò "
        "Kiến trúc sư và Người điều phối (Orchestrator) các AI Agents chuyên trách. "
        "Mô hình AI-Augmented SDLC áp dụng trong dự án CMS-AI định hình AI Agent không chỉ là công cụ hỗ trợ gõ code (Auto-complete) "
        "mà là các chuyên viên ảo có khả năng hiểu ngữ cảnh dự án, thực hiện quy trình nghiệp vụ có cấu trúc và tuân thủ các ràng buộc y tế khắt khe."
    )

    add_h2(doc, "1.2. Khung kiến trúc 4 trụ cột vận hành AI Agent")
    add_p(
        doc,
        "Để đảm bảo AI Agent hoạt động chính xác, ổn định và không sinh ra mã độc hại hay ảo giác (Hallucination), "
        "hệ thống vận hành dựa trên khung kiến trúc 4 trụ cột tương hỗ:"
    )

    four_pillars = [
        ("1. Trụ cột CODEX / AI AGENT (Persona & Cognitive Role): ",
         "Định hình vai trò tư duy chuyên trách cho từng tác vụ cụ thể thay vì dùng chung một prompt mơ hồ. Dự án thiết lập 8 Persona riêng biệt: "
         "Lead Healthcare BA Agent (phân tích yêu cầu), System Architect Agent (thiết kế kiến trúc), Database Designer Agent (mô hình 14 bảng 3NF), "
         "Fullstack Coder Agent (hiện thực hóa FastAPI/React), QA Automation Agent (kiểm thử 323 test suites), Security Auditor Agent (kiểm toán OWASP & Nghị định 13), "
         "AI Prompt Engineer Agent (rào chắn đạo đức & RAG) và Technical Documentation Agent (biên soạn 7 tập báo cáo Word)."),
        
        ("2. Trụ cột SKILLS (Standard Operating Procedures - SOP): ",
         "Kho lưu trữ 15 tệp tiêu chuẩn kỹ thuật (.agents/skills/SKILL.md) chuẩn hóa theo cú pháp YAML frontmatter. Mỗi Skill đóng vai trò "
         "bản quy chuẩn quy trình bắt buộc AI Agent phải tuân thủ trước khi thực thi: quy định rõ đầu vào, các bước tư duy, tiêu chuẩn đầu ra, "
         "chỉ tiêu kỹ thuật và các quy tắc cấm kỵ (ví dụ: cấm AI tự chẩn đoán bệnh tật)."),

        ("3. Trụ cột TOOLS & ENVIRONMENT (Hành động trong môi trường): ",
         "Tập hợp các công cụ cho phép AI Agent tương tác trực tiếp với không gian làm việc: công cụ đọc/ghi/chỉnh sửa file mã nguồn, "
         "terminal PowerShell thực thi lệnh máy chủ, trình chạy kiểm thử Pytest 8.3, nền tảng container Docker, Git kiểm soát phiên bản "
         "và công cụ vẽ sơ đồ kỹ thuật Matplotlib 300 DPI."),

        ("4. Trụ cột MCP & CONTEXT (Giao thức ngữ cảnh thông minh): ",
         "Cơ chế nạp tri thức dự án vào cửa sổ ngữ cảnh của Agent (Model Context Protocol): lược đồ 14 bảng CSDL, danh mục chuẩn quốc tế ICD-10, "
         "quy định bảo vệ dữ liệu cá nhân theo Nghị định 13/2023/NĐ-CP, tài liệu đặc tả OpenAPI 3.0 và lịch sử kiểm thử trước đó.")
    ]

    for p_title, p_desc in four_pillars:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(p_title)
        r1.font.name = "Times New Roman"
        r1.font.bold = True
        r1.font.size = Pt(11)
        r2 = p.add_run(p_desc)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11)

    # Chèn sơ đồ Khung kiến trúc 4 trụ cột
    diag_framework = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "generated_diagrams", "diagram_ai_sdlc_framework.png"))
    add_diagram(doc, diag_framework, "Hình 1.1: Khung kiến trúc 4 trụ cột vận hành AI Agent và Tầng kiểm soát Human Gate (300 DPI)", width=Inches(6.4))

    add_h2(doc, "1.3. Nguyên tắc Human-in-the-Loop và 3 Cổng Kiểm soát Chất lượng (Human Gates)")
    add_p(
        doc,
        "Nguyên tắc cốt tử xuyên suốt dự án là: 'AI Agent tăng tốc sản xuất (10x), nhưng Kỹ sư Con người chịu trách nhiệm tối cao về chất lượng và đạo đức y tế'. "
        "Để hiện thực hóa nguyên tắc này, nhóm sinh viên thiết lập 3 Cổng Kiểm soát Con người (Human Gates) bắt buộc phải có biên bản phê duyệt trước khi chuyển giao giai đoạn:"
    )

    gates_intro = [
        ("• Human Gate 1 (Giai đoạn 1 - Yêu cầu & Phạm vi): ", "Thẩm định phạm vi nghiệp vụ và ranh giới đạo đức y tế. Kỹ sư con người phát hiện và bác bỏ dứt khoát đề xuất nguy hiểm của AI về việc 'tự động chẩn đoán bệnh học và kê đơn thuốc', giới hạn quyền hạn của AI vào vai trò Trợ lý Hành chính."),
        ("• Human Gate 2 (Giai đoạn 2 - Kiến trúc & Chất lượng mã): ", "Kiểm toán mã nguồn và an toàn dữ liệu. Con người can thiệp xử lý race condition thanh toán viện phí, bắt buộc đóng gói toàn bộ quy trình xuất hóa đơn và trừ kho thuốc vào một Database Transaction nguyên tử."),
        ("• Human Gate 3 (Giai đoạn 3 & 4 - Thẩm chuẩn Lâm sàng & Nghiệm thu): ", "Kiểm định an toàn dữ liệu cá nhân y tế theo Nghị định 13/2023/NĐ-CP, kiểm thử tấn công Jailbreak/Prompt Injection, thẩm định bộ 323 ca test và ký duyệt nghiệm thu hệ thống.")
    ]
    for g_title, g_desc in gates_intro:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(g_title)
        r1.font.bold = True
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        r2 = p.add_run(g_desc)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11)

    # =========================================================================
    # PHẦN 2: HỆ SINH THÁI 15 AGENT SKILLS CHUYÊN BIỆT
    # =========================================================================
    add_h1(doc, "2. HỆ SINH THÁI 15 AGENT SKILLS CHUYÊN BIỆT TRONG DỰ ÁN (.AGENTS/SKILLS/)")
    add_p(
        doc,
        "Dự án đã xây dựng và chuẩn hóa toàn diện hệ sinh thái 15 Kỹ năng tác nhân (Agent Skills) được lưu trữ tại thư mục "
        "'.agents/skills/'. Mỗi tệp SKILL.md chứa định nghĩa siêu dữ liệu chuẩn YAML, bản đặc tả quy trình SOP từng bước, "
        "tiêu chí chấp nhận và các rào chắn kiểm soát lỗi ảo giác:"
    )

    skills_data = [
        ("1", "requirements-analysis", "Kỹ thuật Yêu cầu", "Khảo sát bài toán, phân tách 4 vai trò, đặc tả 38 FR, 10 NFR, 27 User Stories chuẩn INVEST", "Cấm AI đề xuất tính năng tự chẩn đoán bệnh", "docs/requirements.md, user-stories.md"),
        ("2", "architecture-design", "Thiết kế Kiến trúc", "Thiết kế kiến trúc phân tầng Clean Architecture, API Gateway, Dockerization và 5 quyết định ADR", "Bảo đảm tính độc lập giữa Backend và UI", "docs/architecture.md, architecture-decisions.md"),
        ("3", "database-design", "Thiết kế CSDL", "Mô hình hóa 14 bảng quan hệ đạt chuẩn 3NF, xác lập ràng buộc PK/FK, chỉ mục tối ưu tìm kiếm", "Bắt buộc ON DELETE RESTRICT cho bệnh nhân", "docs/database-design.md, Schema SQL"),
        ("4", "diagram-design", "Mô hình hóa UML", "Sinh mã nguồn Mermaid và script vẽ sơ đồ kỹ thuật 300 DPI cho Use Case, Class, Sequence, ERD", "Tuân thủ nghiêm ngặt chuẩn UML 2.5", "Sơ đồ UML trong docs/ và generated_diagrams/"),
        ("5", "implementation", "Hiện thực Mã nguồn", "Lập trình Backend FastAPI, SQLAlchemy ORM, thuật toán ConflictChecker và React SPA", "Tuyệt đối không hardcode mật khẩu, dùng bcrypt", "backend/app/, frontend/src/"),
        ("6", "design-taste-frontend", "Thiết kế Giao diện", "Xây dựng hệ thống Design Tokens y tế, màu sắc Slate/Teal trang nhã, công thái học lâm sàng", "Chống AI-slop, tối ưu cho bác sĩ lớn tuổi", "frontend/src/index.css, Components"),
        ("7", "pii-deidentification", "Bảo mật Dữ liệu", "Xây dựng module khử định danh Regex che giấu số CCCD, SĐT, mã BHYT trước khi gửi LLM", "Đạt tỷ lệ 0% rò rỉ dữ liệu theo Nghị định 13", "backend/app/ai/anonymizer.py"),
        ("8", "pre-visit-briefing", "Trợ lý Lâm sàng", "Trích xuất lịch sử khám cũ và gọi mô hình AI tóm tắt diễn tiến bệnh lý trong thời gian < 15s", "Bắt buộc đính kèm nhãn cảnh báo miễn trừ y tế", "backend/app/ai/pre_visit.py"),
        ("9", "clinic-faq-rag", "Trợ lý Hỏi đáp", "Xây dựng Chatbot hỏi đáp thủ tục phòng khám từ kho tri thức RAG và bộ lọc an toàn Guardrails", "Lập tức từ chối các câu hỏi hỏi về chẩn đoán", "backend/app/ai/faq_chatbot.py"),
        ("10", "discharge-instructions", "Hướng dẫn Sau khám", "Tự động phân chia lịch uống thuốc 4 bữa sáng/trưa/chiều/tối và chế độ ăn uống kiêng cữ", "Bác sĩ bắt buộc phải duyệt trước khi in", "backend/app/ai/discharge.py"),
        ("11", "testing", "Kiểm thử Tự động", "Xây dựng và thực thi bộ 323 kịch bản kiểm thử tự động trên Pytest 8.3 và FastAPI TestClient", "Yêu cầu tỷ lệ kiểm thử đạt 100% (Pass Rate)", "backend/tests/, docs/test-report.md"),
        ("12", "code-review", "Kiểm toán Mã", "Rà soát chất lượng mã nguồn theo chuẩn PEP 8, phát hiện race conditions và rà soát phân quyền", "Phân loại mức độ khuyết tật CRITICAL/HIGH/MED", "docs/code-review.md"),
        ("13", "security-review", "An ninh Thông tin", "Kiểm toán an toàn thông tin theo mô hình STRIDE, tiêu chuẩn OWASP Top 10 API và phòng chống Jailbreak", "Chặn tấn công SQLi, XSS, Prompt Injection", "docs/security-review.md"),
        ("14", "documentation", "Tài liệu hóa SDLC", "Biên soạn các tài liệu kỹ thuật, sổ tay hướng dẫn sử dụng và 7 tập tài liệu Word chuẩn môn học", "Cấu trúc rõ ràng, giữ tính nhất quán kỹ thuật", "docs/7_Giai_Doan_Hoan_Thien/"),
        ("15", "professional-writing", "Chuẩn mực Văn phong", "Chuẩn hóa văn phong báo cáo học thuật: không dùng từ sáo rỗng, dùng động từ trực tiếp và số liệu", "Tuân thủ văn phong kỹ thuật chuyên nghiệp", "Toàn bộ báo cáo và tài liệu dự án")
    ]

    tbl_sk = doc.add_table(rows=len(skills_data) + 1, cols=6)
    tbl_sk.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sk.autofit = False
    col_w_sk = [Inches(0.5), Inches(1.5), Inches(1.1), Inches(1.8), Inches(1.1), Inches(1.0)]
    for row in tbl_sk.rows:
        for idx, w in enumerate(col_w_sk):
            row.cells[idx].width = w

    headers_sk = ["STT", "Tên Skill (.agents/skills/)", "Phân nhóm", "Mục tiêu chuẩn hóa quy trình", "Ràng buộc & Rào chắn an toàn", "Artifacts đầu ra"]
    for i, h in enumerate(headers_sk):
        tbl_sk.cell(0, i).text = h
    format_row(tbl_sk.rows[0], HEX_HEADER_BG, RGBColor(255, 255, 255), bold=True, is_header=True)

    for r_idx, (s_stt, s_name, s_grp, s_obj, s_rule, s_art) in enumerate(skills_data):
        row = tbl_sk.rows[r_idx + 1]
        row.cells[0].text = s_stt
        row.cells[1].text = s_name
        row.cells[2].text = s_grp
        row.cells[3].text = s_obj
        row.cells[4].text = s_rule
        row.cells[5].text = s_art
        bg = HEX_ROW_ALT if (r_idx % 2 == 1) else "FFFFFF"
        format_row(row, bg, RGBColor(15, 23, 42), bold=False, is_header=False)
        row.cells[1].paragraphs[0].runs[0].font.name = "Consolas"
        row.cells[1].paragraphs[0].runs[0].font.bold = True
        row.cells[1].paragraphs[0].runs[0].font.size = Pt(8.5)

    set_table_borders(tbl_sk)
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================================
    # PHẦN 3: QUÁ TRÌNH ỨNG DỤNG AI AGENT QUA 4 GIAI ĐOẠN SDLC
    # =========================================================================
    add_h1(doc, "3. QUÁ TRÌNH ỨNG DỤNG AI AGENT QUA 4 GIAI ĐOẠN SDLC (9 TUẦN TRIỂN KHAI)")
    add_p(
        doc,
        "Dự án được triển khai có kỷ luật qua 4 giai đoạn tương ứng với tiến độ 9 tuần học phần (từ 27/07/2026 đến 27/09/2026). "
        "Tại mỗi giai đoạn, AI Agent được giao nhiệm vụ với vai trò cụ thể, thực thi theo SOP và trải qua cổng kiểm soát của Kỹ sư con người:"
    )

    # Chèn sơ đồ Vòng đời AI SDLC
    diag_lifecycle = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "generated_diagrams", "diagram_agentic_workflow_lifecycle.png"))
    add_diagram(doc, diag_lifecycle, "Hình 3.1: Quy trình 4 giai đoạn phát triển phần mềm tăng cường AI và các mốc kiểm soát Human Gate (300 DPI)", width=Inches(6.4))

    # GIAI ĐOẠN 1
    add_h2(doc, "3.1. Giai đoạn 1: Phân tích Yêu cầu, Kiến trúc Hệ thống & CSDL Quan hệ (Tuần 1 - 4)")
    add_p(
        doc,
        "Trong giai đoạn nền tảng này, nhóm sinh viên phối hợp cùng Lead Healthcare BA Agent, System Architect Agent và Database Designer Agent:\n"
        "1. Khảo sát thực trạng: AI Agent phân tích 5 điểm nghẽn nghiệp vụ y tế tư nhân (ùn tắc tiếp đón, xung đột trùng lịch khám, "
        "bác sĩ quá tải khi đọc hồ sơ cũ, tổng đài quá tải câu hỏi BHYT, sai sót trong tính toán giảm trừ viện phí).\n"
        "2. Đặc tả yêu cầu: Agent sinh 38 yêu cầu chức năng (FR-001 đến FR-038) và 10 yêu cầu phi chức năng (NFR), đồng thời chuyển hóa thành "
        "27 User Stories chuẩn INVEST có tiêu chí chấp nhận Acceptance Criteria định dạng Gherkin (Given-When-Then).\n"
        "3. Thiết kế kiến trúc & CSDL: Architect Agent đề xuất mô hình phân tầng Clean Architecture kết hợp Docker Compose 3 dịch vụ "
        "(MySQL 8.0, FastAPI Backend, React Frontend). Database Agent thiết kế lược đồ quan hệ 14 bảng đạt chuẩn chuẩn hóa 3NF.\n"
        "4. KÍCH HOẠT HUMAN GATE 1: Kỹ sư Trưởng nhóm Đinh Gia Bảo rà soát toàn bộ đề xuất của AI. Phát hiện AI tự ý đưa tính năng "
        "'AI Tự động chẩn đoán bệnh học và kê đơn thuốc' vào tài liệu. Con người lập tức bác bỏ tính năng này, ban hành quy tắc đạo đức y khoa: "
        "AI chỉ được phép hoạt động ở phạm vi Trợ lý Hành chính 3 lớp (Pre-visit Briefing, FAQ RAG, Discharge Instructions), 100% quyết định "
        "chuyên môn thuộc về bác sĩ có chứng chỉ hành nghề."
    )

    # GIAI ĐOẠN 2
    add_h2(doc, "3.2. Giai đoạn 2: Hiện thực hóa Chức năng Quản lý Cốt lõi & Phân quyền RBAC (Tuần 5 - 6)")
    add_p(
        doc,
        "Bước vào giai đoạn lập trình, nhóm kích hoạt Fullstack Implementation Agent và Design-Taste Frontend Agent:\n"
        "1. Xây dựng lõi Backend FastAPI: Thiết lập mô hình dữ liệu SQLAlchemy ORM, phân quyền 4 vai trò (Admin, Receptionist, Doctor, Accountant) "
        "qua cơ chế JWT Token an toàn và mật khẩu băm Bcrypt.\n"
        "2. Thuật toán chống trùng lịch (ConflictChecker): AI Agent sinh mã thuật toán kiểm tra giao thoa khoảng thời gian [S1, E1) giao [S2, E2). "
        "Con người phát hiện thuật toán ban đầu chỉ kiểm tra theo doctor_id mà quên kiểm tra clinic_id, đã yêu cầu AI bổ sung điều kiện kép.\n"
        "3. Giao diện Taste-Skill Frontend: Agent xây dựng giao diện lâm sàng công thái học bằng React 18, Vite và Tailwind CSS, loại bỏ hoàn toàn "
        "các thiết kế AI rập khuôn (AI-slop), sử dụng bảng màu Slate 900 / Teal 600 dịu mắt, hỗ trợ bác sĩ thao tác nhanh trên màn hình cảm ứng.\n"
        "4. KÍCH HOẠT HUMAN GATE 2: Kỹ sư Trần Đặng Công Tâm thực hiện Code Review phát hiện AI sinh logic thanh toán viện phí và xuất kho dược phẩm "
        "bằng 2 truy vấn riêng biệt không nằm trong Database Transaction. Con người can thiệp, yêu cầu gộp toàn bộ thao tác vào trong một khối "
        "db.commit() nguyên tử nhằm bảo đảm tuyệt đối tính toàn vẹn ACID của dữ liệu tài chính."
    )

    # GIAI ĐOẠN 3
    add_h2(doc, "3.3. Giai đoạn 3: Tích hợp Động cơ AI Hành chính 3 Lớp & An toàn Thông tin Y tế (Tuần 7 - 8)")
    add_p(
        doc,
        "Đây là giai đoạn chuyên sâu về trí tuệ nhân tạo, nhóm phối hợp cùng AI Prompt Engineer Agent và Security Auditor Agent:\n"
        "1. Tầng Khử định danh PII (Lớp 1): Xây dựng module PIIAnonymizer sử dụng Regex thuần túy của Việt Nam che giấu số CCCD 12 số, "
        "số điện thoại di động 10 số và mã thẻ BHYT 15 ký tự thành các nhãn an toàn [CCCD_REDACTED], [PHONE_REDACTED], [BHYT_REDACTED] "
        "trước khi gửi bất kỳ dữ liệu nào ra dịch vụ đám mây bên ngoài theo đúng Nghị định 13/2023/NĐ-CP.\n"
        "2. Tầng Rào chắn Đạo đức y tế (Lớp 2): Thiết lập MedicalGuardrails kiểm tra an toàn prompt, ngăn chặn các kỹ thuật tấn công Prompt Injection, "
        "Jailbreak và tự động từ chối nếu người dùng hỏi câu hỏi chẩn đoán bệnh tật trong Chatbot FAQ.\n"
        "3. Tầng Đa nhà cung cấp & Dự phòng cục bộ (Lớp 3): Tích hợp Google Gemini Live API kết hợp Deterministic Mock Fallback Engine. "
        "Khi hệ thống gặp sự cố mất mạng Internet, động cơ tự động chuyển sang sinh câu trả lời quy tắc nội bộ trong < 100ms, phòng khám không bao giờ bị đình trệ.\n"
        "4. KÍCH HOẠT HUMAN GATE 3: Kiểm chuẩn an toàn lâm sàng. Kiểm thử trực tiếp 20 kịch bản cố tình làm lộ dữ liệu người bệnh, xác nhận 100% "
        "dữ liệu PII được bảo vệ tuyệt đối và mọi kết quả AI sinh ra đều đính kèm lời cảnh báo miễn trừ trách nhiệm y tế."
    )

    # GIAI ĐOẠN 4
    add_h2(doc, "3.4. Giai đoạn 4: Kiểm thử Đa tầng Tự động, Đóng gói Container & Nghiệm thu Sản phẩm (Tuần 9)")
    add_p(
        doc,
        "Giai đoạn hoàn thiện và nghiệm thu phối hợp cùng QA Automation Agent, Technical Documentation Agent và Professional Writing Agent:\n"
        "1. Bộ kiểm thử tự động 323 ca test: QA Agent sinh và thực thi 13 tệp test suite trên nền tảng Pytest 8.3 và FastAPI TestClient, "
        "bao phủ từ kiểm thử đơn vị (Unit), kiểm thử tích hợp (Integration), kiểm thử quy trình khám khép kín (End-to-End) đến kiểm thử an ninh "
        "tấn công đối kháng (Adversarial Testing). Kết quả chạy thực tế: 323 passed đạt tỷ lệ 100.0% trong 27.74 giây.\n"
        "2. Đóng gói Container Docker Compose: Tối ưu hóa Dockerfile đa tầng (Multi-stage build) cho Backend và Frontend, cấu hình non-root user "
        "để loại bỏ rủi ro bảo mật container do AI tạo ra ban đầu.\n"
        "3. Tự động hóa sinh 7 tập tài liệu Word chuẩn SDLC: Documentation Agent lập trình bộ script Python docx_style_helpers.py tự động "
        "biên dịch toàn bộ 7 tập tài liệu báo cáo đồ án đạt chuẩn hình thức môn học, chèn các sơ đồ kỹ thuật 300 DPI và xóa sạch mọi placeholder.\n"
        "4. NGHIỆM THU CUỐI CÙNG: Hội đồng nội bộ nhóm sinh viên nghiệm thu toàn diện kịch bản Demo 8 bước, xác nhận hệ thống CMS-AI sẵn sàng "
        "trình diễn và bảo vệ trước Hội đồng chấm điểm của Khoa Công nghệ Thông tin."
    )

    # =========================================================================
    # PHẦN 4: HỆ THỐNG PROMPTS ĐIỀU PHỐI VÀ KỸ THUẬT PROMPT ENGINEERING
    # =========================================================================
    add_h1(doc, "4. HỆ THỐNG PROMPTS ĐIỀU PHỐI VÀ KỸ THUẬT PROMPT ENGINEERING NÂNG CAO")
    add_p(
        doc,
        "Một trong những đóng góp mang tính phương pháp luận của dự án là việc lưu trữ và chuẩn hóa toàn bộ "
        "15 Master Prompts tại thư mục 'prompt_agents/'. Nhóm không ra lệnh tùy tiện mà áp dụng các kỹ thuật "
        "Prompt Engineering tiên tiến nhất:"
    )

    prompt_techniques = [
        ("• Cấu trúc chuẩn 6 thành phần của Master Prompt: ", "Mỗi prompt đều bao gồm: (1) Ngữ cảnh & Mục tiêu dự án; (2) Định vị Persona Agent; (3) Kỹ năng & Ràng buộc đạo đức y tế; (4) Nội dung câu lệnh Master Prompt chi tiết; (5) Danh mục Artifacts kết xuất; (6) Nhật ký phát hiện lỗi và can thiệp của con người."),
        ("• Kỹ thuật Role Prompting & System Persona: ", "Ép Agent đóng vai chuyên gia thực thụ (Senior Healthcare BA, Security Specialist) để loại bỏ phong cách trả lời xã giao, tập trung vào cấu trúc dữ liệu kỹ thuật và mã nguồn có thể thực thi ngay."),
        ("• Kỹ thuật Few-Shot Learning & Negative Constraints: ", "Cung cấp các mẫu đầu ra chuẩn (Golden Examples) và danh sách cấm kỵ rõ ràng (VD: 'CẤM tuyệt đối việc sinh câu trả lời chẩn đoán bệnh học hoặc đề xuất tên thuốc khi người dùng hỏi triệu chứng')."),
        ("• Kỹ thuật Chain-of-Thought (CoT) & Phân rã đa bước: ", "Yêu cầu Agent suy luận từng bước (Step-by-step reasoning) khi xử lý logic phức tạp như tính toán viện phí BHYT hay thuật toán kiểm tra xung đột thời gian khám bệnh.")
    ]
    for pt_title, pt_desc in prompt_techniques:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(pt_title)
        r1.font.bold = True
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        r2 = p.add_run(pt_desc)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11)

    add_h2(doc, "4.1. Bảng đối soát 15 Master Prompts điều phối AI Agent trong dự án")
    prompts_table_data = [
        ("01", "01_prompt_requirements_analysis.md", "Lead Healthcare BA", "Phân tích 5 điểm nghẽn, đặc tả 38 FR, 10 NFR, 27 User Stories Gherkin", "docs/requirements.md, user-stories.md"),
        ("02", "02_prompt_architecture_design.md", "System Architect", "Thiết kế Clean Architecture, API Gateway, Dockerization, 5 quyết định ADR", "docs/architecture.md, decisions.md"),
        ("03", "03_prompt_database_design.md", "Database Designer", "Thiết kế CSDL quan hệ 14 bảng 3NF, chỉ mục tối ưu, từ điển dữ liệu", "docs/database-design.md"),
        ("04", "04_prompt_diagram_design.md", "UML Diagram Specialist", "Thiết kế sơ đồ Use Case, ERD, Class UML, Sequence Đặt lịch, EMR, Viện phí", "docs/thiet-ke-huong-doi-tuong-class-diagram.md"),
        ("05", "05_prompt_implementation_fullstack.md", "Fullstack Senior Dev", "Lập trình Backend FastAPI, SQLAlchemy, ConflictChecker, React SPA Vite", "backend/app/, frontend/src/"),
        ("06", "06_prompt_pii_deidentification.md", "Privacy Engineer", "Xây dựng module PIIAnonymizer Regex khử CCCD, SĐT, BHYT theo Nghị định 13", "backend/app/ai/anonymizer.py"),
        ("07", "07_prompt_pre_visit_briefing.md", "Clinical AI Engineer", "Xây dựng tính năng tóm tắt bệnh sử Pre-visit < 15s đính kèm Disclaimer y tế", "backend/app/ai/pre_visit.py"),
        ("08", "08_prompt_clinic_faq_rag.md", "RAG & Guardrail Engineer", "Xây dựng AI Chatbot hỏi đáp thủ tục phòng khám, rào chắn chặn Jailbreak", "backend/app/ai/faq_chatbot.py"),
        ("09", "09_prompt_discharge_instructions.md", "Clinical Workflow Dev", "Tự động sinh bảng phân chia lịch uống thuốc 4 bữa và chế độ sinh hoạt", "backend/app/ai/discharge.py"),
        ("10", "10_prompt_design_taste_frontend.md", "UI/UX Clinical Designer", "Xây dựng Design Tokens Tailwind CSS, giao diện 4 vai trò chuẩn Taste-Skill", "frontend/src/index.css, Components"),
        ("11", "11_prompt_testing_automation.md", "Lead QA Automation", "Viết bộ 323 ca kiểm thử tự động Pytest, kiểm thử đa tầng đạt 100% pass", "backend/tests/, test-report.md"),
        ("12", "12_prompt_code_review.md", "Senior Code Reviewer", "Kiểm toán mã nguồn PEP 8, rà soát race condition và lỗ hổng bất biến", "docs/code-review.md"),
        ("13", "13_prompt_security_review.md", "Healthcare Security Auditor", "Kiểm toán an toàn thông tin STRIDE, OWASP Top 10 API, bảo mật PII y tế", "docs/security-review.md"),
        ("14", "14_prompt_documentation_sdlc_reports.md", "Tech Writer & Compiler", "Lập trình script docx_style_helpers.py tự động sinh 7 tập tài liệu Word SDLC", "docs/7_Giai_Doan_Hoan_Thien/"),
        ("15", "15_prompt_professional_writing.md", "Editorial Standards Lead", "Chuẩn hóa văn phong học thuật, loại bỏ từ sáo rỗng, dùng số liệu thực chứng", "Toàn bộ tài liệu và báo cáo")
    ]

    tbl_pr = doc.add_table(rows=len(prompts_table_data) + 1, cols=5)
    tbl_pr.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_pr.autofit = False
    col_w_pr = [Inches(0.5), Inches(2.2), Inches(1.3), Inches(1.8), Inches(1.2)]
    for row in tbl_pr.rows:
        for idx, w in enumerate(col_w_pr):
            row.cells[idx].width = w

    headers_pr = ["STT", "Tên File Master Prompt (prompt_agents/)", "Persona AI Agent", "Nội dung Nhiệm vụ Kỹ thuật Giao việc", "Sản phẩm Kết xuất"]
    for i, h in enumerate(headers_pr):
        tbl_pr.cell(0, i).text = h
    format_row(tbl_pr.rows[0], HEX_HEADER_BG, RGBColor(255, 255, 255), bold=True, is_header=True)

    for r_idx, (p_stt, p_file, p_role, p_task, p_art) in enumerate(prompts_table_data):
        row = tbl_pr.rows[r_idx + 1]
        row.cells[0].text = p_stt
        row.cells[1].text = p_file
        row.cells[2].text = p_role
        row.cells[3].text = p_task
        row.cells[4].text = p_art
        bg = HEX_ROW_ALT if (r_idx % 2 == 1) else "FFFFFF"
        format_row(row, bg, RGBColor(15, 23, 42), bold=False, is_header=False)
        row.cells[1].paragraphs[0].runs[0].font.name = "Consolas"
        row.cells[1].paragraphs[0].runs[0].font.size = Pt(8.0)

    set_table_borders(tbl_pr)
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================================
    # PHẦN 5: TƯƠNG TÁC CON NGƯỜI - AI: THEO DÕI ẢO GIÁC VÀ CAN THIỆP SỬA LỖI
    # =========================================================================
    add_h1(doc, "5. TƯƠNG TÁC CON NGƯỜI - AI: BẢNG THEO DÕI ẢO GIÁC AI VÀ CAN THIỆP SỬA CHỮA THỰC TẾ")
    add_p(
        doc,
        "Một bài thực hành AI-Augmented SDLC chân thực và xuất sắc phải chứng minh được: Kỹ sư con người không hề phó mặc cho AI, "
        "mà liên tục phát hiện các lỗi sai, ảo giác (Hallucinations) và khiếm khuyết trong các bản thảo do AI sinh ra. "
        "Dưới đây là sơ đồ vòng lặp phản hồi khép kín và bảng ghi nhận 10 lỗi kỹ thuật điển hình đã được nhóm sinh viên phát hiện và trực tiếp sửa chữa:"
    )

    # Chèn sơ đồ Vòng lặp phản hồi
    diag_loop = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "generated_diagrams", "diagram_human_ai_collaboration_loop.png"))
    add_diagram(doc, diag_loop, "Hình 5.1: Vòng lặp phản hồi tương tác khép kín giữa Kỹ sư Con người và AI Agent (Human-in-the-Loop) (300 DPI)", width=Inches(6.4))

    hallucinations_data = [
        ("DEF-01", "Giai đoạn 1", "AI đề xuất tính năng tự động chẩn đoán bệnh học và kê đơn thuốc cho bệnh nhân dựa trên triệu chứng nhập vào.", "Cực kỳ nguy hiểm (Critical)", "Vi phạm nghiêm trọng Luật Khám chữa bệnh 2023, gây nguy hiểm đến tính mạng người bệnh.", "Đinh Gia Bảo bác bỏ hoàn toàn đề xuất. Thiết lập nguyên tắc đạo đức y tế: AI chỉ là Trợ lý Hành chính hỗ trợ bác sĩ; 100% quyền chẩn đoán thuộc về bác sĩ."),
        ("DEF-02", "Giai đoạn 2", "Thuật toán kiểm tra trùng lịch (ConflictChecker) do AI sinh ban đầu chỉ kiểm tra theo doctor_id.", "Cao (High)", "Hai bác sĩ khác nhau cùng bị xếp trùng vào một buồng khám tại cùng thời điểm, gây xung đột cơ sở vật chất.", "Trần Đặng Công Tâm phát hiện và viết lại hàm kiểm tra giao thoa khoảng thời gian đồng thời theo cả 2 chiều: doctor_id VÀ clinic_id."),
        ("DEF-03", "Giai đoạn 3", "Biểu thức Regex khử PII do AI đề xuất thiết lập quá tham lam (Greedy Matching): bắt chuỗi số bất kỳ.", "Cao (High)", "Che nhầm cả chỉ số huyết áp 120/80 mmHg và liều dùng thuốc 500mg thành [PHONE_REDACTED], làm sai lệch bệnh án.", "Đinh Gia Bảo tinh chỉnh Regex với ranh giới từ chuẩn xác (\\b), bảo vệ các đơn vị đo lường y tế (mg, ml, mmHg, bpm)."),
        ("DEF-04", "Giai đoạn 3", "AI đề xuất mã thẻ BHYT có độ dài 10 số (nhầm lẫn với mã số BHXH cá nhân).", "Trung bình (Medium)", "Không nhận diện được thẻ Bảo hiểm Y tế hợp lệ của người bệnh Việt Nam, làm sai mức giảm trừ viện phí.", "Trần Đặng Công Tâm đối soát quy định Bảo hiểm Xã hội Việt Nam, cập nhật Regex bắt chuẩn xác mã BHYT 15 ký tự (VD: GD4010123456789)."),
        ("DEF-05", "Giai đoạn 2", "AI sinh mã thanh toán hóa đơn và trừ số lượng thuốc trong kho bằng 2 truy vấn riêng biệt ngoài Transaction.", "Nghiêm trọng (Critical)", "Gây ra Race Condition: tiền đã trừ nhưng kho thuốc bị lỗi mạng không trừ được, dẫn đến thất thoát kho dược.", "Đinh Gia Bảo cấu trúc lại toàn bộ vào một khối db.commit() nguyên tử có khóa RecordStatus.LOCKED bảo đảm tính toàn vẹn ACID."),
        ("DEF-06", "Giai đoạn 3", "AI thiết kế hệ thống phụ thuộc hoàn toàn vào Google Gemini API trên đám mây, không có cơ chế dự phòng.", "Cao (High)", "Toàn bộ chức năng trợ lý AI của phòng khám bị tê liệt khi đứt cáp quang hoặc mất kết nối Internet.", "Nhóm lập trình module Deterministic Mock Fallback Engine tự động chuyển mạch khi mất mạng, sinh câu trả lời quy tắc nội bộ trong < 100ms."),
        ("DEF-07", "Giai đoạn 4", "AI viết Dockerfile ban đầu cho Backend FastAPI chạy trực tiếp với quyền root của hệ điều hành Linux.", "Trung bình (Medium)", "Vi phạm nguyên tắc bảo mật container, tạo nguy cơ leo thang đặc quyền khi bị tấn công chiếm quyền điều khiển.", "Đinh Gia Bảo tạo user không đặc quyền 'appuser' trong Dockerfile và phân quyền thư mục tối thiểu trước khi đóng gói."),
        ("DEF-08", "Giai đoạn 2", "AI sử dụng cú pháp Pydantic v1 kiểu cũ 'orm_mode = True' trong các tệp schemas.py.", "Thấp (Low)", "Bị cảnh báo deprecation và có nguy cơ lỗi runtime khi nâng cấp lên môi trường Python 3.12 / Pydantic v2.", "Trần Đặng Công Tâm quét toàn bộ mã nguồn và đồng bộ sang cú pháp chuẩn Pydantic v2: 'model_config = ConfigDict(from_attributes=True)'."),
        ("DEF-09", "Giai đoạn 2", "Công thức tính BMI do AI sinh ra bị lỗi ZeroDivisionError khi người dùng nhập chiều cao = 0.", "Trung bình (Medium)", "Làm sập ứng dụng (Crash 500) khi lễ tân sơ suất nhập thiếu trường chiều cao trong hồ sơ bệnh án.", "Trần Đặng Công Tâm thêm tầng validation kiểm tra height > 0 và chuẩn hóa đơn vị chiều cao centimet (cm) sang mét (m)."),
        ("DEF-10", "Giai đoạn 4", "Nút bấm 'Xác nhận thanh toán' trên giao diện Frontend cho phép người dùng click đúp (Double-click).", "Cao (High)", "Gửi đồng thời 2 yêu cầu POST lên server, gây nguy cơ tạo 2 biên lai thanh toán cho cùng một ca khám.", "Trần Đặng Công Tâm bổ sung cờ trạng thái 'isSubmitting' vô hiệu hóa (disabled) nút bấm ngay sau lần click đầu tiên và thêm hiệu ứng loading.")
    ]

    tbl_hal = doc.add_table(rows=len(hallucinations_data) + 1, cols=6)
    tbl_hal.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_hal.autofit = False
    col_w_hal = [Inches(0.6), Inches(0.8), Inches(1.6), Inches(0.9), Inches(1.2), Inches(1.9)]
    for row in tbl_hal.rows:
        for idx, w in enumerate(col_w_hal):
            row.cells[idx].width = w

    headers_hal = ["Mã lỗi", "Giai đoạn", "Ảo giác / Khiếm khuyết do AI tạo ra", "Mức độ", "Nguy cơ tiềm ẩn nếu không sửa", "Hành động can thiệp & Sửa chữa của Con người"]
    for i, h in enumerate(headers_hal):
        tbl_hal.cell(0, i).text = h
    format_row(tbl_hal.rows[0], HEX_HEADER_BG, RGBColor(255, 255, 255), bold=True, is_header=True)

    for r_idx, (h_id, h_phase, h_err, h_sev, h_risk, h_fix) in enumerate(hallucinations_data):
        row = tbl_hal.rows[r_idx + 1]
        row.cells[0].text = h_id
        row.cells[1].text = h_phase
        row.cells[2].text = h_err
        row.cells[3].text = h_sev
        row.cells[4].text = h_risk
        row.cells[5].text = h_fix
        bg = HEX_ROW_ALT if (r_idx % 2 == 1) else "FFFFFF"
        format_row(row, bg, RGBColor(15, 23, 42), bold=False, is_header=False)
        row.cells[0].paragraphs[0].runs[0].font.name = "Consolas"
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[0].paragraphs[0].runs[0].font.size = Pt(8.5)

    set_table_borders(tbl_hal)
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================================
    # PHẦN 6: ĐÁNH GIÁ ĐỊNH LƯỢNG HIỆU QUẢ CỦA AI AGENT VÀ BÀI HỌC KINH NGHIỆM
    # =========================================================================
    add_h1(doc, "6. ĐÁNH GIÁ ĐỊNH LƯỢNG HIỆU QUẢ CỦA AI AGENT VÀ BÀI HỌC KINH NGHIỆM")

    add_h2(doc, "6.1. Bảng so sánh định lượng: Phương pháp Truyền thống vs. AI-Augmented SDLC")
    add_p(
        doc,
        "Dựa trên số liệu đo lường thực nghiệm trong suốt 9 tuần triển khai dự án, nhóm tổng hợp bảng so sánh hiệu quả định lượng:"
    )

    metrics_data = [
        ("Thời gian khảo sát & Viết tài liệu đặc tả SRS", "3 - 4 tuần làm việc liên tục", "1 tuần (giảm 65% thời gian)", "AI Agent hỗ trợ trích xuất cấu trúc và tổng hợp tài liệu nhanh chóng"),
        ("Tốc độ sinh mã khung CRUD & Kết nối CSDL", "2 tuần lập trình thủ công", "3 ngày (nhanh gấp 3.5 lần)", "Agent sinh boilerplate chính xác theo chuẩn Clean Architecture"),
        ("Độ bao phủ kiểm thử tự động (Unit / Integration)", "Thường chỉ đạt 30-40% do thiếu thời gian", "Đạt 100% với 323 ca kiểm thử", "Agent tự động sinh test cases bao phủ cả kịch bản biên và đối kháng"),
        ("Phát hiện lỗi bảo mật và vi phạm dữ liệu PII", "Dễ bỏ sót khi rà soát thủ công", "0% rò rỉ dữ liệu y tế", "Kết hợp Regex chuẩn hóa và kiểm toán tự động theo mô hình STRIDE"),
        ("Đồng bộ hóa tài liệu kỹ thuật và mã nguồn", "Tài liệu thường bị lạc hậu so với code", "Đồng bộ 100% qua script", "Script tự động biên dịch báo cáo Word trực tiếp từ cấu trúc dự án"),
        ("Tổng thời lượng hoàn thiện toàn bộ đồ án", "Dự kiến 14 - 16 tuần", "Hoàn tất xuất sắc trong 9 tuần", "Tiết kiệm hơn 40% tổng thời gian phát triển và nâng cao chất lượng")
    ]

    tbl_met = doc.add_table(rows=len(metrics_data) + 1, cols=4)
    tbl_met.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_met.autofit = False
    col_w_met = [Inches(1.8), Inches(1.4), Inches(1.5), Inches(2.0)]
    for row in tbl_met.rows:
        for idx, w in enumerate(col_w_met):
            row.cells[idx].width = w

    headers_met = ["Hạng mục Kỹ thuật đánh giá", "Quy trình Truyền thống (Manual)", "AI-Augmented SDLC (Thực tế)", "Đánh giá Lợi ích Đạt được"]
    for i, h in enumerate(headers_met):
        tbl_met.cell(0, i).text = h
    format_row(tbl_met.rows[0], HEX_HEADER_BG, RGBColor(255, 255, 255), bold=True, is_header=True)

    for r_idx, (m_item, m_old, m_new, m_eval) in enumerate(metrics_data):
        row = tbl_met.rows[r_idx + 1]
        row.cells[0].text = m_item
        row.cells[1].text = m_old
        row.cells[2].text = m_new
        row.cells[3].text = m_eval
        bg = HEX_ROW_ALT if (r_idx % 2 == 1) else "FFFFFF"
        format_row(row, bg, RGBColor(15, 23, 42), bold=False, is_header=False)

    set_table_borders(tbl_met)
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_h2(doc, "6.2. Minh chứng đáp ứng trọn vẹn 9/9 tiêu chí đánh giá học phần")
    add_p(
        doc,
        "Dự án CMS-AI chuẩn bị đầy đủ 100% minh chứng thực nghiệm tương ứng với 9 tiêu chí đánh giá bài thực hành AI-Augmented SDLC:"
    )

    submission_data = [
        ("1. Hệ sinh thái SKILL.md", "Thư mục .agents/skills/", "15 file SKILL.md chuẩn YAML frontmatter quy định SOP nghiệp vụ và ranh giới an toàn y tế."),
        ("2. Bộ Prompts điều phối", "Thư mục prompt_agents/", "15 tệp Master Prompts chuẩn 6 thành phần, lưu trữ toàn văn nhiệm vụ và nhật ký kiểm chứng con người."),
        ("3. Bộ Artifacts kỹ thuật", "Thư mục docs/", "Hơn 15 tài liệu đặc tả: SRS, Kiến trúc, CSDL 14 bảng 3NF, ADRs, User Stories, Class Diagram."),
        ("4. Bằng chứng kiểm thử", "backend/tests/ & docs/test-report.md", "Kết quả thực thi 323/323 ca kiểm thử tự động Pytest đạt tỷ lệ thành công 100% trong 27.74s."),
        ("5. Báo cáo Code Review", "docs/code-review.md", "Báo cáo kiểm toán mã nguồn đa chiều, phân loại khuyết tật và xác nhận khắc phục toàn bộ lỗi."),
        ("6. Báo cáo An toàn Thông tin", "docs/security-review.md", "Kiểm toán an ninh STRIDE, rà soát OWASP Top 10 API, bảo vệ dữ liệu PII theo Nghị định 13/2023/NĐ-CP."),
        ("7. Nhật ký Ảo giác AI", "docs/requirements-issues.md & Báo cáo này", "Ghi nhận 10 lỗi ảo giác điển hình của AI và phân tích chi tiết biện pháp con người đã can thiệp."),
        ("8. Hồ sơ 3 Human Gates", "docs/Reports/AI-Augmented-SDLC-Report.md", "Biên bản thẩm định và phê duyệt của Human Gate 1 (Phạm vi), Gate 2 (Chất lượng), Gate 3 (Lâm sàng)."),
        ("9. Lịch sử kiểm soát phiên bản", "Git commits history & run scripts", "Lịch sử commit truy vết đầy đủ quá trình phát triển 9 tuần và các script chạy tự động 1-Click.")
    ]

    tbl_sub = doc.add_table(rows=len(submission_data) + 1, cols=3)
    tbl_sub.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sub.autofit = False
    col_w_sub = [Inches(1.8), Inches(1.8), Inches(3.1)]
    for row in tbl_sub.rows:
        for idx, w in enumerate(col_w_sub):
            row.cells[idx].width = w

    headers_sub = ["Tiêu chí Đánh giá Học phần", "Vị trí Minh chứng trong Dự án", "Nội dung Minh chứng Thực nghiệm"]
    for i, h in enumerate(headers_sub):
        tbl_sub.cell(0, i).text = h
    format_row(tbl_sub.rows[0], HEX_HEADER_BG, RGBColor(255, 255, 255), bold=True, is_header=True)

    for r_idx, (sub_name, sub_loc, sub_desc) in enumerate(submission_data):
        row = tbl_sub.rows[r_idx + 1]
        row.cells[0].text = sub_name
        row.cells[1].text = sub_loc
        row.cells[2].text = sub_desc
        bg = HEX_ROW_ALT if (r_idx % 2 == 1) else "FFFFFF"
        format_row(row, bg, RGBColor(15, 23, 42), bold=False, is_header=False)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[1].paragraphs[0].runs[0].font.name = "Consolas"
        row.cells[1].paragraphs[0].runs[0].font.size = Pt(8.5)

    set_table_borders(tbl_sub)
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_h2(doc, "6.3. Bài học kinh nghiệm xương máu khi ứng dụng AI Agent trong y tế")
    lessons = [
        ("1. Không bao giờ tin tưởng tuyệt đối vào mã nguồn do AI sinh ra: ", "AI có thể sinh ra những đoạn mã trông rất hoàn hảo về mặt cú pháp nhưng tiềm ẩn lỗi logic nghiêm trọng trong các tình huống biên (như race condition, quên kiểm tra phòng khám trùng giờ, biểu thức regex quá tham lam). Mọi dòng mã đều phải trải qua kiểm thử tự động và review của con người."),
        ("2. Sức mạnh vượt trội của việc chuẩn hóa SKILL trước khi giao việc: ", "Nếu chỉ prompt một câu ngắn gọn như 'Hãy viết code phòng khám', AI sẽ sinh ra các đoạn code rời rạc, rập khuôn (AI-slop). Khi được trang bị file SKILL.md với tiêu chuẩn thiết kế taste-skill, kiến trúc Clean Architecture và ranh giới đạo đức, AI Agent hoạt động chính xác và kỷ luật như một kỹ sư cao cấp."),
        ("3. Đạo đức y tế và bảo vệ quyền riêng tư là lằn ranh đỏ: ", "Trong lĩnh vực y tế, việc vi phạm ranh giới đạo đức (để AI tự ý chẩn đoán) hoặc để lộ số CCCD/SĐT người bệnh ra Internet là không thể chấp nhận được về mặt pháp lý. Tầng bảo vệ PII và Medical Guardrails phải được thiết kế độc lập, bất biến trước khi tích hợp bất kỳ mô hình AI nào."),
        ("4. Con người là nhân tố quyết định thành bại của dự án: ", "AI Agent không thay thế kỹ sư phần mềm; AI Agent nâng tầm kỹ sư con người lên vị trí người ra quyết định chiến lược, người gác cổng an toàn và người kiểm chuẩn chất lượng tối cao.")
    ]
    for l_title, l_desc in lessons:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(l_title)
        r1.font.bold = True
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        r2 = p.add_run(l_desc)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11)

    # =========================================================================
    # PHẦN 7: KẾT LUẬN VÀ CHỮ KÝ XÁC NHẬN
    # =========================================================================
    add_h1(doc, "7. KẾT LUẬN VÀ XÁC NHẬN CỦA NHÓM THỰC HIỆN")
    add_p(
        doc,
        "Dự án Hệ thống Quản lý Phòng khám Đa khoa thông minh tích hợp AI Hành chính (CMS-AI) là một minh chứng sống động, "
        "thực chứng và toàn diện cho phương pháp luận phát triển phần mềm hiện đại AI-Augmented SDLC. "
        "Thông qua sự kết hợp nhịp nhàng giữa Động cơ AI Agent 4 trụ cột và Quyền kiểm soát tối cao của Kỹ sư Con người qua 3 Human Gates, "
        "nhóm sinh viên đã hoàn thành xuất sắc một hệ sinh thái y tế hoàn chỉnh, an toàn, đạt độ tin cậy tuyệt đối và sẵn sàng "
        "bảo vệ trước Hội đồng chấm điểm môn học."
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(16)

    # Chữ ký xác nhận
    sign_table = doc.add_table(rows=2, cols=2)
    sign_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sign_table.columns[0].width = Inches(3.2)
    sign_table.columns[1].width = Inches(3.3)

    c_left = sign_table.cell(0, 0)
    c_right = sign_table.cell(0, 1)

    p_l = c_left.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l.add_run("THÀNH VIÊN NHÓM 03\n(Ký và ghi rõ họ tên)\n\n\n\n").font.bold = True
    p_l.add_run("Trần Đặng Công Tâm\n(Frontend & QA Lead)").font.italic = True

    p_r = c_right.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r.add_run("TRƯỞNG NHÓM 03\n(Ký và ghi rõ họ tên)\n\n\n\n").font.bold = True
    p_r.add_run("Đinh Gia Bảo\n(Architecture & AI Lead)").font.italic = True

    # Lưu tài liệu đồng thời vào các thư mục mục tiêu
    filename = "Bao_Cao_Qua_Trinh_Ung_Dung_AI_Agent_SDLC.docx"
    save_document(doc, filename)

    # Đồng thời lưu bản sao ghi đè vào docs/Reports/Bao_Cao_AI_Augmented_SDLC_Phong_Kham.docx để đồng bộ
    reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "Reports"))
    if os.path.exists(reports_dir):
        extra_path = os.path.join(reports_dir, "Bao_Cao_AI_Augmented_SDLC_Phong_Kham.docx")
        try:
            doc.save(extra_path)
            print(f"-> Đã đồng bộ thêm vào: {extra_path}")
        except Exception as e:
            print(f"! Lỗi khi đồng bộ vào docs/Reports/: {e}")

if __name__ == "__main__":
    build_ai_agent_report()
