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
  console.log("TOKEN: ",localStorage.getItem('token'));
};
const setData = (userdata) => {
  localStorage.setItem('userdata', userdata);
  console.log("UDATA: ",localStorage.getItem('userdata'));
};

const getData = () => {
  var data = localStorage.getItem('userdata');
  console.log(data);
  return data;
};
export { axiosInstance, setToken, setData, getData };