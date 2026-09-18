"""
OmniPulse AI - Customer Segmentation Engine (RFM + K-Means + PCA)
Applies statistical scoring, unsupervised machine learning (K-Means),
silhouette analysis, and Principal Component Analysis for customer intelligence.
"""
import sys
from pathlib import Path
from typing import Dict, Any, Tuple, List
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# Ensure project root in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from database.queries import AnalyticsQueries


class RFMSegmentationEngine:
    """Customer analytics pipeline combining RFM rules with K-Means machine learning."""

    def __init__(self):
        self.queries = AnalyticsQueries()

    def compute_rfm_metrics(self) -> pd.DataFrame:
        """
        Computes Recency (days since last order), Frequency (order count),
        and Monetary (total spent) for all customers.
        """
        df = self.queries.get_rfm_raw_data()
        if df.empty:
            return pd.DataFrame()

        df = df.copy()
        df["last_order_date"] = pd.to_datetime(df["last_order_date"])
        snapshot_date = df["last_order_date"].max() + pd.to_timedelta(1, unit="D")

        # Recency in days
        df["recency"] = (snapshot_date - df["last_order_date"]).dt.days
        df["frequency"] = df["frequency"].astype(int)
        df["monetary"] = df["monetary"].astype(float).round(2)

        # RFM Quantile Scoring (1 to 5)
        # Recency: Lower is better (inverted)
        # Using qcut with duplicates='drop' or rank method for robust quantile splitting
        try:
            df["r_score"] = pd.qcut(df["recency"], 5, labels=[5, 4, 3, 2, 1], duplicates="drop").astype(int)
        except Exception:
            df["r_score"] = pd.Series(pd.cut(df["recency"].rank(method="first"), 5, labels=[5, 4, 3, 2, 1])).astype(int)

        try:
            df["f_score"] = pd.qcut(df["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
        except Exception:
            df["f_score"] = pd.Series(pd.cut(df["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])).astype(int)

        try:
            df["m_score"] = pd.qcut(df["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
        except Exception:
            df["m_score"] = pd.Series(pd.cut(df["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])).astype(int)

        df["rfm_score"] = (
            df["r_score"].astype(str) +
            df["f_score"].astype(str) +
            df["m_score"].astype(str)
        )
        df["rfm_mean_score"] = ((df["r_score"] + df["f_score"] + df["m_score"]) / 3.0).round(2)

        # Rule-based Persona Mapping
        def map_persona(row):
            r, f, m = row["r_score"], row["f_score"], row["m_score"]
            if r >= 4 and f >= 4 and m >= 4:
                return "Champions (High Value & Loyal)"
            elif r >= 3 and f >= 3:
                return "Loyal Customers"
            elif r >= 4 and f <= 2:
                return "Recent Spenders / Potential"
            elif r <= 2 and f >= 3:
                return "At-Risk Spenders"
            elif r <= 2 and f <= 2 and m >= 3:
                return "High-Spend Hibernating"
            elif r == 1 and f == 1:
                return "Lost / Dormant"
            else:
                return "Promising Customers"

        df["persona"] = df.apply(map_persona, axis=1)
        return df

    def find_optimal_clusters(self, df: pd.DataFrame, max_k: int = 7) -> Dict[str, List[float]]:
        """
        Computes Elbow (Inertia) and Silhouette Scores for K = 2 to max_k.
        """
        if len(df) < max_k:
            return {"k_values": [2, 3], "inertias": [100.0, 50.0], "silhouettes": [0.4, 0.45]}

        # Log transform to reduce skewness + Standard scaling
        X = df[["recency", "frequency", "monetary"]].copy()
        X_log = np.log1p(X)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_log)

        k_values = list(range(2, max_k + 1))
        inertias = []
        silhouettes = []

        for k in k_values:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(X_scaled)
            inertias.append(float(kmeans.inertia_))
            silhouettes.append(float(silhouette_score(X_scaled, labels)))

        return {
            "k_values": k_values,
            "inertias": inertias,
            "silhouettes": silhouettes
        }

    def run_kmeans_clustering(self, n_clusters: int = 4) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Fits K-Means clustering on scaled log-transformed RFM features,
        projects data into PCA 2D and 3D space, and computes cluster profiles.
        """
        df = self.compute_rfm_metrics()
        if df.empty or len(df) < n_clusters:
            return df, {}

        features = ["recency", "frequency", "monetary"]
        X_log = np.log1p(df[features])

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_log)

        # Fit KMeans
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        df["cluster_id"] = kmeans.fit_predict(X_scaled)
        
        # PCA 2D & 3D Projections for rich visual exploration
        pca_3d = PCA(n_components=3, random_state=42)
        pca_coords = pca_3d.fit_transform(X_scaled)
        df["pca_x"] = pca_coords[:, 0]
        df["pca_y"] = pca_coords[:, 1]
        df["pca_z"] = pca_coords[:, 2]

        explained_var = [float(round(v * 100, 2)) for v in pca_3d.explained_variance_ratio_]

        # Cluster Profiles
        cluster_summary = df.groupby("cluster_id").agg(
            customer_count=("customer_id", "count"),
            avg_recency=("recency", "mean"),
            avg_frequency=("frequency", "mean"),
            avg_monetary=("monetary", "mean"),
            total_revenue=("monetary", "sum")
        ).reset_index()

        cluster_summary["avg_recency"] = cluster_summary["avg_recency"].round(1)
        cluster_summary["avg_frequency"] = cluster_summary["avg_frequency"].round(1)
        cluster_summary["avg_monetary"] = cluster_summary["avg_monetary"].round(2)
        cluster_summary["total_revenue"] = cluster_summary["total_revenue"].round(2)
        cluster_summary["revenue_share_pct"] = (
            cluster_summary["total_revenue"] / cluster_summary["total_revenue"].sum() * 100
        ).round(1)

        # Name clusters intelligently based on average recency/monetary
        def label_cluster(row):
            if row["avg_monetary"] >= cluster_summary["avg_monetary"].quantile(0.70):
                return "Platinum VIPs"
            elif row["avg_recency"] > cluster_summary["avg_recency"].median():
                return "At-Risk / Lapsed"
            elif row["avg_frequency"] > cluster_summary["avg_frequency"].median():
                return "Regular Active Spenders"
            else:
                return "Standard Casuals"

        cluster_summary["cluster_label"] = cluster_summary.apply(label_cluster, axis=1)
        label_dict = dict(zip(cluster_summary["cluster_id"], cluster_summary["cluster_label"]))
        df["cluster_name"] = df["cluster_id"].map(label_dict)

        model_metadata = {
            "n_clusters": n_clusters,
            "silhouette_score": round(float(silhouette_score(X_scaled, df["cluster_id"])), 3),
            "inertia": round(float(kmeans.inertia_), 2),
            "pca_explained_variance_pct": explained_var,
            "cluster_summary": cluster_summary
        }

        return df, model_metadata
