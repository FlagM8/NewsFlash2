import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: process.env.BACKEND_SERVICE_URL || 'http://localhost:5001', 
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/*axiosInstance.interceptors.request.use(config => {
  const token = localStorage.getItem('token'); 
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});*/

const setToken = (token) => {
  localStorage.setItem('token', token);
};

export { axiosInstance, setToken };