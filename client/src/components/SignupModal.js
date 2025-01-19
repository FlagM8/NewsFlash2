import React, { useState } from 'react';
import '../styles/Modal.css';

function SignupModal({ onClose, onAuthChange }) {
    const [credentials, setCredentials] = useState({ username: '', password: '', confirmPassword: '' });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setCredentials({ ...credentials, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const { username, password, confirmPassword } = credentials;
        if (!username || !password || !confirmPassword) {
            alert('Please fill in all fields');
        } else if (password !== confirmPassword) {
            alert('Passwords do not match');
        } else {
            onAuthChange(); // Notify App of successful signup
            onClose(); // Close the modal
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
                        required
                    />
                    <input
                        type="password"
                        name="confirmPassword"
                        placeholder="Confirm Password"
                        value={credentials.confirmPassword}
                        onChange={handleChange}
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