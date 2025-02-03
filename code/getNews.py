from pygooglenews import GoogleNews
from newspaper import Article, Config
import nltk
nltk.download('punkt_tab')
from googlenewsdecoder import new_decoderv1
from googlenewsdecoder import gnewsdecoder
from datetime import timedelta, datetime
from main import celery,redis_client, db_news
import json

gn = GoogleNews(lang="en")
tags = ["WORLD", "NATION", "BUSINESS", "TECHNOLOGY", "ENTERTAINMENT", "SCIENCE", "SPORTS", "HEALTH"]
articles_per_tag = 100
overall_top_news_count = 10

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com'
}

"""from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.headless = True  # Run in headless mode (without opening a browser window)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')  # Prevents issues in Docker

    # Use Service to specify the path to chromedriver
service = Service(ChromeDriverManager().install())  # Automatically download and install chromedriver

    # Initialize the WebDriver with the Service object
driver = webdriver.Chrome(service=service, options=options)"""
@celery.task(bind=True)
def get_final_url(self, redirect_url):

    try:
        driver.get(redirect_url)
        final_url = driver.current_url
    except Exception as e:
        print(f"Error occurred: {e}")
        final_url = None
    finally:
        driver.quit()

    return final_url

@celery.task(bind=True)
def fetch_news(self):
    for tag in tags:
        news = gn.topic_headlines(tag, proxies=None, scraping_bee = None)
        for article in news['entries']:
            #news_data = Parse_url(article,tag)
            try:
                alink = article["link"]
                print(alink)
                #article = gnewsdecoder(alink)
                #arurl = article['decoded_url']
                arurl = get_final_url(alink[0])
                art = Article(url=arurl, config=config)
                art.download()
                art.parse()
                art.nlp()
            except Exception as e:
                print("Err: ",e)
            news_data = ({"url": arurl, "title": art.title,"summary": art.summary, "image": art.top_image, "category": tag, "tags":art.keywords,'date': datetime.now()})
            if news_data != None:
                db_news.insert_one(news_data)

@celery.task(bind=True)
def get_top_news():
    top = gn.top_news(proxies=None, scraping_bee = None, start=1, end=15)
    for article in top['entries']:
        top_art = Parse_url(article,"Top")
        redis_client.hset(f"news:top", top_art["url"], json.dumps(top_art))
        redis_client.expire(f"news:top", 21600)

def Parse_url(article, tag):
    try:
        alink = article["link"]
        print(alink)
        article = gnewsdecoder(alink)
        arurl = article['decoded_url']
        art = Article(url=arurl, config=config)
        art.download()
        art.parse()
        art.nlp()
    except Exception as e:
        print("Err: ",e)
        return None
    print("Success")
    return({"url": arurl, "title": art.title,"summary": art.summary, "image": art.top_image, "category": tag, "tags":art.keywords,'date': datetime.now()})

@celery.task(bind=True)
def remove_news():
    one_day_ago = datetime.now() - timedelta(days=1)
    db_news.delete_many({'date': {'$lt': one_day_ago}})

