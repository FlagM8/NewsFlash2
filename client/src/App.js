import React, { useState } from 'react';
import axiosInstance from './axiosInstance';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import WelcomePage from './components/WelcomePage';
import MainFeed from './components/MainFeed';
import TopBar from './components/TopBar';
import UserProfile from './components/UserProfile';

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    const handleAuthChange = () => {
        setIsAuthenticated(true); // Set the user as logged in
    };

    return (
        <Router>
          <TopBar />
            <Routes>
                <Route
                    path="/"
                    element={
                        isAuthenticated ? (
                            <Navigate to="/main" replace />
                        ) : (
                            <WelcomePage onAuthChange={handleAuthChange} />
                        )
                    }
                />
                <Route path="/main" element={<MainFeed />} />
                <Route path="/profile" element={<UserProfile />} />
            </Routes>
        </Router>
    );
}

export default App;
