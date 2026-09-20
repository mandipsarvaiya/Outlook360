"""
Outlook360 - Blue & White Executive Theme & Design System
Clean, professional Enterprise SaaS CSS design tokens, typography,
scannable cards, workflow steps, responsive layouts, and modern headers.
"""
import streamlit as st


def apply_theme(is_landing_page: bool = False):
    """Injects high-end Blue & White aesthetic CSS into Streamlit application."""
    sidebar_landing_css = ""
    if is_landing_page:
        sidebar_landing_css = """
        [data-testid="stSidebar"], [data-testid="collapsedControl"] {
            display: none !important;
        }
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        """

    st.markdown(
        f"""<style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

        /* Base Typography and Background */
        html, body, [class*="css"] {{
            font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #0f172a;
        }}

        .stApp {{
            background: linear-gradient(135deg, #f8fafc 0%, #f0f7ff 45%, #f8fafc 100%);
            color: #0f172a;
        }}

        {sidebar_landing_css}

        /* ---------------------------------------------------------
           LANDING PAGE TOP NAVBAR
           --------------------------------------------------------- */
        .landing-navbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 24px;
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(226, 232, 240, 0.95);
            border-radius: 16px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px -2px rgba(30, 58, 138, 0.05);
            flex-wrap: wrap;
            gap: 12px;
        }}

        .landing-brand {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .landing-brand-logo {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, #1d4ed8, #2563eb);
            border-radius: 10px;
            color: #ffffff;
            font-size: 1.15rem;
            font-weight: 800;
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.28);
        }}

        .landing-brand-title {{
            font-size: 1.25rem;
            font-weight: 850;
            background: linear-gradient(90deg, #1e3a8a, #2563eb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.02em;
            line-height: 1.1;
        }}

        .landing-brand-tag {{
            font-size: 0.72rem;
            color: #64748b;
            font-weight: 500;
        }}

        .landing-nav-links {{
            display: flex;
            align-items: center;
            gap: 4px;
            flex-wrap: wrap;
        }}

        .landing-nav-link {{
            color: #334155 !important;
            font-size: 0.86rem;
            font-weight: 600;
            text-decoration: none !important;
            padding: 7px 14px;
            border-radius: 8px;
            transition: all 0.2s ease;
            display: inline-block;
        }}

        .landing-nav-link:hover {{
            color: #1d4ed8 !important;
            background: #eff6ff;
            text-decoration: none !important;
        }}

        /* ---------------------------------------------------------
           HERO SECTION
           --------------------------------------------------------- */
        .hero-container {{
            text-align: center;
            padding: 24px 16px 16px 16px;
            max-width: 920px;
            margin: 0 auto;
        }}

        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 5px 15px;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 700;
            color: #1d4ed8;
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            margin-bottom: 14px;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.06);
        }}

        .hero-title {{
            font-size: 2.75rem;
            font-weight: 850;
            line-height: 1.18;
            letter-spacing: -0.04em;
            color: #0f172a;
            margin-bottom: 12px;
        }}

        .hero-title-highlight {{
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #0284c7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .hero-headline {{
            font-size: 1.25rem;
            font-weight: 600;
            color: #1e3a8a;
            margin-bottom: 8px;
            letter-spacing: -0.01em;
        }}

        .hero-desc {{
            font-size: 0.98rem;
            color: #475569;
            line-height: 1.6;
            max-width: 740px;
            margin: 0 auto 18px auto;
        }}

        .hero-btn-secondary {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            padding: 10px 20px;
            background: #ffffff;
            color: #1e293b !important;
            font-weight: 600;
            font-size: 0.88rem;
            text-decoration: none !important;
            border: 1px solid #cbd5e1;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
            transition: all 0.2s ease;
        }}

        .hero-btn-secondary:hover {{
            border-color: #2563eb;
            color: #1d4ed8 !important;
            background: #eff6ff;
        }}

        /* ---------------------------------------------------------
           SECTION HEADINGS & CONTAINERS
           --------------------------------------------------------- */
        .section-header-block {{
            text-align: center;
            max-width: 720px;
            margin: 32px auto 16px auto;
            padding: 0 12px;
        }}

        .section-badge {{
            display: inline-block;
            padding: 3px 11px;
            border-radius: 9999px;
            font-size: 0.72rem;
            font-weight: 750;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: #1d4ed8;
            background: #eff6ff;
            border: 1px solid #dbeafe;
            margin-bottom: 6px;
        }}

        .section-heading {{
            font-size: 1.95rem;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: -0.03em;
            margin-bottom: 6px;
            line-height: 1.22;
        }}

        .section-subheading {{
            font-size: 0.94rem;
            color: #64748b;
            line-height: 1.55;
            margin-bottom: 0;
        }}

        /* ---------------------------------------------------------
           HORIZONTAL 6-STEP WORKFLOW
           --------------------------------------------------------- */
        .workflow-container {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 18px;
            padding: 20px 16px;
            margin: 6px 0 24px 0;
            box-shadow: 0 4px 18px -2px rgba(30, 58, 138, 0.04);
        }}

        .workflow-grid {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 10px;
            align-items: stretch;
        }}

        .workflow-card {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-top: 3.5px solid #2563eb;
            border-radius: 12px;
            padding: 14px 10px;
            text-align: center;
            transition: all 0.25s ease;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }}

        .workflow-card:hover {{
            transform: translateY(-3px);
            background: #ffffff;
            border-color: #93c5fd;
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.1);
        }}

        .workflow-step-num {{
            font-size: 0.72rem;
            font-weight: 800;
            color: #2563eb;
            letter-spacing: 0.04em;
            margin-bottom: 2px;
            font-family: 'JetBrains Mono', monospace;
        }}

        .workflow-icon {{
            font-size: 1.35rem;
            margin-bottom: 4px;
        }}

        .workflow-title {{
            font-size: 0.82rem;
            font-weight: 750;
            color: #0f172a;
            margin-bottom: 4px;
            letter-spacing: -0.01em;
        }}

        .workflow-desc {{
            font-size: 0.72rem;
            color: #64748b;
            line-height: 1.35;
        }}

        /* ---------------------------------------------------------
           WHAT IS OUTLOOK360 4-PILLAR CARDS
           --------------------------------------------------------- */
        .pillar-card {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 16px 14px;
            text-align: center;
            transition: all 0.2s ease;
            height: 100%;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        }}

        .pillar-card:hover {{
            transform: translateY(-2px);
            border-color: #93c5fd;
            box-shadow: 0 8px 16px rgba(37, 99, 235, 0.08);
        }}

        .pillar-icon {{
            font-size: 1.4rem;
            margin-bottom: 4px;
        }}

        .pillar-title {{
            font-size: 0.92rem;
            font-weight: 750;
            color: #0f172a;
            margin-bottom: 3px;
        }}

        .pillar-desc {{
            font-size: 0.76rem;
            color: #64748b;
            line-height: 1.4;
        }}

        /* ---------------------------------------------------------
           CORE PLATFORM CAPABILITIES (6-Grid)
           --------------------------------------------------------- */
        .capability-box {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 18px 16px;
            transition: all 0.25s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        }}

        .capability-box:hover {{
            transform: translateY(-3px);
            border-color: #60a5fa;
            box-shadow: 0 10px 22px rgba(37, 99, 235, 0.1);
        }}

        .capability-box-icon {{
            font-size: 1.4rem;
            margin-bottom: 8px;
        }}

        .capability-box-title {{
            font-size: 0.98rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 4px;
            letter-spacing: -0.01em;
        }}

        .capability-box-desc {{
            font-size: 0.82rem;
            color: #475569;
            line-height: 1.45;
            flex-grow: 1;
            margin-bottom: 8px;
        }}

        .capability-box-tag {{
            font-size: 0.72rem;
            font-weight: 600;
            color: #2563eb;
            background: #eff6ff;
            padding: 2px 8px;
            border-radius: 6px;
            align-self: flex-start;
            border: 1px solid #dbeafe;
        }}

        /* ---------------------------------------------------------
           POWERFUL ANALYTICS MODULES (6-Grid & BI Grid)
           --------------------------------------------------------- */
        .module-product-card {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 20px 18px;
            transition: all 0.25s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
            box-shadow: 0 2px 10px rgba(0,0,0,0.02);
        }}

        .module-product-card:hover {{
            transform: translateY(-3px);
            border-color: #2563eb;
            box-shadow: 0 12px 24px rgba(37, 99, 235, 0.12);
        }}

        .module-product-icon {{
            font-size: 1.45rem;
            margin-bottom: 6px;
        }}

        .module-product-title {{
            font-size: 1.08rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 4px;
            letter-spacing: -0.01em;
        }}

        .module-product-desc {{
            font-size: 0.83rem;
            color: #475569;
            line-height: 1.5;
            flex-grow: 1;
            margin-bottom: 12px;
        }}

        /* ---------------------------------------------------------
           BUSINESS INTELLIGENCE (8-Grid)
           --------------------------------------------------------- */
        .bi-card {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 16px 14px;
            transition: all 0.25s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        }}

        .bi-card:hover {{
            transform: translateY(-3px);
            border-color: #3b82f6;
            box-shadow: 0 10px 20px rgba(37, 99, 235, 0.1);
        }}

        .bi-card-icon {{
            font-size: 1.3rem;
            margin-bottom: 4px;
        }}

        .bi-card-title {{
            font-size: 0.95rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 4px;
            letter-spacing: -0.01em;
        }}

        .bi-card-desc {{
            font-size: 0.78rem;
            color: #475569;
            line-height: 1.4;
            flex-grow: 1;
        }}

        /* ---------------------------------------------------------
           BUSINESS QUESTIONS
           --------------------------------------------------------- */
        .question-card {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #2563eb;
            border-radius: 12px;
            padding: 14px 16px;
            margin-bottom: 10px;
            transition: all 0.2s ease;
            box-shadow: 0 2px 6px rgba(0,0,0,0.02);
        }}

        .question-card:hover {{
            transform: translateX(3px);
            border-left-color: #1d4ed8;
            box-shadow: 0 6px 14px rgba(37, 99, 235, 0.08);
        }}

        .question-title {{
            font-size: 0.92rem;
            font-weight: 750;
            color: #0f172a;
            margin-bottom: 3px;
        }}

        .question-meta {{
            font-size: 0.78rem;
            color: #64748b;
        }}

        /* ---------------------------------------------------------
           AI & ML VISUAL PIPELINE
           --------------------------------------------------------- */
        .ai-flow-box {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 18px 14px;
            margin-bottom: 16px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.02);
        }}

        .ai-flow-grid {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 8px;
            align-items: center;
            text-align: center;
        }}

        .ai-flow-step {{
            padding: 10px 6px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            font-size: 0.74rem;
            font-weight: 700;
            color: #1e3a8a;
        }}

        /* ---------------------------------------------------------
           GLASS CONTAINERS & METRICS
           --------------------------------------------------------- */
        .glass-container {{
            background: rgba(255, 255, 255, 0.94);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(226, 232, 240, 0.9);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 16px -2px rgba(30, 58, 138, 0.04);
        }}

        .metric-card {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 18px 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.02);
            transition: all 0.25s ease;
            position: relative;
            overflow: hidden;
        }}

        .metric-card:hover {{
            transform: translateY(-2px);
            border-color: #93c5fd;
            box-shadow: 0 10px 20px rgba(37, 99, 235, 0.08);
        }}

        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #1d4ed8, #2563eb);
        }}

        .metric-label {{
            color: #64748b;
            font-size: 0.78rem;
            font-weight: 650;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 4px;
        }}

        .metric-value {{
            color: #0f172a;
            font-size: 1.75rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 2px;
        }}

        .metric-sub {{
            font-size: 0.78rem;
            color: #2563eb;
            font-weight: 600;
        }}

        /* ---------------------------------------------------------
           ENTERPRISE FOOTER
           --------------------------------------------------------- */
        .enterprise-footer {{
            background: #ffffff;
            border-top: 1px solid #e2e8f0;
            border-radius: 18px 18px 0 0;
            padding: 30px 20px 20px 20px;
            margin-top: 36px;
            text-align: center;
        }}

        .footer-brand {{
            font-size: 1.25rem;
            font-weight: 850;
            background: linear-gradient(90deg, #1e3a8a, #2563eb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 3px;
        }}

        .footer-subtitle {{
            font-size: 0.82rem;
            color: #64748b;
            margin-bottom: 14px;
        }}

        .footer-links-row {{
            display: flex;
            justify-content: center;
            gap: 16px;
            flex-wrap: wrap;
            margin-bottom: 14px;
        }}

        .footer-link-item {{
            color: #475569 !important;
            font-size: 0.82rem;
            font-weight: 600;
            text-decoration: none !important;
            transition: color 0.2s ease;
        }}

        .footer-link-item:hover {{
            color: #1d4ed8 !important;
        }}

        .footer-copy {{
            font-size: 0.75rem;
            color: #94a3b8;
            border-top: 1px solid #f1f5f9;
            padding-top: 14px;
            margin-top: 14px;
        }}

        /* ---------------------------------------------------------
           STREAMLIT OVERRIDES
           --------------------------------------------------------- */
        .stButton>button {{
            background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
            color: #ffffff !important;
            font-weight: 650 !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 9px 20px !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
        }}

        .stButton>button:hover {{
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 18px rgba(37, 99, 235, 0.3) !important;
        }}

        [data-testid="stPageLink-NavLink"] {{
            border: 1px solid #e2e8f0 !important;
            border-radius: 10px !important;
            background: #ffffff !important;
            transition: all 0.2s ease !important;
            font-weight: 600 !important;
            color: #1e293b !important;
        }}

        [data-testid="stPageLink-NavLink"]:hover {{
            border-color: #2563eb !important;
            background: #eff6ff !important;
            color: #1d4ed8 !important;
            transform: translateX(2px) !important;
        }}

        /* Responsive Breakpoints */
        @media (max-width: 900px) {{
            .workflow-grid, .ai-flow-grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
            .hero-title {{
                font-size: 2.1rem;
            }}
        }}

        @media (max-width: 600px) {{
            .workflow-grid, .ai-flow-grid {{
                grid-template-columns: 1fr;
            }}
            .hero-title {{
                font-size: 1.75rem;
            }}
            .landing-navbar {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
        </style>""",
        unsafe_allow_html=True
    )


