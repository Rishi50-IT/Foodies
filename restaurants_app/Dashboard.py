"""Restaurant Admin App — Dashboard.
Run: streamlit run restaurant_app/Dashboard.py --server.port 8502
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

from utils.styles import inject
from utils.auth import RestaurantAuth
from models.order_model import OrderModel
from models.food_model import FoodModel

st.set_page_config(page_title="FoodRush Admin", page_icon="🏪", layout="wide")
inject()

st.session_state.setdefault("restaurant", None)


def auth_sidebar():
    auth = RestaurantAuth()
    with st.sidebar:
        st.markdown("## 🏪 Restaurant Admin")
        if st.session_state.restaurant:
            r = st.session_state.restaurant
            st.success(f"Logged in: {r['name']}")
            if st.button("Logout"):
                st.session_state.restaurant = None
                st.rerun()
            return
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            e = st.text_input("Email", key="rli_e")
            p = st.text_input("Password", type="password", key="rli_p")
            if st.button("Login"):
                ok, res = auth.login(e, p)
                if ok:
                    st.session_state.restaurant = res
                    st.rerun()
                else:
                    st.error(res)
        with tab2:
            rn = st.text_input("Restaurant Name", key="rs_rn")
            on_ = st.text_input("Owner Name", key="rs_on")
            e = st.text_input("Email", key="rs_e")
            ph = st.text_input("Phone", key="rs_ph")
            ad = st.text_input("Address", key="rs_ad")
            p = st.text_input("Password", type="password", key="rs_p")
            if st.button("Register"):
                ok, msg = auth.signup(rn, on_, e, ph, p, ad)
                st.success(msg) if ok else st.error(msg)


auth_sidebar()
if not st.session_state.restaurant:
    st.info("Login to view your dashboard. Try `owner1@foodrush.dev` / `password123`")
    st.stop()

r = st.session_state.restaurant
st.markdown(f'<div class="fr-hero"><h1>{r["name"]}</h1><p>Owner Dashboard</p></div>',
            unsafe_allow_html=True)

om = OrderModel()
fm = FoodModel()
orders = om.list_for_restaurant(r["_id"])
foods = fm.by_restaurant(r["_id"])

# KPIs
revenue = sum(o["total"] for o in orders if o["status"] == "Delivered")
total_orders = len(orders)
customers = len({o["user_email"] for o in orders})

k1, k2, k3, k4 = st.columns(4)
k1.metric("💰 Revenue", f"₹{revenue:,.0f}")
k2.metric("📦 Orders", total_orders)
k3.metric("👥 Customers", customers)
k4.metric("🍽 Menu Items", len(foods))

# Charts
if orders:
    df = pd.DataFrame([{
        "date": o["created_at"].date(),
        "total": o["total"],
        "status": o["status"],
    } for o in orders])

    daily = df.groupby("date")["total"].sum().reset_index()
    fig = px.line(daily, x="date", y="total", title="Daily Sales (₹)", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    by_status = df["status"].value_counts().reset_index()
    by_status.columns = ["status", "count"]
    fig2 = px.pie(by_status, names="status", values="count", title="Orders by Status",
                  hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

    # Popular items
    item_counts = {}
    for o in orders:
        for it in o["items"]:
            item_counts[it["name"]] = item_counts.get(it["name"], 0) + it["qty"]
    pop_df = pd.DataFrame(sorted(item_counts.items(), key=lambda x: -x[1])[:8],
                          columns=["item", "qty"])
    fig3 = px.bar(pop_df, x="item", y="qty", title="Top-selling Items",
                  color="qty", color_continuous_scale="Oranges")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("No orders yet — your charts will appear here once customers place orders.")
