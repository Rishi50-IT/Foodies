import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from utils.styles import inject
from utils.auth import require_login
from utils.cloudinary_upload import upload_image
from models.food_model import FoodModel

st.set_page_config(page_title="Menu · Admin", page_icon="🍽", layout="wide")
inject()
r = require_login("restaurant")
fm = FoodModel()

st.title("🍽 Menu Management")

tab1, tab2 = st.tabs(["➕ Add Item", "✏️ Manage Items"])

CATS = ["Pizza", "Burger", "Biryani", "Chinese", "North Indian",
        "South Indian", "Desserts", "Ice Cream", "Drinks", "Fast Food"]

with tab1:
    with st.form("add_food", clear_on_submit=True):
        c1, c2 = st.columns(2)
        name = c1.text_input("Name")
        cat = c2.selectbox("Category", CATS)
        desc = st.text_area("Description")
        ingr = st.text_input("Ingredients")
        c3, c4, c5 = st.columns(3)
        mrp = c3.number_input("MRP (₹)", min_value=1, value=299)
        disc = c4.slider("Discount %", 0, 80, 20)
        prep = c5.number_input("Prep time (min)", min_value=1, value=20)
        c6, c7, c8 = st.columns(3)
        qty = c6.number_input("Stock qty", min_value=0, value=20)
        veg = c7.checkbox("Vegetarian", True)
        best = c8.checkbox("Bestseller")
        imgs = st.file_uploader("Upload images (multi)", accept_multiple_files=True,
                                type=["png", "jpg", "jpeg"])
        if st.form_submit_button("Add Item"):
            urls = []
            for f in (imgs or []):
                u = upload_image(f)
                if u:
                    urls.append(u)
            if not urls:
                urls = ["https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600"]
            price = int(mrp * (100 - disc) / 100)
            fm.add({
                "restaurant_id": str(r["_id"]),
                "name": name, "category": cat, "description": desc,
                "ingredients": ingr, "images": urls,
                "price": price, "mrp": mrp, "discount": disc,
                "rating": 4.0, "quantity": qty, "prep_time": prep,
                "available": True, "veg": veg, "bestseller": best,
            })
            st.success(f"Added {name}")

with tab2:
    items = fm.by_restaurant(r["_id"])
    if not items:
        st.info("No items yet.")
    for it in items:
        with st.container(border=True):
            c1, c2, c3 = st.columns([1, 3, 2])
            c1.image(it["images"][0], width=120)
            c2.markdown(
                f"**{it['name']}** · {it['category']}  \n"
                f"₹{it['price']} (MRP ₹{it['mrp']}, {it['discount']}% off)  \n"
                f"Stock: {it['quantity']} · {'🟢 Available' if it['available'] else '🔴 Disabled'}"
            )
            with c3:
                new_price = st.number_input("Price", value=it["price"], key=f"pr_{it['_id']}")
                if st.button("Update price", key=f"up_{it['_id']}"):
                    fm.update(str(it["_id"]), {"price": int(new_price)})
                    st.rerun()
                if st.button("Toggle availability", key=f"av_{it['_id']}"):
                    fm.update(str(it["_id"]), {"available": not it["available"]})
                    st.rerun()
                if st.button("🗑 Delete", key=f"dl_{it['_id']}"):
                    fm.delete(str(it["_id"]))
                    st.rerun()
