import csv
import json
import random
import uuid
from datetime import datetime, timedelta

random.seed(42)

# ─────────────────────────────────────────────
#  SHARED REFERENCE DATA
# ─────────────────────────────────────────────

REGIONS = ["Accra", "Kumasi", "Takoradi"]

PRODUCTS = [
    {"product_id": "PROD-001", "name": "Nike Air Max Sneakers",        "category": "Sportswear",   "unit_price": 320.00},
    {"product_id": "PROD-002", "name": "Adidas Running Shorts",        "category": "Sportswear",   "unit_price": 85.00},
    {"product_id": "PROD-003", "name": "Samsung Galaxy A54",           "category": "Technology",   "unit_price": 1850.00},
    {"product_id": "PROD-004", "name": "Apple AirPods Pro",            "category": "Technology",   "unit_price": 1200.00},
    {"product_id": "PROD-005", "name": "Puma Training T-Shirt",        "category": "Sportswear",   "unit_price": 75.00},
    {"product_id": "PROD-006", "name": "Tecno Camon 20 Smartphone",    "category": "Technology",   "unit_price": 980.00},
    {"product_id": "PROD-007", "name": "Under Armour Compression Tights","category": "Sportswear", "unit_price": 110.00},
    {"product_id": "PROD-008", "name": "JBL Bluetooth Speaker",        "category": "Technology",   "unit_price": 450.00},
    {"product_id": "PROD-009", "name": "Reebok Classic Football Boots","category": "Sportswear",   "unit_price": 260.00},
    {"product_id": "PROD-010", "name": "Lenovo IdeaPad Laptop",        "category": "Technology",   "unit_price": 3200.00},
    {"product_id": "PROD-011", "name": "Speedo Swim Goggles",          "category": "Sportswear",   "unit_price": 55.00},
    {"product_id": "PROD-012", "name": "Xiaomi Smart Band 8",          "category": "Technology",   "unit_price": 220.00},
    {"product_id": "PROD-013", "name": "New Balance Running Shoes",    "category": "Sportswear",   "unit_price": 295.00},
    {"product_id": "PROD-014", "name": "Anker USB-C Charging Hub",     "category": "Technology",   "unit_price": 180.00},
    {"product_id": "PROD-015", "name": "Wilson Tennis Racket",         "category": "Sportswear",   "unit_price": 340.00},
]

GHANAIAN_FIRST_NAMES = [
    "Kwame", "Ama", "Kofi", "Abena", "Yaw", "Akosua", "Kweku", "Efua",
    "Kojo", "Adwoa", "Fiifi", "Maame", "Nana", "Adjoa", "Kwabena", "Esi",
    "Kwesi", "Afia", "Mensah", "Akua", "Bright", "Patience", "Emmanuel",
    "Josephine", "Ernest", "Olivia", "Carl", "Grace", "Daniel", "Priscilla",
    "Isaac", "Regina", "Solomon", "Beatrice", "Francis", "Cecilia"
]

GHANAIAN_LAST_NAMES = [
    "Mensah", "Asante", "Boateng", "Owusu", "Acheampong", "Adjei", "Appiah",
    "Darko", "Frimpong", "Gyamfi", "Amoah", "Ofori", "Quaye", "Tetteh",
    "Antwi", "Bonsu", "Dompreh", "Eshun", "Forson", "Gyan", "Hackman",
    "Inkoom", "Jatoe", "Kumi", "Laryea", "Nkrumah", "Peprah", "Sarfo",
    "Crankson", "Dosimey", "Kabu", "Essien", "Asamoah", "Opoku", "Sarpong"
]

REVIEW_TEMPLATES = [
    # Positive (rating 4-5)
    ("Excellent product! Really happy with my purchase from the {region} store.", [4, 5]),
    ("Great quality, fast delivery. Will definitely order again.", [4, 5]),
    ("The {product} exceeded my expectations. Worth every pesewa.", [5]),
    ("Very satisfied. The product arrived on time and in perfect condition.", [4, 5]),
    ("Absolutely love it! Best purchase I have made this year.", [5]),
    ("Top quality item. Customer service was also very helpful.", [4, 5]),
    ("Fantastic value for money. Highly recommend to everyone.", [4, 5]),
    ("Impressive build quality. Works exactly as described.", [4]),
    ("Super fast shipping to {region}. Product is exactly what I needed.", [4, 5]),
    ("Outstanding experience. Already recommended to friends.", [5]),
    # Neutral (rating 3)
    ("Decent product overall. Nothing special but does the job.", [3]),
    ("Average quality for the price. Expected a bit more honestly.", [3]),
    ("It is okay. Delivery took longer than expected to {region}.", [3]),
    ("Product is fine. Packaging could be improved though.", [3]),
    ("Works as described but the quality feels a little cheap.", [3]),
    # Negative (rating 1-2)
    ("Disappointed with the quality. Not worth the price at all.", [1, 2]),
    ("Delivery took too long and product did not match the description.", [1, 2]),
    ("Poor packaging. Item arrived slightly damaged.", [1, 2]),
    ("Expected better quality from this brand. Very underwhelming.", [2]),
    ("Not happy with my purchase. Would not recommend this product.", [1]),
]

