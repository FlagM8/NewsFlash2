import React, { useState, useEffect } from 'react';
import '../styles/UserProfile.css';
import MainFeed from './MainFeed'; // Import MainFeed

function UserProfile() {
    // Hardcoded user data
    const user = {
        username: 'test',
        password: 'test1',
        // profilePicture: 'https://static.wikia.nocookie.net/smiling-friends/images/e/e6/Glep_%28SF%29.png/revision/latest?cb=20240204175445', // Make sure this path is correct on your system
        bio: 'nothing',
    };

    // You no longer need to set the placeholderUser, just use the hardcoded user
    const currentUser = user;

    // Optionally, you can check if the user is available (though it's hardcoded in this case)
    if (!currentUser) {
        return <p>Loading user data...</p>;
    }

    return (
        <div className="user-profile">
            <div className="user-profile-header">
                {/* Use the profile picture */}
                {/* <img
                    src={currentUser.profilePicture}
                    alt={`${currentUser.username}'s profile`}
                    className="profile-picture"
                /> */}
                <h1 className="username">{currentUser.username}</h1>
            </div>
            <div className="user-profile-details">
                <p><strong>Email:</strong> {currentUser.username}@example.com</p> {/* Email can be dynamically set based on username */}
                <p><strong>Bio:</strong> {currentUser.bio}</p>
            </div>

            {/* Pass the user data to MainFeed as a prop */}
            <MainFeed user={currentUser} />
        </div>
    );
}

export default UserProfile;
