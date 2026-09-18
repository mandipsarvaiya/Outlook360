"""
OmniPulse AI - Database and Query Unit Tests
"""
import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from database.connection import db_manager
from database.queries import AnalyticsQueries


class TestDatabaseLayer(unittest.TestCase):
    """Verifies schema tables and basic SQL analytical queries."""

    def test_tables_exist(self):
        tables = db_manager.get_table_names()
        expected = ["business_profiles", "categories", "products", "customers", "orders", "order_items", "inventory_logs"]
        for t in expected:
            self.assertIn(t, tables, f"Expected table '{t}' was not found.")

    def test_executive_kpis(self):
        kpis = AnalyticsQueries.get_executive_kpis()
        self.assertGreater(kpis["total_orders"], 0)
        self.assertGreater(kpis["gross_revenue"], 0.0)
        self.assertGreater(kpis["active_customers"], 0)

    def test_daily_sales_series(self):
        df = AnalyticsQueries.get_daily_sales_timeseries()
        self.assertFalse(df.empty)
        self.assertIn("daily_revenue", df.columns)
        self.assertIn("order_date", df.columns)


if __name__ == "__main__":
    unittest.main()
