"""
Outlook360 - Sales & Pareto Analytics Dashboard
Deep-dive revenue streams, 80/20 Pareto principle product analysis, and payment channel distribution.
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
from app.components.charts import create_pareto_chart, DARK_LAYOUT_TEMPLATE
from app.components.navigation import render_sidebar_header
from ml_engine.eda_engine import EDAEngine
from database.queries import AnalyticsQueries

st.set_page_config(page_title="Sales & Pareto Analytics - Outlook360", page_icon="📈", layout="wide")
apply_theme()
render_sidebar_header()
user = require_auth(allowed_roles=["owner"])

eda = EDAEngine()
kpis = eda.get_kpi_summary()
curr = kpis.get("currency", "₹")

st.markdown("## 📈 Sales Performance & Pareto (80/20) Analytics")
st.markdown("Detailed breakdown of catalog revenue generation, cumulative contribution curves, and payment channels.")

# Pareto 80/20 Analysis Section
pareto_df, summary = eda.get_pareto_analysis()

pcol1, pcol2, pcol3, pcol4 = st.columns(4)
with pcol1:
    st.metric("Total Active SKUs", f"{summary.get('total_products', 0)}")
with pcol2:
    vital = summary.get('vital_products_count', 0)
    st.metric("Vital Few (Top 80% Drivers)", f"{vital} SKUs", delta=f"{summary.get('vital_products_pct', 0)}% of Catalog")
with pcol3:
    st.metric("Useful Many (Bottom 20%)", f"{summary.get('total_products', 0) - vital} SKUs")
with pcol4:
    st.metric("Catalog Gross Revenue", f"{curr}{summary.get('total_revenue', 0.0):,.2f}")

st.markdown("<br>", unsafe_allow_html=True)

if not pareto_df.empty:
    fig_pareto = create_pareto_chart(pareto_df, currency=curr)
    st.plotly_chart(fig_pareto, use_container_width=True)

# Vital vs Non-Vital Product Breakdown Table
with st.expander("📋 View Complete Pareto Product Classification Table", expanded=False):
    st.dataframe(
        pareto_df[[
            "sku", "product_name", "category_name", "total_units_sold",
            "total_revenue", "revenue_share_pct", "cumulative_pct", "pareto_class"
        ]].rename(columns={
            "sku": "SKU",
            "product_name": "Product Name",
            "category_name": "Category",
            "total_units_sold": "Units Sold",
            "total_revenue": f"Revenue ({curr})",
            "revenue_share_pct": "Share %",
            "cumulative_pct": "Cumulative %",
            "pareto_class": "Pareto Class"
        }).style.format({
            f"Revenue ({curr})": "{:,.2f}",
            "Units Sold": "{:,.0f}",
            "Share %": "{:.1f}%",
            "Cumulative %": "{:.1f}%"
        }),
        use_container_width=True
    )

st.markdown("---")

# Payment Methods & Channels Donut Distribution
st.markdown("### 💳 Payment Methods & Sales Channel Distribution")
dist = AnalyticsQueries.get_payment_and_channel_distribution()

dcol1, dcol2 = st.columns(2)

with dcol1:
    pay_df = dist["payment"]
    if not pay_df.empty:
        fig_pay = px.pie(
            pay_df,
            names="payment_method",
            values="total_revenue",
            hole=0.45,
            title="<b>Revenue by Payment Method</b>",
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_pay.update_layout(**DARK_LAYOUT_TEMPLATE, height=340)
        st.plotly_chart(fig_pay, use_container_width=True)

with dcol2:
    chan_df = dist["channel"]
    if not chan_df.empty:
        fig_chan = px.pie(
            chan_df,
            names="channel",
            values="total_revenue",
            hole=0.45,
            title="<b>Revenue by Sales Channel</b>",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_chan.update_layout(**DARK_LAYOUT_TEMPLATE, height=340)
        st.plotly_chart(fig_chan, use_container_width=True)
