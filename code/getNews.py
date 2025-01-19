from pygooglenews import GoogleNews
from newspaper import Article
import nltk
nltk.download('punkt_tab')
from googlenewsdecoder import new_decoderv1
from datetime import timedelta, datetime
from main import mongo,celery,redis_client, db_news

gn = GoogleNews()
tags = ["WORLD", "NATION", "BUSINESS", "TECHNOLOGY", "ENTERTAINMENT", "SCIENCE", "SPORTS", "HEALTH"]
articles_per_tag = 100
overall_top_news_count = 10

@celery.task(bind=True)
def fetch_news(self):
    for tag in tags:
        news = gn.search(tag, lang="en", start=1, end=articles_per_tag)
        for article in news:
            news_data = Parse_url(article,tag)
            if news_data != None:
                db_news.insert_one(news_data)

@celery.task(bind=True)
def get_top_news():
    top = gn.top_news(proxies=None, scraping_bee = None, start=1, end=15)
    for article in top:
        top_art = Parse_url(article,"Top")
        redis_client.hset(f"news:top", top_art["url"], top_art)
        redis_client.expire(f"news:top", 21600)

def Parse_url(article,tag):
    try:
        article = new_decoderv1(article.link)
        arurl = article["decoded_url"]
        art = Article(url=arurl)
        art.download()
        art.parse()
        art.nlp()
    except Exception as e:
         return()
    return({"url": arurl, "title": art.title,"summary": art.summary, "image": art.top_image, "category": tag, "tags":art.keywords,'date': datetime.now()})

@celery.task(bind=True)
def remove_news():
    one_day_ago = datetime.now() - timedelta(days=1)
    mongo.db.news.delete_many({'date': {'$lt': one_day_ago}})

            
