export const NetworkSDK = {
  getDevices: async () => {
    try {
      const res = await fetch('/api/v1/network/devices');
      return await res.json();
    } catch (e) {
      return [];
    }
  },
  setFriendlyName: async (macAddress, friendlyName) => {
    try {
      const res = await fetch('/api/v1/network/devices/friendly-name', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mac_address: macAddress, friendly_name: friendlyName })
      });
      return await res.json();
    } catch (e) {
      return {};
    }
  },
  getTopology: async () => {
    try {
      const res = await fetch('/api/v1/network/topology');
      return await res.json();
    } catch (e) {
      return { nodes: [], edges: [] };
    }
  },
  ping: async (target) => {
    try {
      const res = await fetch('/api/v1/network/actions/ping', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target })
      });
      return await res.json();
    } catch (e) {
      return { status: 'offline' };
    }
  },
  wol: async (target) => {
    try {
      const res = await fetch('/api/v1/network/actions/wol', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target })
      });
      return await res.json();
    } catch (e) {
      return { status: 'failed' };
    }
  }
};
