"""
Clinic Knowledge Base and Information Retrieval Module.
Provides verified facts, operational policies, BHYT guidelines, pricing,
and workflow instructions for Administrative AI Assistant.
"""

from typing import Dict, Any, List, Optional
import re


CLINIC_INFO = {
    "name": "Phòng khám Đa khoa Quốc tế Smart Clinic",
    "address": "Số 123 Đường Giải Phóng, Quận Đống Đa, TP. Hà Nội",
    "hotline": "1900 6868 - 024 3868 9999",
    "email": "cskh@smartclinic.vn",
    "website": "https://smartclinic.vn",
    "opening_hours": {
        "weekdays": "07:30 - 17:30 (Thứ Hai đến Thứ Bảy)",
        "sunday": "07:30 - 12:00 (Chủ Nhật khám buổi sáng)",
        "emergency": "Cấp cứu 24/7",
        "holidays": "Làm việc theo lịch thông báo ngày Lễ/Tết"
    }
}

FAQ_DATABASE = [
    {
        "id": "faq_hours",
        "category": "Lịch làm việc",
        "keywords": ["giờ", "mấy giờ", "mở cửa", "thời gian", "làm việc", "chủ nhật", "ngày nghỉ", "tiếp đón"],
        "answer": (
            "Phòng khám làm việc từ 07:30 đến 17:30 tất cả các ngày từ Thứ Hai đến Thứ Bảy. "
            "Riêng Chủ Nhật, phòng khám mở cửa làm việc buổi sáng từ 07:30 đến 12:00. "
            "Bộ phận Cấp cứu và hỗ trợ thông tin hoạt động 24/7."
        ),
        "related_links": ["/appointments", "/contact"]
    },
    {
        "id": "faq_bhyt",
        "category": "Bảo hiểm Y tế (BHYT)",
        "keywords": ["bhyt", "bảo hiểm", "bảo hiểm y tế", "thẻ bhyt", "mức hưởng", "thông tuyến", "đúng tuyến", "vssid"],
        "answer": (
            "Phòng khám tiếp nhận thẻ BHYT đúng tuyến và thông tuyến theo quy định hiện hành của Bộ Y tế. "
            "Mức hưởng thanh toán BHYT từ 80% đến 100% tùy theo đối tượng ghi trên thẻ (GD, DN, TE, BT, HT). "
            "Khi đi khám BHYT, Quý khách vui lòng mang theo:\n"
            "1. Thẻ CCCD gắn chip (hoặc ứng dụng định danh điện tử VNeID mức độ 2).\n"
            "2. Thẻ BHYT bản gốc (hoặc hình ảnh thẻ trên ứng dụng VssID).\n"
            "3. Giấy chuyển tuyến (nếu khám vượt tuyến cần hưởng quyền lợi tối đa)."
        ),
        "related_links": ["/insurance-guide", "/patient-registration"]
    },
    {
        "id": "faq_booking",
        "category": "Đặt lịch hẹn",
        "keywords": ["đặt lịch", "hẹn khám", "đăng ký", "book lịch", "lịch hẹn", "đặt trước", "hẹn giờ"],
        "answer": (
            "Quý khách có thể đặt lịch hẹn khám trước qua 3 hình thức thuận tiện:\n"
            "1. Đặt lịch trực tuyến qua Cổng thông tin / Ứng dụng Smart Clinic.\n"
            "2. Gọi điện thoại trực tiếp đến Tổng đài Chăm sóc khách hàng: 1900 6868 hoặc 024 3868 9999.\n"
            "3. Đăng ký tại Quầy Tiếp đón Lễ tân khi đến phòng khám.\n"
            "Khuyến khích Quý khách đặt trước 24 giờ để được ưu tiên chọn Bác sĩ và khung giờ mong muốn, tránh chờ đợi."
        ),
        "related_links": ["/appointments/book", "/doctors"]
    },
    {
        "id": "faq_pricing",
        "category": "Bảng giá dịch vụ",
        "keywords": ["giá", "bảng giá", "chi phí", "bao nhiêu tiền", "viện phí", "phí khám", "xét nghiệm bao nhiêu"],
        "answer": (
            "Bảng giá dịch vụ khám bệnh và xét nghiệm cơ bản tại Phòng khám:\n"
            "- Khám chuyên khoa thông thường: 150.000 VNĐ / lượt.\n"
            "- Khám Giáo sư / Bác sĩ Chuyên gia: 300.000 VNĐ / lượt.\n"
            "- Tổng phân tích tế bào máu ngoại vi: 100.000 VNĐ.\n"
            "- Siêu âm bụng tổng quát: 180.000 VNĐ.\n"
            "- Chụp X-quang tim phổi thẳng: 120.000 VNĐ.\n"
            "- Điện tâm đồ (ECG): 80.000 VNĐ.\n"
            "- Nội soi Tai Mũi Họng: 200.000 VNĐ.\n"
            "Chi phí có thể được giảm trừ trực tiếp nếu Quý khách có thẻ BHYT hoặc Bảo hiểm bảo lãnh tư nhân."
        ),
        "related_links": ["/services/price-list", "/insurance-guide"]
    },
    {
        "id": "faq_specialties",
        "category": "Chuyên khoa khám bệnh",
        "keywords": ["chuyên khoa", "khoa", "bác sĩ", "nội", "nhi", "tim mạch", "tai mũi họng", "sản", "da liễu"],
        "answer": (
            "Phòng khám Đa khoa Smart Clinic cung cấp dịch vụ thăm khám thuộc đầy đủ các chuyên khoa mũi nhọn:\n"
            "1. Nội Tổng quát & Tim mạch.\n"
            "2. Nhi khoa & Tiêm chủng.\n"
            "3. Tai Mũi Họng & Hô hấp.\n"
            "4. Sản Phụ khoa & Kế hoạch hóa gia đình.\n"
            "5. Da liễu & Thẩm mỹ y khoa.\n"
            "6. Mắt & Răng Hàm Mặt.\n"
            "7. Chẩn đoán hình ảnh (Siêu âm, X-quang, CT) và Xét nghiệm kỹ thuật cao."
        ),
        "related_links": ["/specialties", "/doctors"]
    },
    {
        "id": "faq_workflow",
        "category": "Quy trình khám bệnh",
        "keywords": ["quy trình", "các bước", "làm thủ tục", "thứ tự", "khám như thế nào", "tiếp đón"],
        "answer": (
            "Quy trình 5 bước khám bệnh nhanh chóng tại Phòng khám:\n"
            "Bước 1: Tiếp đón & Lấy số thứ tự (hoặc xác nhận mã đặt lịch hẹn trước).\n"
            "Bước 2: Đo sinh hiệu (Huyết áp, Mạch, Chiều cao, Cân nặng) tại Quầy điều dưỡng.\n"
            "Bước 3: Bác sĩ chuyên khoa thăm khám lâm sàng và chỉ định cận lâm sàng nếu cần.\n"
            "Bước 4: Thực hiện xét nghiệm / siêu âm / X-quang và quay lại nghe Bác sĩ kết luận chẩn đoán, kê đơn thuốc.\n"
            "Bước 5: Thanh toán viện phí tại Quầy Thu ngân và nhận thuốc tại Nhà thuốc phòng khám."
        ),
        "related_links": ["/workflow-guide", "/patient-registration"]
    }
]


class KnowledgeBase:
    """Knowledge Retrieval Engine for Clinic FAQ."""

    def __init__(self, faqs: List[Dict[str, Any]] = FAQ_DATABASE):
        self.faqs = faqs

    def search(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Searches the knowledge base for the most relevant FAQ entry based on query keywords.
        Returns the matching FAQ dict or None if no match.
        """
        if not query:
            return None

        query_lower = query.lower()
        best_match = None
        best_score = 0

        for item in self.faqs:
            score = 0
            for keyword in item["keywords"]:
                if keyword in query_lower:
                    # Multi-word keyword matches get higher weight
                    weight = len(keyword.split()) * 2
                    score += weight

            if score > best_score:
                best_score = score
                best_match = item

        # Return best match if sufficient keyword confidence
        if best_score > 0 and best_match:
            return best_match

        return None

    def get_all_faqs(self) -> List[Dict[str, Any]]:
        return self.faqs


# Default singleton instance
knowledge_base = KnowledgeBase()
