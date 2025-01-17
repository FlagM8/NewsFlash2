from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()
# Database configuration
MONGO_URI = os.environ.get('MONGO_URI')
#app.config['CORS_HEADERS'] = 'Content-Type'

# instantiate the app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

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

from routes.edits import bp_edits
app.register_blueprint(bp_edits)

from routes.chapters import bp_chapters
app.register_blueprint(bp_chapters)