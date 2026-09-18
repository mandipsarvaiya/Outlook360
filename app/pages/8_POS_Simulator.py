"""
Outlook360 - Live Real-Time POS Simulator & Billing Terminal
Dedicated workspace for Cashiers & Store Owner.
Enables rapid customer onboarding, real-time product cart checkout, AI cross-sell recommendations, and instant invoice printing.
"""
import sys
from datetime import datetime
from pathlib import Path
import streamlit as st
import pandas as pd
from sqlalchemy import text

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.auth_gate import require_auth, render_auth_sidebar
from app.theme import render_custom_css, render_header, render_metric_card
from database.connection import db_manager
from database.queries import AnalyticsQueries
from ml_engine.market_basket import MarketBasketEngine

st.set_page_config(page_title="POS Simulator | Outlook360", page_icon="💳", layout="wide")
render_custom_css()
render_auth_sidebar()
user = require_auth(allowed_roles=["cashier", "owner"])

profile = AnalyticsQueries.get_business_profile()
curr = profile.get("currency", "₹")
tax_rate = float(profile.get("tax_rate", 0.05))

render_header(
    title="Live Point-of-Sale (POS) Billing Terminal",
    subtitle="Process counter checkouts, onboard loyalty customers, and leverage AI cross-selling recommendations.",
    badge_text="💳 Cashier Terminal" if user["role"] == "cashier" else "👑 Store Owner Terminal"
)

# Initialize session cart
if "pos_cart" not in st.session_state:
    st.session_state.pos_cart = []

# Fetch active products & customers
products_df = db_manager.execute_query("""
    SELECT p.product_id, p.sku, p.name, c.name AS category_name, p.unit_price, p.cost_price, p.current_stock 
    FROM products p
    JOIN categories c ON p.category_id = c.category_id
    WHERE p.is_active = 1 
    ORDER BY p.name ASC
""")
customers_df = db_manager.execute_query("SELECT customer_id, customer_code, name, tier, phone, email FROM customers ORDER BY name ASC")

# Quick Customer Registration Expander for Cashiers
with st.expander("➕ Register New Customer / Loyalty Member (Cashier Onboarding)"):
    st.caption("Quickly register a new walk-in customer into the database before checkout.")
    with st.form("new_customer_quick_form"):
        nc_col1, nc_col2, nc_col3 = st.columns(3)
        with nc_col1:
            auto_code = f"CUST-{len(customers_df)+101}"
            nc_code = st.text_input("Customer Code", value=auto_code)
            nc_name = st.text_input("Full Name", placeholder="e.g. Priya Sharma")
        with nc_col2:
            nc_phone = st.text_input("Mobile Phone", placeholder="e.g. +91 98765 43210")
            nc_email = st.text_input("Email Address", placeholder="e.g. priya@gmail.com")
        with nc_col3:
            nc_tier = st.selectbox("Loyalty Tier", ["Standard", "Silver", "Gold", "Platinum"])
            nc_city = st.text_input("City", value="Mumbai")

        submit_new_cust = st.form_submit_button("✨ Register Customer in Database", use_container_width=True)
        if submit_new_cust:
            if not nc_name.strip():
                st.error("Customer name is required!")
            else:
                db_manager.execute_non_query(
                    """
                    INSERT INTO customers (customer_code, name, email, phone, gender, age_group, city, tier, registered_at)
                    VALUES (:code, :name, :email, :phone, 'Other', '26-35', :city, :tier, :reg_date)
                    """,
                    {
                        "code": nc_code.strip().upper(),
                        "name": nc_name.strip(),
                        "email": nc_email.strip() if nc_email else "unspecified@store.in",
                        "phone": nc_phone.strip() if nc_phone else "N/A",
                        "city": nc_city.strip(),
                        "tier": nc_tier,
                        "reg_date": datetime.now().strftime("%Y-%m-%d")
                    }
                )
                st.success(f"🎉 Customer '{nc_name}' registered successfully with Tier: {nc_tier}!")
                st.rerun()