ORDER_STATUSES   = ["delivered", "shipped", "processing", "cancelled"]
STATUS_WEIGHTS   = [0.60, 0.20, 0.12, 0.08]
PAYMENT_METHODS  = ["mobile_money", "credit_card", "debit_card", "cash_on_delivery"]
PAYMENT_WEIGHTS  = [0.50, 0.20, 0.18, 0.12]

def random_date(start_days_ago=90, end_days_ago=0):
    base = datetime(2025, 3, 7)
    start = base - timedelta(days=start_days_ago)
    end   = base - timedelta(days=end_days_ago)
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

def full_name():
    return f"{random.choice(GHANAIAN_FIRST_NAMES)} {random.choice(GHANAIAN_LAST_NAMES)}"

def customer_id():
    return f"CUST-{random.randint(10000, 99999)}"

def order_id():
    return f"ORD-{uuid.uuid4().hex[:10].upper()}"

def weighted_choice(choices, weights):
    r = random.random()
    cumulative = 0
    for choice, weight in zip(choices, weights):
        cumulative += weight
        if r < cumulative:
            return choice
    return choices[-1]


# ═══════════════════════════════════════════════════════════════════
#  1.  CUSTOMER REVIEWS  (CSV — weekly fetch)
# ═══════════════════════════════════════════════════════════════════

def generate_customer_reviews(n=520):
    rows = []
    for i in range(n):
        product  = random.choice(PRODUCTS)
        region   = random.choice(REGIONS)
        template, possible_ratings = random.choice(REVIEW_TEMPLATES)
        rating   = random.choice(possible_ratings)
        review_text = template.format(
            region=region, product=product["name"]
        )
        review_date = random_date(start_days_ago=84, end_days_ago=0)  # ~12 weeks

        rows.append({
            "review_id":    f"REV-{str(i+1).zfill(5)}",
            "customer_id":  customer_id(),
            "customer_name": full_name(),
            "region":       region,
            "product_id":   product["product_id"],
            "product_name": product["name"],
            "category":     product["category"],
            "rating":       rating,
            "review_text":  review_text,
            "review_date":  review_date.strftime("%Y-%m-%d"),
            "week_number":  review_date.isocalendar()[1],
            "verified_purchase": random.choice(["Yes", "Yes", "Yes", "No"]),
        })

    filepath = "./data/customer_reviews_weekly.csv"
    fieldnames = list(rows[0].keys())
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅  customer_reviews_weekly.csv  — {len(rows)} rows")
    return rows


# ═══════════════════════════════════════════════════════════════════
#  2.  ONLINE ORDERS  (JSON — simulates REST API response)
# ═══════════════════════════════════════════════════════════════════

