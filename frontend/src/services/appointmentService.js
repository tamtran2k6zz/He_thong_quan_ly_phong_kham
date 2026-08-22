import api from './api';

export const appointmentService = {
  getAppointments: async (params = {}) => {
    const response = await api.get('/appointments', { params });
    return response.data;
  },

  getAppointment: async (id) => {
    const response = await api.get(`/appointments/${id}`);
    return response.data;
  },

  createAppointment: async (appointmentData) => {
    const response = await api.post('/appointments', appointmentData);
    return response.data;
  },

  updateAppointment: async (id, appointmentData) => {
    const response = await api.put(`/appointments/${id}`, appointmentData);
    return response.data;
  },

  checkInAppointment: async (id) => {
    const response = await api.post(`/appointments/${id}/check-in`);
    return response.data;
  },

  cancelAppointment: async (id) => {
    const response = await api.post(`/appointments/${id}/cancel`);
    return response.data;
  },

  getAvailableSlots: async (doctorId, date, clinicId) => {
    const params = { doctor_id: doctorId, appointment_date: date };
    if (clinicId) params.clinic_id = clinicId;
    const response = await api.get('/appointments/available-slots', { params });
    return response.data;
  },
};
