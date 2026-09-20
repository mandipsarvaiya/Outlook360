"""
Outlook360 - Master Public Landing Page & Enterprise BI Architecture Entry Point
Universal Enterprise Business Intelligence & Predictive Analytics Platform.
"""
import sys
from pathlib import Path
import streamlit as st

# Ensure project root in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.theme import apply_theme
from app.auth_gate import init_auth_state
from app.components.landing_navbar import render_landing_navbar
from app.components.hero import render_hero_section
from app.components.what_is_section import render_what_is_section
from app.components.how_it_works import render_how_it_works
from app.components.platform_capabilities import render_platform_capabilities
from app.components.analytics_modules_showcase import render_analytics_modules_showcase
from app.components.business_intelligence_grid import render_business_intelligence_grid
from app.components.industries_section import render_industries_section
from app.components.business_questions import render_business_questions
from app.components.ai_ml_section import render_ai_ml_section
from app.components.technical_foundation import render_technical_foundation
from app.components.dashboard_preview import render_dashboard_preview
from app.components.footer import render_footer

# Page Configuration
st.set_page_config(
    page_title="Outlook360 - Universal Enterprise BI & Predictive Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply Blue & White Theme & Initialize Auth State
apply_theme(is_landing_page=True)
init_auth_state()

# 1. NAVIGATION
render_landing_navbar()

# 2. HERO
render_hero_section()

# 3. WHAT IS OUTLOOK360?
render_what_is_section()

# 4. HOW OUTLOOK360 WORKS (Visual 6-Step Workflow)
render_how_it_works()

# 5. CORE PLATFORM CAPABILITIES
render_platform_capabilities()

# 6. POWERFUL ANALYTICS MODULES (6 Core Production Modules)
render_analytics_modules_showcase()

# 7. BUSINESS INTELLIGENCE FOR EVERY DECISION (8 Capability Cards)
render_business_intelligence_grid()

# 8. ONE PLATFORM. MULTIPLE BUSINESS DOMAINS.
render_industries_section()

# 9. WHAT CAN OUTLOOK360 HELP YOU UNDERSTAND?
render_business_questions()

# 10. WHERE AI MEETS BUSINESS DATA (AI/ML Workflow & Capabilities)
render_ai_ml_section()

# 11. BUILT ON DATA & AI (Technology Foundation & Expandable Architecture)
render_technical_foundation()

# 12. SEE OUTLOOK360 IN ACTION (Dashboard Preview & Gateway)
render_dashboard_preview()

# 13. FOOTER
render_footer()
