from database.mongodb import get_db


class UserModel:
    def __init__(self):
        self.db = get_db()

    def get(self, email):
        return self.db.users.find_one({"email": email})

    def update(self, email, fields: dict):
        self.db.users.update_one({"email": email}, {"$set": fields})

    # Addresses
    def add_address(self, email, address):
        self.db.addresses.insert_one({"user_email": email, **address})

    def list_addresses(self, email):
        return list(self.db.addresses.find({"user_email": email}))

    def delete_address(self, address_id):
        from bson import ObjectId
        self.db.addresses.delete_one({"_id": ObjectId(address_id)})
