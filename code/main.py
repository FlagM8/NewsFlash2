from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis
from dotenv import load_dotenv
import os

load_dotenv()
# Database configuration
MONGO_URI = os.environ.get('MONGO_URI')

REDIS_URI = os.environ.get('REDIS_URL')

#app.config['CORS_HEADERS'] = 'Content-Type'

# instantiate the app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

redis_client = FlaskRedis(app)
app.config["REDIS_URL"] = REDIS_URI

# enable CORS
CORS(app, resources={r'/*': {'origins': "*"}})

# instiantiate JSON Web Token authentication
jwt = JWTManager(app)
# pymongo config
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)

# create collection instances
db_users = mongo.db.users
db_news = mongo.db.news

# register blueprints

from routes.users import bp_users
app.register_blueprint(bp_users)
