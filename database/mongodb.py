"""MongoDB connection singleton."""
import os
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv

load_dotenv()


class MongoDB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            uri = os.getenv("MONGO_URI","mongodb+srv://Rishi_Munda:Rahul124%40@cluster0.dod06ln.mongodb.net/?appName=Cluster0")
            db_name = os.getenv("MONGO_DB", "foodrush")
            cls._instance.client = MongoClient(uri, serverSelectionTimeoutMS=8000)
            cls._instance.db = cls._instance.client[db_name]
            cls._instance._ensure_indexes()
        return cls._instance

    def _ensure_indexes(self):
        self.db.users.create_index([("email", ASCENDING)], unique=True)
        self.db.restaurants.create_index([("owner_email", ASCENDING)])
        self.db.food_items.create_index([("restaurant_id", ASCENDING)])
        self.db.food_items.create_index([("category", ASCENDING)])
        self.db.orders.create_index([("user_email", ASCENDING)])
        self.db.orders.create_index([("restaurant_id", ASCENDING)])
        self.db.cart.create_index([("user_email", ASCENDING)])
        self.db.wishlist.create_index([("user_email", ASCENDING)])

    def __getitem__(self, name):
        return self.db[name]


def get_db():
    return MongoDB().db
