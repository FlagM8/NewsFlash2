import React from 'react';
import { Link } from 'react-router-dom';
import { checkTokenAndUserData } from './utils';

const TopBar = () => {
  const [isLoggedIn, setIsLoggedIn] = React.useState(false);
  const [userData, setUserData] = React.useState(null);

  React.useEffect(() => {
    checkTokenAndUserData().then((data) => {
      if (data) {
        setIsLoggedIn(true);
        setUserData(data);
      }
    });
  }, []);

  return (
    <div className="top-bar">
      <div className="logo">
        <Link to="/">
          <img src="logo.png" alt="Logo" />
        </Link>
      </div>
      <div className="right-side">
        {isLoggedIn ? (
          <div className="user-profile">
            <Link to="/profile">
              <img src={userData.profilePicture} alt="Profile Picture" />
              <span>{userData.username}</span>
            </Link>
            <div className="dropdown">
              <Link to="/profile/settings">Settings</Link>
              <Link to="/profile/account">Account</Link>
              <Link to="/logout">Logout</Link>
            </div>
          </div>
        ) : (
          <div className="login-signup">
            <Link to="/login">Login</Link>
            <Link to="/signup">Signup</Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default TopBar;