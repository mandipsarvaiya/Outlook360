"""
Outlook360 - Landing Page Top Navigation Bar Component
Provides an enterprise SaaS top header with clean branding and balanced navigation anchors.
"""
import streamlit as st


def render_landing_navbar():
    """Renders the top enterprise SaaS navigation bar with clean styling and balanced layout."""
    is_auth = st.session_state.get("is_authenticated", False)
    user = st.session_state.get("user")

    auth_html = ""
    if is_auth and user:
        role_label = user.get("role", "").capitalize()
        name = user.get("full_name", "User")
        auth_html = f"""<span style="font-size: 0.78rem; font-weight: 700; color: #1e40af; background: #eff6ff; padding: 4px 10px; border-radius: 20px; border: 1px solid #bfdbfe; margin-left: 6px;">👤 {name} ({role_label})</span>"""

    st.markdown(
        f"""<div class="landing-navbar"><div class="landing-brand"><div class="landing-brand-logo">⚡</div><div><div class="landing-brand-title">OUTLOOK360</div><div class="landing-brand-tag">Universal Enterprise BI & Predictive Analytics</div></div></div><div class="landing-nav-links"><a href="#hero" class="landing-nav-link">Home</a><a href="#what-is" class="landing-nav-link">Platform</a><a href="#modules" class="landing-nav-link">Modules</a><a href="#ai-ml" class="landing-nav-link">AI & ML</a><a href="#industries" class="landing-nav-link">Industries</a><a href="#how-it-works" class="landing-nav-link">How It Works</a>{auth_html}</div></div>""",
        unsafe_allow_html=True
    )
