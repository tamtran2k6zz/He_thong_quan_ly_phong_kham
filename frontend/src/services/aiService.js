import api from './api';

export const aiService = {
  // Pre-visit Briefing Tool
  generatePreVisitSummary: async (patientId, patientData = null) => {
    if (patientId && !patientData) {
      const response = await api.post(`/ai/pre-visit-summary/${patientId}`);
      return response.data;
    }
    const payload = patientData ? { ...patientData, patient_id: patientId } : { patient_id: patientId };
    const response = await api.post('/ai/pre-visit-summary', payload);
    return response.data;
  },

  // Clinic Workflow FAQ Chatbot
  answerFAQ: async (question, conversationId = null) => {
    const payload = { question };
    if (conversationId) payload.conversation_id = conversationId;
    const response = await api.post('/ai/faq', payload);
    return response.data;
  },

  // Post-visit Discharge Instructions Tool
  generateDischargeInstructions: async (medicalRecordId, dischargeData = null) => {
    if (medicalRecordId && !dischargeData) {
      const response = await api.post(`/ai/discharge-instructions/${medicalRecordId}`);
      return response.data;
    }
    const payload = dischargeData ? { ...dischargeData, medical_record_id: medicalRecordId } : { medical_record_id: medicalRecordId };
    const response = await api.post('/ai/discharge-instructions', payload);
    return response.data;
  },
};
