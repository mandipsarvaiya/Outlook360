"""
Outlook360 - Database Seeding & Domain Switcher Engine
Populates the relational database with domain datasets and validates foreign key integrity.
"""
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import pandas as pd
from sqlalchemy import text

# Ensure project root in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config.database_config import DatabaseConfig
from database.connection import db_manager
from data_generators.synthetic_generator import SyntheticDataGenerator
from config.settings import AppSettings


def clear_all_tables(clear_users: bool = True) -> None:
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
    """
    Seeds the exact 3 application users required for Outlook360:
    1. Store Owner (E1 / smt10@gmail.com / Smt@10)
    2. Cashier Staff (E2 / cashier@outlook360.local / Cash@123)
    3. Inventory Staff (E3 / inventory@outlook360.local / Inventory@123)
    """
    from database.auth import auth_manager

    target_users = [
        ("E1", "smt10@gmail.com", "Smt@10", "SMT", "owner"),
        ("E2", "cashier@outlook360.local", "Cash@123", "Cashier Staff", "cashier"),
        ("E3", "inventory@outlook360.local", "Inventory@123", "Inventory Staff", "inventory_staff")
    ]

    for emp_id, email, password, full_name, role in target_users:
        check_query = "SELECT user_id FROM users WHERE LOWER(email) = :email OR LOWER(emp_id) = :emp"
        existing = db_manager.execute_query(check_query, {"email": email.lower(), "emp": emp_id.lower()})
        if existing.empty:
            auth_manager.create_user(emp_id, email, password, full_name, role)
            print(f"  + Created Role Account: {role.upper():<16} | ID: {emp_id} | Email: {email}")
        else:
            new_hash = auth_manager.hash_password(password)
            db_manager.execute_non_query(
                "UPDATE users SET password_hash = :hash, email = :email, full_name = :name, role = :role, is_active = 1 WHERE LOWER(emp_id) = :emp",
                {"hash": new_hash, "email": email.lower(), "name": full_name, "role": role.lower(), "emp": emp_id.lower()}
            )
            print(f"  ~ Refreshed Role Account: {role.upper():<16} | ID: {emp_id} | Email: {email}")


def validate_seeded_database() -> Dict[str, Any]:
    """
    Validates database engine, required tables, user accounts, and foreign key integrity.
    """
    validation_results = {
        "engine_valid": True,
        "tables_valid": True,
        "users_valid": True,
        "fk_valid": True,
        "details": []
    }

    # 1. Engine & Database check
    is_sqlite = db_manager.is_sqlite()
    if DatabaseConfig.ENGINE_TYPE == "mysql" and is_sqlite:
        validation_results["engine_valid"] = False
        validation_results["details"].append("ERROR: MySQL configured in .env but SQLite engine is active.")

    # 2. Table existence check
    existing_tables = set(db_manager.get_table_names())
    required_tables = {
        "users", "business_profiles", "categories", "products",
        "customers", "orders", "order_items", "inventory_logs"
    }
    missing_tables = required_tables - existing_tables
    if missing_tables:
        validation_results["tables_valid"] = False
        validation_results["details"].append(f"ERROR: Missing tables: {missing_tables}")

    # 3. Users check
    users_df = db_manager.execute_query("SELECT emp_id, email, role FROM users")
    user_count = len(users_df)
    if user_count != 3:
        validation_results["users_valid"] = False
        validation_results["details"].append(f"ERROR: Expected exactly 3 users, found {user_count}.")

    emp_ids = set(users_df["emp_id"].str.upper()) if not users_df.empty else set()
    if emp_ids != {"E1", "E2", "E3"}:
        validation_results["users_valid"] = False
        validation_results["details"].append(f"ERROR: Expected emp_ids {{'E1', 'E2', 'E3'}}, found {emp_ids}.")

    # 4. Foreign Key Integrity Checks
    fk_checks = [
        ("products -> categories", "SELECT COUNT(*) AS cnt FROM products p LEFT JOIN categories c ON p.category_id = c.category_id WHERE c.category_id IS NULL"),
        ("orders -> customers", "SELECT COUNT(*) AS cnt FROM orders o LEFT JOIN customers c ON o.customer_id = c.customer_id WHERE c.customer_id IS NULL"),
        ("order_items -> orders", "SELECT COUNT(*) AS cnt FROM order_items oi LEFT JOIN orders o ON oi.order_id = o.order_id WHERE o.order_id IS NULL"),
        ("order_items -> products", "SELECT COUNT(*) AS cnt FROM order_items oi LEFT JOIN products p ON oi.product_id = p.product_id WHERE p.product_id IS NULL"),
        ("inventory_logs -> products", "SELECT COUNT(*) AS cnt FROM inventory_logs il LEFT JOIN products p ON il.product_id = p.product_id WHERE p.product_id IS NULL"),
    ]

    for check_name, check_sql in fk_checks:
        df_fk = db_manager.execute_query(check_sql)
        orphan_count = int(df_fk["cnt"].iloc[0]) if not df_fk.empty else 0
        if orphan_count > 0:
            validation_results["fk_valid"] = False
            validation_results["details"].append(f"ERROR: FK violation in {check_name}: {orphan_count} orphan records.")

    return validation_results


