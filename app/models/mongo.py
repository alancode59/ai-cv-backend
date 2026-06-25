import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "ai_cv_db")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]


def get_database():
    return db
