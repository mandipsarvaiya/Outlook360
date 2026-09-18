"""
Outlook360 - Sidebar Navigation & Brand Header Component
Blue & White Executive Theme Edition.
"""
import streamlit as st
from config.settings import AppSettings
from database.connection import db_manager
from database.queries import AnalyticsQueries


def render_sidebar_header():
    """Renders consistent sidebar branding, domain status, and user session in Blue & White style."""
    from app.auth_gate import render_auth_sidebar
    profile = AnalyticsQueries.get_business_profile()
    domain_key = profile.get("domain_key", "supermarket")
    domain_title = AppSettings.SUPPORTED_DOMAINS.get(domain_key, domain_key.title())

    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding: 12px 4px 18px 4px; border-bottom: 1px solid #e2e8f0; margin-bottom: 16px;">
                <div style="font-size: 1.4rem; font-weight: 800; background: linear-gradient(90deg, #1e3a8a, #2563eb); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    ⚡ Outlook360
                </div>
                <div style="font-size: 0.8rem; color: #64748b; font-weight: 500; margin-top: 2px;">
                    Enterprise BI & Predictive Analytics
                </div>
                <div style="margin-top: 10px; display: flex; gap: 6px; flex-wrap: wrap;">
                    <span class="badge badge-domain">{domain_title}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        render_auth_sidebar()

        st.markdown(
            f"""
            <div style="padding: 10px 12px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; font-size: 0.78rem; color: #475569; margin-bottom: 16px;">
                <b style="color: #0f172a;">Active Entity:</b> {profile.get('business_name')}<br>
                <b style="color: #0f172a;">Currency:</b> {profile.get('currency', '₹')} &nbsp;|&nbsp; 
                <b style="color: #0f172a;">Tax Rate:</b> {int(profile.get('tax_rate', 0.05)*100)}%
            </div>
            """,
            unsafe_allow_html=True
        )

