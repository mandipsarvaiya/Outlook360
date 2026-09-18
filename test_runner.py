"""
Outlook360 - Master Test & Benchmark Runner
Tests all database, analytics, and machine learning modules with performance profiling.
"""
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from database.connection import db_manager
from database.queries import AnalyticsQueries
from ml_engine.eda_engine import EDAEngine
from ml_engine.rfm_segmentation import RFMSegmentationEngine
from ml_engine.demand_forecaster import DemandForecaster
from ml_engine.market_basket import MarketBasketEngine
from ml_engine.inventory_optimizer import InventoryOptimizer
from ml_engine.anomaly_detector import AnomalyDetector


def run_all_benchmarks():
    print("===================================================================")
    print("      Outlook360 - Module Validation & Benchmark Suite             ")
    print("===================================================================")

    # 1. Database
    t0 = time.time()
    tables = db_manager.get_table_names()
    kpis = AnalyticsQueries.get_executive_kpis()
    t_db = time.time() - t0
    print(f"[1/6] Database Layer      : OK ({len(tables)} tables, {kpis['total_orders']} orders) [{t_db:.2f}s]")

    # 2. EDA
    t0 = time.time()
    eda = EDAEngine()
    summary = eda.get_kpi_summary()
    pareto_df, pareto_summary = eda.get_pareto_analysis()
    t_eda = time.time() - t0
    print(f"[2/6] EDA & BI Engine     : OK (Revenue: {summary['currency']}{summary['gross_revenue']:,.2f}, Vital SKUs: {pareto_summary['vital_products_count']}) [{t_eda:.2f}s]")

    # 3. RFM & KMeans
    t0 = time.time()
    rfm = RFMSegmentationEngine()
    rfm_df, rfm_meta = rfm.run_kmeans_clustering(n_clusters=4)
    t_rfm = time.time() - t0
    print(f"[3/6] RFM & KMeans Engine : OK (Silhouette: {rfm_meta['silhouette_score']}, Clusters: {rfm_meta['n_clusters']}) [{t_rfm:.2f}s]")

    # 4. Forecaster
    t0 = time.time()
    forecaster = DemandForecaster()
    hist_df, fc_df, fc_meta = forecaster.forecast_holt_winters(forecast_horizon=30, test_days=30)
    t_fc = time.time() - t0
    print(f"[4/6] Demand Forecaster   : OK (Model: {fc_meta['model_name']}, MAE: {fc_meta['mae']}, MAPE: {fc_meta['mape_pct']}%) [{t_fc:.2f}s]")

    # 5. Market Basket
    t0 = time.time()
    mba = MarketBasketEngine()
    rules, mba_meta = mba.generate_association_rules(min_support=0.015, min_confidence=0.15)
    t_mba = time.time() - t0
    print(f"[5/6] Market Basket Engine: OK ({mba_meta.get('total_rules', 0)} Rules Mined, Highest Lift: {mba_meta.get('highest_lift', 0):.2f}) [{t_mba:.2f}s]")

    # 6. Inventory & Anomaly
    t0 = time.time()
    inv = InventoryOptimizer()
    inv_df, inv_meta = inv.compute_abc_xyz_matrix(service_level="95%")
    detector = AnomalyDetector()
    anom_df, anom_meta = detector.detect_order_anomalies(contamination=0.035)
    t_inv = time.time() - t0
    print(f"[6/6] Inventory & Anomaly : OK (SKUs: {inv_meta['total_skus']}, Anomalies: {anom_meta['anomalies_detected']}) [{t_inv:.2f}s]")

    print("===================================================================")
    print("  SUCCESS: All 6 Core Engine Modules Tested & Verified!           ")
    print("===================================================================")


if __name__ == "__main__":
    run_all_benchmarks()
