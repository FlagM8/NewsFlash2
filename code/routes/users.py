from flask import jsonify, request
from bson import json_util, ObjectId
from flask import Blueprint, jsonify
from flask_cors import cross_origin
from main import db_users, db_news, app, redis_client
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta


bp_users = Blueprint('users', __name__)

#app.register_blueprint(bp_users)
@bp_users.route("/signup", methods=["POST"])
@cross_origin(origins='*')
def signup():
    credentials = request.json
    username = credentials.get("username")
    password = credentials.get('password')
    email = credentials.get("email")
    topics = credentials.get("topics")
    
    username_query = {"username": username}
    username_result = db_users.find_one(username_query)
    email_query = {"email": email}
    email_result = db_users.find_one(email_query)

    data_packet = {}
    if username_result:
        data_packet["status"] = "Username already exists"
        return json_util.dumps(data_packet), 401
    elif email_result:
        data_packet["status"] = "Email already exists"
        return json_util.dumps(data_packet), 401
    
    hashed_password = generate_password_hash(password)
    topics = [topic.upper() for topic in topics]
    user_object = User(username=username, password_hash=hashed_password, email=email, topics=topics)
    user_object.quicksave_to_db()

    retrieved_user_data = db_users.find_one({"username": username})
    if retrieved_user_data:
        retrieved_user_data["_id"] = str(retrieved_user_data["_id"])
        access_token = create_access_token(identity=username, expires_delta=timedelta(hours=1))
        return json_util.dumps({"access_token": access_token,
                            "user_data": retrieved_user_data,
                            "status": "Success"}), 201
    else:
        data_packet["status"] = "Error"
        return json_util.dumps(data_packet), 500


@bp_users.route('/login', methods=['POST'])
def login():
    credentials = request.json
    username = credentials.get('username')
    password = credentials.get('password')
    username_query = {"username": username}
    user_data = db_users.find_one(username_query)
    if not user_data:
        return json_util.dumps({'status': 'Invalid username'}), 401
    hashed_password = user_data.get("password_hash")
    if not check_password_hash(hashed_password, password):
        return json_util.dumps({'status': 'Incorrect password'}), 401
    access_token = create_access_token(identity=username, expires_delta=timedelta(hours=1)) 
    retrieved_user_data = db_users.find_one({"username": username})
    if retrieved_user_data:
        retrieved_user_data["_id"] = str(retrieved_user_data["_id"]) 
    return json_util.dumps({"token": access_token,
                            "user_data": retrieved_user_data,
                            "status": "Success"}), 200
@bp_users.route('/getnews', methods=['GET'])
@jwt_required()
def get_news():
    username = get_jwt_identity()
    news_key = f"news:{username}"
    news = redis_client.get(news_key)
    if news:
        news = json_util.loads(news)
    else:
        user_preferences = db_users.find_one({"username": username}).get("topics", [])
        if not user_preferences:
            return json_util.dumps({"success": False, "message": "No preferences found for the user."}), 404
        news = list(db_news.aggregate([
            {"$match": {"category": {"$in": user_preferences}}},
            {"$sample": {"size": 15}}
        ]))
        if not news:
            return json_util.dumps({"success": False, "message": "No news articles found matching user preferences."}), 404 
        redis_client.set(news_key, json_util.dumps(news), ex=10800)
    return app.response_class(
        response=json_util.dumps({"success": True, "news": news}), 
        mimetype="application/json"
    )

@bp_users.route("/user/<user>", methods=["GET"])
def user(user):
    news_list = list(db_chapters.find({"username": user}))
    #sorted_chapter_list = sorted(chapter_list, key=lambda x: x["created_at"])

    for chapter in sorted_chapter_list:
        chapter["created_at"] = Chapter.format_date_data(chapter["created_at"])
        user_data = db_users.find_one({"username": chapter["username"]})
        chapter["picture"] = user_data["picture"]
        story = db_stories.find_one({"_id": chapter["story_id"]})
        chapter["story_name"] = story["title"]
        chapter["comments"] = story["comments"]
    
    user_data = db_users.find_one({"username": user})
    
    data_packet = {
        "user_data": user_data,
        "posts": sorted_chapter_list[::-1]
    }

    return json_util.dumps(data_packet)


@bp_users.route("/settings/<user>", methods=["GET"])
def get_settings(user):
    user_data = db_users.find_one({"username": user})
    settings_data = {
        "color": user_data["color"],
        "bio": user_data["bio"],
        "picture": user_data["picture"]
    }

    return json_util.dumps(settings_data)

@bp_users.route('/follow', methods=['POST'])
@jwt_required()
def follow():
    data = request.json
    if data.get("action") == "follow":
        User.add_follower(data.get("user_being_followed"), data.get("user_follows"))
        return json_util.dumps("Success")
    
    else:
        User.remove_follower(data.get("user_being_followed"), data.get("user_follows"))
        return json_util.dumps("Success")
    
@bp_users.route("/update_settings", methods=["POST"])
@jwt_required()
def update_user_settings():
    data = request.json
    user_query = {"username": data["username"]}
    updated_settings = {
        "$set": {
            "picture": data["selectedImage"],
            "bio": data["selectedBio"],
            "color": data["selectedColor"]
        }
    }
    db_users.update_one(user_query, updated_settings)

    fetched_user_data = db_users.find_one({"username": data["username"]})

    return json_util.dumps({
        "status": "Success",
        "updated_user_data": fetched_user_data
    })    


@bp_users.route('/check-token', methods=['GET'])
@jwt_required()
def check_token():
    try:
        username = get_jwt_identity()
        user_data = db_users.find_one({"username": username})
        if user_data:
            return json_util.dumps({'expired': False, 'userData': user_data}), 200
        else:
            return json_util.dumps({'expired': True}), 404
    except Exception as e:
        return json_util.dumps({'expired': True, 'error': str(e)}), 401
    
@bp_users.route("/update-profile", methods=["POST"])
@jwt_required()
def update_profile():
    username = get_jwt_identity()
    data = request.json
    topics = data.get("topics", [])

    if not topics or not isinstance(topics, list):
        return jsonify({"status": "Invalid topics"}), 400

    topics = [topic.upper() for topic in topics]

    db_users.update_one({"username": username}, {"$set": {"topics": topics}})

    redis_key = f"news:{username}"
    redis_client.delete(redis_key)

    return jsonify({"status": "Profile updated successfully"}), 200