"""
Outlook360 - Customer Segmentation & Loyalty Analytics
Interactive RFM Quantiles, Unsupervised K-Means Clustering, Silhouette Evaluation & PCA 2D/3D Projections.
"""
import sys
from pathlib import Path
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.theme import apply_theme
from app.auth_gate import require_auth
from app.components.charts import create_pca_cluster_chart, DARK_LAYOUT_TEMPLATE
from app.components.navigation import render_sidebar_header
from ml_engine.rfm_segmentation import RFMSegmentationEngine

st.set_page_config(page_title="Customer Segmentation - Outlook360", page_icon="👥", layout="wide")
apply_theme()
render_sidebar_header()
user = require_auth(allowed_roles=["owner"])

st.markdown("## 👥 Customer Segmentation & Loyalty Intelligence")
st.markdown("Combines **Recency, Frequency, Monetary (RFM)** modeling with **K-Means Unsupervised Clustering** and **Principal Component Analysis (PCA)**.")

rfm_engine = RFMSegmentationEngine()

# Model Hyperparameter Sidebar / Controls
col_ctrl1, col_ctrl2 = st.columns([2, 2])
with col_ctrl1:
    n_clusters = st.slider("Select Number of Customer Clusters (K)", min_value=2, max_value=6, value=4, step=1)
with col_ctrl2:
    view_dim = st.radio("PCA Visualization Mode", options=["2D Projection", "3D Interactive Space"], horizontal=True)

# Run Clustering
clustered_df, model_meta = rfm_engine.run_kmeans_clustering(n_clusters=n_clusters)

if not clustered_df.empty and model_meta:
    # Top Model Metrics
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    with mcol1:
        st.metric("Total Segmented Customers", f"{len(clustered_df):,}")
    with mcol2:
        sil = model_meta.get("silhouette_score", 0.0)
        st.metric("Silhouette Score", f"{sil:.3f}", delta="Good Separation" if sil > 0.3 else "Moderate")
    with mcol3:
        st.metric("Model Inertia (WCSS)", f"{model_meta.get('inertia', 0):,.1f}")
    with mcol4:
        exp_var = sum(model_meta.get("pca_explained_variance_pct", [0, 0]))
        st.metric("PCA Explained Variance", f"{exp_var:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # PCA Scatter Plot
    is_3d = (view_dim == "3D Interactive Space")
    fig_pca = create_pca_cluster_chart(clustered_df, is_3d=is_3d)
    st.plotly_chart(fig_pca, use_container_width=True)

    # Cluster Profiles Table
    st.markdown("### 📊 Cluster Behavioral Profiles")
    summary_table = model_meta["cluster_summary"]
    st.dataframe(
        summary_table.rename(columns={
            "cluster_label": "Segment Persona",
            "customer_count": "Customers",
            "avg_recency": "Avg Recency (Days)",
            "avg_frequency": "Avg Orders",
            "avg_monetary": "Avg Spend ($)",
            "total_revenue": "Total Spend ($)",
            "revenue_share_pct": "Spend Share %"
        }).style.format({
            "Customers": "{:,.0f}",
            "Avg Recency (Days)": "{:.1f}",
            "Avg Orders": "{:.1f}",
            "Avg Spend ($)": "${:,.2f}",
            "Total Spend ($)": "${:,.2f}",
            "Spend Share %": "{:.1f}%"
        }),
        use_container_width=True
    )

    st.markdown("---")

    # Optimal Cluster Selection Curve (Elbow & Silhouette)
    with st.expander("🔬 View Elbow & Silhouette Score Diagnostic Curves", expanded=False):
        curve_data = rfm_engine.find_optimal_clusters(clustered_df, max_k=7)
        ccol1, ccol2 = st.columns(2)

        with ccol1:
            fig_elbow = go.Figure()
            fig_elbow.add_trace(go.Scatter(
                x=curve_data["k_values"],
                y=curve_data["inertias"],
                mode="lines+markers",
                line=dict(color="#6366f1", width=2.5),
                marker=dict(size=8, color="#a855f7")
            ))
            fig_elbow.update_layout(**DARK_LAYOUT_TEMPLATE, title="<b>Elbow Method (Inertia vs K)</b>", height=300)
            st.plotly_chart(fig_elbow, use_container_width=True)

        with ccol2:
            fig_sil = go.Figure()
            fig_sil.add_trace(go.Scatter(
                x=curve_data["k_values"],
                y=curve_data["silhouettes"],
                mode="lines+markers",
                line=dict(color="#10b981", width=2.5),
                marker=dict(size=8, color="#34d399")
            ))
            fig_sil.update_layout(**DARK_LAYOUT_TEMPLATE, title="<b>Silhouette Score vs K</b>", height=300)
            st.plotly_chart(fig_sil, use_container_width=True)

    # Customer Explorer Table
    with st.expander("🔍 Customer Directory & Segment Lookup", expanded=False):
        name_col = "customer_name" if "customer_name" in clustered_df.columns else "name"
        st.dataframe(
            clustered_df[[
                "customer_code", name_col, "city", "tier", "recency",
                "frequency", "monetary", "rfm_score", "cluster_name"
            ]].rename(columns={
                "customer_code": "Code",
                name_col: "Customer Name",
                "city": "City",
                "tier": "Tier",
                "recency": "Recency (Days)",
                "frequency": "Orders",
                "monetary": "Total Spend ($)",
                "rfm_score": "RFM Score",
                "cluster_name": "Cluster"
            }),
            use_container_width=True
        )
