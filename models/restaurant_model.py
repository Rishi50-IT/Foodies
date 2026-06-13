from bson import ObjectId
from database.mongodb import get_db


class RestaurantModel:
    def __init__(self):
        self.db = get_db()

    def all(self, limit=100):
        return list(self.db.restaurants.find().limit(limit))

    def get(self, rid):
        return self.db.restaurants.find_one({"_id": ObjectId(rid)})

    def get_by_owner(self, email):
        return self.db.restaurants.find_one({"owner_email": email})

    def update(self, rid, fields):
        self.db.restaurants.update_one({"_id": ObjectId(rid)}, {"$set": fields})

    def popular(self, limit=10):
        return list(self.db.restaurants.find().sort("rating", -1).limit(limit))
