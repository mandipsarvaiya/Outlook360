"""
Outlook360 - Supported Business Domains Component
Presents universal multi-domain adaptability across commercial environments.
"""
import streamlit as st


def render_industries_section():
    """Renders the 'ONE PLATFORM. MULTIPLE BUSINESS DOMAINS.' industry grid."""
    st.markdown(
        """<div id="industries" class="section-header-block"><span class="section-badge">Universal Adaptability</span><h2 class="section-heading">One Platform. Multiple Business Domains.</h2><p class="section-subheading">Outlook360 is designed to adapt to different business environments.</p></div>""",
        unsafe_allow_html=True
    )

    domains = [
        ("🛒", "Supermarket & Grocery", "Perishables, FMCG items, shelf-life pacing, and daily basket checkouts."),
        ("💊", "Pharmacy & Healthcare", "Prescription medicines, OTC healthcare items, and batch expiry tracking."),
        ("👗", "Fashion & Apparel", "Apparel sizes, seasonal lines, designer wear, and inventory clearance."),
        ("💻", "Electronics & Gadgets", "High-value serial SKUs, tech lifecycles, and accessory bundle rates."),
        ("🍽️", "Restaurant & Food", "Artisan menus, perishable ingredients, meal combos, and rush hour peaks."),
        ("🏪", "General Retail", "Multichannel storefronts, retail categories, and customer loyalty retention."),
        ("📦", "Wholesale & Distribution", "Bulk order volumes, lead-time variance, and replenishment planning.")
    ]

    cols1 = st.columns(4)
    for col, (icon, title, desc) in zip(cols1, domains[:4]):
        with col:
            st.markdown(
                f"""<div class="capability-box" style="border-top: 3.5px solid #2563eb;"><div class="capability-box-icon">{icon}</div><div class="capability-box-title">{title}</div><div class="capability-box-desc">{desc}</div></div><div style="margin-bottom: 12px;"></div>""",
                unsafe_allow_html=True
            )

    cols2 = st.columns(3)
    for col, (icon, title, desc) in zip(cols2, domains[4:]):
        with col:
            st.markdown(
                f"""<div class="capability-box" style="border-top: 3.5px solid #0284c7;"><div class="capability-box-icon">{icon}</div><div class="capability-box-title">{title}</div><div class="capability-box-desc">{desc}</div></div><div style="margin-bottom: 12px;"></div>""",
                unsafe_allow_html=True
            )

    # Domain Switcher CTA
    c1, c2, c3 = st.columns([1, 1.8, 1])
    with c2:
        st.page_link("pages/9_Domain_Switcher.py", label="⚡ Switch Active Business Domain (1-Click) →", icon="🌐")
