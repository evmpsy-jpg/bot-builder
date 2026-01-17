import axios from 'axios';

const API_BASE_URL = 'http://62.113.104.172:8000/api';

export const flowsApi = {
  // Сохранить flow (создать или обновить)
  saveFlow: async (botId, flow, flowId = null) => {
    const response = await axios.post(`${API_BASE_URL}/flows/save`, {
      bot_id: botId,
      flow: flow,
      flow_id: flowId
    });
    return response.data;
  },

  // Получить список всех flows для бота
  listFlows: async (botId) => {
    const response = await axios.get(`${API_BASE_URL}/flows/${botId}`);
    return response.data;
  },

  // Получить конкретный flow
  getFlow: async (botId, flowId) => {
    const response = await axios.get(`${API_BASE_URL}/flows/${botId}/${flowId}`);
    return response.data;
  },

  // Удалить flow
  deleteFlow: async (botId, flowId) => {
    const response = await axios.delete(`${API_BASE_URL}/flows/${botId}/${flowId}`);
    return response.data;
  },

  // Активировать flow
  activateFlow: async (botId, flowId) => {
    const response = await axios.put(`${API_BASE_URL}/flows/${botId}/${flowId}/activate`);
    return response.data;
  }
};
