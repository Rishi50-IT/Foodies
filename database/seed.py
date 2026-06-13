"""Seed sample data: categories, 20 restaurants, 200 food items."""
import random
from database.mongodb import get_db
from utils.auth import hash_password

CATEGORIES = [
    ("Pizza", "🍕"), ("Burger", "🍔"), ("Biryani", "🍛"),
    ("Chinese", "🥡"), ("North Indian", "🍲"), ("South Indian", "🥘"),
    ("Desserts", "🍰"), ("Ice Cream", "🍦"), ("Drinks", "🥤"),
    ("Fast Food", "🌭"),
]

# Real food images by category (Unsplash)
IMG = {
    "Pizza":        ["https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600",
                     "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600",
                     "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=600"],
    "Burger":       ["https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600",
                     "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=600",
                     "https://images.unsplash.com/photo-1550547660-d9450f859349?w=600"],
    "Biryani":      ["https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600",
                     "https://images.unsplash.com/photo-1633945274405-b6c8069047b0?w=600"],
    "Chinese":      ["https://images.unsplash.com/photo-1585032226651-759b368d7246?w=600",
                     "https://images.unsplash.com/photo-1552611052-33e04de081de?w=600"],
    "North Indian": ["https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=600",
                     "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600"],
    "South Indian": ["https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=600",
                     "https://images.unsplash.com/photo-1630383249896-424e482df921?w=600"],
    "Desserts":     ["https://images.unsplash.com/photo-1551024506-0bccd828d307?w=600",
                     "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=600"],
    "Ice Cream":    ["https://images.unsplash.com/photo-1501443762994-82bd5dace89a?w=600",
                     "https://images.unsplash.com/photo-1567206563064-6f60f40a2b57?w=600"],
    "Drinks":       ["https://images.unsplash.com/photo-1437418747212-8d9709afab22?w=600",
                     "https://images.unsplash.com/photo-1544145945-f90425340c7e?w=600"],
    "Fast Food":    ["https://images.unsplash.com/photo-1606755962773-d324e0a13086?w=600",
                     "https://images.unsplash.com/photo-1561758033-d89a9ad46330?w=600"],
}

FOOD_NAMES = {
    "Pizza": ["Margherita", "Pepperoni", "Farmhouse", "BBQ Chicken", "Veggie Supreme",
              "Cheese Burst", "Tandoori Paneer", "Mexican Wave"],
    "Burger": ["Classic Cheese", "Aloo Tikki", "Chicken Maharaja", "Veggie Whopper",
               "Crispy Veg", "Smoky BBQ", "Double Patty"],
    "Biryani": ["Chicken Biryani", "Mutton Biryani", "Veg Biryani", "Egg Biryani",
                "Hyderabadi Dum", "Lucknowi Biryani"],
    "Chinese": ["Hakka Noodles", "Manchurian", "Schezwan Rice", "Chilli Chicken",
                "Spring Roll", "Honey Chilli"],
    "North Indian": ["Butter Chicken", "Paneer Tikka", "Dal Makhani", "Chole Bhature",
                     "Rajma Chawal", "Kadhai Paneer"],
    "South Indian": ["Masala Dosa", "Idli Sambhar", "Vada", "Uttapam",
                     "Pongal", "Rasam Rice"],
    "Desserts": ["Gulab Jamun", "Rasmalai", "Chocolate Brownie", "Cheesecake",
                 "Tiramisu", "Kheer"],
    "Ice Cream": ["Vanilla Sundae", "Chocolate Fudge", "Strawberry Scoop",
                  "Butterscotch", "Kulfi", "Mint Chip"],
    "Drinks": ["Mango Lassi", "Cold Coffee", "Fresh Lime", "Masala Chai",
               "Smoothie Bowl", "Iced Tea"],
    "Fast Food": ["French Fries", "Hot Dog", "Nachos", "Sandwich",
                  "Wrap", "Onion Rings"],
}

RESTAURANT_COVERS = [
    "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=900",
    "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=900",
    "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=900",
    "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=900",
    "https://images.unsplash.com/photo-1466978913421-dad2ebd01d17?w=900",
]


def seed_if_empty():
    db = get_db()
    if db.restaurants.count_documents({}) > 0:
        return False

    # Categories
    db.categories.delete_many({})
    db.categories.insert_many([{"name": n, "icon": i} for n, i in CATEGORIES])

    # 20 Restaurants
    pwd = hash_password("password123")
    cuisines = ["Indian", "Chinese", "Italian", "Multi-Cuisine", "Fast Food"]
    restaurant_ids = []
    for i in range(1, 21):
        doc = {
            "name": f"FoodHub #{i}",
            "owner_name": f"Owner {i}",
            "owner_email": f"owner{i}@foodrush.dev",
            "phone": f"99000000{i:02d}",
            "password": pwd,
            "address": f"{i} MG Road, Bengaluru",
            "rating": round(random.uniform(3.8, 4.9), 1),
            "cuisine": random.choice(cuisines),
            "delivery_time": random.randint(20, 45),
            "distance_km": round(random.uniform(0.5, 6.0), 1),
            "cover_image": random.choice(RESTAURANT_COVERS),
            "logo": "https://images.unsplash.com/photo-1555992336-fb0d29498b13?w=200",
            "free_delivery": random.choice([True, False]),
            "discount_badge": random.choice(["20% OFF", "50% OFF", "Flat ₹100 OFF", None]),
        }
        rid = db.restaurants.insert_one(doc).inserted_id
        restaurant_ids.append(str(rid))

    # 200 Food items (10 per restaurant)
    items = []
    for rid in restaurant_ids:
        for _ in range(10):
            cat, _icon = random.choice(CATEGORIES)
            name = random.choice(FOOD_NAMES[cat])
            mrp = random.choice([199, 249, 299, 349, 399, 499])
            disc = random.choice([10, 15, 20, 25, 30, 40, 50])
            price = int(mrp * (100 - disc) / 100)
            veg = cat in ("South Indian", "Desserts", "Ice Cream", "Drinks") or random.random() > 0.4
            items.append({
                "restaurant_id": rid,
                "name": name,
                "category": cat,
                "description": f"Delicious {name.lower()} freshly prepared.",
                "ingredients": "Chef's special blend of spices",
                "images": IMG[cat],
                "price": price,
                "mrp": mrp,
                "discount": disc,
                "rating": round(random.uniform(3.5, 5.0), 1),
                "quantity": random.randint(5, 50),
                "prep_time": random.randint(10, 35),
                "available": True,
                "veg": veg,
                "bestseller": random.random() > 0.7,
            })
    db.food_items.insert_many(items)
    print(f"Seeded 20 restaurants and {len(items)} food items.")
    return True


if __name__ == "__main__":
    seed_if_empty()
