import React, { useState } from 'react';
import '../styles/Modal.css';
import {axiosInstance,setToken} from '../axiosInstance';

const topicsList = [
    "world",
    "nation",
    "business",
    "technology",
    "entertainment",
    "science",
    "sports",
    "health",
  ];
function SignupModal({ onClose, onAuthChange }) {
    const [credentials, setCredentials] = useState({ username: '', password: '', confirmPassword: '', email: '', topics: []});
    const [error, setError] = useState(null);
    const [token, setToken] = useState(null);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setCredentials({ ...credentials, [name]: value });
    };

    const handleTopicClick = (topic) => {
        setCredentials((prev) => {
          const newTopics = prev.topics.includes(topic)
            ? prev.topics.filter((t) => t !== topic) // Remove if already selected
            : [...prev.topics, topic]; // Add if not selected
          return { ...prev, topics: newTopics };
        });
      };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const { username, password, confirmPassword, email, topics } = credentials;
        if (!username || !password || !confirmPassword) {
            alert('Please fill in all fields');
        } else if (password !== confirmPassword) {
            alert('Passwords do not match');
        } else {
            try {
                // Make a POST request to Flask backend's /signup route
                const response = await axiosInstance.post('/signup', {
                    username,
                    password,
                    email,
                    topics
                });

                // Handle successful signup
                if (response.status === 201) {
                    const token = response.data.access_token;
                    const userData = response.data.user_data; //tady jsou user_data - kdyztak koukni do user.py(class User) v modelech, tam uvidis vsechny parametry ktere to ma, pripadne to jde vypsat v konzoli. Musis ulozit data lokalne, at jsou k dispozici
                    alert('Signup successful');
                    localStorage.setItem('token', token);
                    onAuthChange(); // Notify parent component of successful signup
                    onClose(); // Close the modal
                }
            } catch (err) {
                // Handle errors (e.g., username or email already exists)
                if (err.response) {
                    setError(err.response.data.status); // Capture error message from the response
                } else {
                    setError('Something went wrong');
                }
            }
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
                    <input
                        type="email"
                        name="email"
                        placeholder="Email"
                        value={credentials.email}
                        onChange={handleChange}
                        required
                    />
                              {/* Topics Selection */}
                    <input
                        type="text"
                        placeholder="Select topics..."
                        value={credentials.topics.join(", ")}
                        readOnly
                    />
                    <div className="topics-container">
                        {topicsList.map((topic) => (
                        <button
                            type="button"
                            key={topic}
                            className={`topic-button ${credentials.topics.includes(topic) ? "selected" : ""}`}
                            onClick={() => handleTopicClick(topic)}
                        >
                            {topic}
                        </button>
                        ))}
                    </div>
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