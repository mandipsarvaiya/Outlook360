"""
OmniPulse AI - Smart Inventory Optimization & Supply Chain Intelligence Engine
Implements ABC-XYZ Matrix Classification, Statistical Safety Stock Modeling,
and Dynamic Reorder Point (ROP) calculation.
"""
import sys
from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np

# Ensure project root in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from database.connection import db_manager


class InventoryOptimizer:
    """Enterprise inventory analytics, ABC/XYZ classification, and replenishment engine."""

    # Z-scores for standard target service levels
    SERVICE_LEVEL_Z = {
        "90%": 1.28,
        "95%": 1.65,
        "98%": 2.05,
        "99%": 2.33
    }

    def compute_abc_xyz_matrix(self, service_level: str = "95%") -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Calculates ABC (Revenue share) and XYZ (Demand volatility CV) classes,
        computes Safety Stock, Reorder Points, and stockout risk.
        """
        z = self.SERVICE_LEVEL_Z.get(service_level, 1.65)

        # 1. Product baseline & demand statistics
        query = """
        SELECT
            p.product_id,
            p.sku,
            p.name AS product_name,
            c.name AS category_name,
            p.cost_price,
            p.unit_price,
            p.current_stock,
            p.reorder_level AS configured_reorder_level,
            p.lead_time_days,
            p.shelf_life_days,
            COALESCE(SUM(oi.quantity), 0) AS total_units_sold,
            COALESCE(SUM(oi.total_price), 0.0) AS total_revenue,
            COALESCE(SUM(oi.profit_margin), 0.0) AS total_profit
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN order_items oi ON p.product_id = oi.product_id
        LEFT JOIN orders o ON oi.order_id = o.order_id AND o.status = 'Completed'
        GROUP BY p.product_id, p.sku, p.name, c.name, p.cost_price, p.unit_price,
                 p.current_stock, p.reorder_level, p.lead_time_days, p.shelf_life_days
        ORDER BY total_revenue DESC;
        """
        df = db_manager.execute_query(query)
        if df.empty:
            return pd.DataFrame(), {}

        # 2. Daily demand variance per product
        daily_demand_query = """
        SELECT
            oi.product_id,
            DATE(o.order_date) AS sale_date,
            SUM(oi.quantity) AS daily_qty
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.status = 'Completed'
        GROUP BY oi.product_id, DATE(o.order_date);
        """
        daily_df = db_manager.execute_query(daily_demand_query)

        # Compute mean and standard deviation of daily demand per product
        if not daily_df.empty:
            demand_stats = daily_df.groupby("product_id")["daily_qty"].agg(
                avg_daily_demand="mean",
                std_daily_demand="std"
            ).reset_index()
            demand_stats["std_daily_demand"] = demand_stats["std_daily_demand"].fillna(0.0)
            df = df.merge(demand_stats, on="product_id", how="left")
        else:
            df["avg_daily_demand"] = 1.0
            df["std_daily_demand"] = 0.5

        df["avg_daily_demand"] = df["avg_daily_demand"].fillna(0.1)
        df["std_daily_demand"] = df["std_daily_demand"].fillna(0.05)

        # 3. ABC Classification (Cumulative Revenue Share)
        total_revenue = df["total_revenue"].sum()
        df["revenue_share_pct"] = (df["total_revenue"] / total_revenue) * 100 if total_revenue > 0 else 0.0
        df["cumulative_revenue_pct"] = df["revenue_share_pct"].cumsum()

        def assign_abc(cum_pct):
            if cum_pct <= 70.0:
                return "A"
            elif cum_pct <= 90.0:
                return "B"
            else:
                return "C"

        df["abc_class"] = df["cumulative_revenue_pct"].apply(assign_abc)

        # 4. XYZ Classification (Coefficient of Variation CV = std / mean)
        df["cv_demand"] = (df["std_daily_demand"] / np.maximum(df["avg_daily_demand"], 0.01)).round(3)

        def assign_xyz(cv):
            if cv <= 0.45:
                return "X"
            elif cv <= 0.85:
                return "Y"
            else:
                return "Z"

        df["xyz_class"] = df["cv_demand"].apply(assign_xyz)
        df["abc_xyz_segment"] = df["abc_class"] + df["xyz_class"]

        # 5. Statistical Safety Stock & Dynamic Reorder Point
        # Formula: SS = Z * sqrt(LeadTime) * StdDev_Demand
        df["statistical_safety_stock"] = np.ceil(
            z * np.sqrt(df["lead_time_days"]) * df["std_daily_demand"]
        ).astype(int)

        # Formula: ROP = (Avg_Demand * LeadTime) + SafetyStock
        df["calculated_rop"] = np.ceil(
            (df["avg_daily_demand"] * df["lead_time_days"]) + df["statistical_safety_stock"]
        ).astype(int)

        # 6. Stock Status & Urgency Alert
        def evaluate_stock_status(row):
            current = row["current_stock"]
            rop = row["calculated_rop"]
            ss = row["statistical_safety_stock"]
            if current <= 0:
                return "Out of Stock (Critical)"
            elif current <= ss:
                return "Dangerously Low (Under Safety Stock)"
            elif current <= rop:
                return "Reorder Needed (Below ROP)"
            elif current > (rop * 2.5):
                return "Overstocked / Excess Capital"
            else:
                return "Optimal Stock Level"

        df["stock_status"] = df.apply(evaluate_stock_status, axis=1)

        # Suggested Replenishment Order Quantity (EOQ or 30-day supply)
        df["suggested_reorder_qty"] = np.maximum(
            0,
            np.ceil((df["avg_daily_demand"] * 30) + df["statistical_safety_stock"] - df["current_stock"])
        ).astype(int)

        # Summary Metrics
        summary = {
            "total_skus": len(df),
            "service_level": service_level,
            "z_factor": z,
            "items_needing_reorder": len(df[df["current_stock"] <= df["calculated_rop"]]),
            "out_of_stock_count": len(df[df["current_stock"] <= 0]),
            "class_counts": df["abc_xyz_segment"].value_counts().to_dict(),
            "abc_counts": df["abc_class"].value_counts().to_dict(),
            "xyz_counts": df["xyz_class"].value_counts().to_dict()
        }

        return df, summary
