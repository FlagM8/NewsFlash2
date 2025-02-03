from pygooglenews import GoogleNews
from newspaper import Article, Config
import nltk
import json
from googlenewsdecoder import new_decoderv1
from datetime import datetime, timedelta
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Download necessary nltk data
nltk.download('punkt_tab')

# MongoDB Connection
MONGO_URI = "mongodb://root:example@mongodb:27017/admin"
client = MongoClient(MONGO_URI)
db = client.get_database("admin")
db_news = db.news  # Collection for news articles

# Google News API and scraping settings
gn = GoogleNews(lang="en")
tags = ["WORLD", "NATION", "BUSINESS", "TECHNOLOGY", "ENTERTAINMENT", "SCIENCE", "SPORTS", "HEALTH"]

# Configure newspaper3k
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent

# Selenium WebDriver setup
"""options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)"""

def get_final_url(redirect_url):
    """Uses Selenium to get the final redirected URL."""
    try:
        driver.get(redirect_url)
        return driver.current_url
    except Exception as e:
        print(f"Error retrieving final URL: {e}")
        return None

def fetch_news():
    """Fetches news articles and saves them to MongoDB."""
    for tag in tags:
        news = gn.topic_headlines(tag)
        for article in news['entries']:
            try:
                alink = article["link"]
                #final_url = get_final_url(alink) if alink else None
                final_url = new_decoderv1(alink)
                print(final_url['decoded_url'])
                if not final_url:
                    continue
                conv_link = final_url['decoded_url']
                print(conv_link)
                art = Article(conv_link, config=config)
                art.download()
                art.parse() 
                art.nlp()
                
                news_data = {
                    "url": final_url,
                    "title": art.title,
                    "summary": art.summary,
                    "image": art.top_image,
                    "category": tag,
                    "tags": art.keywords,
                    "date": datetime.utcnow()
                }
                db_news.insert_one(news_data)
                print(f"Inserted: {art.title}")
                
            except Exception as e:
                print(f"Error parsing article: {e}")

def remove_old_news():
    """Removes news older than 24 hours."""
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    db_news.delete_many({"date": {"$lt": one_day_ago}})
    print("Old news removed.")

if __name__ == "__main__":
    fetch_news()
    #remove_old_news()
