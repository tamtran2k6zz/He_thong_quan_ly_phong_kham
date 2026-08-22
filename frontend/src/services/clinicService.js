import api from './api';

export const clinicService = {
  // Specialties
  getSpecialties: async () => {
    const response = await api.get('/specialties');
    return response.data;
  },

  createSpecialty: async (data) => {
    const response = await api.post('/specialties', data);
    return response.data;
  },

  updateSpecialty: async (id, data) => {
    const response = await api.put(`/specialties/${id}`, data);
    return response.data;
  },

  deleteSpecialty: async (id) => {
    const response = await api.delete(`/specialties/${id}`);
    return response.data;
  },

  // Clinic consultation rooms
  getClinics: async (specialtyId) => {
    const params = specialtyId ? { specialty_id: specialtyId } : {};
    const response = await api.get('/clinics', { params });
    return response.data;
  },

  createClinic: async (data) => {
    const response = await api.post('/clinics', data);
    return response.data;
  },

  updateClinic: async (id, data) => {
    const response = await api.put(`/clinics/${id}`, data);
    return response.data;
  },

  deleteClinic: async (id) => {
    const response = await api.delete(`/clinics/${id}`);
    return response.data;
  },

  // Doctors
  getDoctors: async (specialtyId) => {
    const params = specialtyId ? { specialty_id: specialtyId } : {};
    const response = await api.get('/doctors', { params });
    return response.data;
  },

  getDoctor: async (id) => {
    const response = await api.get(`/doctors/${id}`);
    return response.data;
  },

  createDoctor: async (data) => {
    const response = await api.post('/doctors', data);
    return response.data;
  },

  updateDoctor: async (id, data) => {
    const response = await api.put(`/doctors/${id}`, data);
    return response.data;
  },

  // Shifts
  getShifts: async (params) => {
    const response = await api.get('/shifts', { params });
    return response.data;
  },

  createShift: async (data) => {
    const response = await api.post('/shifts', data);
    return response.data;
  },

  updateShift: async (id, data) => {
    const response = await api.put(`/shifts/${id}`, data);
    return response.data;
  },

  deleteShift: async (id) => {
    const response = await api.delete(`/shifts/${id}`);
    return response.data;
  },
};
