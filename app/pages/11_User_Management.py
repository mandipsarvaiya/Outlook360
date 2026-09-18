"""
Outlook360 - Employee & Access Management (Store Owner Portal)
Allows Store Owner to create, manage, and audit employee accounts and role assignments.
"""
import streamlit as st
import pandas as pd
from database.auth import auth_manager
from database.connection import db_manager
from app.auth_gate import require_auth, render_auth_sidebar
from app.theme import render_custom_css, render_header, render_metric_card

st.set_page_config(
    page_title="Staff & Access Management | Outlook360",
    page_icon="👥",
    layout="wide"
)

render_custom_css()
render_auth_sidebar()
user = require_auth(allowed_roles=["owner"])

# Render Page Header
render_header(
    title="Staff & Access Control Hub",
    subtitle="Manage role-based employee credentials, onboard new staff, and monitor account status.",
    badge_text="👑 Store Owner Administration"
)

# Fetch user list
df_users = auth_manager.get_all_users()

# Metrics
total_users = len(df_users)
total_cashiers = len(df_users[df_users["role"] == "cashier"]) if not df_users.empty else 0
total_inventory = len(df_users[df_users["role"] == "inventory"]) if not df_users.empty else 0
active_users = len(df_users[df_users["is_active"] == 1]) if not df_users.empty else 0

mcol1, mcol2, mcol3, mcol4 = st.columns(4)
with mcol1:
    render_metric_card("Total Accounts", f"{total_users}", "Registered Staff", "👥", "neutral")
with mcol2:
    render_metric_card("Cashier Staff", f"{total_cashiers}", "POS Operators", "💳", "neutral")
with mcol3:
    render_metric_card("Inventory Staff", f"{total_inventory}", "Warehouse / Stock", "📦", "neutral")
with mcol4:
    render_metric_card("Active Accounts", f"{active_users}", f"{total_users - active_users} Suspended", "✅", "positive")

st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

tab_list, tab_create, tab_modify = st.tabs([
    "📋 Active Staff Directory",
    "➕ Onboard New Employee",
    "⚙️ Account Status & Reset"
])

# -------------------------------------------------------------
# TAB 1: ACTIVE STAFF DIRECTORY
# -------------------------------------------------------------
with tab_list:
    st.markdown("### 📋 System Users & Role Permissions")
    if df_users.empty:
        st.info("No users registered.")
    else:
        display_users = df_users.copy()
        display_users["Role Label"] = display_users["role"].apply(
            lambda r: "👑 Store Owner" if r == "owner" else ("💳 Cashier" if r == "cashier" else "📦 Inventory Staff")
        )
        display_users["Status"] = display_users["is_active"].apply(lambda a: "🟢 Active" if a == 1 else "🔴 Inactive")
        
        st.dataframe(
            display_users[[
                "user_id", "emp_id", "full_name", "email", "Role Label", "Status", "created_at"
            ]].rename(columns={
                "user_id": "User ID",
                "emp_id": "Employee ID",
                "full_name": "Full Name",
                "email": "Email Address",
                "created_at": "Registered At"
            }),
            use_container_width=True
        )

