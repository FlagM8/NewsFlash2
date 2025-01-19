import React, { useState } from 'react';
import LoginModal from './LoginModal';
import SignupModal from './SignupModal';
import '../styles/WelcomePage.css';

function WelcomePage({ onAuthChange }) {
    const [showLogin, setShowLogin] = useState(false);
    const [showSignup, setShowSignup] = useState(false);

    return (
        <div className="welcome-page">
            <div className="welcome-header">
                <h1>Welcome to News Flash</h1>
                <p>Your source for the latest news</p>
                <p>Sign up or log in to get started</p>
                <div className="auth-buttons">
                    <button onClick={() => setShowLogin(true)}>Log In</button>
                    <button onClick={() => setShowSignup(true)}>Sign Up</button>
                </div>
            </div>
            {showLogin && <LoginModal onClose={() => setShowLogin(false)} onAuthChange={onAuthChange} />}
            {showSignup && <SignupModal onClose={() => setShowSignup(false)} onAuthChange={onAuthChange} />}
        </div>
    );
}

export default WelcomePage;
