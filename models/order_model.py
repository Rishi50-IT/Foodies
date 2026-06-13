from bson import ObjectId
from datetime import datetime
from database.mongodb import get_db

STATUSES = ["Placed", "Accepted", "Preparing", "Ready",
            "Out for Delivery", "Delivered", "Cancelled"]


class OrderModel:
    def __init__(self):
        self.db = get_db()

    def create(self, user_email, restaurant_id, items, address, payment_method):
        subtotal = sum(i["price"] * i["qty"] for i in items)
        delivery_fee = 0 if subtotal > 299 else 29
        gst = round(subtotal * 0.05, 2)
        total = round(subtotal + delivery_fee + gst, 2)
        doc = {
            "user_email": user_email,
            "restaurant_id": str(restaurant_id),
            "items": items,
            "address": address,
            "payment_method": payment_method,
            "subtotal": subtotal,
            "delivery_fee": delivery_fee,
            "gst": gst,
            "total": total,
            "status": "Placed",
            "created_at": datetime.utcnow(),
        }
        res = self.db.orders.insert_one(doc)
        doc["_id"] = res.inserted_id
        self.db.notifications.insert_one({
            "user_email": user_email,
            "message": f"Order placed (₹{total})",
            "created_at": datetime.utcnow(),
            "read": False,
        })
        return doc

    def list_for_user(self, email):
        return list(self.db.orders.find({"user_email": email}).sort("created_at", -1))

    def list_for_restaurant(self, rid):
        return list(self.db.orders.find({"restaurant_id": str(rid)}).sort("created_at", -1))

    def set_status(self, oid, status):
        self.db.orders.update_one({"_id": ObjectId(oid)}, {"$set": {"status": status}})
        order = self.db.orders.find_one({"_id": ObjectId(oid)})
        if order:
            self.db.notifications.insert_one({
                "user_email": order["user_email"],
                "message": f"Order {str(oid)[:6]}: {status}",
                "created_at": datetime.utcnow(),
                "read": False,
            })