# -------------------------------------------------------------
# TAB 2: ONBOARD NEW EMPLOYEE
# -------------------------------------------------------------
with tab_create:
    st.markdown("### ➕ Register New Employee Account")
    st.caption("Create role-based credentials for new store employees.")

    with st.form("create_user_form"):
        col1, col2 = st.columns(2)
        with col1:
            new_emp_id = st.text_input("Employee ID", placeholder="e.g. EMP-CSH-02 or EMP-INV-02")
            new_full_name = st.text_input("Full Name", placeholder="e.g. Rajesh Kumar")
            new_email = st.text_input("Work Email Address", placeholder="e.g. rajesh@outlook360.com")
        with col2:
            new_role = st.selectbox(
                "Assigned Role",
                options=["cashier", "inventory", "owner"],
                format_func=lambda r: {
                    "cashier": "💳 Cashier (POS & Customer Billing)",
                    "inventory": "📦 Inventory Staff (Stock & Catalog)",
                    "owner": "👑 Store Owner (Full Access)"
                }.get(r, r)
            )
            new_password = st.text_input("Initial Password", type="password", placeholder="Minimum 6 characters")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")

        submit_create = st.form_submit_button("✨ Create Employee Account", use_container_width=True)
        if submit_create:
            if not new_emp_id or not new_full_name or not new_email or not new_password:
                st.error("Please complete all required fields.")
            elif new_password != confirm_password:
                st.error("Passwords do not match!")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters long.")
            else:
                # Check uniqueness
                check_sql = "SELECT user_id FROM users WHERE LOWER(email) = :email OR LOWER(emp_id) = :emp"
                existing = db_manager.execute_query(check_sql, {"email": new_email.lower(), "emp": new_emp_id.lower()})
                if not existing.empty:
                    st.error("An employee account with this Email or Employee ID already exists!")
                else:
                    success = auth_manager.create_user(
                        emp_id=new_emp_id,
                        email=new_email,
                        password=new_password,
                        full_name=new_full_name,
                        role=new_role
                    )
                    if success:
                        st.success(f"🎉 Account successfully created for {new_full_name} ({new_emp_id.upper()})!")
                        st.rerun()
                    else:
                        st.error("Failed to create user account. Please check server logs.")

# -------------------------------------------------------------
# TAB 3: ACCOUNT STATUS & PASSWORD RESET
# -------------------------------------------------------------
with tab_modify:
    st.markdown("### ⚙️ Manage Existing Staff Accounts")
    st.caption("Deactivate accounts or reset passwords for employees.")

    if not df_users.empty:
        target_uid = st.selectbox(
            "Select Employee Account:",
            options=df_users["user_id"].tolist(),
            format_func=lambda uid: f"ID {uid}: {df_users.loc[df_users['user_id']==uid, 'emp_id'].values[0]} - {df_users.loc[df_users['user_id']==uid, 'full_name'].values[0]} ({df_users.loc[df_users['user_id']==uid, 'role'].values[0]})"
        )
        target_user = df_users[df_users["user_id"] == target_uid].iloc[0]

        col_st1, col_st2 = st.columns(2)
        with col_st1:
            st.markdown("#### Account Status")
            current_status = "Active" if target_user["is_active"] == 1 else "Suspended / Inactive"
            st.write(f"Current Status: **{current_status}**")
            
            action_label = "🔴 Suspend Account" if target_user["is_active"] == 1 else "🟢 Activate Account"
            if target_user["user_id"] == user["user_id"]:
                st.info("You cannot suspend your own logged-in Store Owner account.")
            else:
                if st.button(action_label, use_container_width=True):
                    new_active_val = 0 if target_user["is_active"] == 1 else 1
                    db_manager.execute_non_query(
                        "UPDATE users SET is_active = :val WHERE user_id = :uid",
                        {"val": new_active_val, "uid": int(target_uid)}
                    )
                    st.success("Account status updated!")
                    st.rerun()

        with col_st2:
            st.markdown("#### Reset Password")
            with st.form("reset_pwd_form"):
                new_reset_pwd = st.text_input("New Password", type="password")
                submit_reset = st.form_submit_button("🔑 Reset Password", use_container_width=True)
                if submit_reset:
                    if len(new_reset_pwd) < 6:
                        st.error("Password must be at least 6 characters.")
                    else:
                        new_hash = auth_manager.hash_password(new_reset_pwd)
                        db_manager.execute_non_query(
                            "UPDATE users SET password_hash = :hash WHERE user_id = :uid",
                            {"hash": new_hash, "uid": int(target_uid)}
                        )
                        st.success(f"Password reset successfully for {target_user['full_name']}!")
