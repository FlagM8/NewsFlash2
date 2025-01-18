import React from 'react';
import './articlecard.css';

function ArticleCard({ article }) {
    const { title, description, url, urlToImage } = article;

    return (
        <div className="article-card">
            {urlToImage && (
                <img
                    src={urlToImage}
                    alt={title}
                    className="article-image"
                />
            )}
            <div className="article-details">
                <h2 className="article-title">{title}</h2>
                <p className="article-description">{description}</p>
                <a
                    href={url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="read-more"
                >
                    Read More
                </a>
            </div>
        </div>
    );
}

export default ArticleCard;
