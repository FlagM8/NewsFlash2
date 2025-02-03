from main import db_news
from bson.objectid import ObjectId
from typing import Dict, List
import datetime, random, math

class News:
    def __init__(self, url, title, summary, image, category, tags, date):
        self.url = url
        self.title = title
        self.summary = summary
        self.image = image
        self.category = category
        self.tags = tags
        self.date = date
    def save_to_db(self) -> str:
        result = db_news.insert_one(self.__dict__)
        inserted_id = str(result.inserted_id)
        return inserted_id
