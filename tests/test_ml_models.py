"""
OmniPulse AI - Machine Learning & Analytics Unit Tests
"""
import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ml_engine.eda_engine import EDAEngine
from ml_engine.rfm_segmentation import RFMSegmentationEngine
from ml_engine.demand_forecaster import DemandForecaster
from ml_engine.market_basket import MarketBasketEngine
from ml_engine.inventory_optimizer import InventoryOptimizer
from ml_engine.anomaly_detector import AnomalyDetector


class TestMLEngines(unittest.TestCase):
    """Tests all statistical and machine learning pipelines."""

    def test_eda_engine(self):
        engine = EDAEngine()
        kpis = engine.get_kpi_summary()
        self.assertGreater(kpis["gross_revenue"], 0)
        pareto_df, summary = engine.get_pareto_analysis()
        self.assertFalse(pareto_df.empty)
        self.assertIn("pareto_class", pareto_df.columns)

    def test_rfm_kmeans_clustering(self):
        engine = RFMSegmentationEngine()
        df, meta = engine.run_kmeans_clustering(n_clusters=4)
        self.assertFalse(df.empty)
        self.assertIn("cluster_id", df.columns)
        self.assertIn("pca_x", df.columns)
        self.assertGreater(meta["silhouette_score"], -1.0)

    def test_demand_forecasting(self):
        forecaster = DemandForecaster()
        hist, fc, metrics = forecaster.forecast_holt_winters(forecast_horizon=14, test_days=20)
        self.assertEqual(len(fc), 14)
        self.assertIn("forecast", fc.columns)
        self.assertIn("lower_bound", fc.columns)
        self.assertIn("upper_bound", fc.columns)
        self.assertGreater(metrics["mae"], 0.0)

    def test_market_basket_apriori(self):
        engine = MarketBasketEngine()
        rules, meta = engine.generate_association_rules(min_support=0.01, min_confidence=0.10)
        self.assertIn("total_transactions", meta)

    def test_inventory_optimizer(self):
        optimizer = InventoryOptimizer()
        df, summary = optimizer.compute_abc_xyz_matrix(service_level="95%")
        self.assertFalse(df.empty)
        self.assertIn("abc_class", df.columns)
        self.assertIn("xyz_class", df.columns)
        self.assertIn("calculated_rop", df.columns)

    def test_anomaly_detector(self):
        detector = AnomalyDetector()
        df, summary = detector.detect_order_anomalies(contamination=0.03)
        self.assertFalse(df.empty)
        self.assertIn("is_anomaly", df.columns)
        self.assertIn("anomaly_score", df.columns)


if __name__ == "__main__":
    unittest.main()
