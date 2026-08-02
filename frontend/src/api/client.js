import axios from 'axios';

// Dynamically compute API_BASE_URL based on active browser location host IP
const getDynamicBaseURL = () => {
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }
  if (typeof window !== 'undefined' && window.location) {
    const host = window.location.hostname || '192.168.0.180';
    return `${window.location.protocol}//${host}:8000/api/v1`;
  }
  return '/api/v1';
};

const apiClient = axios.create({
  baseURL: getDynamicBaseURL(),
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add JWT Token Interceptor
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('homelab_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default apiClient;
