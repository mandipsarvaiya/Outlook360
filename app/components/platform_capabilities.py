"""
Outlook360 - Core Platform Capabilities (6-Card Grid) Component
Clean, scannable cards highlighting core strengths in 2-3 seconds per card.
"""
import streamlit as st


def render_platform_capabilities():
    """Renders the 6-card 'CORE PLATFORM CAPABILITIES' grid."""
    st.markdown(
        """<div id="capabilities" class="section-header-block"><span class="section-badge">Platform Capabilities</span><h2 class="section-heading">Core Platform Capabilities</h2><p class="section-subheading">Everything you need to understand, predict and improve your business.</p></div>""",
        unsafe_allow_html=True
    )

    capabilities = [
        ("🗄️", "DATA MANAGEMENT", "Organize business data in one reliable system.", "MySQL • Structured Data"),
        ("📊", "BUSINESS INTELLIGENCE", "Track performance, trends and important business metrics.", "KPIs • Trends • Reports"),
        ("📐", "STATISTICAL ANALYSIS", "Discover patterns, variations and meaningful trends.", "Statistics • Trends • Comparisons"),
        ("🧠", "MACHINE LEARNING", "Uncover hidden patterns and relationships in your data.", "Segmentation • Detection • Classification"),
        ("🔮", "PREDICTIVE ANALYTICS", "Forecast future demand and identify what may happen next.", "Forecasting • Prediction"),
        ("📈", "INTERACTIVE VISUALS", "Explore complex data through clear interactive charts.", "Charts • Dashboards • Insights")
    ]

    col1, col2, col3 = st.columns(3)
    for i, (icon, title, desc, tag) in enumerate(capabilities):
        target_col = col1 if i % 3 == 0 else (col2 if i % 3 == 1 else col3)
        with target_col:
            st.markdown(
                f"""<div class="capability-box"><div class="capability-box-icon">{icon}</div><div class="capability-box-title">{title}</div><div class="capability-box-desc">{desc}</div><div class="capability-box-tag">{tag}</div></div><div style="margin-bottom: 12px;"></div>""",
                unsafe_allow_html=True
            )
