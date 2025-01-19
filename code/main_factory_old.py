from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    # Create the Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.secret_key = os.environ.get('SECRET_KEY')
    app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
    app.config["REDIS_URL"] = os.environ.get('REDIS_URL')

    # Initialize extensions
    redis_client = FlaskRedis(app)
    jwt = JWTManager(app)
    mongo = PyMongo(app)
    CORS(app, resources={r'/*': {'origins': "*"}})

    # Register blueprints
    from routes.users import bp_users
    app.register_blueprint(bp_users)

    # Attach database instances to app
    app.mongo = mongo
    app.redis_client = redis_client

    return app