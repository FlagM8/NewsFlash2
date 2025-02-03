from main import celery as celer
from celery.schedules import crontab
from getNews import fetch_news, get_top_news, remove_news

celer.conf.beat_schedule = {
    "fetch_news_every_hour": {
        "task": "getNews.fetch_news",
        "schedule": crontab(minute=0, hour="*"),  # Every hour
    },
    "fetch_top_news_every_6_hours": {
        "task": "getNews.get_top_news",
        "schedule": crontab(minute=0, hour="*/6"),  # Every 6 hours
    },
    "remove_old_news_daily": {
        "task": "getNews.remove_news",
        "schedule": crontab(minute=0, hour=0),  # Daily at midnight
    },
}

@celer.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(0, fetch_news.s(), name="fetch_news_now")
