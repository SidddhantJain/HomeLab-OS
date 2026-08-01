export const PluginsSDK = {
  list: async () => {
    try {
      const res = await fetch('/api/v1/plugins');
      return await res.json();
    } catch (e) {
      return [];
    }
  },
  register: async (pluginId, name, version = '1.0.0') => {
    try {
      const res = await fetch('/api/v1/plugins/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ plugin_id: pluginId, name, version })
      });
      return await res.json();
    } catch (e) {
      return {};
    }
  }
};
