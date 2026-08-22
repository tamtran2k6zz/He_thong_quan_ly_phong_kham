import api from './api';

export const patientService = {
  getPatients: async (query = '', skip = 0, limit = 50) => {
    const params = { skip, limit };
    if (query) params.q = query;
    const response = await api.get('/patients', { params });
    return response.data;
  },

  getPatient: async (id) => {
    const response = await api.get(`/patients/${id}`);
    return response.data;
  },

  createPatient: async (patientData) => {
    const response = await api.post('/patients', patientData);
    return response.data;
  },

  updatePatient: async (id, patientData) => {
    const response = await api.put(`/patients/${id}`, patientData);
    return response.data;
  },
};
