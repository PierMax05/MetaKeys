// api.service.js
import axios from "axios";
import { CSRF_TOKEN, getCookie } from "./csrf_token.js";

const ApiService = {
  init(baseURL) {
    axios.defaults.baseURL = baseURL;
    axios.defaults.headers.common['X-CSRFToken'] = CSRF_TOKEN;

    // Imposta il token di accesso dal cookie se esiste
    const accessToken = getCookie('accessToken');
    if (accessToken) {
      this.setHeader(accessToken);
    }

    // Intercettore di risposta per gestire il rinnovo del token
    axios.interceptors.response.use(
      response => response,
      async error => {
        const originalRequest = error.config;
        if (error.response.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          try {
            // Gestisci il caso in cui il token di accesso non è valido
            document.cookie = 'accessToken=; Max-Age=0; path=/; secure; HttpOnly';
            window.location.href = '/login'; // Reindirizza alla pagina di login
          } catch (err) {
            console.error('Token refresh failed', err);
            window.location.href = '/login'; // Reindirizza alla pagina di login
          }
        }
        return Promise.reject(error);
      }
    );
  },

  setHeader(token) {
    axios.defaults.headers.common['Authorization'] = `Token ${token}`;
  },

  removeHeader() {
    axios.defaults.headers.common = {};
  },

  get(resource) {
    return axios.get(resource);
  },

  post(resource, data) {
    return axios.post(resource, data);
  },
  patch(resource, data) {
    return axios.patch(resource, data);
  },
  put(resource, data) {
    return axios.put(resource, data);
  },
  delete(resource) {
    return axios.delete(resource)
  }
};

export default ApiService;