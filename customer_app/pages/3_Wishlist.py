import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from utils.styles import inject
from utils.auth import require_login
from database.mongodb import get_db

st.set_page_config(page_title="Wishlist · FoodRush", page_icon="❤️", layout="wide")
inject()
st.title("❤️ Wishlist")
user = require_login("customer")

db = get_db()
items = list(db.wishlist.find({"user_email": user["email"]}))
if not items:
    st.info("Your wishlist is empty.")
    st.stop()

cols = st.columns(3)
for i, it in enumerate(items):
    with cols[i % 3]:
        st.image(it["image"], use_container_width=True)
        st.markdown(f"**{it['name']}** — ₹{it['price']}")
        if st.button("Remove", key=f"wlrm_{it['_id']}"):
            db.wishlist.delete_one({"_id": it["_id"]})
            st.rerun()
