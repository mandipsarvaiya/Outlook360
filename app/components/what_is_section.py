"""
Outlook360 - 'What is Outlook360?' Overview & 4-Pillar Highlights Component
Presents concise platform definition with 4 clear visual action cards.
"""
import streamlit as st


def render_what_is_section():
    """Renders the concise 'What is Outlook360?' section with 4 scannable pillars."""
    st.markdown(
        """<div id="what-is" class="section-header-block"><span class="section-badge">Platform Overview</span><h2 class="section-heading">What is Outlook360?</h2><p class="section-subheading">Outlook360 is a universal Enterprise Business Intelligence and Predictive Analytics platform that transforms business data into meaningful insights, forecasts and decision-support information.</p></div>""",
        unsafe_allow_html=True
    )

    pillars = [
        ("🔍", "UNDERSTAND", "See what is happening across your business."),
        ("🔮", "PREDICT", "Identify future trends and demand patterns."),
        ("⚙️", "OPTIMIZE", "Discover opportunities to improve operations."),
        ("🎯", "DECIDE", "Turn insights into confident, data-driven actions.")
    ]

    cols = st.columns(4)
    for col, (icon, title, desc) in zip(cols, pillars):
        with col:
            st.markdown(
                f"""<div class="pillar-card"><div class="pillar-icon">{icon}</div><div class="pillar-title">{title}</div><div class="pillar-desc">{desc}</div></div>""",
                unsafe_allow_html=True
            )
