from werkzeug.security import check_password_hash
from bson.objectid import ObjectId
from typing import Dict, List
import datetime, random, math
from main import db_users
#from flask import current_app as app



#db_users = app.mongo.db.users 
class User:
    def __init__(self, username, email, password_hash, topics=None, _id=None, created_at=None) -> None:
        self._id = ObjectId(_id) if _id else ObjectId()
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at or datetime.datetime.now().isoformat()
        self.topics = topics or []

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    
    def quicksave_to_db(self) -> None:
        db_users.insert_one(self.__dict__)
        
    # retrieve user data by username
    @staticmethod
    def find_by_username(username: str) -> Dict:
        return db_users.find_one({'username': username})

    # retrieve user data by email
    @staticmethod
    def find_by_email(email: str) -> Dict:
        return db_users.find_one({'email': email})

    @staticmethod
    def format_date_data(user_data: Dict) -> Dict:
        t = datetime.datetime.fromisoformat(user_data["creation_date"])
        formatted_date = t.strftime('%b %d, %Y')
        user_data["creation_date"] = formatted_date
        return user_data

    @staticmethod
    def update_topics(username, topics) -> None:
        user_query = {"username": username}
        db_users.update_one(user_query, {"$set": {"topics": topics}})