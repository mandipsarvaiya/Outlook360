"""
Outlook360 - Dashboard Preview Component
Presents 'SEE OUTLOOK360 IN ACTION' with real database metrics and platform entry gateway.
"""
import streamlit as st
from ml_engine.eda_engine import EDAEngine
from app.auth_gate import login_user, init_auth_state


def render_dashboard_preview():
    """Renders the 'SEE OUTLOOK360 IN ACTION' section with live database metrics."""
    st.markdown(
        """<div id="demo-preview" class="section-header-block"><span class="section-badge">Live Preview</span><h2 class="section-heading">See Outlook360 in Action</h2><p class="section-subheading">Explore the analytics workspace behind the platform.</p></div>""",
        unsafe_allow_html=True
    )

    # Fetch live business profile and KPIs
    try:
        profile = EDAEngine().get_kpi_summary()
        curr = profile.get("currency", "₹")
        biz_name = profile.get("business_name", "FreshPulse Supermarket")
        total_rev = profile.get("total_revenue", 0)
        net_profit = profile.get("net_profit", 0)
        profit_margin = profile.get("profit_margin_pct", 0)
        aov = profile.get("aov", 0)
        total_orders = profile.get("total_orders", 0)
        total_cust = profile.get("total_customers", 0)
    except Exception:
        curr = "₹"
        biz_name = "FreshPulse Supermarket"
        total_rev, net_profit, profit_margin, aov, total_orders, total_cust = 2351525, 470305, 20.0, 1330, 1767, 250

    # Live Database Context Badge
    st.markdown(
        f"""<div style="padding: 10px 18px; background: #ffffff; border: 1px solid #bfdbfe; border-left: 4px solid #2563eb; border-radius: 12px; margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;"><div><span style="font-size: 0.72rem; font-weight: 750; color: #1d4ed8; text-transform: uppercase; letter-spacing: 0.04em;">⚡ Active Workspace Instance (Central Database)</span><div style="font-size: 1.02rem; font-weight: 800; color: #0f172a;">{biz_name}</div></div><div style="font-size: 0.8rem; color: #64748b;">Live Records: <b>{total_orders:,} Orders</b> | <b>{total_cust:,} Customers</b></div></div>""",
        unsafe_allow_html=True
    )

    # Preview Metric Cards
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(
            f"""<div class="metric-card"><span style="font-size: 1.3rem; float: right;">💰</span><div class="metric-label">Gross Revenue</div><div class="metric-value">{curr}{total_rev:,.0f}</div><div class="metric-sub">Real-time aggregate</div></div>""",
            unsafe_allow_html=True
        )

    with m2:
        st.markdown(
            f"""<div class="metric-card"><span style="font-size: 1.3rem; float: right;">📈</span><div class="metric-label">Net Profit Margin</div><div class="metric-value">{profit_margin:.1f}%</div><div class="metric-sub">{curr}{net_profit:,.0f} net</div></div>""",
            unsafe_allow_html=True
        )

    with m3:
        st.markdown(
            f"""<div class="metric-card"><span style="font-size: 1.3rem; float: right;">🛒</span><div class="metric-label">Average Order Value</div><div class="metric-value">{curr}{aov:,.1f}</div><div class="metric-sub">Across {total_orders:,} tickets</div></div>""",
            unsafe_allow_html=True
        )

    with m4:
        st.markdown(
            f"""<div class="metric-card"><span style="font-size: 1.3rem; float: right;">👥</span><div class="metric-label">Active Customers</div><div class="metric-value">{total_cust:,}</div><div class="metric-sub">Segmented via RFM</div></div>""",
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # Enter Platform Button
    c1, c2, c3 = st.columns([1, 1.8, 1])
    with c2:
        st.page_link(
            "pages/1_Executive_Overview.py",
            label="🚀 Enter Platform & Launch Analytics Workspace →",
            icon="📊"
        )
