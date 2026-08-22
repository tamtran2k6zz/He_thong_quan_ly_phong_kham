"""
Guardrails and Medical Safety Module for Administrative AI Engine.
Includes:
- Mandatory Medical Disclaimer
- Prompt Injection & Jailbreak Filters
- Clinical Diagnosis & Drug Prescription Refusal Guards
- Standard System Prompts for Administrative Tasks
"""

import re
from typing import Tuple, Optional, Dict, Any


MEDICAL_DISCLAIMER: str = (
    "⚠️ TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y TẾ: Trợ lý AI chỉ phục vụ mục đích hành chính "
    "và hỗ trợ thông tin quy trình. Kết quả từ AI KHÔNG thay thế cho chẩn đoán, "
    "kết luận chuyên môn hoặc chỉ định điều trị của bác sĩ."
)

SAFE_REFUSAL_MESSAGE: str = (
    "Hệ thống AI không có chức năng chẩn đoán bệnh lý hoặc kê đơn thuốc y tế. "
    "Quý khách vui lòng đặt lịch khám chuyên khoa để được bác sĩ thăm khám trực tiếp "
    "và đưa ra chẩn đoán chính xác cùng phác đồ điều trị phù hợp.\n\n" + MEDICAL_DISCLAIMER
)

# System Prompts for AI Tools
BASE_ADMIN_SYSTEM_PROMPT = """Bạn là Trợ lý AI Hành chính của Phòng khám Đa khoa thông minh.
Nhiệm vụ của bạn là hỗ trợ nhân viên y tế và bệnh nhân về các thủ tục hành chính, quy trình khám bệnh, bảng giá, bảo hiểm y tế và tóm tắt hồ sơ thông tin.

CÁC NGUYÊN TẮC BẮT BUỘC (GUARDRAILS):
1. TUYỆT ĐỐI KHÔNG tự chẩn đoán bệnh tật, không phỏng đoán tình trạng bệnh của bệnh nhân.
2. TUYỆT ĐỐI KHÔNG tự ý kê đơn thuốc, không chỉ định liều dùng thuốc kháng sinh hoặc thuốc nguy hiểm.
3. Nếu người dùng hỏi câu hỏi yêu cầu chẩn đoán bệnh hoặc kê đơn thuốc, bạn phải lịch sự từ chối và hướng dẫn họ đặt lịch khám với bác sĩ chuyên khoa.
4. Luôn tuân thủ định dạng thông tin rõ ràng, trang trọng, chuẩn mực ngôn ngữ y tế Việt Nam.
"""

PRE_VISIT_SYSTEM_PROMPT = """Bạn là Trợ lý AI Hành chính hỗ trợ Bác sĩ xem nhanh tóm tắt hồ sơ bệnh án trước khi vào khám (Pre-visit Briefing).
Dựa trên dữ liệu hồ sơ bệnh nhân được cung cấp:
1. Trích xuất và làm nổi bật: Cảnh báo Dị ứng thuốc/thực phẩm (NẾU CÓ).
2. Tóm tắt tiền sử bệnh lý mạn tính và các đợt khám/điều trị gần nhất.
3. Trình bày ngắn gọn, súc tích theo định dạng gạch đầu dòng rõ ràng để Bác sĩ nắm bắt trong 10 giây.
4. Không tự ý thêm bớt các triệu chứng hoặc chẩn đoán không có trong hồ sơ.
"""

FAQ_CHATBOT_SYSTEM_PROMPT = """Bạn là Chatbot Hướng dẫn Quy trình và Giải đáp thắc mắc Phòng khám Đa khoa (Clinic Workflow FAQ Chatbot).
Nhiệm vụ của bạn là giải đáp cho bệnh nhân và nhân viên các câu hỏi về:
- Giờ làm việc, địa chỉ, lịch khám chuyên khoa.
- Thủ tục sử dụng thẻ BHYT, giấy tờ cần mang theo khi khám bệnh.
- Hướng dẫn quy trình đặt lịch hẹn khám trước và tiếp đón tại quầy.
- Bảng giá tham khảo các dịch vụ khám bệnh và cận lâm sàng.

QUY TẮC AN TOÀN Y TẾ:
- Tuyệt đối từ chối trả lời nếu người dùng hỏi chẩn đoán bệnh ("tôi bị bệnh gì", "đau tức ngực là bị gì", v.v.) hoặc xin đơn thuốc ("uống thuốc gì", "kê đơn kháng sinh", v.v.).
- Khi từ chối, hãy giải thích lịch sự rằng AI chỉ hỗ trợ thông tin hành chính quy trình và hướng dẫn người bệnh đặt lịch khám với bác sĩ.
"""

