"""
Outlook360 - KPI Cards UI Component
Renders executive KPI metrics with trend indicators, profit margins, and dynamic badges.
"""
import streamlit as st


def render_kpi_card(
    label: str,
    value: str,
    subtext: str = "",
    badge_text: str = "",
    badge_type: str = "primary"
):
    """Renders a single glassmorphic executive metric card."""
    badge_html = f'<span class="badge badge-domain" style="float: right;">{badge_text}</span>' if badge_text else ""
    st.markdown(
        f"""
        <div class="metric-card">
            {badge_html}
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_kpi_grid(kpis: dict):
    """Renders standard 4-card executive KPI summary row."""
    curr = kpis.get("currency", "$")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        rev = kpis.get("gross_revenue", 0.0)
        render_kpi_card(
            label="Gross Revenue",
            value=f"{curr}{rev:,.2f}",
            subtext=f"{kpis.get('total_orders', 0):,} Total Orders Completed",
            badge_text="Gross"
        )

    with col2:
        profit = kpis.get("net_profit", 0.0)
        margin = kpis.get("profit_margin_pct", 0.0)
        render_kpi_card(
            label="Net Profit Margin",
            value=f"{curr}{profit:,.2f}",
            subtext=f"Margin: {margin:.1f}% on Sales",
            badge_text=f"{margin:.1f}%"
        )

    with col3:
        aov = kpis.get("average_order_value", 0.0)
        render_kpi_card(
            label="Average Order Value",
            value=f"{curr}{aov:,.2f}",
            subtext="Per Completed Transaction",
            badge_text="AOV"
        )

    with col4:
        custs = kpis.get("active_customers", 0)
        units = kpis.get("total_items_sold", 0)
        render_kpi_card(
            label="Active Customers",
            value=f"{custs:,}",
            subtext=f"{units:,} Units Transacted",
            badge_text="Cust"
        )
