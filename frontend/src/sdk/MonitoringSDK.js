import { client } from './client';

export const MonitoringSDK = {
  getStatus: async () => {
    const res = await client.get('/monitoring/status');
    return res.data;
  },
  getHistory: async (metricName, limit = 50) => {
    const res = await client.get(`/monitoring/history?metric_name=${metricName}&limit=${limit}`);
    return res.data;
  },
  getServices: async () => {
    const res = await client.get('/monitoring/services');
    return res.data;
  }
};
