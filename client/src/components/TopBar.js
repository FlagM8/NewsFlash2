import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { axiosInstance, setData } from '../axiosInstance';
import '../styles/TopBar.css';
import LoginModal from './LoginModal';
import SignupModal from './SignupModal';
//import logo from '../newsflash.png'; // Import the logo

const TopBar = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userData, setUserData] = useState(null);
  const [showLogin, setShowLogin] = useState(false);
  const [showSignup, setShowSignup] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('userdata');
    if (token && userData) {
      setIsLoggedIn(true);
      //setData(userData);
      console.log(userData);
    }
  }, []);

  const handleAuthChange = () => {
    setIsLoggedIn(true);
    const userData = localStorage.getItem('userdata');
    //setUserData(userData);
    navigate('/main');
  };

  const handleLogout = async () => {
    try {
      //await axiosInstance.post('/logout');
      localStorage.removeItem('token');
      localStorage.removeItem('userdata');
      localStorage.clear();
      setIsLoggedIn(false);
      setUserData(null);
      navigate('/', { replace: true });
      console.log(localStorage.getItem('token')); // Should be null after logout
console.log(localStorage.getItem('userdata')); // Should be null after logout
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="top-bar">
      <img
        src="https://images.cults3d.com/vufhuKKRNV2mJ4XF1sId5t8BiZ4=/516x516/filters:no_upscale():format(webp)/https://fbi.cults3d.com/uploaders/13073908/illustration-file/a905a545-aeed-41e3-9dac-9100cf208c69/Flash_Logo_01.png"
        alt="NewsFlash Logo"
        className="top-bar-logo"
        onClick={() => navigate('/main')}
      />
      {isLoggedIn ? (
        <div className="logged-in">
          <img
            src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/dd4b4cff-ce5c-4ac9-b9d5-084db5133314/dgydgze-979dbab6-1172-474c-9107-6b0f77e9f39e.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2RkNGI0Y2ZmLWNlNWMtNGFjOS1iOWQ1LTA4NGRiNTEzMzMxNFwvZGd5ZGd6ZS05NzlkYmFiNi0xMTcyLTQ3NGMtOTEwNy02YjBmNzdlOWYzOWUucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.AaoHMlproSIUy19qY-H4__V_7ncwWQXSJcYO3l6idWI"
            alt={userData?.username}
            className="profile-picture"
            onClick={() => navigate('/profile')}
          />
          <span className="username">{userData?.username}</span>
          <button className="logout-button" onClick={handleLogout}>
            Logout
          </button>
        </div>
      ) : (
        <div className="logged-out">
          <button onClick={() => setShowLogin(true)}>Log In</button>
          <button onClick={() => setShowSignup(true)}>Sign Up</button>
          {showLogin && (
            <LoginModal
              onClose={() => setShowLogin(false)}
              onAuthChange={handleAuthChange}
            />
          )}
          {showSignup && (
            <SignupModal
              onClose={() => setShowSignup(false)}
              onAuthChange={handleAuthChange}
            />
          )}
        </div>
      )}
    </div>
  );
};

export default TopBar;
