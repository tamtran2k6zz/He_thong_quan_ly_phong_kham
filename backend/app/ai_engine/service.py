"""
Administrative AI Service.
Orchestrates:
1. Pre-visit Briefing Tool
2. Clinic Workflow FAQ Chatbot
3. Post-visit Discharge Instructions Generator
With PII de-identification, safety guardrails, disclaimer enforcement, and audit/invocation logging.
"""

from datetime import datetime, date
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

from backend.app.ai_engine.anonymizer import PIIAnonymizer
from backend.app.ai_engine.guardrails import (
    AdminAIGuardrails,
    MEDICAL_DISCLAIMER,
    SAFE_REFUSAL_MESSAGE,
    PRE_VISIT_SYSTEM_PROMPT,
    FAQ_CHATBOT_SYSTEM_PROMPT,
    DISCHARGE_SYSTEM_PROMPT,
)
from backend.app.ai_engine.knowledge_base import knowledge_base
from backend.app.ai_engine.providers import get_ai_provider, AIProvider
from backend.app.models.patient import Patient
from backend.app.models.medical_record import MedicalRecord
from backend.app.models.prescription import Prescription
from backend.app.models.audit import AIInvocationLog


class AdminAIService:
    """Core Administrative AI Service with privacy guarantees."""

    def __init__(self, provider: Optional[AIProvider] = None):
        self._provider = provider

    @property
    def provider(self) -> AIProvider:
        if self._provider is None:
            self._provider = get_ai_provider()
        return self._provider

    def _log_invocation(
        self,
        db: Optional[Session],
        feature_name: str,
        anonymized_prompt: str,
        response_text: str,
        model_used: str,
        latency_ms: int,
        user_id: Optional[int] = None,
        disclaimer_included: bool = True
    ) -> Optional[AIInvocationLog]:
        """Persists AI invocation details into the database with sanitized prompts."""
        if db is None:
            return None

        try:
            log_entry = AIInvocationLog(
                user_id=user_id,
                feature_name=feature_name,
                anonymized_prompt=anonymized_prompt,
                response_text=response_text,
                model_used=model_used,
                latency_ms=latency_ms,
                disclaimer_included=disclaimer_included,
                created_at=datetime.utcnow()
            )
            db.add(log_entry)
            db.commit()
            db.refresh(log_entry)
            return log_entry
        except Exception:
            db.rollback()
            return None

    def generate_pre_visit_summary(
        self,
        patient_id: Optional[int] = None,
        patient_data: Optional[Dict[str, Any]] = None,
        db: Optional[Session] = None,
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Gathers patient history and allergy records, anonymizes PII,
        and generates a concise briefing for the attending physician.
        """
        # 1. Resolve patient data from DB or provided payload
        patient: Optional[Patient] = None
        if db and patient_id:
            patient = db.query(Patient).filter(Patient.id == patient_id).first()

        p_name = ""
        p_code = ""
        p_allergies = ""
        p_history = ""
        p_gender = "Nam"
        p_age = 40
        recent_visits_text = "Không có ghi nhận lần khám trước đó."

        if patient:
            p_name = patient.full_name
            p_code = patient.medical_code
            p_allergies = patient.drug_allergies or ""
            p_history = patient.medical_history or ""
            p_gender = patient.gender
            if patient.date_of_birth:
                today = date.today()
                p_age = today.year - patient.date_of_birth.year - (
                    (today.month, today.day) < (patient.date_of_birth.month, patient.date_of_birth.day)
                )

            # Look up recent medical records
            past_records = (
                db.query(MedicalRecord)
                .filter(MedicalRecord.patient_id == patient.id)
                .order_by(MedicalRecord.exam_date.desc())
                .limit(3)
                .all()
            )
            if past_records:
                summaries = []
                for r in past_records:
                    date_str = r.exam_date.strftime("%d/%m/%Y") if r.exam_date else ""
                    diag = r.diagnosis_icd10 or r.icd10_code or "Khám thông thường"
                    summaries.append(f"- Ngày {date_str}: {diag} ({r.chief_complaint})")
                recent_visits_text = "\n".join(summaries)
        elif patient_data:
            p_name = patient_data.get("full_name") or patient_data.get("patient_name") or ""
            p_code = patient_data.get("patient_code") or patient_data.get("medical_code") or f"BN-{patient_id or 1}"
            p_allergies = patient_data.get("drug_allergies") or patient_data.get("allergies") or ""
            p_history = patient_data.get("medical_history") or ""
            p_gender = patient_data.get("gender") or "Nam"
            p_age = patient_data.get("age") or 40
            recent_visits_text = patient_data.get("recent_visits_summary") or recent_visits_text

        # 2. Extract chronic conditions and clinical alerts
        chronic_conditions: List[str] = []
        for cond in ["Tăng huyết áp", "Đái tháo đường", "Hen phế quản", "Tim mạch", "Dạ dày", "Viêm gan", "Gout"]:
            if cond.lower() in p_history.lower():
                chronic_conditions.append(cond)

        clinical_alerts: List[str] = []
        if p_allergies:
            clinical_alerts.append(f"CẢNH BÁO DỊ ỨNG: {p_allergies}")
        if chronic_conditions:
            clinical_alerts.append(f"Bệnh mạn tính cần theo dõi: {', '.join(chronic_conditions)}")

        # 3. Formulate Prompt & Anonymize PII
        raw_prompt = (
            f"Bệnh nhân: {p_name}\n"
            f"Mã hồ sơ: {p_code}\n"
            f"Tuổi: {p_age}, Giới tính: {p_gender}\n"
            f"Dị ứng thuốc: {p_allergies or 'Không'}\n"
            f"Tiền sử bệnh: {p_history or 'Không'}\n"
            f"Lần khám gần nhất:\n{recent_visits_text}"
        )

        anonymized_prompt, _ = PIIAnonymizer.anonymize(raw_prompt, patient_name=p_name)

        # 4. Generate AI summary
        ai_res = self.provider.generate(
            prompt=anonymized_prompt,
            system_prompt=PRE_VISIT_SYSTEM_PROMPT
        )

        # 5. Attach disclaimer and structure output
        summary_content = AdminAIGuardrails.append_disclaimer(ai_res.content)

        # 6. Log invocation
        self._log_invocation(
            db=db,
            feature_name="PRE_VISIT_SUMMARY",
            anonymized_prompt=anonymized_prompt,
            response_text=summary_content,
            model_used=ai_res.model,
            latency_ms=ai_res.latency_ms,
            user_id=user_id,
            disclaimer_included=True
        )

        return {
            "patient_id": patient_id or (patient.id if patient else 1),
            "patient_name": p_name or "[PATIENT_NAME_REDACTED]",
            "medical_code": p_code,
            "age": p_age,
            "gender": p_gender,
            "allergies": p_allergies or None,
            "medical_history": p_history or None,
            "recent_visits_summary": recent_visits_text,
            "chronic_conditions": chronic_conditions,
            "clinical_alerts": clinical_alerts,
            "summary": summary_content,
            "content": summary_content,
            "disclaimer": MEDICAL_DISCLAIMER,
            "disclaimer_included": True
        }

    def answer_faq(
        self,
        question: str,
        db: Optional[Session] = None,
        user_id: Optional[int] = None,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Processes clinic workflow questions with safety guardrails and disclaimer.
        """
        # 1. Anonymize any PII inside user question
        anonymized_question, _ = PIIAnonymizer.anonymize(question)

        # 2. Check Guardrails for diagnostic inquiry / prompt injection / prescription request
        is_safe, refusal_reason, safe_resp = AdminAIGuardrails.check_input_safety(anonymized_question)

        if not is_safe:
            answer_text = safe_resp or SAFE_REFUSAL_MESSAGE
            # Log refusal to AI invocation logs
            self._log_invocation(
                db=db,
                feature_name="CLINIC_FAQ",
                anonymized_prompt=anonymized_question,
                response_text=answer_text,
                model_used="guardrail-safety-filter",
                latency_ms=1,
                user_id=user_id,
                disclaimer_included=True
            )
            return {
                "question": question,
                "answer": answer_text,
                "response": answer_text,
                "category": "Tư vấn An toàn Y tế",
                "related_links": ["/appointments/book", "/doctors"],
                "is_medical_advice_refused": True,
                "disclaimer": MEDICAL_DISCLAIMER,
                "disclaimer_included": True
            }

        # 3. Search Knowledge Base
        kb_match = knowledge_base.search(anonymized_question)
        category = kb_match["category"] if kb_match else "Hỏi đáp chung"
        related_links = kb_match["related_links"] if kb_match else ["/contact"]

        # 4. Generate Answer via AI Provider
        ai_res = self.provider.generate(
            prompt=anonymized_question,
            system_prompt=FAQ_CHATBOT_SYSTEM_PROMPT
        )

        final_answer = AdminAIGuardrails.append_disclaimer(ai_res.content)

        # 5. Log Invocation
        self._log_invocation(
            db=db,
            feature_name="CLINIC_FAQ",
            anonymized_prompt=anonymized_question,
            response_text=final_answer,
            model_used=ai_res.model,
            latency_ms=ai_res.latency_ms,
            user_id=user_id,
            disclaimer_included=True
        )

        return {
            "question": question,
            "answer": final_answer,
            "response": final_answer,
            "category": category,
            "related_links": related_links,
            "is_medical_advice_refused": False,
            "disclaimer": MEDICAL_DISCLAIMER,
            "disclaimer_included": True
        }

    def generate_discharge_instructions(
        self,
        medical_record_id: Optional[int] = None,
        discharge_data: Optional[Dict[str, Any]] = None,
        db: Optional[Session] = None,
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generates post-visit home care guidance, medication schedule, and follow-up reminders.
        """
        record: Optional[MedicalRecord] = None
        if db and medical_record_id:
            record = db.query(MedicalRecord).filter(MedicalRecord.id == medical_record_id).first()

        diag_text = "Viêm họng cấp tính"
        diag_icd10 = "J02.9"
        doctor_advice = "Uống nhiều nước ấm, nghỉ ngơi hợp lý."
        follow_up_days = 7
        med_schedule: List[Dict[str, Any]] = []
        p_name = ""

        if record:
            diag_text = record.diagnosis_icd10 or diag_text
            diag_icd10 = record.icd10_code or diag_icd10
            doctor_advice = record.doctor_notes or doctor_advice
            if record.patient:
                p_name = record.patient.full_name

            # Check prescription items
            if record.prescription and record.prescription.items:
                for item in record.prescription.items:
                    m_name = item.medicine.name if item.medicine else f"Thuốc {item.medicine_id}"
                    med_schedule.append({
                        "medicine_name": m_name,
                        "dosage": item.dosage,
                        "frequency": item.frequency,
                        "instructions": item.instructions or "Uống sau khi ăn"
                    })
        elif discharge_data:
            p_name = discharge_data.get("patient_name") or ""
            diag_icd10 = discharge_data.get("diagnosis_icd10") or diag_icd10
            diag_text = discharge_data.get("diagnosis_text") or diag_text
            doctor_advice = discharge_data.get("doctor_advice") or doctor_advice
            follow_up_days = discharge_data.get("follow_up_days") or follow_up_days
            med_schedule = discharge_data.get("prescriptions") or []

        # Format medication list
        med_text_lines = []
        for idx, m in enumerate(med_schedule, start=1):
            med_text_lines.append(
                f"{idx}. {m.get('medicine_name', 'Thuốc')}: Liều {m.get('dosage', '1 viên')}, {m.get('frequency', '')}. HD: {m.get('instructions', '')}"
            )
        meds_text = "\n".join(med_text_lines) if med_text_lines else "Uống thuốc theo đơn chỉ định."

        raw_prompt = (
            f"Bệnh nhân: {p_name}\n"
            f"Chẩn đoán: {diag_text} (ICD-10: {diag_icd10})\n"
            f"Đơn thuốc:\n{meds_text}\n"
            f"Lời dặn bác sĩ: {doctor_advice}\n"
            f"Hẹn tái khám sau: {follow_up_days} ngày"
        )

        anonymized_prompt, _ = PIIAnonymizer.anonymize(raw_prompt, patient_name=p_name)

        ai_res = self.provider.generate(
            prompt=anonymized_prompt,
            system_prompt=DISCHARGE_SYSTEM_PROMPT
        )

        instructions_content = AdminAIGuardrails.append_disclaimer(ai_res.content)

        # Log Invocation
        self._log_invocation(
            db=db,
            feature_name="DISCHARGE_INSTRUCTIONS",
            anonymized_prompt=anonymized_prompt,
            response_text=instructions_content,
            model_used=ai_res.model,
            latency_ms=ai_res.latency_ms,
            user_id=user_id,
            disclaimer_included=True
        )

        return {
            "medical_record_id": medical_record_id or 1,
            "diagnosis": f"{diag_text} ({diag_icd10})",
            "medication_schedule": med_schedule,
            "dietary_guidelines": "Ăn thức ăn chín mềm, uống nhiều nước ấm (1.5 - 2 lít/ngày), tránh đồ cay nóng và nước đá.",
            "activity_recommendations": "Nghỉ ngơi tại nơi thoáng khí, tránh làm việc nặng nhọc hoặc gắng sức quá mức.",
            "warning_signs": [
                "Sốt cao liên tục > 38.5°C không đáp ứng thuốc hạ sốt",
                "Khó thở, tức ngực hoặc tím tái",
                "Nổi ban dị ứng, ngứa, sưng môi/mặt sau khi uống thuốc"
            ],
            "follow_up_advice": f"Tái khám sau {follow_up_days} ngày hoặc khi có dấu hiệu bất thường.",
            "instructions": instructions_content,
            "content": instructions_content,
            "disclaimer": MEDICAL_DISCLAIMER,
            "disclaimer_included": True
        }


# Singleton service instance
admin_ai_service = AdminAIService()
