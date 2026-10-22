"""Build data/demo.sqlite: a small, deterministic sales warehouse.

Run: ``uv run python data/seed_demo.py``. Stdlib only, seeded random, so the
numbers in a demo are the same every time.
"""

from __future__ import annotations

import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

OUT = Path(__file__).with_name("demo.sqlite")
random.seed(7)

REGIONS = ["North", "South", "East", "West"]
CATEGORIES = {
    "Coffee": ["Espresso Beans 1kg", "Filter Blend 500g", "Decaf Beans 1kg", "Cold Brew Pack"],
    "Tea": ["Earl Grey Tin", "Sencha Loose 200g", "Chai Sachets", "Peppermint Box"],
    "Equipment": ["Hand Grinder", "Pour-over Kit", "Milk Frother", "Scale 0.1g"],
    "Accessories": ["Filter Papers x100", "Travel Cup", "Storage Canister", "Cleaning Tabs"],
}
FIRST = [
    "Ana",
    "Ben",
    "Chloe",
    "Dev",
    "Ewa",
    "Finn",
    "Greta",
    "Hugo",
    "Iris",
    "Jan",
    "Kai",
    "Lena",
]
LAST = ["Nowak", "Smith", "Garcia", "Kowalski", "Brown", "Rossi", "Meyer", "Dubois", "Silva"]


def build(path: Path = OUT) -> None:
    if path.exists():
        path.unlink()
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.executescript(
        """
        create table customers (
            customer_id integer primary key, name text, region text, segment text, signup_date text);
        create table products (
            product_id integer primary key, name text, category text, unit_price real);
        create table orders (
            order_id integer primary key, customer_id integer, order_date text, status text,
            foreign key(customer_id) references customers(customer_id));
        create table order_items (
            order_item_id integer primary key, order_id integer, product_id integer,
            quantity integer, unit_price real,
            foreign key(order_id) references orders(order_id),
            foreign key(product_id) references products(product_id));
        create table inventory (
            product_id integer primary key, on_hand integer, reorder_point integer, updated_at text);
        """
    )
    customers = []
    start = date(2024, 1, 1)
    for i in range(1, 61):
        customers.append(
            (
                i,
                f"{random.choice(FIRST)} {random.choice(LAST)}",
                random.choice(REGIONS),
                random.choice(["consumer", "consumer", "business"]),
                (start + timedelta(days=random.randint(0, 600))).isoformat(),
            )
        )
    c.executemany("insert into customers values (?,?,?,?,?)", customers)

    products = []
    pid = 1
    for cat, names in CATEGORIES.items():
        for n in names:
            price = {"Coffee": 14, "Tea": 9, "Equipment": 39, "Accessories": 7}[cat]
            products.append((pid, n, cat, round(price * random.uniform(0.8, 1.6), 2)))
            pid += 1
    c.executemany("insert into products values (?,?,?,?)", products)
    price_of = {p[0]: p[3] for p in products}

    # Two planted causes give the root-cause agent something real to find:
    # from July 2025 most West-region orders are cancelled (a fulfilment problem),
    # and from August 2025 the Hand Grinder is out of stock, so nobody buys it.
    region_of = {c[0]: c[2] for c in customers}
    grinder = next(p[0] for p in products if p[1] == "Hand Grinder")
    west_trouble = date(2025, 7, 1)
    grinder_out = date(2025, 8, 1)

    orders, items = [], []
    item_id = 1
    for oid in range(1, 1801):
        cust = random.randint(1, 60)
        # even spread over the 21 months, so a real change stands out from noise
        odate = start + timedelta(days=(oid - 1) * 640 // 1800 + random.randint(0, 3))
        weights = [20, 65, 10, 5]
        if odate >= west_trouble and region_of[cust] == "West":
            weights = [8, 25, 62, 5]
        status = random.choices(["shipped", "delivered", "cancelled", "returned"], weights)[0]
        orders.append((oid, cust, odate.isoformat(), status))
        for _ in range(random.randint(1, 4)):
            p = random.randint(1, len(products))
            if p == grinder and odate >= grinder_out:
                p = random.choice([x for x in range(1, len(products) + 1) if x != grinder])
            items.append((item_id, oid, p, random.randint(1, 5), price_of[p]))
            item_id += 1
    c.executemany("insert into orders values (?,?,?,?)", orders)
    c.executemany("insert into order_items values (?,?,?,?,?)", items)

    inventory = [
        (
            p[0],
            0 if p[0] == grinder else random.randint(5, 120),
            random.choice([10, 20, 30]),
            date(2025, 9, 30).isoformat(),
        )
        for p in products
    ]
    c.executemany("insert into inventory values (?,?,?,?)", inventory)
    conn.commit()
    conn.close()
    print(
        f"wrote {path}: {len(customers)} customers, {len(products)} products, "
        f"{len(orders)} orders, {len(items)} order items"
    )


if __name__ == "__main__":
    build()