st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("### 🛒 Product Catalog & Cart Builder")

    # Product Selector
    if not products_df.empty:
        prod_names = products_df["name"].tolist()
        chosen_item_name = st.selectbox("Select Product to Add", options=prod_names)
        item_row = products_df[products_df["name"] == chosen_item_name].iloc[0]

        pcol1, pcol2, pcol3 = st.columns([2, 1, 1])
        with pcol1:
            st.markdown(f"""
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.6rem 0.8rem;">
                <span style="font-weight: 700; color: #0f172a; font-size: 1.05rem;">{curr}{item_row['unit_price']:,.2f}</span>
                <span style="color: #64748b; font-size: 0.85rem;"> / unit</span> &nbsp;|&nbsp; 
                <span style="color: {'#15803d' if item_row['current_stock'] > 10 else '#b91c1c'}; font-weight: 600; font-size: 0.88rem;">
                    Stock: {item_row['current_stock']} units
                </span>
            </div>
            """, unsafe_allow_html=True)
        with pcol2:
            qty = st.number_input("Qty", min_value=1, max_value=max(1, int(item_row['current_stock'])), value=1, step=1)
        with pcol3:
            st.markdown("<div style='margin-top: 0.15rem;'></div>", unsafe_allow_html=True)
            if st.button("➕ Add to Cart", use_container_width=True):
                # Check if item already in cart
                existing = next((item for item in st.session_state.pos_cart if item["product_id"] == item_row["product_id"]), None)
                if existing:
                    existing["quantity"] += qty
                    existing["total_price"] = round(existing["quantity"] * existing["unit_price"], 2)
                else:
                    st.session_state.pos_cart.append({
                        "product_id": int(item_row["product_id"]),
                        "sku": item_row["sku"],
                        "name": item_row["name"],
                        "unit_price": float(item_row["unit_price"]),
                        "cost_price": float(item_row["cost_price"]),
                        "quantity": int(qty),
                        "total_price": round(qty * float(item_row["unit_price"]), 2)
                    })
                st.rerun()

    # Active Cart Display
    st.markdown("#### 🧺 Current Order Basket")
    if st.session_state.pos_cart:
        cart_df = pd.DataFrame(st.session_state.pos_cart)
        st.dataframe(
            cart_df[["sku", "name", "unit_price", "quantity", "total_price"]].rename(columns={
                "sku": "SKU", "name": "Item", "unit_price": f"Price ({curr})",
                "quantity": "Qty", "total_price": f"Total ({curr})"
            }).style.format({
                f"Price ({curr})": "₹{:,.2f}",
                f"Total ({curr})": "₹{:,.2f}"
            }),
            use_container_width=True
        )

        if st.button("🗑️ Clear Basket"):
            st.session_state.pos_cart = []
            st.rerun()

        # Real-time AI Cross-Sell Suggestions
        st.markdown("---")
        st.markdown("#### 🤖 AI Recommendation Engine (Co-Purchase Affinity)")
        try:
            mba = MarketBasketEngine()
            last_item = st.session_state.pos_cart[-1]["name"]
            recs = mba.get_recommendations_for_product(last_item, top_n=2)
            if recs:
                for r in recs:
                    st.info(f"💡 **Frequently Bought Together:** Customers purchasing *{last_item}* also buy **{r['recommended_product']}** (Lift: {r['lift_score']:.2f}x).")
        except Exception:
            pass
    else:
        st.info("Cart is currently empty. Select an item above to start building an order.")

