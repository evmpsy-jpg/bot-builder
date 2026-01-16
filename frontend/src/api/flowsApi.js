import axios from 'axios';

const API_URL = 'http://62.113.104.172:8000/api';

export const flowsApi = {
  // Сохранить flow
  saveFlow: async (botId, flow) => {
    const response = await axios.post(`${API_URL}/flows/save`, {
      bot_id: botId,
      flow: flow
    });
    return response.data;
  },

  // Получить flow
  getFlow: async (botId) => {
    const response = await axios.get(`${API_URL}/flows/${botId}`);
    return response.data;
  },

  // Список всех flows
  listFlows: async () => {
    const response = await axios.get(`${API_URL}/flows`);
    return response.data;
  },

  // Удалить flow
  deleteFlow: async (botId) => {
    const response = await axios.delete(`${API_URL}/flows/${botId}`);
    return response.data;
  }
};