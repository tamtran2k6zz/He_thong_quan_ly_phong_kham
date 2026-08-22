import api from './api';

export const consultationService = {
  // Queue
  getQueue: async (doctorId, date) => {
    const params = {};
    if (doctorId) params.doctor_id = doctorId;
    if (date) params.appointment_date = date;
    const response = await api.get('/medical_records/queue', { params });
    return response.data;
  },

  // Medical Records
  getMedicalRecords: async (params = {}) => {
    const response = await api.get('/medical_records', { params });
    return response.data;
  },

  getMedicalRecord: async (id) => {
    const response = await api.get(`/medical_records/${id}`);
    return response.data;
  },

  createMedicalRecord: async (recordData) => {
    const response = await api.post('/medical_records', recordData);
    return response.data;
  },

  updateMedicalRecord: async (id, recordData) => {
    const response = await api.put(`/medical_records/${id}`, recordData);
    return response.data;
  },

  addServiceOrder: async (recordId, serviceData) => {
    const response = await api.post(`/medical_records/${recordId}/services`, serviceData);
    return response.data;
  },

  completeMedicalRecord: async (recordId) => {
    const response = await api.post(`/medical_records/${recordId}/complete`);
    return response.data;
  },

  // Prescriptions
  getPrescriptions: async (params = {}) => {
    const response = await api.get('/prescriptions', { params });
    return response.data;
  },

  createPrescription: async (prescriptionData) => {
    const response = await api.post('/prescriptions', prescriptionData);
    return response.data;
  },

  // Medicines Catalog
  getMedicines: async (query = '', isActive = true) => {
    const params = { limit: 100 };
    if (query) params.q = query;
    if (isActive !== null) params.is_active = isActive;
    const response = await api.get('/medicines', { params });
    return response.data;
  },

  getMedicine: async (id) => {
    const response = await api.get(`/medicines/${id}`);
    return response.data;
  },

  createMedicine: async (data) => {
    const response = await api.post('/medicines', data);
    return response.data;
  },

  updateMedicine: async (id, data) => {
    const response = await api.put(`/medicines/${id}`, data);
    return response.data;
  },
};
