"""from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
from routes.auth import auth


# Load environment variables from .env file
load_dotenv() 

MONGO_URI = os.environ.get('MONGO_URI')
SECRET_KEY = os.environ.get('SECRET_KEY')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:8080", "http://frontend:8080"]}})
app.register_blueprint(auth, url_prefix="/auth")
app.config['SECRET_KEY'] = SECRET_KEY 
app.config['CORS_HEADERS'] = 'Content-Type'
client = MongoClient(MONGO_URI)
db = client["nsdb"]


@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = app.make_response('')
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:8080"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
        return response
"""


from flask import Flask, request, jsonify
from main_factory import create_app
#from routes.auth import auth

# Create the app and db instance
app, db, CORS = create_app()

# Register the auth blueprint
#app.register_blueprint(auth, url_prefix="/register")

@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = app.make_response('')
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:8080"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
        return response
@app.route('/register', methods=['POST', 'GET'])
def register():
    return jsonify({"message": "User registered successfully"}), 201
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)