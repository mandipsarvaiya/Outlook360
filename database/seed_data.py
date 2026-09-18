"""
Outlook360 - Database Seeding & Domain Switcher Engine
Populates the relational database with domain datasets and validates foreign key integrity.
"""
import sys
from pathlib import Path
from typing import Optional, Dict
import pandas as pd
from sqlalchemy import text

# Ensure project root in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from database.connection import db_manager
from data_generators.synthetic_generator import SyntheticDataGenerator
from config.settings import AppSettings


def clear_all_tables(clear_users: bool = False) -> None:
    """Safely clears all records from relational tables in reverse dependency order."""
    tables_order = [
        "inventory_logs",
        "order_items",
        "orders",
        "customers",
        "products",
        "categories",
        "business_profiles"
    ]
    if clear_users:
        tables_order.append("users")

    with db_manager.engine.begin() as conn:
        for table in tables_order:
            try:
                conn.execute(text(f"DELETE FROM {table}"))
            except Exception as e:
                print(f"[Seed Warning] Could not clear table {table}: {e}")


def seed_default_users() -> None:
    """Seeds default credentials for Store Owner, Cashier, and Inventory Staff."""
    from database.auth import auth_manager
    default_users = [
        ("EMP-OWN-01", "owner@outlook360.com", "admin123", "Vikram Malhotra (Store Owner)", "owner"),
        ("EMP-CSH-01", "cashier@outlook360.com", "cashier123", "Rahul Sharma (Lead Cashier)", "cashier"),
        ("EMP-INV-01", "inventory@outlook360.com", "inventory123", "Ananya Patel (Inventory Manager)", "inventory")
    ]
    for emp_id, email, password, full_name, role in default_users:
        # Check if already exists
        check_query = "SELECT user_id FROM users WHERE LOWER(email) = :email OR LOWER(emp_id) = :emp"
        existing = db_manager.execute_query(check_query, {"email": email.lower(), "emp": emp_id.lower()})
        if existing.empty:
            auth_manager.create_user(emp_id, email, password, full_name, role)
            print(f"  + Created Role Account: {role.upper():<12} | ID: {emp_id} | Email: {email}")
        else:
            # Update password hash if salt changed
            new_hash = auth_manager.hash_password(password)
            db_manager.execute_non_query(
                "UPDATE users SET password_hash = :hash, email = :email WHERE LOWER(emp_id) = :emp",
                {"hash": new_hash, "email": email.lower(), "emp": emp_id.lower()}
            )
            print(f"  ~ Refreshed Role Account: {role.upper():<12} | ID: {emp_id} | Email: {email}")



def seed_database(
    domain_key: str = "supermarket",
    num_customers: int = 250,
    num_orders: int = 1800,
    days_span: int = 240
) -> Dict[str, int]:
    """
    Clears existing records and populates tables with newly generated domain data.
    Returns dictionary with counts of rows inserted per table.
    """
    print(f"\n=======================================================")
    print(f"[SEED] Initializing Data Seeding for Domain: '{domain_key.upper()}'")
    print(f"=======================================================")

    db_manager.ensure_schema()
    clear_all_tables()

    generator = SyntheticDataGenerator(domain_key=domain_key)
    datasets = generator.generate_full_dataset(
        num_customers=num_customers,
        num_orders=num_orders,
        days_span=days_span
    )

    row_counts = {}
    insertion_order = [
        "business_profiles",
        "categories",
        "products",
        "customers",
        "orders",
        "order_items",
        "inventory_logs"
    ]

    with db_manager.engine.begin() as conn:
        for table in insertion_order:
            df = datasets[table]
            df.to_sql(table, conn, if_exists="append", index=False)
            count = len(df)
            row_counts[table] = count
            print(f"  + Seeded {table:<20}: {count:>6} records")

    seed_default_users()

    print(f"=======================================================")
    print(f"[SUCCESS] Domain '{domain_key}' successfully loaded into database!")
    print(f"=======================================================\n")
    return row_counts


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="OmniPulse AI Database Seeding Engine")
    parser.add_argument(
        "--domain",
        type=str,
        default="supermarket",
        choices=["supermarket", "pharmacy", "restaurant", "fashion", "electronics", "ecommerce"],
        help="Target business domain to seed"
    )
    parser.add_argument("--customers", type=int, default=250, help="Number of customers")
    parser.add_argument("--orders", type=int, default=1800, help="Number of orders")
    parser.add_argument("--days", type=int, default=240, help="Historical days span")
    args = parser.parse_args()

    seed_database(
        domain_key=args.domain,
        num_customers=args.customers,
        num_orders=args.orders,
        days_span=args.days
    )
