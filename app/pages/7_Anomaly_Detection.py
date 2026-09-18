"""
Outlook360 - Anomaly & Fraud Detection Dashboard
Unsupervised Isolation Forest and statistical Z-score outlier detection for sales invoices.
"""
import sys
from pathlib import Path
import streamlit as st
import plotly.express as px

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.theme import apply_theme
from app.auth_gate import require_auth
from app.components.charts import DARK_LAYOUT_TEMPLATE
from app.components.navigation import render_sidebar_header
from ml_engine.anomaly_detector import AnomalyDetector
from ml_engine.eda_engine import EDAEngine

st.set_page_config(page_title="Anomaly Detection - Outlook360", page_icon="🚨", layout="wide")
apply_theme()
render_sidebar_header()
user = require_auth(allowed_roles=["owner"])

profile = EDAEngine().get_kpi_summary()
curr = profile.get("currency", "₹")

st.markdown("## 🚨 Transaction Anomaly & Fraud Detection Engine")
st.markdown("Employs **Isolation Forest (Unsupervised Ensemble)** and **Statistical Z-Scores** to detect abnormal discounts, cart size surges, and off-hour transactional anomalies.")

detector = AnomalyDetector()

# Contamination Slider
contamination = st.slider("Model Contamination Factor (Expected Outlier %)", min_value=0.01, max_value=0.08, value=0.035, step=0.005, format="%.3f")

anom_df, summary = detector.detect_order_anomalies(contamination=contamination)

if not anom_df.empty:
    # Summary KPI Cards
    acol1, acol2, acol3, acol4 = st.columns(4)
    with acol1:
        st.metric("Total Invoices Scanned", f"{summary.get('total_analyzed', 0):,}")
    with acol2:
        detected = summary.get('anomalies_detected', 0)
        st.metric("Flagged Outlier Invoices", f"{detected}", delta=f"{summary.get('anomaly_rate_pct', 0)}% Anomaly Rate")
    with acol3:
        st.metric("Normal Avg Spend", f"{curr}{summary.get('mean_normal_amount', 0):,.2f}")
    with acol4:
        st.metric("Anomaly Avg Spend", f"{curr}{summary.get('mean_anomaly_amount', 0):,.2f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Anomaly Scatter Chart
    fig_anom = px.scatter(
        anom_df,
        x="subtotal",
        y="discount_amount",
        color=anom_df["is_anomaly"].map({0: "Normal Transaction", 1: "Flagged Anomaly"}),
        size="total_item_units",
        hover_name="invoice_no",
        hover_data=["customer_name", "total_amount", "discount_ratio", "anomaly_reason", "hour_of_day"],
        title="<b>Transaction Anomaly Landscape (Subtotal vs Discount Amount)</b>",
        color_discrete_map={"Normal Transaction": "#6366f1", "Flagged Anomaly": "#ef4444"}
    )
    fig_anom.update_layout(**DARK_LAYOUT_TEMPLATE, height=400)
    st.plotly_chart(fig_anom, use_container_width=True)

    # Flagged Anomalies Detail Table
    st.markdown("### 📋 Flagged Suspicious Transactions & Root Cause Analysis")
    anomalies_only = anom_df[anom_df["is_anomaly"] == 1].sort_values(by="anomaly_score", ascending=False)

    if not anomalies_only.empty:
        st.dataframe(
            anomalies_only[[
                "invoice_no", "order_date", "customer_name", "customer_tier",
                "total_amount", "discount_amount", "discount_ratio",
                "total_item_units", "anomaly_score", "anomaly_reason"
            ]].rename(columns={
                "invoice_no": "Invoice #",
                "order_date": "Date & Time",
                "customer_name": "Customer",
                "customer_tier": "Tier",
                "total_amount": f"Total ({curr})",
                "discount_amount": f"Discount ({curr})",
                "discount_ratio": "Discount Ratio",
                "total_item_units": "Units",
                "anomaly_score": "Outlier Score",
                "anomaly_reason": "AI Diagnosis Reason"
            }).style.format({
                f"Total ({curr})": "{:,.2f}",
                f"Discount ({curr})": "{:,.2f}",
                "Discount Ratio": "{:.1%}",
                "Outlier Score": "{:.3f}"
            }),
            use_container_width=True
        )
    else:
        st.success("No anomalies detected at the current threshold level.")
