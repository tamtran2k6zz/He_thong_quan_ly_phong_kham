import api from './api';

export const auditService = {
  getAuditLogs: async (params = {}) => {
    const response = await api.get('/audit/logs', { params });
    return response.data;
  },

  getAILogs: async (params = {}) => {
    const response = await api.get('/audit/ai-logs', { params });
    return response.data;
  },
};
