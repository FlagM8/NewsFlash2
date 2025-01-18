from pygooglenews import GoogleNews
from main import app, celery, r, mongo

@celery.task(bind=True)
def fetch_news(self):
