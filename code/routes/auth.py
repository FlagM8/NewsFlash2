from flask import Blueprint, request, jsonify, current_app
from main import db, app, CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import utils

bcrypt = Bcrypt()
#auth = Blueprint("auth", __name__)

#CORS(auth, resources={r"/*": {"origins": "http://localhost:8080"}}, supports_credentials=True)
#app.register_blueprint(auth, url_prefix="/auth")

"""
@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
    user = {
        "username": data['username'],
        "email": data['email'],
        "password": hashed_password,
        "preferences": []
    }
    db.users.insert_one(user)
    return jsonify({"message": "User registered successfully"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    user = db.users.find_one({"username": data['username']})
    if user and bcrypt.check_password_hash(user['password'], data['password']):
        token = create_access_token(identity=user['username'])
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401 """

# Registration endpoint
@current_app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400
    
    hashed_password = generate_password_hash(data['password'], method='sha256')
    user = {
        "email": data['email'],
        "password": hashed_password,
        "username": data.get('username', {})
    }
    
    if utils.findUser(email=data['email'], username=data['username']):
        return jsonify({"error": "User already exists"}), 409
    
    db.users.insert_one(user)
    return jsonify({"message": "User registered successfully"}), 201

# Login endpoint
@current_app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = utils.findUser(email=data['email'], username=data['username'])
    
    if not user or not check_password_hash(user['password'], data['password']):
        return jsonify({"error": "Invalid credentials"}), 401
    
    token = jwt.encode({
        "user_id": str(user['_id']),
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")
    
    return jsonify({"token": token}), 200