def generate_online_orders(n=650):
    orders = []
    for i in range(n):
        product    = random.choice(PRODUCTS)
        region     = random.choice(REGIONS)
        qty        = random.randint(1, 4)
        unit_price = product["unit_price"]
        discount   = round(random.choice([0, 0, 0, 5, 10, 15]) / 100, 2)
        subtotal   = round(unit_price * qty, 2)
        discount_amount = round(subtotal * discount, 2)
        total      = round(subtotal - discount_amount, 2)
        status     = weighted_choice(ORDER_STATUSES, STATUS_WEIGHTS)
        payment    = weighted_choice(PAYMENT_METHODS, PAYMENT_WEIGHTS)
        order_date = random_date(start_days_ago=90, end_days_ago=0)

        delivered_date = None
        if status == "delivered":
            delivered_date = (order_date + timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%dT%H:%M:%S")

        orders.append({
            "order_id":          order_id(),
            "customer_id":       customer_id(),
            "customer_name":     full_name(),
            "region":            region,
            "product_id":        product["product_id"],
            "product_name":      product["name"],
            "category":          product["category"],
            "quantity":          qty,
            "unit_price_ghs":    unit_price,
            "discount_rate":     discount,
            "discount_amount_ghs": discount_amount,
            "total_amount_ghs":  total,
            "payment_method":    payment,
            "order_status":      status,
            "order_date":        order_date.strftime("%Y-%m-%dT%H:%M:%S"),
            "delivered_date":    delivered_date,
            "source":            "online_api",
        })

    # Wrap as a realistic API response envelope
    payload = {
        "api_version":   "1.0",
        "endpoint":      "/api/v1/orders",
        "generated_at":  "2025-03-07T00:00:00",
        "total_records": len(orders),
        "regions":       REGIONS,
        "data":          orders,
    }

    filepath = "./data/online_orders_api_simulation.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"✅  online_orders_api_simulation.json  — {len(orders)} records")
    return orders


# ═══════════════════════════════════════════════════════════════════
#  3.  INVENTORY DATABASE SEED  (CSV — database source)
# ═══════════════════════════════════════════════════════════════════

def generate_inventory(restock_entries=180):
    # ── 3a: products master table ──────────────────────────────────
    products_path = "./data/inventory_products_master.csv"
    with open(products_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "product_id","product_name","category","unit_price_ghs",
            "supplier","reorder_level","is_active"
        ])
        writer.writeheader()
        suppliers = {
            "Sportswear":  ["SportZone GH Ltd", "Accra Athletics Co.", "GoldCoast Sports"],
            "Technology":  ["TechHub Ghana", "Digital City Accra",  "Ighana Electronics"],
        }
        for p in PRODUCTS:
            writer.writerow({
                "product_id":      p["product_id"],
                "product_name":    p["name"],
                "category":        p["category"],
                "unit_price_ghs":  p["unit_price"],
                "supplier":        random.choice(suppliers[p["category"]]),
                "reorder_level":   random.randint(10, 30),
                "is_active":       "TRUE",
            })
    print(f"✅  inventory_products_master.csv  — {len(PRODUCTS)} products")

    # ── 3b: current stock levels per region ───────────────────────
    stock_path = "./data/inventory_stock_levels.csv"
    stock_rows = []
    for p in PRODUCTS:
        for region in REGIONS:
            qty = random.randint(5, 150)
            stock_rows.append({
                "stock_id":          f"STK-{p['product_id']}-{region[:3].upper()}",
                "product_id":        p["product_id"],
                "product_name":      p["name"],
                "region":            region,
                "quantity_in_stock": qty,
                "warehouse_location": f"{region} Central Warehouse",
                "last_restocked":    random_date(30, 1).strftime("%Y-%m-%d"),
                "last_updated":      "2025-03-07",
            })
    with open(stock_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(stock_rows[0].keys()))
        writer.writeheader()
        writer.writerows(stock_rows)
    print(f"✅  inventory_stock_levels.csv  — {len(stock_rows)} stock entries ({len(PRODUCTS)} products × {len(REGIONS)} regions)")

    # ── 3c: restock / movement log ────────────────────────────────
    log_path = "./data/inventory_restock_log.csv"
    log_rows = []
    movement_types = ["restock", "restock", "restock", "adjustment", "return"]
    for i in range(restock_entries):
        product   = random.choice(PRODUCTS)
        region    = random.choice(REGIONS)
        mv_type   = random.choice(movement_types)
        qty_delta = random.randint(10, 100) if mv_type == "restock" else random.randint(1, 10)
        log_rows.append({
            "log_id":         f"LOG-{str(i+1).zfill(5)}",
            "product_id":     product["product_id"],
            "product_name":   product["name"],
            "region":         region,
            "movement_type":  mv_type,
            "quantity_delta": qty_delta if mv_type != "adjustment" else -random.randint(1, 5),
            "reason":         "Scheduled restock" if mv_type == "restock" else
                              "Customer return"   if mv_type == "return"  else
                              "Inventory audit correction",
            "performed_by":   full_name(),
            "log_date":       random_date(90, 0).strftime("%Y-%m-%d %H:%M:%S"),
        })
    with open(log_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(log_rows[0].keys()))
        writer.writeheader()
        writer.writerows(log_rows)
    print(f"✅  inventory_restock_log.csv  — {len(log_rows)} movement entries")


# ═══════════════════════════════════════════════════════════════════
#  RUN ALL
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n Generating InsightFlow Sample Data \n")
    generate_customer_reviews(n=520)
    generate_online_orders(n=650)
    generate_inventory(restock_entries=180)
    print("\n All files saved\n")