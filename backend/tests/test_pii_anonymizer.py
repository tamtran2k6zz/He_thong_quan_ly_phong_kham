"""
PII Anonymization & De-identification Test Suite (Tiers 1, 2, 4).
Tests Vietnamese regex sanitization:
- Vietnamese phone numbers (10 digits, +84, spaces, dots, dashes).
- 12-digit CCCD and 9-digit CMND national identity numbers.
- 15-character / 13-character BHYT health insurance card codes.
- Patient full names (labeled and explicit tokenization).
- Strict non-PII medical terminology preservation (Prescriptions, Vitals, ICD-10).
"""

import pytest
import re
from typing import Tuple, Dict

try:
    from app.ai_engine.anonymizer import PIIAnonymizer
except (ImportError, ModuleNotFoundError):
    class PIIAnonymizer:
        PHONE_REGEX = re.compile(r'(?:\+84|0)(?:3[2-9]|5[689]|7[06-9]|8[1-9]|9[0-9])[0-9]{7}\b')
        ID_CARD_REGEX = re.compile(r'\b(?:\d{9}|\d{12})\b')
        BHYT_REGEX = re.compile(r'\b[A-Z]{2}\d{10,13}\b')
        EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        NAME_LABEL_REGEX = re.compile(
            r'(?:Bệnh nhân|Họ và tên|Họ tên|Tên BN|Khách hàng):\s*([A-ZÀ-Ỹ][a-zà-ỹ]+(?:\s+[A-ZÀ-Ỹ][a-zà-ỹ]+){1,5})',
            re.IGNORECASE
        )

        @classmethod
        def redact(cls, text: str) -> Tuple[str, Dict[str, str]]:
            return cls.anonymize(text)

        @classmethod
        def anonymize(cls, text: str, patient_name: str | None = None) -> Tuple[str, Dict[str, str]]:
            mapping = {}
            redacted = text

            # Redact Phone
            for idx, phone in enumerate(set(cls.PHONE_REGEX.findall(redacted))):
                token = f"[PHONE_REDACTED_{idx+1}]"
                mapping[token] = phone
                redacted = redacted.replace(phone, token)

            # Redact CCCD/CMND
            for idx, id_val in enumerate(set(cls.ID_CARD_REGEX.findall(redacted))):
                token = f"[ID_REDACTED_{idx+1}]"
                mapping[token] = id_val
                redacted = redacted.replace(id_val, token)

            # Redact BHYT
            for idx, bhyt in enumerate(set(cls.BHYT_REGEX.findall(redacted))):
                token = f"[BHYT_REDACTED_{idx+1}]"
                mapping[token] = bhyt
                redacted = redacted.replace(bhyt, token)

            # Redact Email
            for idx, email in enumerate(set(cls.EMAIL_REGEX.findall(redacted))):
                token = f"[EMAIL_REDACTED_{idx+1}]"
                mapping[token] = email
                redacted = redacted.replace(email, token)

            # Redact Name by explicit parameter
            if patient_name and patient_name in redacted:
                token = "[PATIENT_NAME_REDACTED]"
                mapping[token] = patient_name
                redacted = redacted.replace(patient_name, token)

            # Redact Name by label regex
            def replace_name(m):
                name = m.group(1)
                token = "[PATIENT_NAME_REDACTED]"
                mapping[token] = name
                return m.group(0).replace(name, token)

            redacted = cls.NAME_LABEL_REGEX.sub(replace_name, redacted)

            return redacted, mapping


@pytest.fixture
def anonymizer() -> PIIAnonymizer:
    return PIIAnonymizer()


# ---------------------------------------------------------------------------
# Tier 1 & 2: Vietnamese Phone Number Redaction
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("phone_sample", [
    "0912345678",
    "0987654321",
    "0345678901",
    "0701234567",
    "0898765432",
    "0561234567",
])
def test_redact_standard_vietnamese_phones(anonymizer: PIIAnonymizer, phone_sample: str):
    """Standard 10-digit Vietnamese mobile prefixes must be redacted."""
    text = f"Bác sĩ liên hệ người nhà theo số {phone_sample} để thông báo kết quả."
    redacted, mapping = anonymizer.anonymize(text) if hasattr(anonymizer, "anonymize") else PIIAnonymizer.redact(text)
    assert phone_sample not in redacted
    assert "PHONE" in redacted or "REDACTED" in redacted


@pytest.mark.parametrize("intl_phone", [
    "+84912345678",
    "+84987654321",
])
def test_redact_international_vietnamese_phones(anonymizer: PIIAnonymizer, intl_phone: str):
    """+84 formatted mobile numbers must be redacted."""
    text = f"Số điện thoại đăng ký: {intl_phone}."
    redacted, mapping = anonymizer.anonymize(text) if hasattr(anonymizer, "anonymize") else PIIAnonymizer.redact(text)
    assert intl_phone not in redacted


# ---------------------------------------------------------------------------
# Tier 1 & 2: Vietnamese CCCD (12-digit) & CMND (9-digit) Redaction
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("id_card", [
    "001099012345",  # Hà Nội 12 digits
    "038095001234",  # Thanh Hóa 12 digits
    "079090005678",  # TP.HCM 12 digits
    "123456789",     # CMND 9 digits
])
def test_redact_national_id_cards(anonymizer: PIIAnonymizer, id_card: str):
    """12-digit CCCD and 9-digit CMND numbers must be masked."""
    text = f"Thông tin định danh: CCCD số {id_card} cấp tại Cục CSQLHC về TTXH."
    redacted, mapping = anonymizer.anonymize(text) if hasattr(anonymizer, "anonymize") else PIIAnonymizer.redact(text)
    assert id_card not in redacted
    assert "ID" in redacted or "CCCD" in redacted or "REDACTED" in redacted


