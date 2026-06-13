import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from utils.styles import inject
from utils.auth import require_login
from utils.payment import PaymentProcessor
from models.order_model import OrderModel
from models.user_model import UserModel

st.set_page_config(page_title="Cart · FoodRush", page_icon="🛒", layout="wide")
inject()
st.title("🛒 Your Cart")
user = require_login("customer")

cart = st.session_state.get("cart", [])
if not cart:
    st.info("Your cart is empty. Go add something tasty!")
    st.stop()

for idx, item in enumerate(list(cart)):
    c1, c2, c3, c4, c5 = st.columns([1, 3, 1, 1, 1])
    c1.image(item["image"], width=80)
    c2.markdown(f"**{item['name']}**  \n₹{item['price']}")
    if c3.button("−", key=f"dec_{idx}"):
        item["qty"] = max(1, item["qty"] - 1)
        st.rerun()
    c3.write(f"Qty: {item['qty']}")
    if c4.button("＋", key=f"inc_{idx}"):
        item["qty"] += 1
        st.rerun()
    if c5.button("🗑 Remove", key=f"rm_{idx}"):
        cart.pop(idx)
        st.rerun()

subtotal = sum(i["price"] * i["qty"] for i in cart)
delivery = 0 if subtotal > 299 else 29
gst = round(subtotal * 0.05, 2)
total = round(subtotal + delivery + gst, 2)

st.divider()
st.markdown("### Bill Summary")
st.write(f"Subtotal: ₹{subtotal}")
st.write(f"Delivery fee: ₹{delivery}  (free above ₹299)")
st.write(f"GST (5%): ₹{gst}")
st.markdown(f"## Grand Total: ₹{total}")

coupon = st.text_input("Coupon code")
if coupon:
    if coupon.upper() == "FOODRUSH50":
        total = round(total * 0.5, 2)
        st.success(f"Coupon applied! New total: ₹{total}")
    else:
        st.error("Invalid coupon")

st.divider()
st.markdown("### Delivery Address")
um = UserModel()
addrs = um.list_addresses(user["email"])
if addrs:
    addr_choice = st.radio(
        "Select address",
        [f"{a.get('label','Address')} — {a.get('line','')}, {a.get('city','')}" for a in addrs],
    )
    selected_addr = addrs[[f"{a.get('label','Address')} — {a.get('line','')}, {a.get('city','')}" for a in addrs].index(addr_choice)]
else:
    st.warning("No saved addresses. Add one from your Profile page.")
    st.stop()

method = st.selectbox("Payment method", PaymentProcessor.METHODS)

if st.button("🚀 Place Order", type="primary"):
    # Group by restaurant
    by_rest = {}
    for i in cart:
        by_rest.setdefault(i["restaurant_id"], []).append(i)
    om = OrderModel()
    pp = PaymentProcessor()
    for rid, items in by_rest.items():
        order = om.create(user["email"], rid, items, selected_addr, method)
        txn = pp.process(user["email"], order["total"], method, str(order["_id"]))
        st.success(f"Order placed! Total ₹{order['total']} via {method}")
        st.code(pp.invoice(txn, order))
    st.session_state.cart = []
    st.balloons()
