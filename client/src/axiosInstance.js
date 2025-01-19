import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: process.env.BACKEND_SERVICE_URL || 'http://localhost:5001', 
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
      },
});

export default axiosInstance;
