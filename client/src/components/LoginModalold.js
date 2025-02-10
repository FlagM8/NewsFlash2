import React, { useState } from 'react';
import '../styles/Modal.css';

function LoginModal({ onClose, onAuthChange }) {
    const [credentials, setCredentials] = useState({ username: '', password: '' });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setCredentials({ ...credentials, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // Simulate successful login
        if (credentials.username === 'user' && credentials.password === 'password') {
            onAuthChange(); // Notify App of successful login
            onClose();
        } else {
            alert('Invalid credentials');
        }
    };

    return (
        <div className="modal">
            <div className="modal-content">
                <h2>Log In</h2>
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
                        required
                    />
                    <button type="submit">Log In</button>
                </form>
                <button className="close-button" onClick={onClose}>
                    Close
                </button>
            </div>
        </div>
    );
}

export default LoginModal;
