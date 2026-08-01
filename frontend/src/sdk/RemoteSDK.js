export const RemoteSDK = {
  getStatus: async () => {
    try {
      const res = await fetch('/api/v1/remote/status');
      return await res.json();
    } catch (e) {
      return { status: 'offline' };
    }
  },
  executeCommand: async (command) => {
    try {
      const res = await fetch('/api/v1/remote/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command, confirmation: true })
      });
      return await res.json();
    } catch (e) {
      return { status: 'failed' };
    }
  },
  executeTerminalCommand: async (command) => {
    try {
      const res = await fetch('/api/v1/remote/terminal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command })
      });
      return await res.json();
    } catch (e) {
      return { status: 'failed' };
    }
  },
  browseFiles: async (path = '/projects') => {
    try {
      const res = await fetch(`/api/v1/filemanager/browse?path=${encodeURIComponent(path)}`);
      return await res.json();
    } catch (e) {
      return [];
    }
  }
};
