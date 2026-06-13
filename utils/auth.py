"""Authentication helpers using bcrypt."""
import bcrypt
import streamlit as st
from database.mongodb import get_db


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(password: str, hashed) -> bool:
    if isinstance(hashed, str):
        hashed = hashed.encode()
    try:
        return bcrypt.checkpw(password.encode(), hashed)
    except Exception:
        return False


class CustomerAuth:
    def __init__(self):
        self.db = get_db()

    def signup(self, name, email, phone, password):
        if self.db.users.find_one({"email": email}):
            return False, "Email already registered"
        self.db.users.insert_one({
            "name": name, "email": email, "phone": phone,
            "password": hash_password(password),
        })
        return True, "Signup successful"

    def login(self, email, password):
        user = self.db.users.find_one({"email": email})
        if not user or not verify_password(password, user["password"]):
            return False, "Invalid email or password"
        return True, user


class RestaurantAuth:
    def __init__(self):
        self.db = get_db()

    def signup(self, restaurant_name, owner_name, email, phone, password, address):
        if self.db.restaurants.find_one({"owner_email": email}):
            return False, "Email already registered"
        self.db.restaurants.insert_one({
            "name": restaurant_name,
            "owner_name": owner_name,
            "owner_email": email,
            "phone": phone,
            "password": hash_password(password),
            "address": address,
            "rating": 4.2,
            "cuisine": "Multi-Cuisine",
            "delivery_time": 30,
            "distance_km": 2.5,
            "cover_image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
            "logo": "https://images.unsplash.com/photo-1555992336-fb0d29498b13?w=200",
            "free_delivery": True,
            "discount_badge": "20% OFF",
        })
        return True, "Restaurant registered"

    def login(self, email, password):
        rest = self.db.restaurants.find_one({"owner_email": email})
        if not rest or not verify_password(password, rest["password"]):
            return False, "Invalid email or password"
        return True, rest


def require_login(kind="customer"):
    """Gate a Streamlit page on session login."""
    key = "user" if kind == "customer" else "restaurant"
    if key not in st.session_state or st.session_state[key] is None:
        st.warning("Please login first.")
        st.stop()
    return st.session_state[key]
