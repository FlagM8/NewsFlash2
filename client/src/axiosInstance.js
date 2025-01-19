import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: process.env.BACKEND_SERVICE_URL || 'http://code:5001', 
    timeout: 5000,
});

export default axiosInstance;
