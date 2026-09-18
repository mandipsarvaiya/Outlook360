"""
Outlook360 - Smart Inventory Optimization & Supply Chain Intelligence
9-Box ABC-XYZ Classification, Statistical Safety Stock Modeling, and Dynamic Reorder Point (ROP) calculation.
"""
import sys
from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.theme import apply_theme
from app.auth_gate import require_auth
from app.components.charts import create_abc_xyz_matrix_chart
from app.components.navigation import render_sidebar_header
from ml_engine.inventory_optimizer import InventoryOptimizer
from ml_engine.eda_engine import EDAEngine

st.set_page_config(page_title="Inventory Optimization - Outlook360", page_icon="📦", layout="wide")
apply_theme()
render_sidebar_header()
user = require_auth(allowed_roles=["owner"])

profile = EDAEngine().get_kpi_summary()
curr = profile.get("currency", "₹")

st.markdown("## 📦 Smart Inventory & Supply Chain Optimization")
st.markdown("Implements **ABC-XYZ Matrix Analysis** and statistical **Safety Stock & Dynamic Reorder Point (ROP)** formulas to prevent stockouts and reduce carrying cost.")

optimizer = InventoryOptimizer()

# Service Level Selector
col1, col2 = st.columns([2, 2])
with col1:
    target_service_level = st.selectbox(
        "Target Service Level (Z-Factor)",
        options=["90%", "95%", "98%", "99%"],
        index=1,
        help="Higher service level ensures near-zero stockouts at the expense of higher safety stock holding."
    )
with col2:
    filter_status = st.selectbox(
        "Filter Inventory Status",
        options=["All SKUs", "Reorder Needed (Below ROP)", "Dangerously Low (Under Safety Stock)", "Optimal Stock Level", "Overstocked / Excess"]
    )

inv_df, summary = optimizer.compute_abc_xyz_matrix(service_level=target_service_level)

if not inv_df.empty:
    # Summary KPI Cards
    scol1, scol2, scol3, scol4 = st.columns(4)
    with scol1:
        st.metric("Total Catalog SKUs", f"{summary.get('total_skus', 0)}")
    with scol2:
        reorder_cnt = summary.get('items_needing_reorder', 0)
        st.metric("SKUs Needing Reorder", f"{reorder_cnt}", delta=f"-{reorder_cnt} action required" if reorder_cnt > 0 else "All Good")
    with scol3:
        st.metric("Target Service Level", f"{summary.get('service_level', '95%')} (Z={summary.get('z_factor', 1.65)})")
    with scol4:
        out_cnt = summary.get('out_of_stock_count', 0)
        st.metric("Stockouts (Zero Units)", f"{out_cnt}")

    st.markdown("<br>", unsafe_allow_html=True)

    # 9-Box ABC-XYZ Heatmap Matrix
    fig_matrix = create_abc_xyz_matrix_chart(inv_df)
    st.plotly_chart(fig_matrix, use_container_width=True)

    # Filtered Table
    display_df = inv_df.copy()
    if filter_status != "All SKUs":
        display_df = display_df[display_df["stock_status"] == filter_status]

    st.markdown(f"### 📋 Inventory Replenishment & Safety Stock Schedule ({len(display_df)} SKUs)")
    st.dataframe(
        display_df[[
            "sku", "product_name", "category_name", "current_stock",
            "statistical_safety_stock", "calculated_rop", "lead_time_days",
            "abc_xyz_segment", "stock_status", "suggested_reorder_qty"
        ]].rename(columns={
            "sku": "SKU",
            "product_name": "Product Name",
            "category_name": "Category",
            "current_stock": "Current Stock",
            "statistical_safety_stock": "Safety Stock (SS)",
            "calculated_rop": "Reorder Point (ROP)",
            "lead_time_days": "Lead Time (Days)",
            "abc_xyz_segment": "ABC-XYZ Class",
            "stock_status": "Stock Health Status",
            "suggested_reorder_qty": "Suggested Order Qty"
        }),
        use_container_width=True
    )
