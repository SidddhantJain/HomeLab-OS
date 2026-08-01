import { client } from './client';

export const PluginsSDK = {
  list: async () => {
    const res = await client.get('/plugins');
    return res.data;
  },
  register: async (pluginId, name, version = '1.0.0') => {
    const res = await client.post('/plugins/register', { plugin_id: pluginId, name, version });
    return res.data;
  }
};
