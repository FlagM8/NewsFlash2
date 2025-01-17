from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os

def create_app():
    # Load environment variables
    load_dotenv()

    # Initialize Flask app
    app = Flask(__name__)

    # CORS Configuration
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Database configuration
    MONGO_URI = os.environ.get('MONGO_URI')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['CORS_HEADERS'] = 'Content-Type'

    # MongoDb
    client = MongoClient(MONGO_URI)
    db = client["nsdb"]
    
    return app, db, CORS