import React, { useState } from 'react';
import '../styles/Modal.css';
import { axiosInstance, setToken, setData } from '../axiosInstance';

function LoginModal({ onClose, onAuthChange }) {
    const [credentials, setCredentials] = useState({ username: '', password: '' });
    const [error, setError] = useState(null);
    const [token, setUserToken] = useState(null);
    const [userData, setUserData] = useState(null);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setCredentials({ ...credentials, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axiosInstance.post('/login', credentials);
            if (response.status === 200) {
                const token = response.data.token;
                const userData = response.data.user_data;
                console.log("TOKEN: ", token);
                console.log("UDATA: ", userData);
                setToken(token);
                //setUserToken(token);
                //setUserData(userData);
                //setData(userData);
                localStorage.setItem("userdata", JSON.stringify(userData));
                console.log("UDATA:2 ", localStorage.getItem('userdata'));
                onAuthChange();
                onClose();
            }
        } catch (err) {
            if (err.response) {
                setError(err.response.data.status);
            } else {
                setError('Something went wrong');
            }
        }
    };

    return (
        <div className="modal">
            <div className="modal-content">
                <h2>Log In</h2>
                {error && <p className="error-message">{error}</p>}
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
