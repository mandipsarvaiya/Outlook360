"""
OmniPulse AI - Optimized SQL Queries & Analytical Views
Provides high-performance analytical queries for executive metrics,
temporal trends, customer purchase history, and product performance.
"""
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import pandas as pd

# Ensure project root in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from database.connection import db_manager


class AnalyticsQueries:
    """Pre-compiled, optimized SQL queries for data science and dashboard reporting."""

    @staticmethod
    def get_business_profile() -> Dict[str, Any]:
        """Fetches active business profile details."""
        query = "SELECT * FROM business_profiles ORDER BY id DESC LIMIT 1"
        df = db_manager.execute_query(query)
        return df.iloc[0].to_dict() if not df.empty else {
            "domain_key": "supermarket",
            "business_name": "FreshPulse Supermarket",
            "currency": "$",
            "tax_rate": 0.05,
            "tagline": "Universal Enterprise BI Platform"
        }

    @staticmethod
    def get_executive_kpis() -> Dict[str, Any]:
        """Calculates high-level executive financial and operational KPIs."""
        query = """
        SELECT
            COUNT(DISTINCT o.order_id) AS total_orders,
            COUNT(DISTINCT o.customer_id) AS active_customers,
            COALESCE(SUM(o.total_amount), 0.0) AS gross_revenue,
            COALESCE(SUM(o.discount_amount), 0.0) AS total_discounts,
            COALESCE(SUM(oi.profit_margin), 0.0) AS net_profit,
            COALESCE(AVG(o.total_amount), 0.0) AS average_order_value,
            COALESCE(SUM(oi.quantity), 0) AS total_items_sold
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.status = 'Completed';
        """
        df = db_manager.execute_query(query)
        if df.empty:
            return {
                "total_orders": 0, "active_customers": 0, "gross_revenue": 0.0,
                "total_discounts": 0.0, "net_profit": 0.0, "average_order_value": 0.0,
                "total_items_sold": 0, "profit_margin_pct": 0.0
            }
        
        row = df.iloc[0].to_dict()
        rev = row["gross_revenue"]
        profit = row["net_profit"]
        row["profit_margin_pct"] = round((profit / rev * 100), 2) if rev > 0 else 0.0
        return row

    @staticmethod
    def get_daily_sales_timeseries() -> pd.DataFrame:
        """Fetches daily revenue, order counts, and net profit for time series modeling."""
        query = """
        SELECT
            DATE(o.order_date) AS order_date,
            COUNT(DISTINCT o.order_id) AS order_count,
            SUM(o.total_amount) AS daily_revenue,
            SUM(oi.profit_margin) AS daily_profit,
            SUM(oi.quantity) AS daily_quantity
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.status = 'Completed'
        GROUP BY DATE(o.order_date)
        ORDER BY order_date ASC;
        """
        df = db_manager.execute_query(query)
        if not df.empty:
            df["order_date"] = pd.to_datetime(df["order_date"])
        return df

    @staticmethod
    def get_category_performance() -> pd.DataFrame:
        """Aggregates revenue, units sold, and profit across product categories."""
        query = """
        SELECT
            c.name AS category_name,
            c.department,
            COUNT(DISTINCT p.product_id) AS product_count,
            SUM(oi.quantity) AS units_sold,
            SUM(oi.total_price) AS category_revenue,
            SUM(oi.profit_margin) AS category_profit,
            ROUND(SUM(oi.profit_margin) / NULLIF(SUM(oi.total_price), 0) * 100, 2) AS profit_margin_pct
        FROM categories c
        JOIN products p ON c.category_id = p.category_id
        JOIN order_items oi ON p.product_id = oi.product_id
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.status = 'Completed'
        GROUP BY c.category_id, c.name, c.department
        ORDER BY category_revenue DESC;
        """
        return db_manager.execute_query(query)

    @staticmethod
    def get_product_pareto() -> pd.DataFrame:
        """Retrieves individual product sales for 80/20 Pareto analysis."""
        query = """
        SELECT
            p.product_id,
            p.sku,
            p.name AS product_name,
            c.name AS category_name,
            p.current_stock,
            p.reorder_level,
            SUM(oi.quantity) AS total_units_sold,
            SUM(oi.total_price) AS total_revenue,
            SUM(oi.profit_margin) AS total_profit
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN order_items oi ON p.product_id = oi.product_id
        LEFT JOIN orders o ON oi.order_id = o.order_id AND o.status = 'Completed'
        GROUP BY p.product_id, p.sku, p.name, c.name, p.current_stock, p.reorder_level
        ORDER BY total_revenue DESC;
        """
        return db_manager.execute_query(query)

    @staticmethod
    def get_rfm_raw_data() -> pd.DataFrame:
        """Calculates Recency, Frequency, and Monetary baseline for all customers."""
        query = """
        SELECT
            c.customer_id,
            c.customer_code,
            c.name AS customer_name,
            c.city,
            c.tier,
            c.registered_at,
            COUNT(DISTINCT o.order_id) AS frequency,
            COALESCE(SUM(o.total_amount), 0.0) AS monetary,
            MAX(o.order_date) AS last_order_date
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status = 'Completed'
        GROUP BY c.customer_id, c.customer_code, c.name, c.city, c.tier, c.registered_at
        HAVING frequency > 0;
        """
        return db_manager.execute_query(query)

    @staticmethod
    def get_basket_transactions() -> pd.DataFrame:
        """Retrieves order-product pairs for Market Basket Analysis."""
        query = """
        SELECT
            oi.order_id,
            p.name AS product_name
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE o.status = 'Completed'
        ORDER BY oi.order_id;
        """
        return db_manager.execute_query(query)

    @staticmethod
    def get_hourly_heatmap_data() -> pd.DataFrame:
        """Extracts day of week and hour of day order density."""
        # SQLite compatible strftime or MySQL EXTRACT
        if db_manager.is_sqlite():
            query = """
            SELECT
                strftime('%w', order_date) AS day_of_week,
                strftime('%H', order_date) AS hour_of_day,
                COUNT(order_id) AS order_count,
                SUM(total_amount) AS revenue
            FROM orders
            WHERE status = 'Completed'
            GROUP BY day_of_week, hour_of_day;
            """
        else:
            query = """
            SELECT
                DAYOFWEEK(order_date) - 1 AS day_of_week,
                HOUR(order_date) AS hour_of_day,
                COUNT(order_id) AS order_count,
                SUM(total_amount) AS revenue
            FROM orders
            WHERE status = 'Completed'
            GROUP BY day_of_week, hour_of_day;
            """
        return db_manager.execute_query(query)

    @staticmethod
    def get_payment_and_channel_distribution() -> Dict[str, pd.DataFrame]:
        """Fetches payment method and channel splits."""
        pay_query = """
        SELECT payment_method, COUNT(*) AS count, SUM(total_amount) AS total_revenue
        FROM orders WHERE status = 'Completed'
        GROUP BY payment_method ORDER BY total_revenue DESC;
        """
        chan_query = """
        SELECT channel, COUNT(*) AS count, SUM(total_amount) AS total_revenue
        FROM orders WHERE status = 'Completed'
        GROUP BY channel ORDER BY total_revenue DESC;
        """
        return {
            "payment": db_manager.execute_query(pay_query),
            "channel": db_manager.execute_query(chan_query)
        }
