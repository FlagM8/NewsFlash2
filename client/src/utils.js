const checkTokenAndUserData = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const response = await axiosInstance.post('/check-token', {
          token,
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