"""
Outlook360 - Powerful Analytics Modules (6 Modules Showcase) Component
Presents the 6 core analytics modules with concise descriptions and direct page links.
"""
import streamlit as st


def render_analytics_modules_showcase():
    """Renders the 6-card 'POWERFUL ANALYTICS MODULES' product grid."""
    st.markdown(
        """<div id="modules" class="section-header-block"><span class="section-badge">Core Products</span><h2 class="section-heading">Powerful Analytics Modules</h2><p class="section-subheading">Explore the tools that turn business data into actionable insights.</p></div>""",
        unsafe_allow_html=True
    )

    modules = [
        ("📊", "Executive Overview", "See your overall business performance at a glance.", "pages/1_Executive_Overview.py", "Explore Module →"),
        ("📈", "Sales Analytics", "Understand revenue, sales trends and product performance.", "pages/2_Sales_Analytics.py", "Explore Module →"),
        ("👥", "Customer Segmentation", "Discover customer groups and purchasing behavior.", "pages/3_Customer_Segmentation.py", "Explore Module →"),
        ("🔮", "Demand Forecasting", "Estimate future demand from historical patterns.", "pages/4_Demand_Forecasting.py", "Explore Module →"),
        ("🛒", "Market Basket Analysis", "Find products customers frequently purchase together.", "pages/5_Market_Basket_Analysis.py", "Explore Module →"),
        ("📦", "Inventory Optimization", "Identify stock risks and improve inventory planning.", "pages/6_Inventory_Optimization.py", "Explore Module →")
    ]

    cols1 = st.columns(3)
    for col, (icon, title, desc, path, link_label) in zip(cols1, modules[:3]):
        with col:
            st.markdown(
                f"""<div class="module-product-card"><div class="module-product-icon">{icon}</div><div class="module-product-title">{title}</div><div class="module-product-desc">{desc}</div></div>""",
                unsafe_allow_html=True
            )
            st.page_link(path, label=link_label, icon=icon)

    st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

    cols2 = st.columns(3)
    for col, (icon, title, desc, path, link_label) in zip(cols2, modules[3:]):
        with col:
            st.markdown(
                f"""<div class="module-product-card"><div class="module-product-icon">{icon}</div><div class="module-product-title">{title}</div><div class="module-product-desc">{desc}</div></div>""",
                unsafe_allow_html=True
            )
            st.page_link(path, label=link_label, icon=icon)
