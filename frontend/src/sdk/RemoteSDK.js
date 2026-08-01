import { client } from './client';

export const RemoteSDK = {
  getStatus: async () => {
    const res = await client.get('/remote/status');
    return res.data;
  },
  executeCommand: async (command) => {
    const res = await client.post('/remote/command', { command, confirmation: true });
    return res.data;
  },
  executeTerminalCommand: async (command) => {
    const res = await client.post('/remote/terminal', { command });
    return res.data;
  },
  browseFiles: async (path = '/projects') => {
    const res = await client.get(`/filemanager/browse?path=${encodeURIComponent(path)}`);
    return res.data;
  }
};
