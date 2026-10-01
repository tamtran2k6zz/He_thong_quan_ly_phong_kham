# -*- coding: utf-8 -*-
"""
Script sinh file 04_GenAI_SoftwareDevelopment_object-oriented-design.docx
Tài liệu thiết kế hướng đối tượng (Mô hình lớp Class Diagram) cho Hệ thống CMS-AI (Nhóm 07).
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from generate_class_diagram_docx import build_docx

if __name__ == "__main__":
    build_docx()
