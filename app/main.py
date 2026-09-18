"""
Outlook360 - Master Application Entry Point
Universal Business Intelligence & Predictive Analytics Platform
Blue & White Executive Edition with Role-Based Portals.
"""
import sys
from pathlib import Path
import streamlit as st

# Ensure project root in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.theme import apply_theme
from app.auth_gate import init_auth_state, login_user
from app.components.kpi_cards import render_kpi_grid
from app.components.navigation import render_sidebar_header
from ml_engine.eda_engine import EDAEngine
from config.settings import AppSettings
from database.connection import db_manager

# Page Configuration
st.set_page_config(
    page_title="Outlook360 - Universal Enterprise BI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Blue & White Theme & Auth Header
apply_theme()
init_auth_state()
render_sidebar_header()

# Main Header
profile = EDAEngine().get_kpi_summary()
curr = profile.get("currency", "₹")

# Check Auth Status
user = st.session_state.get("user")
is_auth = st.session_state.get("is_authenticated", False)

if is_auth and user:
    role = user.get("role", "").lower()
    role_badge = {
        "owner": ("👑 Store Owner Portal", "#1e40af"),
        "cashier": ("💳 Cashier Terminal Portal", "#047857"),
        "inventory": ("📦 Inventory Staff Portal", "#b45309")
    }.get(role, ("User Portal", "#334155"))

    st.markdown(
        f"""
        <div style="padding: 12px 18px; background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid {role_badge[1]}; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.04); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <span style="display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 0.78rem; font-weight: 700; color: #ffffff; background: {role_badge[1]}; margin-bottom: 4px;">
                    {role_badge[0]}
                </span>
                <div style="font-size: 1.25rem; font-weight: 800; color: #0f172a;">Welcome back, {user.get('full_name')}</div>
                <div style="font-size: 0.82rem; color: #64748b;">Employee ID: <b>{user.get('emp_id')}</b> | Email: <b>{user.get('email')}</b></div>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 0.8rem; color: #64748b;">Enterprise Workspace</span><br>
                <b style="color: #1e3a8a; font-size: 0.95rem;">{profile.get('business_name')}</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <div style="padding: 16px 20px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 12px; margin-bottom: 20px;">
            <div style="font-size: 1.1rem; font-weight: 700; color: #1e3a8a; margin-bottom: 4px;">
                🔐 Role-Based Access Control (RBAC) System
            </div>
            <div style="font-size: 0.88rem; color: #3b82f6; margin-bottom: 10px;">
                Sign in to unlock your role's dedicated portal: <b>Store Owner</b> (Gmail), <b>Cashier</b> (EMP ID), or <b>Inventory Staff</b> (EMP ID).
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    # Quick login helpers
    qcol1, qcol2, qcol3 = st.columns(3)
    with qcol1:
        if st.button("👑 Sign In: Store Owner", use_container_width=True):
            login_user("owner@outlook360.com", "admin123")
            st.rerun()
    with qcol2:
        if st.button("💳 Sign In: Cashier", use_container_width=True):
            login_user("EMP-CSH-01", "cashier123")
            st.rerun()
    with qcol3:
        if st.button("📦 Sign In: Inventory Staff", use_container_width=True):
            login_user("EMP-INV-01", "inventory123")
            st.rerun()

st.markdown(
    f"""
    <div style="padding: 6px 0 16px 0;">
        <h1 style="font-size: 2.35rem; margin-bottom: 4px; background: linear-gradient(90deg, #1e3a8a, #2563eb); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            ⚡ {profile.get('business_name')}
        </h1>
        <p style="color: #64748b; font-size: 1.02rem; font-weight: 500; margin-bottom: 0;">
            <b>Outlook360</b>: Universal Enterprise Business Intelligence, Inventory Optimization & Machine Learning Platform
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Render Top KPI Cards
render_kpi_grid(profile)

st.markdown("<br>", unsafe_allow_html=True)

# Architecture & Module Quick-Jump Grid
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### 🏛️ Universal System Architecture")
    st.markdown(
        """
        <div class="glass-container">
            <p style="color: #334155; font-size: 0.92rem; line-height: 1.6; margin-bottom: 12px;">
                Outlook360 uses a <b>Domain-Agnostic 3NF & Star Schema</b> that seamlessly models any retail, healthcare, hospitality, or direct-to-consumer enterprise:
            </p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                <div style="padding: 14px; background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0; border-left: 4px solid #1d4ed8;">
                    <b style="color: #1e3a8a; font-size: 0.88rem;">1. Relational Database Layer</b><br>
                    <span style="font-size: 0.8rem; color: #64748b;">Enterprise 3NF relational schema with foreign keys & analytical indexes</span>
                </div>
                <div style="padding: 14px; background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0; border-left: 4px solid #0284c7;">
                    <b style="color: #0369a1; font-size: 0.88rem;">2. Automated BI & KPI Engine</b><br>
                    <span style="font-size: 0.8rem; color: #64748b;">Gross margin, Pareto 80/20, MoM velocity, hourly footfall heatmaps</span>
                </div>
                <div style="padding: 14px; background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0; border-left: 4px solid #4f46e5;">
                    <b style="color: #3730a3; font-size: 0.88rem;">3. Customer RFM & K-Means</b><br>
                    <span style="font-size: 0.8rem; color: #64748b;">Elbow method, Silhouette scores & PCA 2D/3D visual embeddings</span>
                </div>
                <div style="padding: 14px; background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0; border-left: 4px solid #2563eb;">
                    <b style="color: #1d4ed8; font-size: 0.88rem;">4. Predictive Demand Forecaster</b><br>
                    <span style="font-size: 0.8rem; color: #64748b;">Holt-Winters triple exponential smoothing with 95% confidence bounds</span>
                </div>
                <div style="padding: 14px; background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0; border-left: 4px solid #0891b2;">
                    <b style="color: #0e7490; font-size: 0.88rem;">5. Market Basket Mining (Apriori)</b><br>
                    <span style="font-size: 0.8rem; color: #64748b;">Support, Confidence, Lift & real-time cross-sell recommender</span>
                </div>
                <div style="padding: 14px; background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0; border-left: 4px solid #059669;">
                    <b style="color: #065f46; font-size: 0.88rem;">6. ABC-XYZ Inventory & ROP</b><br>
                    <span style="font-size: 0.8rem; color: #64748b;">9-box revenue vs volatility matrix & statistical safety stock calculator</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown("### 🌐 Supported Business Domains")
    st.markdown(
        f"""
        <div class="glass-container">
            <p style="color: #64748b; font-size: 0.88rem; margin-bottom: 12px;">
                Switch between industries in 1-click via the <b>Domain Switcher</b>:
            </p>
            <ul style="color: #1e293b; font-size: 0.88rem; line-height: 2.0; list-style: none; padding-left: 0;">
                <li>🛒 <b>Supermarket & Grocery</b> <span style="color:#64748b;">(Perishables, FMCG, Dairy)</span></li>
                <li>💊 <b>Pharmacy & Healthcare</b> <span style="color:#64748b;">(Rx, OTC, Diagnostics)</span></li>
                <li>🍽️ <b>Restaurant & Bistro</b> <span style="color:#64748b;">(Mains, Combos, Rush hours)</span></li>
                <li>👗 <b>Fashion & Apparel</b> <span style="color:#64748b;">(Wardrobe, Footwear, Luxury)</span></li>
                <li>📱 <b>Electronics & Mobile</b> <span style="color:#64748b;">(Smartphones, Attach rate)</span></li>
                <li>📦 <b>E-Commerce Direct</b> <span style="color:#64748b;">(D2C, Logistics, Multichannel)</span></li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# Quick Navigation Links
st.markdown("### 🚀 Role-Based Workspace Portals & Modules")
mcol1, mcol2, mcol3, mcol4 = st.columns(4)

with mcol1:
    st.markdown("#### 👑 Store Owner")
    st.page_link("pages/1_Executive_Overview.py", label="Executive BI Overview", icon="📊")
    st.page_link("pages/2_Sales_Analytics.py", label="Sales & Pareto (80/20)", icon="📈")
    st.page_link("pages/11_User_Management.py", label="Staff & Access Control", icon="👥")

with mcol2:
    st.markdown("#### 🧠 AI & Data Science")
    st.page_link("pages/3_Customer_Segmentation.py", label="Customer RFM & K-Means", icon="👥")
    st.page_link("pages/4_Demand_Forecasting.py", label="Predictive Demand Forecast", icon="🔮")
    st.page_link("pages/5_Market_Basket_Analysis.py", label="Market Basket (Apriori)", icon="🛒")

with mcol3:
    st.markdown("#### 📦 Inventory & Operations")
    st.page_link("pages/10_Inventory_Management.py", label="Inventory Control & Alerts", icon="📦")
    st.page_link("pages/6_Inventory_Optimization.py", label="ABC-XYZ Matrix Analysis", icon="📊")
    st.page_link("pages/7_Anomaly_Detection.py", label="Anomaly & Fraud Radar", icon="🚨")

with mcol4:
    st.markdown("#### 💳 Counter & Settings")
    st.page_link("pages/8_POS_Simulator.py", label="Live POS Billing Terminal", icon="💳")
    st.page_link("pages/9_Domain_Switcher.py", label="Universal Domain Switcher", icon="🌐")
