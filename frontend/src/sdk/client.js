/**
 * HomeLab OS HTTP Client Instance
 */
export const client = {
  get: async (url) => {
    try {
      const fullUrl = url.startsWith('/api') ? url : `/api/v1${url.startsWith('/') ? '' : '/'}${url}`;
      const res = await fetch(fullUrl);
      const data = await res.json();
      return { data };
    } catch (e) {
      return { data: null };
    }
  },
  post: async (url, body) => {
    try {
      const fullUrl = url.startsWith('/api') ? url : `/api/v1${url.startsWith('/') ? '' : '/'}${url}`;
      const res = await fetch(fullUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body || {})
      });
      const data = await res.json();
      return { data };
    } catch (e) {
      return { data: null };
    }
  },
  put: async (url, body) => {
    try {
      const fullUrl = url.startsWith('/api') ? url : `/api/v1${url.startsWith('/') ? '' : '/'}${url}`;
      const res = await fetch(fullUrl, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body || {})
      });
      const data = await res.json();
      return { data };
    } catch (e) {
      return { data: null };
    }
  },
  delete: async (url) => {
    try {
      const fullUrl = url.startsWith('/api') ? url : `/api/v1${url.startsWith('/') ? '' : '/'}${url}`;
      const res = await fetch(fullUrl, { method: 'DELETE' });
      const data = await res.json();
      return { data };
    } catch (e) {
      return { data: null };
    }
  }
};