with col_right:
    st.markdown("### 🧾 Invoice & Checkout Terminal")

    # Customer Selection
    cust_options = ["Walk-In Customer (Standard)"] + [f"{c['name']} ({c['tier']})" for _, c in customers_df.iterrows()]
    selected_cust_str = st.selectbox("Customer Profile", options=cust_options)

    if selected_cust_str != "Walk-In Customer (Standard)":
        cust_name = selected_cust_str.split(" (")[0]
        cust_row = customers_df[customers_df["name"] == cust_name].iloc[0]
        cust_id = int(cust_row["customer_id"])
        tier = cust_row["tier"]
    else:
        cust_id = 1
        tier = "Standard"

    payment_method = st.selectbox("Payment Method", options=["UPI / QR Code", "Credit Card", "Debit Card", "Cash", "Net Banking"])
    channel = st.selectbox("Sales Channel", options=["In-Store POS", "Online Order", "Mobile App"])

    # Calculations
    subtotal = sum(item["total_price"] for item in st.session_state.pos_cart)
    discount_pct = 0.10 if tier == "Platinum" else (0.05 if tier == "Gold" else (0.02 if tier == "Silver" else 0.0))
    discount_amount = round(subtotal * discount_pct, 2)
    tax_amount = round((subtotal - discount_amount) * tax_rate, 2)
    final_total = round(subtotal - discount_amount + tax_amount, 2)

    st.markdown(
        f"""
        <div style="background: #ffffff; padding: 20px; border: 1px solid #e2e8f0; border-top: 4px solid #2563eb; border-radius: 12px; margin: 12px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.04);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #64748b; font-weight: 500;">Subtotal:</span>
                <b style="color: #0f172a;">{curr}{subtotal:,.2f}</b>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #64748b; font-weight: 500;">Discount ({tier} {int(discount_pct*100)}%):</span>
                <b style="color: #059669;">-{curr}{discount_amount:,.2f}</b>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #64748b; font-weight: 500;">GST / Tax ({int(tax_rate*100)}%):</span>
                <b style="color: #0f172a;">+{curr}{tax_amount:,.2f}</b>
            </div>
            <hr style="border-color: #e2e8f0; margin: 12px 0;">
            <div style="display: flex; justify-content: space-between; font-size: 1.3rem;">
                <span style="color: #0f172a; font-weight: 800;">Grand Total:</span>
                <b style="color: #1d4ed8; font-weight: 800;">{curr}{final_total:,.2f}</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("💳 Complete Transaction & Print Invoice", disabled=len(st.session_state.pos_cart) == 0, use_container_width=True):
        # Database Insertion
        now_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        inv_no = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        with db_manager.engine.begin() as conn:
            # 1. Insert Order Header
            ins_order = text("""
                INSERT INTO orders (invoice_no, order_date, customer_id, payment_method, channel, subtotal, discount_amount, tax_amount, total_amount, status)
                VALUES (:inv, :dt, :cid, :pay, :chan, :sub, :disc, :tax, :tot, 'Completed')
            """)
            result = conn.execute(ins_order, {
                "inv": inv_no, "dt": now_dt, "cid": cust_id, "pay": payment_method,
                "chan": channel, "sub": subtotal, "disc": discount_amount, "tax": tax_amount, "tot": final_total
            })
            order_id = result.lastrowid or db_manager.execute_query("SELECT MAX(order_id) AS mid FROM orders")["mid"].iloc[0]

            # 2. Insert Order Items & Deduct Stock
            for item in st.session_state.pos_cart:
                profit = round(item["total_price"] - (item["cost_price"] * item["quantity"]), 2)
                conn.execute(text("""
                    INSERT INTO order_items (order_id, product_id, quantity, unit_cost, unit_price, total_price, profit_margin)
                    VALUES (:oid, :pid, :qty, :cost, :price, :tot, :prof)
                """), {
                    "oid": order_id, "pid": item["product_id"], "qty": item["quantity"],
                    "cost": item["cost_price"], "price": item["unit_price"], "tot": item["total_price"], "prof": profit
                })

                # Deduct inventory stock
                conn.execute(text("""
                    UPDATE products SET current_stock = MAX(0, current_stock - :qty) WHERE product_id = :pid
                """), {"qty": item["quantity"], "pid": item["product_id"]})

                # Log inventory movement
                conn.execute(text("""
                    INSERT INTO inventory_logs (product_id, change_type, quantity, timestamp, reason, cost_impact)
                    VALUES (:pid, 'Sale', :qty, :dt, :reason, :impact)
                """), {
                    "pid": item["product_id"], "qty": -item["quantity"], "dt": now_dt,
                    "reason": f"POS Invoice #{inv_no} (Cashier: {user['full_name']})", 
                    "impact": round(item["cost_price"] * item["quantity"], 2)
                })

        st.success(f"🎉 Transaction Completed! Invoice **{inv_no}** generated and inventory deducted.")
        st.session_state.pos_cart = []
        st.rerun()
