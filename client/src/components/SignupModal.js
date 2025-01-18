import React, { useState } from 'react';
import '../styles/Modal.css';


function SignupModal({ onClose, onAuthChange }) {
    const [credentials, setCredentials] = useState({ username: '', password: '' });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setCredentials({ ...credentials, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // Simulate successful signup
        if (credentials.username && credentials.password) {
            onAuthChange(); // Notify App of successful signup
            onClose();
        } else {
            alert('Please fill in all fields');
        }
    };

    return (
        <div className="modal">
            <div className="modal-content">
                <h2>Sign Up</h2>
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        name="username"
                        placeholder="Username"
                        value={credentials.username}
                        onChange={handleChange}
                        required
                    />
                    <input
                        type="password"
                        name="password"
                        placeholder="Password"
                        value={credentials.password}
                        onChange={handleChange}
                        checkifpasswordsMatch={credentials.password === credentials.confirmPassword}
                        required
                    />
                    <input
                        type="password"
                        name="confirmPassword"
                        placeholder="Confirm Password"
                        value={credentials.confirmPassword}
                        onChange={handleChange}
                        checkifpasswordsMatch={credentials.password === credentials.confirmPassword}
                        required
                    />
                    <button type="submit">Sign Up</button>
                </form>
                <button className="close-button" onClick={onClose}>
                    Close
                </button>
            </div>
        </div>
    );
}

export default SignupModal;
