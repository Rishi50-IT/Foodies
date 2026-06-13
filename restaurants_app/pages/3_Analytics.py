import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.styles import inject
from utils.auth import require_login
from models.order_model import OrderModel

st.set_page_config(page_title="Analytics · Admin", page_icon="📈", layout="wide")
inject()
r = require_login("restaurant")
om = OrderModel()
orders = om.list_for_restaurant(r["_id"])

st.title("📈 Analytics")

if not orders:
    st.info("Once you receive orders, analytics will appear here.")
    st.stop()

df = pd.DataFrame([{
    "date": o["created_at"].date(),
    "hour": o["created_at"].hour,
    "weekday": o["created_at"].strftime("%a"),
    "month": o["created_at"].strftime("%Y-%m"),
    "total": o["total"],
    "status": o["status"],
    "items": sum(i["qty"] for i in o["items"]),
} for o in orders])

# Revenue
daily = df.groupby("date")["total"].sum().reset_index()
st.plotly_chart(px.area(daily, x="date", y="total", title="Revenue Over Time"),
                use_container_width=True)

# Peak hours
hourly = df.groupby("hour")["total"].count().reset_index(name="orders")
st.plotly_chart(px.bar(hourly, x="hour", y="orders", title="Peak Hours",
                       color="orders", color_continuous_scale="Reds"),
                use_container_width=True)

c1, c2 = st.columns(2)
weekly = df.groupby("weekday")["total"].sum().reset_index()
c1.plotly_chart(px.bar(weekly, x="weekday", y="total", title="Weekly Sales"),
                use_container_width=True)
monthly = df.groupby("month")["total"].sum().reset_index()
c2.plotly_chart(px.bar(monthly, x="month", y="total", title="Monthly Sales"),
                use_container_width=True)

# Top items
item_counts = {}
for o in orders:
    for it in o["items"]:
        item_counts[it["name"]] = item_counts.get(it["name"], 0) + it["qty"]
pop = pd.DataFrame(sorted(item_counts.items(), key=lambda x: -x[1])[:10],
                   columns=["item", "qty"])
st.plotly_chart(px.bar(pop, x="item", y="qty", title="Top-selling Items"),
                use_container_width=True)
