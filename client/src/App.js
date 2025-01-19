import React, { useState } from 'react';
import axiosInstance from './axiosInstance';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import WelcomePage from './components/WelcomePage';
import MainFeed from './components/MainFeed';

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    const handleAuthChange = () => {
        setIsAuthenticated(true); // Set the user as logged in
    };

    return (
        <Router>
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
            </Routes>
        </Router>
    );
}

export default App;
