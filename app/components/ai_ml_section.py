"""
Outlook360 - AI & Machine Learning Section Component
Presents 'WHERE AI MEETS BUSINESS DATA' workflow and verified AI capability cards.
"""
import streamlit as st


def render_ai_ml_section():
    """Renders the AI/ML visual workflow and compact capability cards."""
    st.markdown(
        """<div id="ai-ml" class="section-header-block"><span class="section-badge">Predictive Intelligence</span><h2 class="section-heading">Where AI Meets Business Data</h2><p class="section-subheading">Use data to discover patterns, predict trends and support better decisions.</p></div>""",
        unsafe_allow_html=True
    )

    # Visual Flow Box
    flow_steps = [
        "1. BUSINESS DATA",
        "2. DATA PREPARATION",
        "3. FEATURE ENGINEERING",
        "4. MACHINE LEARNING",
        "5. PREDICTION",
        "6. BUSINESS INSIGHT"
    ]
    flow_html = "".join([f"""<div class="ai-flow-step">{s}</div>""" for s in flow_steps])
    st.markdown(
        f"""<div class="ai-flow-box"><div class="ai-flow-grid">{flow_html}</div></div>""",
        unsafe_allow_html=True
    )

    # Compact AI Capability Cards
    ai_caps = [
        ("🔮", "Demand Forecasting", "Estimate forward demand curves using historical seasonal patterns."),
        ("👥", "Customer Segmentation", "Group customers by purchasing value and behavioral personas."),
        ("🔍", "Pattern Detection", "Discover underlying transaction trends and customer cycles."),
        ("🛒", "Product Relationships", "Identify frequently co-purchased bundles and affinities."),
        ("📦", "Inventory Intelligence", "Forecast safety stock requirements and reorder levels."),
        ("🚨", "Anomaly Detection", "Isolate suspicious transaction surges and atypical patterns.")
    ]

    cols1 = st.columns(3)
    for col, (icon, title, desc) in zip(cols1, ai_caps[:3]):
        with col:
            st.markdown(
                f"""<div class="capability-box"><div class="capability-box-icon">{icon}</div><div class="capability-box-title">{title}</div><div class="capability-box-desc">{desc}</div></div><div style="margin-bottom: 12px;"></div>""",
                unsafe_allow_html=True
            )

    cols2 = st.columns(3)
    for col, (icon, title, desc) in zip(cols2, ai_caps[3:]):
        with col:
            st.markdown(
                f"""<div class="capability-box"><div class="capability-box-icon">{icon}</div><div class="capability-box-title">{title}</div><div class="capability-box-desc">{desc}</div></div><div style="margin-bottom: 12px;"></div>""",
                unsafe_allow_html=True
            )
