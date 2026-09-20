"""
Outlook360 - Authentication Gate & RBAC Security Layer
Provides unified login interfaces, session management, role badges, and page access guards.
"""
import streamlit as st
from typing import List, Optional, Dict, Any
from database.auth import auth_manager
from app.theme import render_custom_css


def init_auth_state() -> None:
    """Initializes authentication session state variables."""
    if "is_authenticated" not in st.session_state:
        st.session_state["is_authenticated"] = False
    if "user" not in st.session_state:
        st.session_state["user"] = None


def login_user(identifier: str, password: str) -> bool:
    """Attempts user authentication and sets session state."""
    user = auth_manager.authenticate_user(identifier, password)
    if user:
        st.session_state["is_authenticated"] = True
        st.session_state["user"] = user
        return True
    return False


def logout_user() -> None:
    """Clears authentication session state."""
    st.session_state["is_authenticated"] = False
    st.session_state["user"] = None
    st.rerun()


def render_login_screen() -> None:
    """Renders the Blue & White Role-Based Authentication Portal."""
    render_custom_css()
    
    st.markdown("""
    <div style="text-align: center; margin-top: 1.5rem; margin-bottom: 2rem;">
        <div style="display: inline-flex; align-items: center; justify-content: center; width: 64px; height: 64px; background: linear-gradient(135deg, #2563eb, #1d4ed8); border-radius: 16px; box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.4); margin-bottom: 1rem;">
            <span style="font-size: 2rem;">⚡</span>
        </div>
        <h1 style="color: #0f172a; font-weight: 800; font-size: 2.2rem; margin: 0; letter-spacing: -0.02em;">
            Outlook360 <span style="color: #2563eb;">AI</span>
        </h1>
        <p style="color: #64748b; font-size: 1.05rem; margin-top: 0.4rem; font-weight: 500;">
            Enterprise Multi-Tenant Intelligence & Role-Based Access Portal
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 1.75rem 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.06); margin-bottom: 1.5rem;">
            <h3 style="color: #1e293b; margin-top: 0; font-weight: 700; font-size: 1.25rem;">🔐 System Authentication</h3>
            <p style="color: #64748b; font-size: 0.88rem; margin-bottom: 1rem;">
                Select your assigned business role to access your dedicated workflow workspace.
            </p>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs([
            "👑 Store Owner",
            "💳 Cashier Portal",
            "📦 Inventory Staff"
        ])

        with tab1:
            st.caption("Access all Executive BI, Machine Learning, Forecasting, and Staff Control.")
            with st.form("owner_login_form"):
                owner_email = st.text_input("Gmail / Work Email", placeholder="smt10@gmail.com", key="owner_email")
                owner_pwd = st.text_input("Password", type="password", placeholder="••••••••", key="owner_pwd")
                submit_owner = st.form_submit_button("👑 Sign In as Store Owner", use_container_width=True)
                
                if submit_owner:
                    if not owner_email or not owner_pwd:
                        st.error("Please enter both email and password.")
                    else:
                        if login_user(owner_email, owner_pwd):
                            if st.session_state["user"]["role"] != "owner":
                                st.warning("Authenticated, but this account is not assigned Store Owner privileges.")
                            st.success(f"Welcome back, {st.session_state['user']['full_name']}!")
                            st.rerun()
                        else:
                            st.error("Invalid credentials. Please verify your email and password.")

        with tab2:
            st.caption("Access Live POS Billing Terminal, Customer Registration, and Shift Receipts.")
            with st.form("cashier_login_form"):
                cashier_id = st.text_input("Employee ID", placeholder="EMP-CSH-01", key="csh_id")
                cashier_pwd = st.text_input("Password", type="password", placeholder="••••••••", key="csh_pwd")
                submit_csh = st.form_submit_button("💳 Sign In as Cashier", use_container_width=True)
                
                if submit_csh:
                    if not cashier_id or not cashier_pwd:
                        st.error("Please enter Employee ID and password.")
                    else:
                        if login_user(cashier_id, cashier_pwd):
                            st.success(f"Welcome, {st.session_state['user']['full_name']}!")
                            st.rerun()
                        else:
                            st.error("Invalid Cashier Employee ID or password.")

        with tab3:
            st.caption("Access Product Catalog CRUD, Stock In/Out Adjustments, and Low Stock Alerts.")
            with st.form("inv_login_form"):
                inv_id = st.text_input("Employee ID", placeholder="EMP-INV-01", key="inv_id")
                inv_pwd = st.text_input("Password", type="password", placeholder="••••••••", key="inv_pwd")
                submit_inv = st.form_submit_button("📦 Sign In as Inventory Staff", use_container_width=True)
                
                if submit_inv:
                    if not inv_id or not inv_pwd:
                        st.error("Please enter Employee ID and password.")
                    else:
                        if login_user(inv_id, inv_pwd):
                            st.success(f"Welcome, {st.session_state['user']['full_name']}!")
                            st.rerun()
                        else:
                            st.error("Invalid Inventory Staff Employee ID or password.")

        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        with st.expander("⚡ Quick-Fill Demo Credentials (For Evaluation & Viva)"):
            st.markdown("""
            Click any button below to instantly populate credentials:
            """)
            qcol1, qcol2, qcol3 = st.columns(3)
            with qcol1:
                if st.button("👑 Store Owner", use_container_width=True):
                    login_user("smt10@gmail.com", "12345")
                    st.rerun()
            with qcol2:
                if st.button("💳 Cashier", use_container_width=True):
                    login_user("EMP-CSH-01", "cashier123")
                    st.rerun()
            with qcol3:
                if st.button("📦 Inventory", use_container_width=True):
                    login_user("EMP-INV-01", "inventory123")
                    st.rerun()


def render_auth_sidebar() -> None:
    """Renders authentication status and user badge in the Streamlit sidebar."""
    init_auth_state()
    user = st.session_state.get("user")

    if st.session_state.get("is_authenticated") and user:
        role = user.get("role", "").lower()
        role_label = {
            "owner": "👑 Store Owner",
            "cashier": "💳 Cashier",
            "inventory": "📦 Inventory Staff"
        }.get(role, role.capitalize())

        badge_bg = {
            "owner": "linear-gradient(135deg, #1e40af, #2563eb)",
            "cashier": "linear-gradient(135deg, #047857, #10b981)",
            "inventory": "linear-gradient(135deg, #b45309, #f59e0b)"
        }.get(role, "linear-gradient(135deg, #334155, #64748b)")

        st.sidebar.markdown(f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <div style="display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; color: #ffffff; background: {badge_bg}; margin-bottom: 0.5rem;">
                {role_label}
            </div>
            <div style="font-weight: 700; color: #0f172a; font-size: 0.95rem;">{user.get('full_name')}</div>
            <div style="font-size: 0.78rem; color: #64748b;">ID: {user.get('emp_id')} | {user.get('email')}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.sidebar.button("🚪 Sign Out", use_container_width=True):
            logout_user()
    else:
        st.sidebar.info("🔒 Guest Session. Please sign in to access protected modules.")


def require_auth(allowed_roles: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
    """
    Guards a page against unauthorized access.
    If not logged in, displays login screen and halts execution.
    If logged in but wrong role, displays access denied alert and halts execution.
    """
    init_auth_state()
    
    if not st.session_state.get("is_authenticated"):
        render_login_screen()
        st.stop()
        return None

    user = st.session_state.get("user")
    if not user:
        render_login_screen()
        st.stop()
        return None

    # Role check (Store Owner has access to everything)
    user_role = user.get("role", "").lower()
    if allowed_roles and user_role != "owner" and user_role not in [r.lower() for r in allowed_roles]:
        render_custom_css()
        st.markdown(f"""
        <div style="background: #fef2f2; border: 1px solid #fca5a5; border-radius: 14px; padding: 2rem; margin: 2rem 0; text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">⛔</div>
            <h2 style="color: #991b1b; margin-top: 0; font-weight: 700;">Access Restricted</h2>
            <p style="color: #7f1d1d; font-size: 1rem; max-width: 500px; margin: 0 auto 1.5rem auto;">
                Your account (<strong>{user.get('full_name')}</strong> - <em>{user_role.capitalize()}</em>) does not have permission to access this module.
                This module is reserved for: <strong>{', '.join([r.capitalize() for r in allowed_roles])}</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 Switch Account / Log In Again", use_container_width=True):
                logout_user()
        st.stop()
        return None

    return user
