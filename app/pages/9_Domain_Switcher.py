"""
Outlook360 - Domain Switcher & Dataset Manager
Enables instant migration across 6 business domains and data export tools.
"""
import sys
from pathlib import Path
import streamlit as st
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.theme import apply_theme
from app.auth_gate import require_auth
from app.components.navigation import render_sidebar_header
from config.settings import AppSettings
from database.seed_data import seed_database
from database.connection import db_manager
from database.queries import AnalyticsQueries

st.set_page_config(page_title="Domain Switcher - Outlook360", page_icon="🌐", layout="wide")
apply_theme()
render_sidebar_header()
user = require_auth(allowed_roles=["owner"])

profile = AnalyticsQueries.get_business_profile()
current_domain = profile.get("domain_key", "supermarket")

st.markdown("## 🌐 Universal Domain Switcher & Dataset Hub")
st.markdown("Switch the underlying enterprise database to any industry domain in one click to demonstrate universal schema adaptability.")

col_main1, col_main2 = st.columns([3, 2])

with col_main1:
    st.markdown("### 🔄 Select New Business Domain")

    domain_options = {
        "supermarket": "🛒 FreshPulse Supermarket & Grocery (FMCG, Perishables)",
        "pharmacy": "💊 MediPulse Pharmacy & Healthcare (Rx, Diagnostics, Wellness)",
        "restaurant": "🍽️ GourmetPulse Bistro & Cafe (Artisan Kitchen, Combos)",
        "fashion": "👗 VoguePulse Apparel & Couture (Apparel, Footwear, Luxury)",
        "electronics": "📱 TechPulse Electronics & Gadgets (Phones, Computing, Audio)",
        "ecommerce": "📦 OmniCart Direct D2C Marketplace (Multichannel, Logistics)"
    }

    chosen_domain = st.selectbox(
        "Select Target Domain Template",
        options=list(domain_options.keys()),
        format_func=lambda k: domain_options[k],
        index=list(domain_options.keys()).index(current_domain) if current_domain in domain_options else 0
    )

    scol1, scol2 = st.columns(2)
    with scol1:
        num_orders = st.slider("Simulation Volume (Orders)", min_value=500, max_value=3000, value=1800, step=100)
    with scol2:
        num_customers = st.slider("Customer Base", min_value=100, max_value=500, value=250, step=50)

    if st.button("🚀 Switch & Re-Seed Enterprise Database"):
        with st.spinner(f"Generating synthetic enterprise dataset for '{chosen_domain}'..."):
            counts = seed_database(
                domain_key=chosen_domain,
                num_customers=num_customers,
                num_orders=num_orders,
                days_span=240
            )
            st.success(f"🎉 Successfully seeded {counts.get('orders', 0):,} orders across {counts.get('products', 0)} products for domain '{chosen_domain.upper()}'!")
            st.rerun()

with col_main2:
    st.markdown("### 💾 Live Database Status & Export")
    tables = db_manager.get_table_names()
    st.markdown(
        f"""
        <div class="glass-container">
            <b>Database Engine:</b> {'SQLite 3 (Zero-Config)' if db_manager.is_sqlite() else 'MySQL 8.0'}<br>
            <b>Active Domain:</b> {profile.get('business_name')}<br>
            <b>Total Tables:</b> {len(tables)} Relational Entities<br>
            <b>Orders Logged:</b> {db_manager.get_row_count('orders'):,} Records<br>
            <b>Order Items:</b> {db_manager.get_row_count('order_items'):,} Line Items
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("#### 📥 Export Relational Tables (CSV)")
    export_table = st.selectbox("Select Table to Export", options=tables)
    if export_table:
        table_df = db_manager.execute_query(f"SELECT * FROM {export_table}")
        csv_data = table_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"⬇️ Download {export_table}.csv ({len(table_df)} rows)",
            data=csv_data,
            file_name=f"{chosen_domain}_{export_table}.csv",
            mime="text/csv"
        )
