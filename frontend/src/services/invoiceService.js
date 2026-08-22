import api from './api';

export const invoiceService = {
  getInvoices: async (params = {}) => {
    const response = await api.get('/invoices', { params });
    return response.data;
  },

  getInvoice: async (id) => {
    const response = await api.get(`/invoices/${id}`);
    return response.data;
  },

  createInvoice: async (data) => {
    const response = await api.post('/invoices', data);
    return response.data;
  },

  payInvoice: async (id, payData) => {
    const response = await api.post(`/invoices/${id}/pay`, payData);
    return response.data;
  },
};
