// utils.js
import { axiosInstance } from './axiosInstance';

const checkTokenAndUserData = async (setIsLoggedIn, setUserData) => {
  const token = localStorage.getItem('token');
  if (!token) {
    setIsLoggedIn(false);
    return;
  }
  if (token) {
    try {
      const response = await axiosInstance.get('/check-token', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (response.data.expired) {
        localStorage.removeItem('token');
        setIsLoggedIn(false);
      } else {
        setIsLoggedIn(true);
        const userData = response.data.userData;
        setUserData(userData);
      }
    } catch (error) {
      localStorage.removeItem('token');
      setIsLoggedIn(false);
    }
  } else {
    setIsLoggedIn(false);
  }
};

export { checkTokenAndUserData };