#!/usr/bin/env python3
import csv
import random
import sys
from datetime import datetime, timedelta

random.seed(42)

REGIONS = ["North", "South", "East", "West"]
CATEGORIES = ["Electronics", "Furniture", "Office Supplies"]
SUBCATEGORIES = {
    "Electronics": ["Phones", "Laptops", "Accessories"],
    "Furniture": ["Chairs", "Tables", "Storage"],
    "Office Supplies": ["Paper", "Binders", "Writing"]
}
SEGMENTS = ["Consumer", "Corporate", "Home Office"]


def daterange(start_date, end_date):
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=1)


def generate_daily_orders(date, orders_per_day):
    rows = []
    for _ in range(orders_per_day):
        order_id = f"ORD-{date.strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        region = random.choice(REGIONS)
        category = random.choice(CATEGORIES)
        subcategory = random.choice(SUBCATEGORIES[category])
        segment = random.choice(SEGMENTS)
        quantity = max(1, int(random.gauss(3, 1)))
        unit_price = round(max(5.0, random.gauss(50.0, 25.0)), 2)
        discount = max(0.0, min(0.4, random.choice([0.0, 0.0, 0.1, 0.2, 0.3])))
        sales = round(quantity * unit_price * (1 - discount), 2)
        cost = round(sales * random.uniform(0.5, 0.8), 2)
        profit = round(sales - cost, 2)
        customer_id = f"C-{random.randint(10000, 99999)}"
        city = random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"])  # demo
        rows.append({
            "Order Date": date.strftime("%Y-%m-%d"),
            "Order ID": order_id,
            "Customer ID": customer_id,
            "Segment": segment,
            "City": city,
            "Region": region,
            "Category": category,
            "Sub-Category": subcategory,
            "Quantity": quantity,
            "Unit Price": unit_price,
            "Discount": discount,
            "Sales": sales,
            "Cost": cost,
            "Profit": profit
        })
    return rows


def main():
    out_path = "/workspace/data/synthetic_sales.csv"
    start = datetime.today().date() - timedelta(days=365)
    end = datetime.today().date()
    daily_min, daily_max = 20, 60

    all_rows = []
    for day in daterange(start, end):
        # Seasonal variation: more orders on weekdays
        weekday = day.weekday()
        base = random.randint(daily_min, daily_max)
        if weekday >= 5:  # weekend
            orders = int(base * 0.6)
        else:
            orders = int(base * 1.1)
        all_rows.extend(generate_daily_orders(day, max(5, orders)))

    fieldnames = [
        "Order Date", "Order ID", "Customer ID", "Segment", "City", "Region",
        "Category", "Sub-Category", "Quantity", "Unit Price", "Discount",
        "Sales", "Cost", "Profit"
    ]

    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Wrote {len(all_rows)} rows to {out_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)