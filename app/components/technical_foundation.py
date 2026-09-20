"""
Outlook360 - Built on Data & AI (Technical Foundation) Component
Presents technology badges with an expandable technical architecture breakdown.
"""
import streamlit as st


def render_technical_foundation():
    """Renders the 'BUILT ON DATA & AI' badges and technical architecture."""
    st.markdown(
        """<div class="section-header-block"><span class="section-badge">Technology Stack</span><h2 class="section-heading">Built on Data & AI</h2><p class="section-subheading">Enterprise-grade technologies and statistical algorithms powering every insight.</p></div>""",
        unsafe_allow_html=True
    )

    # Technology Badges
    tech_badges = [
        ("🗄️", "MySQL"),
        ("🐍", "Python"),
        ("🐼", "Pandas"),
        ("🔢", "NumPy"),
        ("🧠", "Scikit-learn"),
        ("📈", "Plotly"),
        ("🤖", "Machine Learning"),
        ("🔮", "Predictive Analytics")
    ]

    tech_html = "".join([
        f"""<span style="font-size: 0.82rem; font-weight: 700; color: #1e3a8a; background: #ffffff; border: 1px solid #cbd5e1; padding: 6px 14px; border-radius: 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">{icon} {name}</span>"""
        for icon, name in tech_badges
    ])

    # Core Statistical Concepts Badges
    concept_badges = [
        "K-Means",
        "PCA",
        "Holt-Winters",
        "Apriori",
        "Isolation Forest",
        "3NF",
        "ACID"
    ]

    concept_html = "".join([
        f"""<span style="font-size: 0.78rem; font-weight: 600; color: #0284c7; background: #f0f9ff; border: 1px solid #bae6fd; padding: 4px 12px; border-radius: 16px;">⚡ {name}</span>"""
        for name in concept_badges
    ])

    st.markdown(
        f"""<div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin-bottom: 12px;">{tech_html}</div><div style="display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; margin-bottom: 20px;">{concept_html}</div>""",
        unsafe_allow_html=True
    )

    # Technical Architecture (Expandable)
    with st.expander("🛠️ Technical Architecture & Modeling Standards (Click to View)"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                "**Relational Database & Data Pipeline:**\n\n"
                "- **3NF Relational Architecture:** Strict referential integrity across sales, items, customers, and inventory.\n"
                "- **ACID Transaction Guarantee:** Atomic POS checkout transactions and inventory decrementing.\n"
                "- **Vectorized Data Processing:** High-throughput aggregations with Pandas & NumPy."
            )
        with col2:
            st.markdown(
                "**Machine Learning & Modeling:**\n\n"
                "- **Holt-Winters Smoothing:** Triple exponential forecasting with weekly 7-day seasonality.\n"
                "- **K-Means & PCA:** Unsupervised customer RFM clustering with 2D/3D embeddings.\n"
                "- **Apriori Algorithm:** Association rule mining calculating Support, Confidence, and Lift.\n"
                "- **Isolation Forest:** Tree ensemble outlier detection for transaction anomaly monitoring."
            )
