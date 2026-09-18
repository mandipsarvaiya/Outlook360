"""
Outlook360 - Inventory Management & Stock Operations Portal
Dedicated portal for Inventory Staff & Store Owner.
Enables Product Catalog CRUD, Stock In/Out Adjustments, and Low Stock Early-Warning Radar.
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from database.connection import db_manager
from app.auth_gate import require_auth, render_auth_sidebar
from app.theme import render_custom_css, render_header, render_metric_card

# Enforce Authentication & Role Check
st.set_page_config(
    page_title="Inventory Management | Outlook360",
    page_icon="📦",
    layout="wide"
)

render_custom_css()
render_auth_sidebar()
user = require_auth(allowed_roles=["inventory", "owner"])

# Render Page Header
render_header(
    title="Inventory & Stock Control Hub",
    subtitle="Manage product catalog, log stock movements, and monitor low-stock early warnings.",
    badge_text="Inventory Staff Workspace" if user["role"] == "inventory" else "Store Owner Workspace"
)


# Helper query functions
def load_categories():
    return db_manager.execute_query("SELECT category_id, name, department FROM categories ORDER BY name ASC")

def load_products():
    sql = """
    SELECT 
        p.product_id,
        p.sku,
        p.name AS product_name,
        c.name AS category_name,
        p.category_id,
        p.cost_price,
        p.unit_price,
        (p.unit_price - p.cost_price) AS margin,
        p.current_stock,
        p.reorder_level,
        p.lead_time_days,
        p.is_active
    FROM products p
    JOIN categories c ON p.category_id = c.category_id
    ORDER BY p.product_id DESC
    """
    return db_manager.execute_query(sql)

def load_inventory_logs(limit=30):
    sql = f"""
    SELECT 
        l.log_id,
        l.product_id,
        p.name AS product_name,
        l.change_type,
        l.quantity,
        l.reason,
        l.cost_impact,
        l.timestamp
    FROM inventory_logs l
    JOIN products p ON l.product_id = p.product_id
    ORDER BY l.log_id DESC
    LIMIT {limit}
    """
    return db_manager.execute_query(sql)


# --- Load Live Data ---
df_products = load_products()
df_categories = load_categories()

# Top Metric Cards
total_skus = len(df_products)
active_skus = len(df_products[df_products["is_active"] == 1]) if not df_products.empty else 0
total_units = df_products["current_stock"].sum() if not df_products.empty else 0
total_valuation = (df_products["current_stock"] * df_products["cost_price"]).sum() if not df_products.empty else 0

# Low stock detection
low_stock_df = df_products[df_products["current_stock"] <= df_products["reorder_level"]] if not df_products.empty else pd.DataFrame()
critical_stockout_df = df_products[df_products["current_stock"] == 0] if not df_products.empty else pd.DataFrame()

col1, col2, col3, col4 = st.columns(4)
with col1:
    render_metric_card("Total Catalog SKUs", f"{total_skus:,}", f"{active_skus} Active SKUs", "📦", "neutral")
with col2:
    render_metric_card("Total Stock on Hand", f"{total_units:,} Units", "Across All Categories", "📊", "neutral")
with col3:
    render_metric_card("Inventory Valuation", f"₹{total_valuation:,.2f}", "At Cost Price", "💰", "positive")
with col4:
    alert_status = "negative" if len(low_stock_df) > 0 else "positive"
    render_metric_card("Low Stock Alerts", f"{len(low_stock_df)} Items", f"{len(critical_stockout_df)} Critical (0 Stock)", "🚨", alert_status)

st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

# Tabs for Operations
tab_alerts, tab_catalog, tab_adjust, tab_add, tab_logs = st.tabs([
    "🚨 Low Stock Alerts",
    "📋 Product Catalog",
    "🔄 Stock In / Out Adjustment",
    "➕ Add New Product",
    "📜 Stock Audit Logs"
])

# -------------------------------------------------------------
# TAB 1: LOW STOCK ALERTS & EARLY WARNING RADAR
# -------------------------------------------------------------
with tab_alerts:
    st.markdown("### 🚨 Low Stock & Stockout Early-Warning Radar")
    st.caption("Automated threshold monitor: Highlights items where Current Stock ≤ Reorder Point.")

    if low_stock_df.empty:
        st.success("✅ All product inventory levels are healthy! No SKUs currently below reorder threshold.")
    else:
        st.warning(f"⚠️ **{len(low_stock_df)} items require immediate procurement restocking!**")
        
        # Calculate suggested reorder quantity
        alert_view = low_stock_df.copy()
        alert_view["Deficit"] = alert_view["reorder_level"] - alert_view["current_stock"]
        alert_view["Suggested_Order_Qty"] = alert_view.apply(
            lambda r: max(r["reorder_level"] * 2 - r["current_stock"], 20), axis=1
        )
        alert_view["Est_Procurement_Cost"] = alert_view["Suggested_Order_Qty"] * alert_view["cost_price"]

        display_cols = [
            "sku", "product_name", "category_name", "current_stock", 
            "reorder_level", "lead_time_days", "Suggested_Order_Qty", "cost_price", "Est_Procurement_Cost"
        ]
        
        # Format for table display
        formatted_alerts = alert_view[display_cols].rename(columns={
            "sku": "SKU",
            "product_name": "Product Name",
            "category_name": "Category",
            "current_stock": "Current Stock",
            "reorder_level": "Reorder Level",
            "lead_time_days": "Lead Time (Days)",
            "Suggested_Order_Qty": "Recommended Order",
            "cost_price": "Unit Cost (₹)",
            "Est_Procurement_Cost": "Est. Cost (₹)"
        })

        st.dataframe(
            formatted_alerts.style.format({
                "Unit Cost (₹)": "₹{:,.2f}",
                "Est. Cost (₹)": "₹{:,.2f}"
            }).apply(
                lambda row: ['background-color: #fee2e2; color: #991b1b; font-weight: 600;' if row['Current Stock'] == 0 
                             else 'background-color: #fef3c7; color: #92400e;' for _ in row], 
                axis=1
            ),
            use_container_width=True
        )

        # Quick Reorder Action
        st.markdown("#### ⚡ Quick Stock Replenishment")
        reorder_sku = st.selectbox(
            "Select Low Stock Item to Replenish:",
            options=low_stock_df["product_id"].tolist(),
            format_func=lambda pid: f"{low_stock_df.loc[low_stock_df['product_id']==pid, 'sku'].values[0]} - {low_stock_df.loc[low_stock_df['product_id']==pid, 'product_name'].values[0]} (Stock: {low_stock_df.loc[low_stock_df['product_id']==pid, 'current_stock'].values[0]})"
        )
        
        selected_row = low_stock_df[low_stock_df["product_id"] == reorder_sku].iloc[0]
        rec_qty = int(max(selected_row["reorder_level"] * 2 - selected_row["current_stock"], 20))
        
        col_r1, col_r2, col_r3 = st.columns([1, 1, 1])
        with col_r1:
            restock_units = st.number_input("Received Units (Stock In)", min_value=1, value=rec_qty, step=5)
        with col_r2:
            vendor_note = st.text_input("Supplier PO / Invoice Ref", value=f"PO-{datetime.now().strftime('%Y%m%d')}-01")
        with col_r3:
            st.markdown("<div style='margin-top: 1.8rem;'></div>", unsafe_allow_html=True)
            if st.button("📥 Confirm Stock In", use_container_width=True):
                new_stock = int(selected_row["current_stock"] + restock_units)
                # Update product table
                db_manager.execute_non_query(
                    "UPDATE products SET current_stock = :new_stock WHERE product_id = :pid",
                    {"new_stock": new_stock, "pid": int(reorder_sku)}
                )
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Insert inventory log
                db_manager.execute_non_query(
                    """
                    INSERT INTO inventory_logs (product_id, change_type, quantity, timestamp, reason, cost_impact)
                    VALUES (:pid, 'Purchase', :qty, :ts, :reason, :impact)
                    """,
                    {
                        "pid": int(reorder_sku),
                        "qty": int(restock_units),
                        "ts": now_str,
                        "reason": f"Restocked via Quick Alert Hub. Ref: {vendor_note} (By: {user['full_name']})",
                        "impact": round(float(selected_row["cost_price"]) * restock_units, 2)
                    }
                )
                st.success(f"✅ Successfully replenished {restock_units} units for '{selected_row['product_name']}'. New Stock: {new_stock}")
                st.rerun()

# -------------------------------------------------------------
# TAB 2: PRODUCT CATALOG VIEW & EDIT
# -------------------------------------------------------------
with tab_catalog:
    st.markdown("### 📋 Product Master Catalog")
    st.caption("Search, filter, update prices, and maintain catalog metadata.")

    # Search & Filters
    fcol1, fcol2, fcol3 = st.columns([2, 1, 1])
    with fcol1:
        search_kw = st.text_input("🔍 Search SKU or Product Name", placeholder="e.g., Basmati, Milk, SKU-101")
    with fcol2:
        cat_filter = st.selectbox("Filter by Category", ["All Categories"] + df_categories["name"].tolist())
    with fcol3:
        status_filter = st.selectbox("Status", ["All", "Active Only", "Inactive Only"])

    filtered_df = df_products.copy()
    if search_kw:
        filtered_df = filtered_df[
            filtered_df["sku"].str.contains(search_kw, case=False, na=False) |
            filtered_df["product_name"].str.contains(search_kw, case=False, na=False)
        ]
    if cat_filter != "All Categories":
        filtered_df = filtered_df[filtered_df["category_name"] == cat_filter]
    if status_filter == "Active Only":
        filtered_df = filtered_df[filtered_df["is_active"] == 1]
    elif status_filter == "Inactive Only":
        filtered_df = filtered_df[filtered_df["is_active"] == 0]

    st.dataframe(
        filtered_df[[
            "product_id", "sku", "product_name", "category_name", 
            "cost_price", "unit_price", "margin", "current_stock", "reorder_level", "is_active"
        ]].rename(columns={
            "product_id": "ID",
            "sku": "SKU",
            "product_name": "Product Name",
            "category_name": "Category",
            "cost_price": "Cost (₹)",
            "unit_price": "Selling Price (₹)",
            "margin": "Margin (₹)",
            "current_stock": "Stock",
            "reorder_level": "Reorder Level",
            "is_active": "Active"
        }).style.format({
            "Cost (₹)": "₹{:,.2f}",
            "Selling Price (₹)": "₹{:,.2f}",
            "Margin (₹)": "₹{:,.2f}"
        }),
        use_container_width=True
    )

    # Edit Product Form
    st.markdown("---")
    st.markdown("#### ✏️ Edit Product Details")
    if not df_products.empty:
        edit_prod_id = st.selectbox(
            "Select Product to Edit:",
            options=df_products["product_id"].tolist(),
            format_func=lambda pid: f"ID {pid}: {df_products.loc[df_products['product_id']==pid, 'sku'].values[0]} - {df_products.loc[df_products['product_id']==pid, 'product_name'].values[0]}"
        )
        
        prod_row = df_products[df_products["product_id"] == edit_prod_id].iloc[0]

        with st.form("edit_product_form"):
            ecol1, ecol2 = st.columns(2)
            with ecol1:
                edit_name = st.text_input("Product Name", value=prod_row["product_name"])
                edit_cat = st.selectbox(
                    "Category", 
                    options=df_categories["category_id"].tolist(),
                    index=df_categories["category_id"].tolist().index(prod_row["category_id"]) if prod_row["category_id"] in df_categories["category_id"].tolist() else 0,
                    format_func=lambda cid: df_categories.loc[df_categories["category_id"]==cid, "name"].values[0]
                )
                edit_cost = st.number_input("Cost Price (₹)", min_value=0.5, value=float(prod_row["cost_price"]), step=1.0)
            with ecol2:
                edit_price = st.number_input("Selling Unit Price (₹)", min_value=0.5, value=float(prod_row["unit_price"]), step=1.0)
                edit_reorder = st.number_input("Reorder Threshold", min_value=1, value=int(prod_row["reorder_level"]), step=1)
                edit_lead = st.number_input("Lead Time (Days)", min_value=1, value=int(prod_row["lead_time_days"]), step=1)
                edit_active = st.checkbox("Product is Active", value=bool(prod_row["is_active"]))

            submit_edit = st.form_submit_button("💾 Save Product Changes", use_container_width=True)
            if submit_edit:
                db_manager.execute_non_query(
                    """
                    UPDATE products 
                    SET name = :name, category_id = :cat, cost_price = :cost, 
                        unit_price = :price, reorder_level = :reorder, lead_time_days = :lead, is_active = :active
                    WHERE product_id = :pid
                    """,
                    {
                        "name": edit_name.strip(),
                        "cat": int(edit_cat),
                        "cost": float(edit_cost),
                        "price": float(edit_price),
                        "reorder": int(edit_reorder),
                        "lead": int(edit_lead),
                        "active": 1 if edit_active else 0,
                        "pid": int(edit_prod_id)
                    }
                )
                st.success(f"✅ Product '{edit_name}' updated successfully!")
                st.rerun()

# -------------------------------------------------------------
# TAB 3: STOCK IN / OUT ADJUSTMENT (LEDGER LOGGING)
# -------------------------------------------------------------
with tab_adjust:
    st.markdown("### 🔄 Stock Movement & Quantity Adjustment")
    st.caption("Record stock adjustments (Restock In, Wastage / Damage, Customer Return, Audit Correction) with complete ledger tracking.")

    with st.form("stock_adjustment_form"):
        adj_col1, adj_col2 = st.columns(2)
        with adj_col1:
            adj_prod_id = st.selectbox(
                "Select Product",
                options=df_products["product_id"].tolist(),
                format_func=lambda pid: f"{df_products.loc[df_products['product_id']==pid, 'sku'].values[0]} - {df_products.loc[df_products['product_id']==pid, 'product_name'].values[0]} (Current: {df_products.loc[df_products['product_id']==pid, 'current_stock'].values[0]})"
            )
            adj_type = st.selectbox(
                "Adjustment Type",
                [
                    "RESTOCK_IN (Goods Received)",
                    "DAMAGE_OUT (Wastage / Expiry / Damaged)",
                    "RETURN_IN (Customer Return to Stock)",
                    "AUDIT_CORRECTION (Physical Stock Count)"
                ]
            )
        with adj_col2:
            adj_qty = st.number_input("Quantity Delta / Units", min_value=1, value=10, step=1)
            adj_reason = st.text_input("Reason / Reference Note", placeholder="e.g. Broken packaging / Supplier invoice #542")

        submit_adj = st.form_submit_button("📝 Post Stock Adjustment", use_container_width=True)
        if submit_adj:
            target_prod = df_products[df_products["product_id"] == adj_prod_id].iloc[0]
            current_s = int(target_prod["current_stock"])
            
            raw_type = adj_type.split(" ")[0]
            if "RESTOCK" in raw_type or "RETURN" in raw_type:
                new_s = current_s + int(adj_qty)
                delta_sign = int(adj_qty)
            elif "DAMAGE" in raw_type:
                new_s = max(0, current_s - int(adj_qty))
                delta_sign = -int(adj_qty)
            else: # AUDIT_CORRECTION
                new_s = int(adj_qty)
                delta_sign = new_s - current_s

            # Update product stock
            db_manager.execute_non_query(
                "UPDATE products SET current_stock = :new_s WHERE product_id = :pid",
                {"new_s": new_s, "pid": int(adj_prod_id)}
            )
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            impact_val = round(abs(delta_sign) * float(target_prod["cost_price"]), 2)
            # Insert log
            db_manager.execute_non_query(
                """
                INSERT INTO inventory_logs (product_id, change_type, quantity, timestamp, reason, cost_impact)
                VALUES (:pid, :ctype, :qty, :ts, :reason, :impact)
                """,
                {
                    "pid": int(adj_prod_id),
                    "ctype": raw_type,
                    "qty": delta_sign,
                    "ts": now_str,
                    "reason": f"{adj_reason} (Posted by {user['full_name']})",
                    "impact": impact_val
                }
            )
            st.success(f"✅ Stock adjusted for '{target_prod['product_name']}'. Previous: {current_s} ➔ New Stock: {new_s}")
            st.rerun()

# -------------------------------------------------------------
# TAB 4: ADD NEW PRODUCT
# -------------------------------------------------------------
with tab_add:
    st.markdown("### ➕ Register New Product in Catalog")
    st.caption("Add a new SKU with category assignment, pricing, and initial stock.")

    with st.form("add_product_form"):
        acol1, acol2 = st.columns(2)
        with acol1:
            auto_sku = f"SKU-{len(df_products)+101}"
            new_sku = st.text_input("SKU Code (Unique)", value=auto_sku)
            new_name = st.text_input("Product Title", placeholder="e.g. Organic Brown Basmati Rice 1kg")
            new_cat_id = st.selectbox(
                "Category",
                options=df_categories["category_id"].tolist(),
                format_func=lambda cid: df_categories.loc[df_categories["category_id"]==cid, "name"].values[0]
            )
            new_cost = st.number_input("Cost Price (₹)", min_value=1.0, value=120.0, step=5.0)
        with acol2:
            new_price = st.number_input("Selling Price (₹)", min_value=1.0, value=175.0, step=5.0)
            new_initial_stock = st.number_input("Initial Opening Stock", min_value=0, value=50, step=5)
            new_reorder_lvl = st.number_input("Reorder Level Threshold", min_value=1, value=15, step=1)
            new_lead_time = st.number_input("Supplier Lead Time (Days)", min_value=1, value=3, step=1)

        submit_add = st.form_submit_button("✨ Register Product in Database", use_container_width=True)
        if submit_add:
            if not new_name.strip() or not new_sku.strip():
                st.error("Please provide both a valid SKU and Product Title.")
            else:
                # Check SKU uniqueness
                sku_check = db_manager.execute_query("SELECT product_id FROM products WHERE LOWER(sku) = :sku", {"sku": new_sku.strip().lower()})
                if not sku_check.empty:
                    st.error(f"SKU '{new_sku}' already exists in the catalog! Please choose a unique SKU.")
                else:
                    db_manager.execute_non_query(
                        """
                        INSERT INTO products (sku, name, category_id, cost_price, unit_price, current_stock, reorder_level, lead_time_days, is_active)
                        VALUES (:sku, :name, :cat, :cost, :price, :stock, :reorder, :lead, 1)
                        """,
                        {
                            "sku": new_sku.strip().upper(),
                            "name": new_name.strip(),
                            "cat": int(new_cat_id),
                            "cost": float(new_cost),
                            "price": float(new_price),
                            "stock": int(new_initial_stock),
                            "reorder": int(new_reorder_lvl),
                            "lead": int(new_lead_time)
                        }
                    )
                    st.success(f"🎉 Product '{new_name}' (SKU: {new_sku.upper()}) added successfully!")
                    st.rerun()

# -------------------------------------------------------------
# TAB 5: AUDIT LOGS
# -------------------------------------------------------------
with tab_logs:
    st.markdown("### 📜 Stock Movement Ledger & Audit Trail")
    st.caption("Immutable chronological record of all stock additions, deductions, damages, and POS sales.")

    logs_df = load_inventory_logs(limit=50)
    if logs_df.empty:
        st.info("No inventory logs recorded yet.")
    else:
        st.dataframe(
            logs_df.rename(columns={
                "log_id": "Log ID",
                "product_id": "Product ID",
                "product_name": "Product Name",
                "change_type": "Movement Type",
                "quantity_delta": "Quantity Delta",
                "stock_after": "Stock After",
                "notes": "Audit Notes",
                "created_at": "Timestamp"
            }),
            use_container_width=True
        )
