import axios from 'axios';

// ✅ SOLO variable de entorno (nada de localhost en producción)
const API_URL = import.meta.env.VITE_API_URL;

// 🚨 Si no existe la variable, fallar explícitamente
if (!API_URL) {
  throw new Error('❌ VITE_API_URL no está definida. Revisa las variables de entorno en Vercel.');
}

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 🔐 Interceptor para agregar el token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;

