"""
Outlook360 - Business Intelligence for Every Decision (8-Card Matrix) Component
Presents 8 compact operational and tactical business intelligence capability cards.
"""
import streamlit as st


def render_business_intelligence_grid():
    """Renders the 8-card 'BUSINESS INTELLIGENCE FOR EVERY DECISION' matrix."""
    st.markdown(
        """<div class="section-header-block"><span class="section-badge">Decision Support</span><h2 class="section-heading">Business Intelligence for Every Decision</h2><p class="section-subheading">From everyday operations to long-term strategic planning.</p></div>""",
        unsafe_allow_html=True
    )

    items = [
        ("📊", "BUSINESS INTELLIGENCE", "See your overall business performance in one place."),
        ("📈", "SALES ANALYTICS", "Understand what drives your revenue."),
        ("👥", "CUSTOMER INTELLIGENCE", "Discover customer groups, behavior and value."),
        ("🔮", "DEMAND PREDICTION", "Forecast future demand for better planning."),
        ("📦", "INVENTORY INTELLIGENCE", "Identify stock risks and improve inventory decisions."),
        ("🛒", "MARKET BASKET ANALYSIS", "Discover products customers frequently buy together."),
        ("🚨", "MACHINE LEARNING", "Detect unusual patterns and uncover hidden insights."),
        ("📄", "INTERACTIVE REPORTING", "Explore data through clear dashboards, charts and reports.")
    ]

    cols1 = st.columns(4)
    for col, (icon, title, desc) in zip(cols1, items[:4]):
        with col:
            st.markdown(
                f"""<div class="bi-card"><div class="bi-card-icon">{icon}</div><div class="bi-card-title">{title}</div><div class="bi-card-desc">{desc}</div></div><div style="margin-bottom: 10px;"></div>""",
                unsafe_allow_html=True
            )

    cols2 = st.columns(4)
    for col, (icon, title, desc) in zip(cols2, items[4:]):
        with col:
            st.markdown(
                f"""<div class="bi-card"><div class="bi-card-icon">{icon}</div><div class="bi-card-title">{title}</div><div class="bi-card-desc">{desc}</div></div><div style="margin-bottom: 10px;"></div>""",
                unsafe_allow_html=True
            )