def render_custom_css():
    """Alias for apply_theme()."""
    apply_theme()


def render_header(title: str, subtitle: str = "", badge_text: str = None):
    """Renders a modern Blue & White page header with title, subtitle, and badge."""
    badge_html = f"""<span style="display: inline-block; padding: 3px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; color: #1d4ed8; background: #eff6ff; border: 1px solid #bfdbfe; margin-bottom: 8px;">{badge_text}</span>""" if badge_text else ""
    st.markdown(
        f"""<div style="padding: 6px 0 20px 0;">{badge_html}<h1 style="font-size: 2.1rem; margin-top: 2px; margin-bottom: 4px; background: linear-gradient(90deg, #1e3a8a, #2563eb); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{title}</h1><p style="color: #64748b; font-size: 0.98rem; font-weight: 500; margin-bottom: 0;">{subtitle}</p></div>""",
        unsafe_allow_html=True
    )


def render_metric_card(label: str, value: str, delta: str = None, icon: str = None, status: str = "neutral"):
    """Renders a Blue & White frosted glass metric card."""
    delta_color = "#15803d" if status == "positive" else ("#b91c1c" if status == "negative" else "#2563eb")
    delta_html = f"""<div style="font-size: 0.82rem; color: {delta_color}; font-weight: 600; margin-top: 4px;">{delta}</div>""" if delta else ""
    icon_html = f"""<span style="font-size: 1.4rem; float: right;">{icon}</span>""" if icon else ""

    st.markdown(
        f"""<div class="metric-card">{icon_html}<div class="metric-label">{label}</div><div class="metric-value">{value}</div>{delta_html}</div>""",
        unsafe_allow_html=True
    )
