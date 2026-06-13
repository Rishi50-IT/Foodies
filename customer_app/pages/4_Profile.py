import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from utils.styles import inject
from utils.auth import require_login
from models.user_model import UserModel
from database.mongodb import get_db

st.set_page_config(page_title="Profile · FoodRush", page_icon="👤", layout="wide")
inject()
st.title("👤 My Profile")
user = require_login("customer")
um = UserModel()
db = get_db()

st.subheader("Account")
st.write(f"**Name:** {user['name']}")
st.write(f"**Email:** {user['email']}")
st.write(f"**Phone:** {user.get('phone','—')}")

st.divider()
st.subheader("📍 Addresses")
for a in um.list_addresses(user["email"]):
    c1, c2 = st.columns([5, 1])
    c1.write(f"**{a.get('label','Address')}** — {a.get('line','')}, {a.get('city','')} — {a.get('pincode','')}")
    if c2.button("Delete", key=f"da_{a['_id']}"):
        um.delete_address(str(a["_id"]))
        st.rerun()

with st.form("add_addr"):
    st.markdown("**Add new address**")
    label = st.text_input("Label (Home / Work)")
    line = st.text_input("Street")
    city = st.text_input("City")
    pincode = st.text_input("Pincode")
    if st.form_submit_button("Save"):
        um.add_address(user["email"], {
            "label": label, "line": line, "city": city, "pincode": pincode,
        })
        st.rerun()

st.divider()
st.subheader("🔔 Notifications")
notes = list(db.notifications.find({"user_email": user["email"]}).sort("created_at", -1).limit(20))
if not notes:
    st.caption("No notifications yet.")
for n in notes:
    st.write(f"• {n['message']} — _{n['created_at'].strftime('%d %b %H:%M')}_")
