from bson import ObjectId
from database.mongodb import get_db


class FoodModel:
    def __init__(self):
        self.db = get_db()

    def all(self, filters=None, limit=200):
        q = filters or {}
        return list(self.db.food_items.find(q).limit(limit))

    def get(self, fid):
        return self.db.food_items.find_one({"_id": ObjectId(fid)})

    def by_restaurant(self, rid):
        return list(self.db.food_items.find({"restaurant_id": str(rid)}))

    def by_category(self, cat):
        return list(self.db.food_items.find({"category": cat}))

    def add(self, doc):
        return self.db.food_items.insert_one(doc).inserted_id

    def update(self, fid, fields):
        self.db.food_items.update_one({"_id": ObjectId(fid)}, {"$set": fields})

    def delete(self, fid):
        self.db.food_items.delete_one({"_id": ObjectId(fid)})

    def bestsellers(self, limit=10):
        return list(self.db.food_items.find({"bestseller": True}).limit(limit))

    def trending(self, limit=10):
        return list(self.db.food_items.find().sort("rating", -1).limit(limit))
