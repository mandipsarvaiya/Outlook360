"""
Outlook360 - Executive Overview Dashboard
Comprehensive financial KPIs, MoM growth trends, department breakdowns, and footfall heatmaps.
"""
import sys
from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.theme import apply_theme
from app.auth_gate import require_auth
from app.components.kpi_cards import render_kpi_grid
from app.components.charts import create_revenue_trend_chart, create_heatmap_chart
from app.components.navigation import render_sidebar_header
from ml_engine.eda_engine import EDAEngine
from database.queries import AnalyticsQueries

st.set_page_config(page_title="Executive Overview - Outlook360", page_icon="📊", layout="wide")
apply_theme()
render_sidebar_header()
user = require_auth(allowed_roles=["owner"])

eda = EDAEngine()
kpis = eda.get_kpi_summary()
curr = kpis.get("currency", "₹")

st.markdown("## 📊 Executive BI & Financial Overview")
st.markdown("Real-time aggregated financial performance, growth velocity, and store traffic density.")

# Top KPI Cards
render_kpi_grid(kpis)

st.markdown("<br>", unsafe_allow_html=True)

# Daily Revenue & Profit Trend Chart
daily_df = AnalyticsQueries.get_daily_sales_timeseries()
if not daily_df.empty:
    fig_rev = create_revenue_trend_chart(daily_df, currency=curr)
    st.plotly_chart(fig_rev, use_container_width=True)

# Monthly Growth & Department Breakdown
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📈 Month-over-Month (MoM) Growth")
    monthly_df = eda.get_monthly_growth_trend()
    if not monthly_df.empty:
        st.dataframe(
            monthly_df[["month_label", "revenue", "profit", "orders", "revenue_growth_pct", "profit_margin_pct"]].rename(columns={
                "month_label": "Month",
                "revenue": f"Revenue ({curr})",
                "profit": f"Profit ({curr})",
                "orders": "Orders",
                "revenue_growth_pct": "MoM Growth %",
                "profit_margin_pct": "Margin %"
            }).style.format({
                f"Revenue ({curr})": "{:,.2f}",
                f"Profit ({curr})": "{:,.2f}",
                "Orders": "{:,.0f}",
                "MoM Growth %": "{:+.1f}%",
                "Margin %": "{:.1f}%"
            }),
            use_container_width=True,
            height=260
        )

with col2:
    st.markdown("### 🏢 Category & Department Share")
    cat_df = AnalyticsQueries.get_category_performance()
    if not cat_df.empty:
        st.dataframe(
            cat_df[["category_name", "department", "units_sold", "category_revenue", "profit_margin_pct"]].rename(columns={
                "category_name": "Category",
                "department": "Department",
                "units_sold": "Units Sold",
                "category_revenue": f"Revenue ({curr})",
                "profit_margin_pct": "Margin %"
            }).style.format({
                f"Revenue ({curr})": "{:,.2f}",
                "Units Sold": "{:,.0f}",
                "Margin %": "{:.1f}%"
            }),
            use_container_width=True,
            height=260
        )

st.markdown("<br>", unsafe_allow_html=True)

# Hourly Footfall Density Heatmap
st.markdown("### 🕒 Operational Traffic & Footfall Heatmap")
heatmap_matrix = eda.get_hourly_heatmap_matrix()
if not heatmap_matrix.empty:
    fig_heat = create_heatmap_chart(heatmap_matrix)
    st.plotly_chart(fig_heat, use_container_width=True)