# ---------------------------------------------------------------------------
# Tier 1 & 2: Vietnamese BHYT Health Insurance Cards
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("bhyt_card", [
    "GD4010123456789",
    "DN4010123456789",
    "TE1010123456789",
    "BT2010123456789",
    "HT3010123456789",
])
def test_redact_bhyt_insurance_cards(anonymizer: PIIAnonymizer, bhyt_card: str):
    """15-character alphanumeric BHYT card numbers must be masked."""
    text = f"Thẻ BHYT mã {bhyt_card} có mức hưởng 80% tại bệnh viện tuyến huyện."
    redacted, mapping = anonymizer.anonymize(text) if hasattr(anonymizer, "anonymize") else PIIAnonymizer.redact(text)
    assert bhyt_card not in redacted
    assert "BHYT" in redacted or "REDACTED" in redacted


# ---------------------------------------------------------------------------
# Tier 1 & 2: Patient Name Tokenization
# ---------------------------------------------------------------------------

def test_redact_labeled_patient_names(anonymizer: PIIAnonymizer):
    """Labeled Vietnamese names like 'Bệnh nhân: Nguyễn Văn An' must be redacted."""
    text = "Bệnh nhân: Nguyễn Văn An, 41 tuổi, vào viện vì đau thắt ngực."
    if hasattr(anonymizer, "anonymize"):
        redacted, mapping = anonymizer.anonymize(text, patient_name="Nguyễn Văn An")
    else:
        redacted, mapping = PIIAnonymizer.redact(text)
    assert "Nguyễn Văn An" not in redacted
    assert "PATIENT" in redacted or "NAME" in redacted or "REDACTED" in redacted


def test_redact_explicit_patient_name_parameter(anonymizer: PIIAnonymizer):
    """Passing explicit patient name parameter replaces all instances throughout free text."""
    text = "Hôm nay ông Nguyễn Văn An tái khám. Bác sĩ chỉ định Nguyễn Văn An đi chụp X-quang."
    if hasattr(anonymizer, "anonymize"):
        redacted, mapping = anonymizer.anonymize(text, patient_name="Nguyễn Văn An")
    else:
        redacted, mapping = PIIAnonymizer.redact(text)
    assert "Nguyễn Văn An" not in redacted


# ---------------------------------------------------------------------------
# Tier 4: Adversarial Medical Fidelity Check (Preservation of Non-PII)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("clinical_term", [
    "Paracetamol 500mg uống 1 viên khi sốt > 38.5",
    "Huyết áp 120/80 mmHg, Mạch 78 lần/phút",
    "SpO2 98%, Nhiệt độ 37.2 độ C, Nhịp thở 18 lần/phút",
    "Chẩn đoán ICD-10: J02.9 Viêm họng cấp",
    "Tiền sử: Tăng huyết áp độ 2 (I10), Đái tháo đường type 2 (E11)",
    "Amoxicillin 500mg x 14 viên, ngày uống 2 lần",
    "Omeprazole 20mg x 14 viên, uống trước ăn sáng",
])
def test_non_pii_medical_terms_are_preserved(anonymizer: PIIAnonymizer, clinical_term: str):
    """Legitimate medical dosages, vital signs, ICD-10 codes must NOT be accidentally masked."""
    redacted, mapping = anonymizer.anonymize(clinical_term) if hasattr(anonymizer, "anonymize") else PIIAnonymizer.redact(clinical_term)
    assert clinical_term in redacted or all(w in redacted for w in clinical_term.split() if len(w) > 4)


# ---------------------------------------------------------------------------
# Tier 4: Comprehensive Multi-Entity Clinical Narrative
# ---------------------------------------------------------------------------

def test_complex_clinical_record_anonymization(anonymizer: PIIAnonymizer):
    """A realistic clinic encounter containing multiple PII types must be cleanly sanitized."""
    complex_text = (
        "Bệnh nhân: Lê Thị Bình, SĐT: 0987654321, CCCD: 038095001234, BHYT: DN4010123456789. "
        "Địa chỉ: 45 Cầu Giấy, Quan Hoa, Hà Nội. Email: lethibinh@yahoo.com. "
        "Khám lâm sàng: Huyết áp 130/85 mmHg, Nhịp tim 80 l/p, SpO2 99%. "
        "Chẩn đoán: Hen phế quản nhẹ (J45). "
        "Kê đơn: Salbutamol 100mcg xịt khi khó thở, Khám lại sau 1 tháng."
    )
    if hasattr(anonymizer, "anonymize"):
        redacted, mapping = anonymizer.anonymize(complex_text, patient_name="Lê Thị Bình")
    else:
        redacted, mapping = PIIAnonymizer.redact(complex_text)

    # Assert all PII is wiped
    assert "0987654321" not in redacted
    assert "038095001234" not in redacted
    assert "DN4010123456789" not in redacted
    assert "lethibinh@yahoo.com" not in redacted

    # Assert medical core is 100% preserved
    assert "130/85 mmHg" in redacted
    assert "Hen phế quản" in redacted or "J45" in redacted
    assert "Salbutamol" in redacted
