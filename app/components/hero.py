"""
Outlook360 - Landing Page Hero Component
Presents the enterprise value proposition, primary CTAs, and scannable headline structure.
"""
import streamlit as st


def render_hero_section():
    """Renders the main hero banner with styled CTA buttons."""
    st.markdown(
        """<div id="hero" class="hero-container"><div class="hero-badge"><span>⚡ Universal Enterprise Business Intelligence & Predictive Analytics Platform</span></div><h1 class="hero-title">Turn Business Data Into <span class="hero-title-highlight">Better Decisions</span></h1><div class="hero-headline">Transform business data into clear insights, accurate forecasts and smarter decisions.</div><p class="hero-desc">Outlook360 brings analytics, statistics and machine learning together to help organizations understand performance, customers, sales, inventory and future demand.</p></div>""",
        unsafe_allow_html=True
    )

    # Hero Action Buttons
    c_left, c_mid, c_right = st.columns([1.5, 1.4, 1.5])
    with c_mid:
        b1, b2 = st.columns(2)
        with b1:
            st.page_link("pages/1_Executive_Overview.py", label="Explore Platform →", icon="🚀")
        with b2:
            st.markdown(
                '<a href="#modules" class="hero-btn-secondary" style="width: 100%; height: 44px; display: inline-flex; align-items: center; justify-content: center; box-sizing: border-box; text-align: center; border-radius: 10px; font-size: 0.88rem; font-weight: 650; text-decoration: none;">View Modules ↓</a>',
                unsafe_allow_html=True
            )
