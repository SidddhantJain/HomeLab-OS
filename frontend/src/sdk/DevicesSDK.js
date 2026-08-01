import { client } from './client';

export const DevicesSDK = {
  list: async () => {
    const res = await client.get('/network/devices');
    return res.data;
  },
  updateAlias: async (mac, alias) => {
    const res = await client.post('/network/devices/friendly-name', { mac_address: mac, friendly_name: alias });
    return res.data;
  }
};
