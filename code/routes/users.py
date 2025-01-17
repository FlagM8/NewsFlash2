from flask import jsonify, request
from bson import json_util
from flask import Blueprint, jsonify
from main import db_users, db_chapters, db_stories
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta


