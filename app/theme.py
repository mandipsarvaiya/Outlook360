"""
Outlook360 - Blue & White Executive Theme & Design System
Provides clean, crisp white backgrounds with royal blue & sapphire accents,
frosted glass cards, modern typography, headers, and metric components.
"""
import streamlit as st


def apply_theme():
    """Injects high-end Blue & White aesthetic CSS into Streamlit application."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

        /* Base Typography and Background */
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #f0f7ff 50%, #f8fafc 100%);
            color: #0f172a;
        }

        /* Glassmorphic Metric Cards (White & Blue Accents) */
        .metric-card {
            background: rgba(255, 255, 255, 0.92);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(226, 232, 240, 0.9);
            border-radius: 16px;
            padding: 22px 24px;
            box-shadow: 0 4px 20px -2px rgba(30, 58, 138, 0.06), 0 2px 6px -1px rgba(30, 58, 138, 0.04);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .metric-card:hover {
            transform: translateY(-3px);
            border-color: rgba(37, 99, 235, 0.4);
            box-shadow: 0 12px 28px -4px rgba(37, 99, 235, 0.12);
        }

        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3.5px;
            background: linear-gradient(90deg, #1d4ed8, #2563eb, #38bdf8);
        }

        .metric-label {
            color: #64748b;
            font-size: 0.82rem;
            font-weight: 600;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .metric-value {
            color: #0f172a;
            font-size: 1.85rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 4px;
        }

        .metric-sub {
            font-size: 0.82rem;
            color: #2563eb;
            font-weight: 600;
        }

        /* Section Containers */
        .glass-container {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(226, 232, 240, 0.85);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 16px -2px rgba(30, 58, 138, 0.05);
        }

        /* Badges */
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.02em;
        }

        .badge-domain {
            background: #eff6ff;
            color: #1d4ed8;
            border: 1px solid #bfdbfe;
        }

        .badge-db {
            background: #ecfdf5;
            color: #047857;
            border: 1px solid #a7f3d0;
        }

        .badge-vital {
            background: #fffbeb;
            color: #b45309;
            border: 1px solid #fde68a;
        }

        /* Sidebar Styling & Top Brand Pinning */
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #e2e8f0;
            box-shadow: 2px 0 10px rgba(0,0,0,0.02);
        }

        [data-testid="stSidebarContent"] {
            display: flex !important;
            flex-direction: column !important;
        }

        [data-testid="stSidebarUserContent"] {
            order: -1 !important;
        }

        [data-testid="stSidebarNav"] {
            padding-top: 10px;
        }

        [data-testid="stSidebarNav"] span {
            font-weight: 600;
            color: #334155;
        }

        /* Custom headers */
        h1, h2, h3 {
            color: #0f172a !important;
            font-weight: 800 !important;
            letter-spacing: -0.03em !important;
        }

        /* Streamlit Button Customization */
        .stButton>button {
            background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #3b82f6 100%) !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 22px !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25) !important;
        }

        .stButton>button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.35) !important;
            color: #ffffff !important;
        }

        /* Metric cards inside streamlit */
        [data-testid="stMetricValue"] {
            color: #0f172a !important;
            font-weight: 800 !important;
        }

        [data-testid="stMetricLabel"] {
            color: #64748b !important;
            font-weight: 600 !important;
        }

        /* Dataframe styling */
        [data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
            background: #ffffff;
        }

        /* Expander styling */
        .streamlit-expanderHeader {
            background: #ffffff !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            color: #1e293b !important;
            border: 1px solid #e2e8f0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_custom_css():
    """Alias for apply_theme()."""
    apply_theme()


def render_header(title: str, subtitle: str = "", badge_text: str = None):
    """Renders a modern Blue & White page header with title, subtitle, and badge."""
    badge_html = f"""<span style="display: inline-block; padding: 3px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; color: #1d4ed8; background: #eff6ff; border: 1px solid #bfdbfe; margin-bottom: 8px;">{badge_text}</span>""" if badge_text else ""
    st.markdown(
        f"""
        <div style="padding: 6px 0 20px 0;">
            {badge_html}
            <h1 style="font-size: 2.1rem; margin-top: 2px; margin-bottom: 4px; background: linear-gradient(90deg, #1e3a8a, #2563eb); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                {title}
            </h1>
            <p style="color: #64748b; font-size: 0.98rem; font-weight: 500; margin-bottom: 0;">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_metric_card(label: str, value: str, delta: str = None, icon: str = None, status: str = "neutral"):
    """Renders a Blue & White frosted glass metric card."""
    delta_color = "#15803d" if status == "positive" else ("#b91c1c" if status == "negative" else "#2563eb")
    delta_html = f"""<div style="font-size: 0.82rem; color: {delta_color}; font-weight: 600; margin-top: 4px;">{delta}</div>""" if delta else ""
    icon_html = f"""<span style="font-size: 1.4rem; float: right;">{icon}</span>""" if icon else ""

    st.markdown(
        f"""
        <div class="metric-card">
            {icon_html}
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True
    )
