"""
Outlook360 - Universal Synthetic Enterprise Data Generator
Simulates realistic enterprise transaction logs, customer purchase behaviors,
co-purchase affinities, and inventory ledgers across any business domain.
"""
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
from faker import Faker

# Ensure project root in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from data_generators.domain_configs import get_domain_config


class SyntheticDataGenerator:
    """Generates synthetic enterprise datasets tailored to a specific domain configuration."""

    def __init__(self, domain_key: str = "supermarket", seed: int = 42):
        self.domain_key = domain_key
        self.config = get_domain_config(domain_key)
        self.fake = Faker()
        Faker.seed(seed)
        random.seed(seed)
        np.random.seed(seed)

    def generate_full_dataset(
        self,
        num_customers: int = 250,
        num_orders: int = 1800,
        days_span: int = 240
    ) -> Dict[str, pd.DataFrame]:
        """
        Generates complete relational datasets:
        categories, products, customers, orders, order_items, inventory_logs, and business_profile.
        """
        # 1. Business Profile
        business_profile_df = pd.DataFrame([{
            "domain_key": self.config["domain_key"],
            "business_name": self.config["business_name"],
            "currency": self.config["currency"],
            "tax_rate": self.config["tax_rate"],
            "tagline": self.config["tagline"],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])

        # 2. Categories
        cat_rows = []
        for i, c in enumerate(self.config["categories"], start=1):
            cat_rows.append({
                "category_id": i,
                "name": c["name"],
                "department": c["department"],
                "description": f"All items and catalog entries in {c['name']} under {c['department']}.",
                "tax_slab_percent": c.get("tax_slab", 0.05)
            })
        categories_df = pd.DataFrame(cat_rows)
        cat_id_map = {row["name"]: row["category_id"] for row in cat_rows}

        # 3. Products
        prod_rows = []
        for i, p in enumerate(self.config["products"], start=1):
            prod_rows.append({
                "product_id": i,
                "sku": p["sku"],
                "name": p["name"],
                "category_id": cat_id_map[p["category"]],
                "cost_price": round(float(p["cost"]), 2),
                "unit_price": round(float(p["price"]), 2),
                "current_stock": int(p["stock"]),
                "reorder_level": int(p["reorder"]),
                "lead_time_days": int(p["lead_time"]),
                "shelf_life_days": int(p.get("shelf_life", 365)),
                "is_active": 1,
                "created_at": (datetime.now() - timedelta(days=days_span + 30)).strftime("%Y-%m-%d %H:%M:%S")
            })
        products_df = pd.DataFrame(prod_rows)
        prod_dict = {p["name"]: p for p in prod_rows}
        prod_list = prod_rows

        # 4. Customers
        customer_rows = []
        cities = ["New York", "Chicago", "San Francisco", "Austin", "Seattle", "Boston", "Los Angeles", "Denver"]
        age_groups = ["18-25", "26-35", "36-50", "51-65", "65+"]
        tiers = ["Standard", "Silver", "Gold", "Platinum"]
        tier_weights = [0.55, 0.25, 0.15, 0.05]

        start_date = datetime.now() - timedelta(days=days_span)

        for c_id in range(1, num_customers + 1):
            reg_offset = random.randint(0, int(days_span * 0.8))
            reg_date = (start_date + timedelta(days=reg_offset)).date()
            name = self.fake.name()
            email = f"{name.lower().replace(' ', '.')}_{c_id}@{self.fake.free_email_domain()}"
            customer_rows.append({
                "customer_id": c_id,
                "customer_code": f"CUST-{c_id:04d}",
                "name": name,
                "email": email,
                "phone": self.fake.phone_number(),
                "gender": random.choice(["Male", "Female", "Non-Binary"]),
                "age_group": random.choice(age_groups),
                "city": random.choice(cities),
                "tier": random.choices(tiers, weights=tier_weights)[0],
                "registered_at": reg_date.strftime("%Y-%m-%d")
            })
        customers_df = pd.DataFrame(customer_rows)

        # 5. Orders & Order Items
        order_rows = []
        item_rows = []
        item_counter = 1
        payment_methods = ["Credit Card", "Debit Card", "UPI / Mobile Pay", "Cash", "Net Banking"]
        payment_weights = [0.45, 0.25, 0.15, 0.10, 0.05]
        channels = ["In-Store POS", "Online Web", "Mobile App"]
        channel_weights = [0.55, 0.30, 0.15]

        # Customer frequency skew (Pareto distribution for realistic spenders)
        customer_weights = np.random.pareto(a=1.8, size=num_customers)
        customer_weights /= customer_weights.sum()

        end_date = datetime.now()
        total_seconds = int((end_date - start_date).total_seconds())

        # Pre-compute affinity bundle products
        bundles = self.config.get("affinity_bundles", [])

        # Generate timestamps with realistic daily and weekly curves
        order_timestamps = []
        for _ in range(num_orders):
            # Pick a day with mild growth trend
            rand_sec = random.randint(0, total_seconds)
            order_dt = start_date + timedelta(seconds=rand_sec)

            # Hour skew: Peak around 12:00-14:00 (Lunch) and 18:00-21:00 (Evening)
            hour_prob = np.array([
                0.01, 0.01, 0.005, 0.005, 0.005, 0.01, # 00:00 - 05:00
                0.02, 0.04, 0.06, 0.07, 0.08, 0.09,    # 06:00 - 11:00
                0.12, 0.11, 0.07, 0.06, 0.06, 0.08,    # 12:00 - 17:00
                0.10, 0.09, 0.06, 0.04, 0.02, 0.01     # 18:00 - 23:00
            ], dtype=float)
            hour_prob = hour_prob / hour_prob.sum()
            hour = np.random.choice(range(24), p=hour_prob)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            order_dt = order_dt.replace(hour=hour, minute=minute, second=second)
            order_timestamps.append(order_dt)

        order_timestamps.sort()

        for o_id, order_dt in enumerate(order_timestamps, start=1):
            cust_idx = np.random.choice(range(num_customers), p=customer_weights)
            cust = customer_rows[cust_idx]

            # Decide basket contents: bundle trigger or random products
            basket_products = []
            if bundles and random.random() < 0.40:
                # Pick an affinity bundle
                chosen_bundle = random.choice(bundles)
                for item_name in chosen_bundle:
                    if item_name in prod_dict:
                        basket_products.append(prod_dict[item_name])
                # Optionally add 1 random other item
                if random.random() < 0.35:
                    basket_products.append(random.choice(prod_list))
            else:
                # Random basket size between 1 and 5 items
                num_items_in_order = random.choices([1, 2, 3, 4, 5], weights=[0.25, 0.35, 0.20, 0.12, 0.08])[0]
                selected_prods = random.sample(prod_list, min(num_items_in_order, len(prod_list)))
                basket_products.extend(selected_prods)

            # Deduplicate by product_id
            unique_basket = {p["product_id"]: p for p in basket_products}.values()

            subtotal = 0.0
            total_cost = 0.0

            for prod in unique_basket:
                # Quantity: mostly 1 or 2, rarely 3-5
                qty = random.choices([1, 2, 3, 4], weights=[0.70, 0.20, 0.07, 0.03])[0]
                unit_price = prod["unit_price"]
                unit_cost = prod["cost_price"]
                line_total = round(qty * unit_price, 2)
                line_profit = round(line_total - (qty * unit_cost), 2)

                subtotal += line_total
                total_cost += (qty * unit_cost)

                item_rows.append({
                    "item_id": item_counter,
                    "order_id": o_id,
                    "product_id": prod["product_id"],
                    "quantity": qty,
                    "unit_cost": unit_cost,
                    "unit_price": unit_price,
                    "total_price": line_total,
                    "profit_margin": line_profit
                })
                item_counter += 1

            # Customer tier discounts
            discount_pct = 0.0
            if cust["tier"] == "Platinum":
                discount_pct = 0.10
            elif cust["tier"] == "Gold":
                discount_pct = 0.05
            elif cust["tier"] == "Silver":
                discount_pct = 0.02

            # Occasional promotional discount
            if random.random() < 0.15:
                discount_pct += random.choice([0.05, 0.10, 0.15])

            discount_amount = round(subtotal * discount_pct, 2)
            tax_amount = round((subtotal - discount_amount) * self.config["tax_rate"], 2)
            total_amount = round(subtotal - discount_amount + tax_amount, 2)

            order_rows.append({
                "order_id": o_id,
                "invoice_no": f"INV-{order_dt.strftime('%Y%m%d')}-{o_id:05d}",
                "order_date": order_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "customer_id": cust["customer_id"],
                "payment_method": random.choices(payment_methods, weights=payment_weights)[0],
                "channel": random.choices(channels, weights=channel_weights)[0],
                "subtotal": round(subtotal, 2),
                "discount_amount": discount_amount,
                "tax_amount": tax_amount,
                "total_amount": total_amount,
                "status": "Completed" if random.random() > 0.02 else "Cancelled",
                "created_at": order_dt.strftime("%Y-%m-%d %H:%M:%S")
            })

        orders_df = pd.DataFrame(order_rows)
        order_items_df = pd.DataFrame(item_rows)

        # 6. Inventory Logs (Stock movements)
        inv_rows = []
        inv_counter = 1
        for prod in prod_rows:
            # Initial stock log
            init_qty = prod["current_stock"] + random.randint(100, 300)
            inv_rows.append({
                "log_id": inv_counter,
                "product_id": prod["product_id"],
                "change_type": "Purchase",
                "quantity": init_qty,
                "timestamp": (start_date - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S"),
                "reason": "Initial Opening Inventory Batch",
                "cost_impact": round(init_qty * prod["cost_price"], 2)
            })
            inv_counter += 1

            # Restock batches throughout the span
            for month_step in range(1, int(days_span / 30) + 1):
                restock_qty = random.randint(40, 120)
                restock_date = start_date + timedelta(days=month_step * 30 + random.randint(-5, 5))
                if restock_date <= end_date:
                    inv_rows.append({
                        "log_id": inv_counter,
                        "product_id": prod["product_id"],
                        "change_type": "Purchase",
                        "quantity": restock_qty,
                        "timestamp": restock_date.strftime("%Y-%m-%d %H:%M:%S"),
                        "reason": f"Supplier Restock Order #{month_step}",
                        "cost_impact": round(restock_qty * prod["cost_price"], 2)
                    })
                    inv_counter += 1

        inventory_logs_df = pd.DataFrame(inv_rows)

        return {
            "business_profiles": business_profile_df,
            "categories": categories_df,
            "products": products_df,
            "customers": customers_df,
            "orders": orders_df,
            "order_items": order_items_df,
            "inventory_logs": inventory_logs_df
        }
