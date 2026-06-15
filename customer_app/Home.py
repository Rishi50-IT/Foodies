"""Customer App — Home page.
Run: streamlit run customer_app/Home.py --server.port 8501
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from utils.styles import inject
from utils.auth import CustomerAuth
from models.restaurant_model import RestaurantModel
from models.food_model import FoodModel
from database.seed import seed_if_empty

st.set_page_config(page_title="FoodRush", page_icon="🍔", layout="wide")
inject()


import streamlit as st



st.markdown("""
<style>

/* Sidebar background (no transparency) */
[data-testid="stSidebar"] {
    background-color: #2d2d2d !important;
    opacity: 1 !important;
}

/* Remove blur effect */
[data-testid="stSidebar"] > div:first-child {
    background-color: #2d2d2d !important;
    backdrop-filter: none !important;
}

/* Sidebar labels and text */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: white !important;
}

/* Login and Signup input boxes */
[data-testid="stSidebar"] input {
    background-color: white !important;
    color: black !important;
    border: 1px solid #888 !important;
}

/* Placeholder text */
[data-testid="stSidebar"] input::placeholder {
    color: #666 !important;
}

/* Tabs */
[data-testid="stSidebar"] button {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# Auto-seed on first run
if os.getenv("AUTO_SEED", "true").lower() == "true":
    try:
        seed_if_empty()
    except Exception as e:
        st.error(f"DB connection failed: {e}")
        st.stop()

# ---------- Session state ----------
st.session_state.setdefault("user", None)
st.session_state.setdefault("cart", [])
st.session_state.setdefault("wishlist_foods", [])


# ---------- Sidebar: Auth ----------
def auth_sidebar():
    auth = CustomerAuth()
    with st.sidebar:
        st.markdown("## 🍔 FoodRush")
        if st.session_state.user:
            u = st.session_state.user
            st.success(f"Hi, {u['name']}")
            if st.button("Logout"):
                st.session_state.user = None
                st.rerun()
            return
        tab1, tab2 = st.tabs(["Login", "Signup"])
        with tab1:
            e = st.text_input("Email", key="li_e")
            p = st.text_input("Password", type="password", key="li_p")
            if st.button("Login", key="li_btn"):
                ok, res = auth.login(e, p)
                if ok:
                    st.session_state.user = res
                    st.rerun()
                else:
                    st.error(res)
        with tab2:
            n = st.text_input("Name", key="su_n")
            e = st.text_input("Email", key="su_e")
            ph = st.text_input("Phone", key="su_ph")
            p = st.text_input("Password", type="password", key="su_p")
            if st.button("Create account", key="su_btn"):
                ok, msg = auth.signup(n, e, ph, p)
                st.success(msg) if ok else st.error(msg)


auth_sidebar()

# ---------- Hero ----------
st.markdown(
    '<div class="fr-hero"><h1>Hungry? You\'re in the right place 🍽️</h1>'
    '<p>Order from the best restaurants near you — fast, fresh, delicious.</p></div>',
    unsafe_allow_html=True,
)

# ---------- Search ----------
q = st.text_input("🔍 Search for restaurants, dishes, cuisines", "")

# ---------- Categories ----------
from database.mongodb import get_db
db = get_db()
cats = list(db.categories.find())
st.subheader("Explore Categories")
cols = st.columns(min(len(cats), 10))
selected_cat = st.session_state.get("selected_cat")
for i, c in enumerate(cats):
    with cols[i % len(cols)]:
        if st.button(f"{c['icon']}\n{c['name']}", key=f"cat_{c['name']}"):
            st.session_state["selected_cat"] = c["name"] if selected_cat != c["name"] else None
            st.rerun()
if selected_cat:
    st.info(f"Filtering by: **{selected_cat}** — click again to clear.")

# ---------- Filters ----------
with st.expander("Filters"):
    f1, f2, f3, f4 = st.columns(4)
    only_veg = f1.checkbox("Veg only")
    min_rating = f2.slider("Min rating", 0.0, 5.0, 0.0, 0.5)
    price_max = f3.slider("Max price (₹)", 50, 500, 500, 50)
    bestseller_only = f4.checkbox("Bestsellers")

# ---------- Build query ----------
fm = FoodModel()
query = {"available": True}
if selected_cat:
    query["category"] = selected_cat
if only_veg:
    query["veg"] = True
if bestseller_only:
    query["bestseller"] = True
query["rating"] = {"$gte": min_rating}
query["price"] = {"$lte": price_max}
if q:
    query["name"] = {"$regex": q, "$options": "i"}

foods = fm.all(query, limit=60)

# ---------- Restaurants ----------
rm = RestaurantModel()
st.subheader("🏆 Popular Restaurants")
pop = rm.popular(8)
rcols = st.columns(4)
for i, r in enumerate(pop):
    with rcols[i % 4]:
        badges = ""
        if r.get("free_delivery"):
            badges += '<span class="badge b-free">FREE DELIVERY</span>'
        if r.get("discount_badge"):
            badges += f'<span class="badge b-off">{r["discount_badge"]}</span>'
        st.markdown(f"""
        <div class="fr-card">
          <img src="{r['cover_image']}" class="fr-img"/>
          <div class="fr-title">{r['name']}</div>
          <div class="fr-meta">⭐ {r['rating']} · {r['cuisine']} · {r['delivery_time']} min · {r['distance_km']} km</div>
          <div style="margin-top:.4rem">{badges}</div>
        </div>""", unsafe_allow_html=True)

# ---------- Food cards ----------
st.subheader("🍽️ Recommended For You" if not q else f"Results for '{q}'")
if not foods:
    st.info("No items match your filters.")
else:
    fcols = st.columns(3)
    for i, f in enumerate(foods):
        with fcols[i % 3]:
            img = f["images"][0] if f.get("images") else "https://via.placeholder.com/400"
            veg_b = '<span class="badge b-veg">● VEG</span>' if f["veg"] else '<span class="badge b-nonveg">● NON-VEG</span>'
            best_b = '<span class="badge b-best">⭐ BESTSELLER</span>' if f.get("bestseller") else ""
            st.markdown(f"""
            <div class="fr-card">
              <img src="{img}" class="fr-img"/>
              <div style="margin-top:.4rem">{veg_b}{best_b}</div>
              <div class="fr-title">{f['name']}</div>
              <div class="fr-meta">{f['category']} · ⭐ {f['rating']} · ⏱ {f['prep_time']} min</div>
              <div style="margin-top:.4rem">
                <span class="fr-price">₹{f['price']}</span>
                <span class="fr-mrp">₹{f['mrp']}</span>
                <span class="fr-disc">{f['discount']}% OFF</span>
              </div>
              <div class="fr-meta" style="margin-top:.3rem">{f['description']}</div>
            </div>""", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            if c1.button("ADD TO CART", key=f"add_{f['_id']}"):
                if not st.session_state.user:
                    st.warning("Login to add items.")
                else:
                    item = {
                        "food_id": str(f["_id"]),
                        "restaurant_id": f["restaurant_id"],
                        "name": f["name"],
                        "price": f["price"],
                        "image": img,
                        "qty": 1,
                    }
                    found = next((x for x in st.session_state.cart if x["food_id"] == item["food_id"]), None)
                    if found:
                        found["qty"] += 1
                    else:
                        st.session_state.cart.append(item)
                    st.toast(f"Added {f['name']} to cart 🛒")
            if c2.button("♡ Wishlist", key=f"wl_{f['_id']}"):
                if not st.session_state.user:
                    st.warning("Login to use wishlist.")
                else:
                    db.wishlist.update_one(
                        {"user_email": st.session_state.user["email"], "food_id": str(f["_id"])},
                        {"$set": {"name": f["name"], "image": img, "price": f["price"]}},
                        upsert=True,
                    )
                    st.toast("Saved to wishlist ❤️")

# Floating cart count
if st.session_state.cart:
    n = sum(i["qty"] for i in st.session_state.cart)
    st.sidebar.markdown(f"### 🛒 Cart: **{n}** item(s)")
