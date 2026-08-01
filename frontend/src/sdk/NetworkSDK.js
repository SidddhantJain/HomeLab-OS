import { client } from './client';

export const NetworkSDK = {
  getDevices: async () => {
    const res = await client.get('/network/devices');
    return res.data;
  },
  setFriendlyName: async (macAddress, friendlyName) => {
    const res = await client.post('/network/devices/friendly-name', { mac_address: macAddress, friendly_name: friendlyName });
    return res.data;
  },
  getTopology: async () => {
    const res = await client.get('/network/topology');
    return res.data;
  },
  ping: async (target) => {
    const res = await client.post('/network/actions/ping', { target });
    return res.data;
  },
  wol: async (target) => {
    const res = await client.post('/network/actions/wol', { target });
    return res.data;
  }
};
