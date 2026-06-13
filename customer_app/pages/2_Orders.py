import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from utils.styles import inject
from utils.auth import require_login
from models.order_model import OrderModel, STATUSES

st.set_page_config(page_title="Orders · FoodRush", page_icon="📦", layout="wide")
inject()
st.title("📦 My Orders")
user = require_login("customer")

om = OrderModel()
orders = om.list_for_user(user["email"])
if not orders:
    st.info("No orders yet.")
    st.stop()

# Auto-refresh for live tracking
st.caption("Tip: refresh the page to see live status updates from the restaurant.")
if st.button("🔄 Refresh"):
    st.rerun()

for o in orders:
    with st.container(border=True):
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"**Order `{str(o['_id'])[:8]}`** · {o['created_at'].strftime('%d %b %Y, %H:%M')}")
            for it in o["items"]:
                st.write(f"• {it['name']} × {it['qty']} — ₹{it['price']*it['qty']}")
            st.markdown(f"**Total: ₹{o['total']}** · {o['payment_method']}")
        with c2:
            st.markdown(f"### {o['status']}")
        # Progress bar
        flow = ["Placed", "Accepted", "Preparing", "Ready", "Out for Delivery", "Delivered"]
        if o["status"] in flow:
            step = flow.index(o["status"]) + 1
            st.progress(step / len(flow), text=" → ".join(flow[:step]))
        elif o["status"] == "Cancelled":
            st.error("Cancelled")