DISCHARGE_SYSTEM_PROMPT = """Bạn là Trợ lý AI Hành chính hỗ trợ Bác sĩ tạo bản Hướng dẫn dặn dò sau khám và Nhắc lịch tái khám cho bệnh nhân (Post-visit Discharge Instructions).
Dựa trên thông tin chẩn đoán, lời dặn của bác sĩ và đơn thuốc đã kê:
1. Trình bày rõ ràng Lịch uống thuốc (Tên thuốc, liều lượng, thời điểm uống: trước/sau ăn).
2. Tóm tắt chế độ ăn uống, sinh hoạt, nghỉ ngơi phù hợp với bệnh lý.
3. Liệt kê các dấu hiệu bất thường cần đến cơ sở y tế ngay.
4. Nhắc nhở thời gian tái khám theo chỉ định.
5. Ngôn ngữ thân thiện, dễ hiểu cho người bệnh và thân nhân.
"""


class AdminAIGuardrails:
    # Prompt injection & jailbreak keywords / patterns
    INJECTION_PATTERNS = [
        r'(?i)ignore\s+(?:all\s+)?(?:previous|prior)\s+instructions',
        r'(?i)bỏ\s+qua\s+(?:toàn\s+bộ|hết)\s+(?:chỉ\s+dẫn|hướng\s+dẫn|yêu\s+cầu|quy\s+định)\s+trước',
        r'(?i)you\s+are\s+(?:now|acting\s+as)\s+(?:a|the)?\s*(?:doctor|chief\s+medical|physician)',
        r'(?i)bạn\s+là\s+bác\s+sĩ\s+(?:trưởng|chuyên\s+khoa|điều\s+trị)',
        r'(?i)system\s+override',
        r'(?i)jailbreak',
        r'(?i)disregard\s+safety\s+rules',
    ]

    # Clinical medical diagnosis inquiry patterns
    DIAGNOSIS_PATTERNS = [
        r'(?i)(?:tôi|em|anh|chị|cháu|bác|người\s+nhà)\s+(?:bị\s+bệnh\s+gì|mắc\s+bệnh\s+gì|đang\s+bị\s+gì)',
        r'(?i)(?:chẩn\s+đoán|diagnose)\s+(?:bệnh|tình\s+trạng|bệnh\s+lý|cho\s+tôi|giúp\s+tôi)',
        r'(?i)(?:đau|sốt|ho|tức\s+ngực|khó\s+thở|chóng\s+mặt).+(?:bị\s+bệnh\s+gì|là\s+bệnh\s+gì|có\s+phải\s+bị)',
        r'(?i)diagnose\s+my\b',
        r'(?i)what\s+disease\s+do\s+i\s+have',
    ]

    # Medical prescription & drug suggestion patterns
    PRESCRIPTION_PATTERNS = [
        r'(?i)(?:nên|cần|hãy)?\s*(?:uống|dùng|mua)\s+thuốc\s+gì',
        r'(?i)(?:kê\s+đơn|kê\s+thuốc|kê\s+to|prescribe)\s+(?:thuốc|kháng\s+sinh|liều|cho\s+tôi|giúp)',
        r'(?i)kê\s+đơn\s+(?:amoxicillin|paracetamol|kháng\s+sinh|omeprazole|thuốc)',
        r'(?i)prescribe\s+(?:amoxicillin|omeprazole|medication|drugs|antibiotic)',
        r'(?i)liều\s+lượng\s+thuốc\s+kháng\s+sinh',
    ]

    @classmethod
    def check_input_safety(cls, text: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validates user input text against prompt injection, diagnostic, and prescription rules.
        Returns:
            (is_safe, refusal_reason, safe_response)
            - is_safe (bool): True if safe to process; False if violated guardrails.
            - refusal_reason (str | None): Category of violation (INJECTION, DIAGNOSIS_REQUEST, PRESCRIPTION_REQUEST).
            - safe_response (str | None): Polite refusal text if not safe, None if safe.
        """
        if not text:
            return True, None, None

        normalized_text = text.strip()

        # 1. Check Prompt Injections / Jailbreaks
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, normalized_text):
                return False, "PROMPT_INJECTION_DETECTED", SAFE_REFUSAL_MESSAGE

        # 2. Check Clinical Diagnosis Requests
        for pattern in cls.DIAGNOSIS_PATTERNS:
            if re.search(pattern, normalized_text):
                return False, "DIAGNOSIS_REQUEST_DETECTED", SAFE_REFUSAL_MESSAGE

        # 3. Check Medical Prescription Requests
        for pattern in cls.PRESCRIPTION_PATTERNS:
            if re.search(pattern, normalized_text):
                return False, "PRESCRIPTION_REQUEST_DETECTED", SAFE_REFUSAL_MESSAGE

        return True, None, None

    @classmethod
    def append_disclaimer(cls, content: str) -> str:
        """Appends the mandatory medical disclaimer to any AI generated response if not already present."""
        if not content:
            return MEDICAL_DISCLAIMER
        if "TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y TẾ" in content or "LƯU Ý Y TẾ" in content:
            return content
        return f"{content.strip()}\n\n{MEDICAL_DISCLAIMER}"


# Global convenience function
def check_prompt_guardrails(text: str) -> Tuple[bool, Optional[str], Optional[str]]:
    return AdminAIGuardrails.check_input_safety(text)
