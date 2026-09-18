"""
Outlook360 - Market Basket Analysis & Cross-Sell Recommender
Association rule mining using the Apriori algorithm with interactive recommendation testing.
"""
import sys
from pathlib import Path
import streamlit as st
import plotly.express as px

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.theme import apply_theme
from app.auth_gate import require_auth
from app.components.charts import DARK_LAYOUT_TEMPLATE
from app.components.navigation import render_sidebar_header
from ml_engine.market_basket import MarketBasketEngine
from database.connection import db_manager

st.set_page_config(page_title="Market Basket Analysis - Outlook360", page_icon="🛒", layout="wide")
apply_theme()
render_sidebar_header()
user = require_auth(allowed_roles=["owner"])

st.markdown("## 🛒 Market Basket Analysis & Affinity Mining")
st.markdown("Uncovers hidden co-purchase behaviors using the **Apriori Algorithm** to calculate **Support, Confidence, and Lift** for smart cross-selling.")

mba_engine = MarketBasketEngine()

# Hyperparameter Controls
col1, col2, col3 = st.columns(3)
with col1:
    min_support = st.slider("Minimum Support Threshold", min_value=0.005, max_value=0.08, value=0.015, step=0.005, format="%.3f")
with col2:
    min_conf = st.slider("Minimum Confidence Threshold", min_value=0.05, max_value=0.80, value=0.15, step=0.05)
with col3:
    min_lift = st.slider("Minimum Lift Threshold", min_value=1.0, max_value=10.0, value=1.1, step=0.2)

rules_df, summary = mba_engine.generate_association_rules(
    min_support=min_support,
    min_confidence=min_conf,
    min_lift=min_lift
)

# Summary Cards
scol1, scol2, scol3, scol4 = st.columns(4)
with scol1:
    st.metric("Total Transactions Analyzed", f"{summary.get('total_transactions', 0):,}")
with scol2:
    st.metric("Frequent Itemsets Mined", f"{summary.get('frequent_itemsets_count', 0):,}")
with scol3:
    st.metric("Strong Association Rules", f"{summary.get('total_rules', 0):,}")
with scol4:
    st.metric("Highest Lift Score", f"{summary.get('highest_lift', 0.0):.2f}x", delta="Strong Affinity")

st.markdown("<br>", unsafe_allow_html=True)

# Scatter plot of rules: Support vs Confidence colored by Lift
if not rules_df.empty:
    fig_rules = px.scatter(
        rules_df,
        x="support",
        y="confidence",
        size="lift",
        color="lift",
        hover_name="rule_display",
        hover_data=["support", "confidence", "lift", "conviction"],
        title="<b>Association Rules Landscape (Support vs Confidence sized by Lift)</b>",
        color_continuous_scale="Plasma"
    )
    fig_rules.update_layout(**DARK_LAYOUT_TEMPLATE, height=380)
    st.plotly_chart(fig_rules, use_container_width=True)

    # Association Rules Table
    st.markdown("### 📋 Top Ranked Association Rules")
    st.dataframe(
        rules_df[[
            "rule_display", "support", "confidence", "lift", "leverage", "conviction"
        ]].rename(columns={
            "rule_display": "Association Rule (If Bought ➔ Also Buys)",
            "support": "Support",
            "confidence": "Confidence",
            "lift": "Lift Multiplier",
            "leverage": "Leverage",
            "conviction": "Conviction"
        }).style.format({
            "Support": "{:.3f}",
            "Confidence": "{:.1%}",
            "Lift Multiplier": "{:.2f}x",
            "Leverage": "{:.4f}",
            "Conviction": "{:.2f}"
        }),
        use_container_width=True,
        height=300
    )

st.markdown("---")

# Interactive Recommendation Sandbox
st.markdown("### 🎯 Live Cross-Sell Recommendation Simulator")
st.markdown("Select any item in the active catalog to query the association rules engine in real-time:")

# Fetch product list
prod_df = db_manager.execute_query("SELECT name FROM products ORDER BY name ASC")
if not prod_df.empty:
    all_prods = prod_df["name"].tolist()
    selected_prod = st.selectbox("Select Target Product in Customer Cart:", options=all_prods)

    if selected_prod:
        recs = mba_engine.get_recommendations_for_product(selected_prod, rules_df=rules_df, top_n=3)
        if recs:
            st.markdown(f"**Recommended Cross-Sell Add-Ons for `{selected_prod}`:**")
            rcols = st.columns(len(recs))
            for i, rec in enumerate(recs):
                with rcols[i]:
                    st.markdown(
                        f"""
                        <div class="glass-container" style="border-top: 3.5px solid #2563eb; background: #ffffff; padding: 18px; border: 1px solid #e2e8f0; border-radius: 12px;">
                            <div style="font-weight: 700; color: #0f172a; font-size: 1.02rem; margin-bottom: 6px;">
                                {rec['recommended_product']}
                            </div>
                            <div style="font-size: 0.82rem; color: #2563eb; font-weight: 700;">
                                🔥 Lift: {rec['lift_score']:.2f}x higher affinity
                            </div>
                            <div style="font-size: 0.78rem; color: #64748b; margin-top: 4px;">
                                Confidence: {rec['confidence_pct']}% &nbsp;|&nbsp; Support: {rec['support_pct']}%
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.info(f"No cross-sell association rules found above current thresholds for '{selected_prod}'. Try lowering the minimum support or lift slider above.")
