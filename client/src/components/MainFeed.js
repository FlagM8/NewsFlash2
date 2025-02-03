import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/MainFeed.css';
import {axiosInstance} from '../axiosInstance';

function MainFeed({ user }) {
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();
    const token = localStorage.getItem('token');
    console.log(token);

    // const goToUserProfile = () => {
    //     navigate('/profile'); // Redirect to the profile page
    // };

    useEffect(() => {
        const fetchArticles = async () => {
            try {
                setLoading(true);
                const response = await axiosInstance.get('/getnews', {
                    headers: {
                      Authorization: `Bearer ${localStorage.getItem('token')}`,
                    },
                  });
                const data = await response.json();
                setArticles(data.articles);
            } catch (error) {
                console.error('Error fetching articles:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchArticles();
    }, [token]);

    return (
        <div className="main-feed">
            <header className="main-feed-header">
                <h1>News Flash</h1>
                {/* add user name */}
                <p>Stay updated with the latest news from around the world.</p>

                {/* User Profile Button */}
                {/* <button className="user-profile-button" onClick={goToUserProfile}>
                    Render user profile picture if available
                    {user.profilePicture && (
                        // <img
                        //     src={user.profilePicture}
                        //     alt={`${user.username}'s profile`}
                        //     className="user-profile-picture"
                        // />
                    )}
                    <p>{user.username}</p>
                </button> */}
            </header>

            <div className="main-feed-content">
                {loading ? (
                    <p>Loading articles...</p>
                ) : articles.length > 0 ? (
                    <div className="articles-list">
                        {articles.map((article, index) => (
                            <div key={index} className="article-card">
                                {article.urlToImage && (
                                    <img
                                        src={article.urlToImage}
                                        alt={article.title}
                                        className="article-image"
                                    />
                                )}
                                <div className="article-details">
                                    <h2 className="article-title">{article.title}</h2>
                                    <p className="article-description">{article.description}</p>
                                    <a
                                        href={article.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="read-more"
                                    >
                                        Read More
                                    </a>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p>No articles found.</p>
                )}
            </div>
        </div>
    );
}

export default MainFeed;
