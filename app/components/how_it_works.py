"""
Outlook360 - Visual 6-Step Workflow Component
Presents 'HOW OUTLOOK360 WORKS' in a clean, scannable horizontal flow.
"""
import streamlit as st


def render_how_it_works():
    """Renders the 6-step visual data-to-insight workflow cards."""
    st.markdown(
        """<div id="how-it-works" class="section-header-block"><span class="section-badge">Data-to-Insight Workflow</span><h2 class="section-heading">HOW OUTLOOK360 WORKS</h2><p class="section-subheading">From business data to actionable insights.</p></div>""",
        unsafe_allow_html=True
    )

    steps = [
        ("01", "🗄️", "BUSINESS DATA", "Sales • Products • Customers • Inventory"),
        ("02", "⚙️", "DATA PROCESSING", "Clean • Organize • Prepare"),
        ("03", "📊", "ANALYTICS", "Trends • Patterns • Performance"),
        ("04", "🧠", "AI & MACHINE LEARNING", "Segments • Relationships • Patterns"),
        ("05", "🔮", "PREDICTION", "Demand • Trends • Forecasts"),
        ("06", "💡", "BUSINESS INSIGHTS", "Clear • Actionable • Data-driven")
    ]

    cards_html = ""
    for i, (num, icon, title, desc) in enumerate(steps):
        cards_html += f"""<div class="workflow-card"><div class="workflow-step-num">{num}</div><div class="workflow-icon">{icon}</div><div class="workflow-title">{title}</div><div class="workflow-desc">{desc}</div></div>"""

    st.markdown(
        f"""<div class="workflow-container"><div class="workflow-grid">{cards_html}</div></div>""",
        unsafe_allow_html=True
    )
