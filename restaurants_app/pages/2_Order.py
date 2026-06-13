import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from utils.styles import inject
from utils.auth import require_login
from models.order_model import OrderModel, STATUSES

st.set_page_config(page_title="Orders · Admin", page_icon="📋", layout="wide")
inject()
r = require_login("restaurant")
om = OrderModel()

st.title("📋 Incoming Orders")
if st.button("🔄 Refresh"):
    st.rerun()

orders = om.list_for_restaurant(r["_id"])
if not orders:
    st.info("No orders yet.")
    st.stop()

flow = {
    "Placed": ["Accepted", "Cancelled"],
    "Accepted": ["Preparing"],
    "Preparing": ["Ready"],
    "Ready": ["Out for Delivery"],
    "Out for Delivery": ["Delivered"],
}

for o in orders:
    with st.container(border=True):
        c1, c2 = st.columns([3, 2])
        with c1:
            st.markdown(f"**Order `{str(o['_id'])[:8]}`** · {o['created_at'].strftime('%d %b %H:%M')}")
            st.caption(f"Customer: {o['user_email']} · {o['payment_method']}")
            for it in o["items"]:
                st.write(f"• {it['name']} × {it['qty']} — ₹{it['price']*it['qty']}")
            st.markdown(f"**Total: ₹{o['total']}**")
            addr = o.get("address", {})
            st.caption(f"📍 {addr.get('line','')}, {addr.get('city','')} — {addr.get('pincode','')}")
        with c2:
            st.markdown(f"### Status: {o['status']}")
            next_steps = flow.get(o["status"], [])
            for ns in next_steps:
                if st.button(f"➡ {ns}", key=f"{o['_id']}_{ns}"):
                    om.set_status(str(o["_id"]), ns)
                    st.rerun()
