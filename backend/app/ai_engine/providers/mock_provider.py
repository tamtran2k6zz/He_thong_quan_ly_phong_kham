"""
Deterministic Offline Mock AI Provider.
Provides 100% offline, zero-network, test-resilient responses for administrative AI tools:
- Pre-visit medical history briefings
- Workflow FAQ chatbot answers
- Post-visit discharge instructions
"""

import time
from typing import Optional, Dict, Any
from backend.app.ai_engine.providers.base import AIProvider, AIProviderResponse
from backend.app.ai_engine.guardrails import (
    AdminAIGuardrails,
    MEDICAL_DISCLAIMER,
    SAFE_REFUSAL_MESSAGE
)
from backend.app.ai_engine.knowledge_base import knowledge_base


class MockDeterministicAIProvider(AIProvider):
    """Deterministic rule-based AI provider for offline tests and zero-dependency mode."""

    def __init__(self, model_name: str = "mock-deterministic-v1"):
        self.model_name = model_name

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> AIProviderResponse:
        start_time = time.time()
        sys_lower = (system_prompt or "").lower()
        prompt_lower = (prompt or "").lower()

        # 1. Guardrail Safety Check
        is_safe, refusal_reason, safe_resp = AdminAIGuardrails.check_input_safety(prompt)
        if not is_safe:
            content = safe_resp or SAFE_REFUSAL_MESSAGE
            elapsed = int((time.time() - start_time) * 1000)
            return AIProviderResponse(
                content=content,
                model=self.model_name,
                latency_ms=max(1, elapsed),
                raw_response={"refusal_reason": refusal_reason}
            )

        # 2. Branch by System Prompt / Task Type
        if "discharge" in sys_lower or "dặn dò" in sys_lower or "post-visit" in sys_lower or "hướng dẫn sau khám" in sys_lower:
            content = self._handle_discharge(prompt)
        elif "briefing" in sys_lower or "pre-visit" in sys_lower or "tóm tắt" in sys_lower or "bệnh án" in sys_lower:
            content = self._handle_briefing(prompt)
        elif "faq" in sys_lower or "chatbot" in sys_lower or "hỏi đáp" in sys_lower:
            content = self._handle_faq(prompt, prompt_lower)
        else:
            # General fallback based on prompt content
            if any(w in prompt_lower for w in ["dặn dò", "xuất viện", "discharge", "đơn thuốc", "hướng dẫn sau"]):
                content = self._handle_discharge(prompt)
            elif any(w in prompt_lower for w in ["dị ứng", "bệnh án", "hồ sơ", "briefing", "tiền sử"]):
                content = self._handle_briefing(prompt)
            else:
                content = self._handle_faq(prompt, prompt_lower)

        elapsed = int((time.time() - start_time) * 1000)
        return AIProviderResponse(
            content=content,
            model=self.model_name,
            latency_ms=max(1, elapsed),
            raw_response={"prompt_type": "deterministic_rule_matched"}
        )

    def _handle_faq(self, prompt: str, prompt_lower: str) -> str:
        # Check specific keyword clusters
        if any(w in prompt_lower for w in ["giờ", "mấy giờ", "mở cửa", "thời gian", "làm việc"]):
            return (
                "Phòng khám làm việc từ 07:30 đến 17:30 tất cả các ngày từ Thứ Hai đến Thứ Bảy. "
                "Riêng Chủ Nhật phòng khám làm việc buổi sáng từ 07:30 đến 12:00."
            )
        elif any(w in prompt_lower for w in ["bhyt", "bảo hiểm", "bảo hiểm y tế"]):
            return (
                "Phòng khám tiếp nhận thẻ BHYT đúng tuyến và thông tuyến theo quy định. "
                "Mức hưởng BHYT từ 80% đến 100% tùy đối tượng thẻ. Quý khách vui lòng mang theo CCCD gắn chip và thẻ BHYT (hoặc ứng dụng VssID)."
            )
        elif any(w in prompt_lower for w in ["đặt lịch", "hẹn khám", "đăng ký", "book lịch"]):
            return (
                "Quý khách có thể đặt lịch hẹn trực tuyến qua hệ thống hoặc gọi hotline phòng khám 1900 6868 "
                "hoặc đăng ký trực tiếp tại Quầy Tiếp đón Lễ tân."
            )
        elif any(w in prompt_lower for w in ["giá", "chi phí", "bao nhiêu tiền", "bảng giá", "viện phí"]):
            return (
                "Bảng giá dịch vụ: Khám chuyên khoa thông thường 150.000 VNĐ, Khám chuyên gia 300.000 VNĐ, "
                "Siêu âm bụng 180.000 VNĐ, X-quang 120.000 VNĐ. Có áp dụng giảm trừ BHYT theo quy định."
            )
        elif any(w in prompt_lower for w in ["đau", "uống thuốc gì", "bị bệnh", "thuốc gì", "diagnose", "chẩn đoán", "kê đơn"]):
            return (
                "Hệ thống AI không có chức năng chẩn đoán hoặc kê đơn thuốc. "
                "Quý khách vui lòng đặt lịch khám chuyên khoa để được bác sĩ thăm khám trực tiếp."
            )

        # Query Knowledge Base search
        kb_match = knowledge_base.search(prompt)
        if kb_match:
            return kb_match["answer"]

        return (
            "Xin chào! Tôi là Trợ lý Hành chính Phòng khám Smart Clinic. "
            "Tôi có thể hỗ trợ quý khách thông tin về lịch khám, thủ tục BHYT, đặt lịch hẹn và bảng giá dịch vụ."
        )

    def _handle_briefing(self, prompt: str) -> str:
        # Extract allergy details if present
        allergies = "Không ghi nhận dị ứng đặc biệt"
        if "dị ứng" in prompt.lower():
            for line in prompt.splitlines():
                if "dị ứng" in line.lower():
                    allergies = line.strip().lstrip("- :*")

        history = "Tiền sử bệnh mạn tính được ghi nhận trong hồ sơ."
        if "tiền sử" in prompt.lower() or "medical_history" in prompt.lower():
            for line in prompt.splitlines():
                if "tiền sử" in line.lower():
                    history = line.strip().lstrip("- :*")

        return (
            "### TÓM TẮT HỒ SƠ BỆNH ÁN (PRE-VISIT BRIEFING):\n"
            f"- **Cảnh báo Dị ứng:** {allergies}\n"
            f"- **Tiền sử bệnh lý:** {history}\n"
            "- **Lần khám gần nhất:** Tình trạng ổn định, tuân thủ phác đồ điều trị.\n"
            "- **Lưu ý lâm sàng:** Đề nghị Bác sĩ kiểm tra sinh hiệu và xác nhận lại tiền sử dị ứng trước khi chỉ định phác đồ thuốc mới."
        )

    def _handle_discharge(self, prompt: str) -> str:
        return (
            "### HƯỚNG DẪN DẶN DÒ SAU KHÁM & ĐƠN THUỐC (DISCHARGE INSTRUCTIONS):\n"
            "1. **Hướng dẫn Uống thuốc:** Tuân thủ đúng liều lượng và thời gian theo đơn của bác sĩ. Uống thuốc sau bữa ăn (trừ các thuốc chỉ định uống trước ăn).\n"
            "2. **Chế độ Ăn uống & Nghỉ ngơi:** Uống nhiều nước ấm (1.5 - 2 lít/ngày), ăn thức ăn chín mềm, hạn chế đồ cay nóng và chất kích thích, ngủ đủ giấc.\n"
            "3. **Dấu hiệu Cần tái khám ngay:** Nếu xuất hiện sốt cao liên tục > 38.5°C không hạ, khó thở, đau tức ngực dữ dội hoặc nổi mẩn dị ứng, cần đến cơ sở y tế ngay.\n"
            "4. **Lịch Tái khám:** Tái khám sau 7 ngày hoặc theo ngày hẹn trên phiếu khám."
        )
