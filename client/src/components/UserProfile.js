import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {axiosInstance,setToken, setData, getData} from '../axiosInstance';
import '../styles/UserProfile.css';

const topicsList = [
    "WORLD",
    "NATION",
    "BUSSINESS",
    "TECHNOLOGY",
    "ENTERTAINMENT",
    "SCIENCE",
    "SPORTS",
    "HEALTH",
];

function UserProfile() {
    const navigate = useNavigate();
    const storedUser = JSON.parse(localStorage.getItem('userdata'));
    const [user, setUser] = useState(storedUser);
    const [selectedTopics, setSelectedTopics] = useState(storedUser?.topics || []);
    const [editing, setEditing] = useState(false);

    useEffect(() => {
        if (!storedUser) {
            navigate('/login');
        }
        console.log(storedUser.topics);
    }, [storedUser, navigate]);

    const handleTopicClick = (topic) => {
        if (editing) {
            setSelectedTopics((prev) =>
                prev.includes(topic) ? prev.filter(t => t !== topic) : [...prev, topic]
            );
        }
    };

    const handleSend = async () => {
        try {
            const updatedUser = { ...user, topics: selectedTopics };
            await axiosInstance.post('/update-profile', {"topics":selectedTopics}, {
                headers: {
                  Authorization: `Bearer ${localStorage.getItem('token')}`,
                },
              });
            localStorage.setItem('user', JSON.stringify(updatedUser));
            //setUser(updatedUser);
            setEditing(false); // Quit editing after saving
            navigate('/main'); // Redirect to /main
        } catch (error) {
            console.error("Error updating profile:", error);
        }
    };

    const handleQuit = () => {
        setSelectedTopics(user.topics);
        setEditing(false);
    };

    return (
        <div className="user-profile">
        {/* Profile Picture Section */}
        <div className="profile-header">
            <img
                src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/dd4b4cff-ce5c-4ac9-b9d5-084db5133314/dgydgze-979dbab6-1172-474c-9107-6b0f77e9f39e.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2RkNGI0Y2ZmLWNlNWMtNGFjOS1iOWQ1LTA4NGRiNTEzMzMxNFwvZGd5ZGd6ZS05NzlkYmFiNi0xMTcyLTQ3NGMtOTEwNy02YjBmNzdlOWYzOWUucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.AaoHMlproSIUy19qY-H4__V_7ncwWQXSJcYO3l6idWI"
                alt="Profile"
                className="profile-pic"
            />
            <h1>{user?.username}'s Profile</h1>
        </div>

        <p><strong>Email:</strong> {user?.email}</p>


            <div className="topics-section">
                <h3>Topics of Interest</h3>
                <div className="topics-container">
                    {topicsList.map(topic => (
                        <button
                            key={topic}
                            className={`topic-button ${selectedTopics.includes(topic) ? "selected" : ""}`}
                            onClick={() => handleTopicClick(topic)}
                            disabled={!editing}
                        >
                            {topic}
                        </button>
                    ))}
                </div>
            </div>

            {editing ? (
                <div className="profile-actions">
                    <button className="send-button" onClick={handleSend}>Send</button>
                    <button className="quit-button" onClick={handleQuit}>Quit</button>
                </div>
            ) : (
                <button className="edit-button" onClick={() => setEditing(true)}>Edit Settings</button>
            )}
        </div>
    );
}

export default UserProfile;
