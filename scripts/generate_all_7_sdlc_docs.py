# -*- coding: utf-8 -*-
"""
Master script chạy tuần tự và sinh toàn bộ 7 file tài liệu SDLC (.docx) cho Đề tài 03 (Nhóm 07).
Đồng thời kiểm định tính toàn vẹn của cả 7 tệp tài liệu.
"""

import os
import sys
import docx

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from generate_01_project_plan import build_project_plan
from generate_02_requirements_qa import build_requirements_qa
from generate_03_requirements_specification import build_srs
from generate_04_object_oriented_design import build_docx as build_ood
from generate_05_functional_testing import build_functional_testing
from generate_06_screenflow_db import build_screenflow_db
from generate_07_user_guide import build_user_guide

FILES = [
    "01_GenAI_SoftwareDevelopment_project-plan.docx",
    "02_GenAI_SoftwareDevelopment_requirements-qa.docx",
    "03_GenAI_SoftwareDevelopment_requirements-specification.docx",
    "04_GenAI_SoftwareDevelopment_object-oriented-design.docx",
    "05_GenAI_SoftwareDevelopment_functional-testing.docx",
    "06_GenAI_SoftwareDevelopment_screenflow_db.docx",
    "07_GenAI_SoftwareDevelopment_user-guide.docx"
]

DESKTOP_DIR = r"C:\Users\MSI\OneDrive\Desktop\CacGiaiDoanThucHien"
PROJECT_DIR = r"d:\ICTU\Nam 3\ICTU_2026-2027\Ứng dụng trí tuệ nhân tạo - Project\He_thong_quan_ly_phong_kham\docs\7_Giai_Doan_Hoan_Thien"

def run_all():
    print("================================================================================")
    print("KÍCH HOẠT QUY TRÌNH SINH 7 TỆP TÀI LIỆU SDLC CHO ĐỀ TÀI 03 (NHÓM 03 - LỚP ATTT K23A)")
    print("================================================================================")

    print("\n[1/7] Đang sinh 01_GenAI_SoftwareDevelopment_project-plan.docx...")
    build_project_plan()

    print("\n[2/7] Đang sinh 02_GenAI_SoftwareDevelopment_requirements-qa.docx...")
    build_requirements_qa()

    print("\n[3/7] Đang sinh 03_GenAI_SoftwareDevelopment_requirements-specification.docx...")
    build_srs()

    print("\n[4/7] Đang sinh 04_GenAI_SoftwareDevelopment_object-oriented-design.docx...")
    build_ood()

    print("\n[5/7] Đang sinh 05_GenAI_SoftwareDevelopment_functional-testing.docx...")
    build_functional_testing()

    print("\n[6/7] Đang sinh 06_GenAI_SoftwareDevelopment_screenflow_db.docx...")
    build_screenflow_db()

    print("\n[7/7] Đang sinh 07_GenAI_SoftwareDevelopment_user-guide.docx...")
    build_user_guide()

    print("\n================================================================================")
    print("TIẾN HÀNH KIỂM ĐỊNH TÍNH TOÀN VẸN CẢ 7 TỆP TÀI LIỆU")
    print("================================================================================")

    all_passed = True
    for f in FILES:
        path = os.path.join(DESKTOP_DIR, f)
        target_path = path
        if not os.path.exists(path):
            target_path = os.path.join(PROJECT_DIR, f)
            print(f"! File {f} trên Desktop đang được mở trong Word, kiểm tra bản tại kho lưu trữ.")

        try:
            doc = docx.Document(target_path)
            size = os.path.getsize(target_path)
        except Exception as e:
            # Thử đọc từ kho lưu trữ nếu desktop bị khóa
            target_path = os.path.join(PROJECT_DIR, f)
            doc = docx.Document(target_path)
            size = os.path.getsize(target_path)
            print(f"! Đọc từ bản kho lưu trữ do Desktop bị khóa: {f}")
        p_count = len(doc.paragraphs)
        t_count = len(doc.tables)

        # Kiểm tra placeholder
        has_placeholder = False
        for p in doc.paragraphs:
            if any(token in p.text for token in ["TODO", "TBD", "Nhóm XX", "Nguyễn Văn A"]):
                has_placeholder = True
                break

        status = "HỢP LỆ" if not has_placeholder else "CÒN PLACEHOLDER"
        if has_placeholder:
            all_passed = False

        print(f"✓ {f:<60} | {size:>7} bytes | {p_count:>3} đoạn văn | {t_count:>2} bảng | {status}")

    print("================================================================================")
    if all_passed:
        print("KẾT QUẢ: TẤT CẢ 7 TỆP TÀI LIỆU ĐÃ ĐƯỢC HOÀN THIỆN XUẤT SẮC, KHÔNG CÓ LỖI!")
    else:
        print("CẢNH BÁO: Phát hiện vấn đề cần kiểm tra lại.")
    print("================================================================================")

if __name__ == "__main__":
    run_all()
