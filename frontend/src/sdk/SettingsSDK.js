export const SettingsSDK = {
  get: async () => {
    try {
      const res = await fetch('/api/v1/settings');
      return await res.json();
    } catch (e) {
      return { theme: 'dark', language: 'en' };
    }
  },
  update: async (settingsData) => {
    try {
      const res = await fetch('/api/v1/settings', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settingsData)
      });
      return await res.json();
    } catch (e) {
      return {};
    }
  }
};
