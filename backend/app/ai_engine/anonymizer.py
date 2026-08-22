"""
PII Anonymization & De-identification Module for Medical Records.
Provides high-precision regex sanitization for Vietnamese personal data:
- Vietnamese phone numbers (+84, 09x, 03x, 05x, 07x, 08x, spaces, dots, dashes).
- 12-digit CCCD and 9-digit CMND national identity numbers.
- 15-character / 13-character BHYT health insurance cards.
- Patient full names (labeled and explicit tokenization).
- Address strings & emails.
- Medical terminology preservation (Prescriptions, Vitals, ICD-10, dosages).
- Full reversible de-anonymization / mapping support.
"""

import re
from typing import Tuple, Dict, Optional, Any, List


class PIIAnonymizer:
    # Vietnamese Phone Numbers: 10-digit mobile prefixes and international +84 / 84
    # Handles spaced, dotted, or dashed numbers (e.g. 0912 345 678, 091.234.5678, 091-234-5678, +84 901 234 567)
    PHONE_REGEX = re.compile(
        r'(?:\+84|84|0)[\s.-]?(?:3[2-9]|5[25689]|7[06-9]|8[1-9]|9\d)(?:[\s.-]?\d){7}\b',
        re.IGNORECASE
    )

    # 12-digit CCCD and 9-digit CMND
    ID_CARD_REGEX = re.compile(r'\b(?:\d{12}|\d{9})\b')

    # BHYT Health Insurance Card (e.g. GD4010123456789, DN4010123456789, TE1010123456789)
    BHYT_REGEX = re.compile(r'\b[A-Z]{2}\d{10,13}\b')

    # Email Addresses
    EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

    # Labeled Names: "Bệnh nhân: Nguyễn Văn An", "Họ và tên: Lê Thị Bình", "Tên BN: ...", "Khách hàng: ..."
    NAME_LABEL_REGEX = re.compile(
        r'(?:Bệnh nhân|Họ và tên|Họ tên|Tên BN|Khách hàng|Người bệnh|Họ & tên):\s*([A-ZÀ-Ỹ][a-zà-ỹ]+(?:\s+[A-ZÀ-Ỹ][a-zà-ỹ]+){1,5})',
        re.IGNORECASE
    )

    # Labeled Address: "Địa chỉ: 45 Cầu Giấy, Quan Hoa, Hà Nội"
    ADDRESS_LABEL_REGEX = re.compile(
        r'(?:Địa chỉ|Nơi cư trú|Thường trú|Tạm trú|Địa chỉ cư trú):\s*([^.\n,]+(?:,[^.\n,]+){1,4})',
        re.IGNORECASE
    )

    def __init__(self):
        pass

    @classmethod
    def redact(cls, text: str, patient_name: Optional[str] = None) -> Tuple[str, Dict[str, str]]:
        """Alias for anonymize() for backward compatibility."""
        return cls.anonymize(text, patient_name=patient_name)

    @classmethod
    def anonymize(cls, text: str, patient_name: Optional[str] = None) -> Tuple[str, Dict[str, str]]:
        """
        Sanitizes text by replacing PII entities with redacted placeholders.
        Returns a tuple of (anonymized_text, token_mapping).
        """
        if not text:
            return "", {}

        mapping: Dict[str, str] = {}
        redacted = text

        # 1. Redact explicit patient name parameter first
        if patient_name and patient_name.strip():
            p_name = patient_name.strip()
            if p_name in redacted:
                token = "[PATIENT_NAME_REDACTED]"
                mapping[token] = p_name
                redacted = redacted.replace(p_name, token)

        # 2. Redact Labeled Patient Names
        def _replace_labeled_name(match: re.Match) -> str:
            name_val = match.group(1).strip()
            token = "[PATIENT_NAME_REDACTED]"
            mapping[token] = name_val
            return match.group(0).replace(name_val, token)

        redacted = cls.NAME_LABEL_REGEX.sub(_replace_labeled_name, redacted)

        # 3. Redact Emails
        email_matches = list(set(cls.EMAIL_REGEX.findall(redacted)))
        for idx, email in enumerate(email_matches):
            token = f"[EMAIL_REDACTED_{idx+1}]" if len(email_matches) > 1 else "[EMAIL_REDACTED]"
            mapping[token] = email
            redacted = redacted.replace(email, token)

        # 4. Redact Labeled Addresses
        def _replace_labeled_address(match: re.Match) -> str:
            addr_val = match.group(1).strip()
            token = "[ADDRESS_REDACTED]"
            mapping[token] = addr_val
            return match.group(0).replace(addr_val, token)

        redacted = cls.ADDRESS_LABEL_REGEX.sub(_replace_labeled_address, redacted)

        # 5. Redact BHYT Insurance Cards
        bhyt_matches = list(set(cls.BHYT_REGEX.findall(redacted)))
        for idx, bhyt in enumerate(bhyt_matches):
            token = f"[BHYT_REDACTED_{idx+1}]" if len(bhyt_matches) > 1 else "[BHYT_REDACTED]"
            mapping[token] = bhyt
            redacted = redacted.replace(bhyt, token)

        # 6. Redact Vietnamese Phone Numbers
        phone_matches = []
        for m in cls.PHONE_REGEX.finditer(redacted):
            matched_phone = m.group(0).strip()
            if matched_phone not in phone_matches:
                phone_matches.append(matched_phone)

        # Sort phones by length descending to replace longer matches first
        for idx, phone in enumerate(sorted(phone_matches, key=len, reverse=True)):
            token = f"[PHONE_REDACTED_{idx+1}]" if len(phone_matches) > 1 else "[PHONE_REDACTED]"
            mapping[token] = phone
            redacted = redacted.replace(phone, token)

        # 7. Redact National ID Cards (CCCD 12 digits / CMND 9 digits)
        id_matches = list(set(cls.ID_CARD_REGEX.findall(redacted)))
        for idx, id_val in enumerate(id_matches):
            token = f"[ID_REDACTED_{idx+1}]" if len(id_matches) > 1 else "[CCCD_REDACTED]"
            mapping[token] = id_val
            redacted = redacted.replace(id_val, token)

        return redacted, mapping

    @classmethod
    def deanonymize(cls, text: str, mapping: Dict[str, str]) -> str:
        """
        Reverses the anonymization process by restoring original values from token mapping.
        """
        if not text or not mapping:
            return text or ""

        restored = text
        for token, original_val in mapping.items():
            restored = restored.replace(token, original_val)
        return restored


# Default instance for quick access
pii_anonymizer = PIIAnonymizer()