def seed_database(
    domain_key: str = "supermarket",
    num_customers: int = 250,
    num_orders: int = 1800,
    days_span: int = 240
) -> Dict[str, int]:
    """
    Clears existing records and populates tables with newly generated domain data.
    Strictly verifies MySQL engine if configured, seeds the 3 designated users, and validates integrity.
    """
    print(f"\n=======================================================")
    print(f"[SEED] Initializing Data Seeding for Domain: '{domain_key.upper()}'")
    print(f"=======================================================")

    # Strict target check: If MySQL is configured, do not fall back to SQLite
    if DatabaseConfig.ENGINE_TYPE == "mysql" and db_manager.is_sqlite():
        raise RuntimeError(
            "CRITICAL: Database engine is configured as MySQL (DB_ENGINE=mysql in .env), "
            "but MySQL connection failed and fallback to SQLite occurred. "
            "Outlook360 controlled seed operation strictly requires MySQL and will NOT seed SQLite."
        )

    db_manager.ensure_schema()
    clear_all_tables(clear_users=True)

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
    row_counts["users"] = db_manager.get_row_count("users")

    # Post-seeding validation
    val = validate_seeded_database()
    if not (val["engine_valid"] and val["tables_valid"] and val["users_valid"] and val["fk_valid"]):
        error_msg = "\n".join(val["details"])
        raise RuntimeError(f"Database validation failed after seeding:\n{error_msg}")

    engine_name = "SQLite" if db_manager.is_sqlite() else "MySQL"
    db_name = DatabaseConfig.SQLITE_PATH if db_manager.is_sqlite() else DatabaseConfig.DB_NAME

    print(f"\n=======================================================")
    print(f"OUTLOOK360 FRESH DATASET")
    print(f"=======================================================\n")
    print(f"Database Engine: {engine_name}")
    print(f"Database: {db_name}\n")
    print(f"Users: {row_counts.get('users', 3)}")
    print(f"Business Profiles: {row_counts.get('business_profiles', 0)}")
    print(f"Categories: {row_counts.get('categories', 0)}")
    print(f"Products: {row_counts.get('products', 0)}")
    print(f"Customers: {row_counts.get('customers', 0)}")
    print(f"Orders: {row_counts.get('orders', 0)}")
    print(f"Order Items: {row_counts.get('order_items', 0)}")
    print(f"Inventory Logs: {row_counts.get('inventory_logs', 0)}\n")
    print(f"Foreign Key Validation: PASS")
    print(f"User Validation: PASS")
    print(f"Database Validation: PASS\n")
    print(f"STATUS: SUCCESS")
    print(f"=======================================================\n")

    return row_counts


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Outlook360 Database Seeding Engine")
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
