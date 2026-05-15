import csv
import os
import random
from datetime import datetime
from faker import Faker

fake = Faker()

os.makedirs("csv_data", exist_ok=True)

# 1. roles
roles = [["id", "name"]]
for i, name in enumerate(["Admin", "Manager", "Staff"], 1):
    roles.append([i, name])
with open("csv_data/roles.csv", "w", newline="") as f:
    csv.writer(f).writerows(roles)

# 2. users (50 rows)
users = [["id", "name", "email", "password", "role_id", "is_active", "created_at"]]
for i in range(1, 51):
    users.append([
        i,
        fake.name(),
        fake.email(),
        fake.password(length=12),
        random.choice([1,2,3]),
        random.choice([0,1]),
        fake.date_time_this_year().isoformat()
    ])
with open("csv_data/users.csv", "w", newline="") as f:
    csv.writer(f).writerows(users)

# 3. categories
categories = [["id", "name"]]
cat_names = ["Medicines", "Surgical", "Cosmetics", "First Aid", "Vitamins", "Medical Devices", "Orthopedics", "Baby Care"]
for i, name in enumerate(cat_names, 1):
    categories.append([i, name])
with open("csv_data/categories.csv", "w", newline="") as f:
    csv.writer(f).writerows(categories)

# 4. units
units = [["id", "name"]]
unit_names = ["strip", "box", "bottle", "ml", "tablet", "capsule", "vial", "pack"]
for i, name in enumerate(unit_names, 1):
    units.append([i, name])
with open("csv_data/units.csv", "w", newline="") as f:
    csv.writer(f).writerows(units)

# 5. products (100 rows)
products = [["id", "name", "sku", "category_id", "unit_id", "quantity", "reorder_level", "unit_price", "is_active", "created_at"]]
for i in range(1, 101):
    name = fake.word().capitalize() + " " + random.choice(["500mg", "250mg", "10ml", "100ml", "1L", "2mg", "5mg", "10mg"])
    sku = fake.unique.bothify(text="SKU-#####")
    products.append([
        i, name, sku,
        random.randint(1, len(cat_names)),
        random.randint(1, len(unit_names)),
        random.randint(0, 500),
        random.randint(10, 50),
        round(random.uniform(1.5, 100.0), 2),
        random.choice([0,1]),
        fake.date_time_this_year().isoformat()
    ])
with open("csv_data/products.csv", "w", newline="") as f:
    csv.writer(f).writerows(products)

# 6. suppliers (50 rows)
suppliers = [["id", "name", "contact_person", "email", "phone", "payment_terms", "is_active", "created_at"]]
for i in range(1, 51):
    suppliers.append([
        i,
        fake.company(),
        fake.name(),
        fake.email(),
        fake.phone_number(),
        random.choice(["Net 30", "Net 15", "COD", "Net 60"]),
        random.choice([0,1]),
        fake.date_time_this_year().isoformat()
    ])
with open("csv_data/suppliers.csv", "w", newline="") as f:
    csv.writer(f).writerows(suppliers)

# 7. product_suppliers
ps = [["id", "product_id", "supplier_id", "unit_cost", "is_preferred"]]
counter = 1
used_pairs = set()
for product_id in range(1, 101):
    num = random.randint(1, 3)
    supplier_ids = random.sample(range(1, 51), num)
    for supplier_id in supplier_ids:
        if (product_id, supplier_id) in used_pairs:
            continue
        used_pairs.add((product_id, supplier_id))
        ps.append([
            counter, product_id, supplier_id,
            round(random.uniform(1.0, 90.0), 2),
            1 if supplier_id == supplier_ids[0] else 0
        ])
        counter += 1
with open("csv_data/product_suppliers.csv", "w", newline="") as f:
    csv.writer(f).writerows(ps)

# 8. purchase_orders (100 rows)
po = [["id", "supplier_id", "created_by", "approved_by", "approved_at", "status", "notes", "created_at", "updated_at"]]
for i in range(1, 101):
    created_at_dt = fake.date_time_this_year()
    created_at_str = created_at_dt.isoformat()
    approved_by = random.randint(1, 50) if random.random() > 0.3 else None
    approved_at_str = fake.date_time_between(start_date=created_at_dt, end_date="+30d").isoformat() if approved_by else None
    updated_at_dt = fake.date_time_between(start_date=created_at_dt, end_date="+30d")
    po.append([
        i,
        random.randint(1, 50),
        random.randint(1, 50),
        approved_by,
        approved_at_str,
        random.choice(["pending", "approved", "received", "cancelled"]),
        fake.sentence() if random.random() > 0.7 else None,
        created_at_str,
        updated_at_dt.isoformat()
    ])
with open("csv_data/purchase_orders.csv", "w", newline="") as f:
    csv.writer(f).writerows(po)

# 9. purchase_order_items
poi = [["id", "purchase_order_id", "product_id", "quantity_ordered", "quantity_received", "unit_cost"]]
counter = 1
for po_id in range(1, 101):
    num_items = random.randint(1, 5)
    product_ids = random.sample(range(1, 101), num_items)
    for product_id in product_ids:
        qty_ordered = random.randint(10, 200)
        qty_received = random.randint(0, qty_ordered) if random.random() > 0.2 else qty_ordered
        poi.append([
            counter, po_id, product_id,
            qty_ordered, qty_received,
            round(random.uniform(1.0, 80.0), 2)
        ])
        counter += 1
with open("csv_data/purchase_order_items.csv", "w", newline="") as f:
    csv.writer(f).writerows(poi)

# 10. stock_movements
sm = [["id", "product_id", "user_id", "quantity_before", "quantity_after", "reason", "changed_at"]]
counter = 1
for product_id in range(1, 101):
    num_moves = random.randint(3, 10)
    qty_current = random.randint(0, 200)
    for _ in range(num_moves):
        qty_before = qty_current
        change = random.randint(-20, 50)
        qty_after = max(0, qty_before + change)
        qty_current = qty_after
        sm.append([
            counter, product_id,
            random.randint(1, 50) if random.random() > 0.3 else None,
            qty_before, qty_after,
            random.choice(["PO received", "Manual adjustment", "Sale", "Return", "Expired"]),
            fake.date_time_this_year().isoformat()
        ])
        counter += 1
with open("csv_data/stock_movements.csv", "w", newline="") as f:
    csv.writer(f).writerows(sm)

print("All CSV files generated in 'csv_data' folder.")

