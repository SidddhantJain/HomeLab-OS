export const DevicesSDK = {
  list: async () => {
    try {
      const res = await fetch('/api/v1/network/devices');
      return await res.json();
    } catch (e) {
      return [];
    }
  },
  updateAlias: async (mac, alias) => {
    try {
      const res = await fetch('/api/v1/network/devices/friendly-name', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mac_address: mac, friendly_name: alias })
      });
      return await res.json();
    } catch (e) {
      return {};
    }
  }
};
