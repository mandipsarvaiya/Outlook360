"""
Outlook360 - Enterprise SaaS Footer Component
Clean footer with platform branding and section links.
"""
import streamlit as st


def render_footer():
    """Renders the enterprise landing page footer."""
    st.markdown(
        """<div class="enterprise-footer"><div class="footer-brand">⚡ OUTLOOK360</div><div class="footer-subtitle">Universal Enterprise Business Intelligence & Predictive Analytics Platform</div><div class="footer-links-row"><a href="#hero" class="footer-link-item">Home</a><a href="#what-is" class="footer-link-item">Platform</a><a href="#how-it-works" class="footer-link-item">How It Works</a><a href="#capabilities" class="footer-link-item">Capabilities</a><a href="#modules" class="footer-link-item">Modules</a><a href="#industries" class="footer-link-item">Industries</a><a href="#ai-ml" class="footer-link-item">AI & ML</a></div><div class="footer-copy">&copy; 2026 Outlook360. All rights reserved. Open-source under MIT License.</div></div>""",
        unsafe_allow_html=True
    )
