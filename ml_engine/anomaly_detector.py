"""
OmniPulse AI - Transaction Anomaly & Fraud Detection Engine
Uses Isolation Forest (unsupervised tree ensemble) and statistical Z-score
to identify fraudulent patterns, abnormal discounts, and extreme basket outliers.
"""
import sys
from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Ensure project root in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from database.connection import db_manager


class AnomalyDetector:
    """Unsupervised anomaly and outlier detection pipeline for sales transactions."""

    def detect_order_anomalies(
        self,
        contamination: float = 0.035,
        random_state: int = 42
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Runs Isolation Forest on order transaction features to flag anomalous orders.
        """
        query = """
        SELECT
            o.order_id,
            o.invoice_no,
            o.order_date,
            o.customer_id,
            c.name AS customer_name,
            c.tier AS customer_tier,
            o.payment_method,
            o.channel,
            o.subtotal,
            o.discount_amount,
            o.tax_amount,
            o.total_amount,
            COUNT(oi.item_id) AS total_line_items,
            SUM(oi.quantity) AS total_item_units
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.status = 'Completed'
        GROUP BY o.order_id, o.invoice_no, o.order_date, o.customer_id, c.name,
                 c.tier, o.payment_method, o.channel, o.subtotal, o.discount_amount,
                 o.tax_amount, o.total_amount;
        """
        df = db_manager.execute_query(query)
        if df.empty or len(df) < 20:
            return pd.DataFrame(), {"error": "Insufficient transaction records"}

        df = df.copy()
        df["order_date"] = pd.to_datetime(df["order_date"])
        df["hour_of_day"] = df["order_date"].dt.hour
        df["discount_ratio"] = (df["discount_amount"] / np.maximum(df["subtotal"], 0.01)).round(3)

        # Statistical Z-Scores
        mean_tot = df["total_amount"].mean()
        std_tot = df["total_amount"].std()
        df["z_score_amount"] = ((df["total_amount"] - mean_tot) / np.maximum(std_tot, 1e-5)).round(2)

        # Feature matrix for Isolation Forest
        feature_cols = ["subtotal", "discount_amount", "discount_ratio", "total_amount", "total_item_units", "hour_of_day"]
        X = df[feature_cols].fillna(0.0)

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Train Isolation Forest
        iso_forest = IsolationForest(
            n_estimators=120,
            contamination=contamination,
            random_state=random_state
        )
        # 1 for inliers, -1 for outliers
        preds = iso_forest.fit_predict(X_scaled)
        scores = iso_forest.decision_function(X_scaled)

        df["is_anomaly"] = np.where(preds == -1, 1, 0)
        # Invert score so higher = more anomalous
        df["anomaly_score"] = ((scores.max() - scores) / (scores.max() - scores.min())).round(3)

        # Anomaly Explanation logic
        def explain_anomaly(row):
            if row["is_anomaly"] == 0:
                return "Normal Pattern"
            reasons = []
            if row["discount_ratio"] > 0.25:
                reasons.append(f"Excessive Discount ({round(row['discount_ratio']*100)}%)")
            if row["z_score_amount"] > 2.5:
                reasons.append(f"Unusually High Spend (${row['total_amount']:.2f})")
            if row["total_item_units"] >= 8:
                reasons.append(f"Bulk Quantity Surge ({row['total_item_units']} units)")
            if row["hour_of_day"] in [1, 2, 3, 4, 5]:
                reasons.append(f"Off-Hours Transaction ({row['hour_of_day']:02d}:00)")
            return "; ".join(reasons) if reasons else "Multi-Feature Outlier"

        df["anomaly_reason"] = df.apply(explain_anomaly, axis=1)

        anomalies_only = df[df["is_anomaly"] == 1].sort_values(by="anomaly_score", ascending=False)

        summary = {
            "total_analyzed": len(df),
            "anomalies_detected": int(df["is_anomaly"].sum()),
            "anomaly_rate_pct": round((df["is_anomaly"].sum() / len(df)) * 100, 2),
            "mean_normal_amount": round(float(df[df["is_anomaly"] == 0]["total_amount"].mean()), 2),
            "mean_anomaly_amount": round(float(anomalies_only["total_amount"].mean()), 2) if not anomalies_only.empty else 0.0
        }

        return df, summary
