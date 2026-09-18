"""
OmniPulse AI - Automated Exploratory Data Analysis & Business Intelligence Engine
Computes statistical aggregates, temporal trends, Pareto distributions, and executive KPIs.
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

from database.queries import AnalyticsQueries


class EDAEngine:
    """Automated EDA and descriptive statistical analytics pipeline."""

    def __init__(self):
        self.queries = AnalyticsQueries()

    def get_kpi_summary(self) -> Dict[str, Any]:
        """Returns structured executive KPIs with formatted values."""
        raw_kpis = self.queries.get_executive_kpis()
        profile = self.queries.get_business_profile()
        currency = profile.get("currency", "$")

        return {
            "business_name": profile.get("business_name", "Enterprise Retail"),
            "domain_key": profile.get("domain_key", "supermarket"),
            "currency": currency,
            "gross_revenue": float(raw_kpis.get("gross_revenue", 0.0)),
            "net_profit": float(raw_kpis.get("net_profit", 0.0)),
            "profit_margin_pct": float(raw_kpis.get("profit_margin_pct", 0.0)),
            "total_orders": int(raw_kpis.get("total_orders", 0)),
            "active_customers": int(raw_kpis.get("active_customers", 0)),
            "average_order_value": float(raw_kpis.get("average_order_value", 0.0)),
            "total_items_sold": int(raw_kpis.get("total_items_sold", 0)),
            "total_discounts": float(raw_kpis.get("total_discounts", 0.0))
        }

    def get_monthly_growth_trend(self) -> pd.DataFrame:
        """Computes Month-over-Month (MoM) revenue, profit, and growth percentage."""
        daily_df = self.queries.get_daily_sales_timeseries()
        if daily_df.empty:
            return pd.DataFrame()

        daily_df["month_year"] = daily_df["order_date"].dt.to_period("M")
        monthly = daily_df.groupby("month_year").agg(
            revenue=("daily_revenue", "sum"),
            profit=("daily_profit", "sum"),
            orders=("order_count", "sum"),
            quantity=("daily_quantity", "sum")
        ).reset_index()

        monthly["month_label"] = monthly["month_year"].astype(str)
        monthly["revenue_growth_pct"] = monthly["revenue"].pct_change() * 100
        monthly["profit_margin_pct"] = (monthly["profit"] / monthly["revenue"]) * 100
        monthly.fillna({"revenue_growth_pct": 0.0}, inplace=True)
        return monthly

    def get_pareto_analysis(self) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Calculates Pareto 80/20 distribution:
        Sorts products by revenue descending, computes cumulative percentage,
        and flags products as 'Vital Few (Top 80%)' vs 'Trivial Many (Bottom 20%)'.
        """
        df = self.queries.get_product_pareto()
        if df.empty:
            return df, {}

        df = df.copy()
        df["total_revenue"] = df["total_revenue"].fillna(0.0)
        df = df.sort_values(by="total_revenue", ascending=False).reset_index(drop=True)

        total_rev = df["total_revenue"].sum()
        df["revenue_share_pct"] = (df["total_revenue"] / total_rev) * 100 if total_rev > 0 else 0
        df["cumulative_revenue"] = df["total_revenue"].cumsum()
        df["cumulative_pct"] = (df["cumulative_revenue"] / total_rev) * 100 if total_rev > 0 else 0

        # Pareto Classification
        df["pareto_class"] = np.where(df["cumulative_pct"] <= 80.0, "Vital Few (Top 80%)", "Useful Many (Bottom 20%)")

        vital_count = len(df[df["pareto_class"] == "Vital Few (Top 80%)"])
        total_count = len(df)
        vital_product_pct = round((vital_count / total_count) * 100, 1) if total_count > 0 else 0

        summary = {
            "total_products": total_count,
            "vital_products_count": vital_count,
            "vital_products_pct": vital_product_pct,
            "total_revenue": total_rev
        }
        return df, summary

    def get_hourly_heatmap_matrix(self) -> pd.DataFrame:
        """Formats hourly footfall and sales data into a 7-day x 24-hour matrix."""
        df = self.queries.get_hourly_heatmap_data()
        if df.empty:
            return pd.DataFrame()

        df["day_of_week"] = df["day_of_week"].astype(int)
        df["hour_of_day"] = df["hour_of_day"].astype(int)

        day_names = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
        df["day_name"] = df["day_of_week"].map(day_names)

        # Pivot to Day x Hour
        pivot_df = df.pivot_table(
            index="day_name",
            columns="hour_of_day",
            values="order_count",
            aggfunc="sum",
            fill_value=0
        )
        # Reorder days
        ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        pivot_df = pivot_df.reindex([d for d in ordered_days if d in pivot_df.index])
        return pivot_df
