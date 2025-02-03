from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis
from dotenv import load_dotenv
from celery import Celery
import json
#from tasks import celery_tasks
import os

load_dotenv()
# Database configuration
MONGO_URI = os.environ.get('MONGO_URI')

REDIS_URI = os.environ.get('REDIS_URL')

#app.config['CORS_HEADERS'] = 'Content-Type'

# instantiate the app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.config["JWT_SECRET_KEY"] = os.environ.get('SECRET_KEY')

app.config["REDIS_URL"] = REDIS_URI
redis_client = FlaskRedis(app)


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["REDIS_URL"],
        broker=app.config["REDIS_URL"],
        worker_concurrency=1
    )
    celery.conf.update(app.config)

    return celery

celery = make_celery(app)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000",
                             "allow_headers": ["Content-Type", "Authorization"],
                             "supports_credentials": True}})


# instiantiate JSON Web Token authentication
jwt = JWTManager(app)
# pymongo config
app.config["MONGO_URI"] = 'mongodb://root:example@mongodb:27017/admin'
mongo = PyMongo(app)

# create collection instances
db_users = mongo.db.users
db_news = mongo.db.news

# register blueprints

from routes.users import bp_users
app.register_blueprint(bp_users)

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response

@app.before_request
def before_request():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response
    
"""from celery.schedules import crontab
from getNews import fetch_news, get_top_news, remove_news

celery.conf.beat_schedule = {
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
"""

# Register periodic tasks
#@celery.on_after_finalize.connect
#def setup_periodic_tasks(sender, **kwargs):
#    sender.add_periodic_task(0, fetch_news.s(), name="fetch_news_now")
#    sender.add_periodic_task(crontab(minute=0, hour="*"), fetch_news.s(), name="fetch_news_every_hour")
#    sender.add_periodic_task(crontab(minute=0, hour="*/6"), get_top_news.s(), name="fetch_top_news_every_6_hours")
#    sender.add_periodic_task(crontab(minute=0, hour=0), remove_news.s(), name="remove_old_news_daily")
    


#with app.app_context():
#    fetch_news.apply_async()

#fetch_news()
with open("news_data.json", "r", encoding="utf-8") as f:
    news_list = json.load(f)

db_news.insert_many(news_list)
@app.route("/check", methods=["GET"])
def check_db():
    test = db_news.find_one({"category":"BUSINESS"})
    if test:
        return jsonify({"success": True, "news": test})
    else:
        return "No news found"
