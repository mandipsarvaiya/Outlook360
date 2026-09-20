"""
Outlook360 - Business Questions Component
Maps real business questions to clear analytical answers.
"""
import streamlit as st


def render_business_questions():
    """Renders the scannable 'WHAT CAN OUTLOOK360 HELP YOU UNDERSTAND?' card section."""
    st.markdown(
        """<div id="questions" class="section-header-block"><span class="section-badge">Strategic Answers</span><h2 class="section-heading">What Can Outlook360 Help You Understand?</h2><p class="section-subheading">Turn everyday business questions into clear, data-driven decisions.</p></div>""",
        unsafe_allow_html=True
    )

    questions = [
        ("📊", "How is the business performing?", "Track daily revenue, net profit margin velocity, and peak store footfall.", "Executive Overview"),
        ("📈", "Which products are driving sales?", "Use Pareto 80/20 analysis to isolate vital top-selling product drivers.", "Sales Analytics"),
        ("👥", "Who are your most valuable customers?", "Score customer recency, frequency, and monetary value automatically.", "Customer Intelligence"),
        ("🔮", "What could demand look like next?", "Forecast future sales curves using historical business patterns.", "Demand Prediction"),
        ("🛒", "Which products are frequently purchased together?", "Discover high-affinity item combinations for cross-selling.", "Market Basket"),
        ("📦", "Where are inventory risks appearing?", "Calculate safety stock buffers and dynamic reorder points.", "Inventory Intelligence")
    ]

    col1, col2 = st.columns(2)
    for i, (icon, q, ans, mod) in enumerate(questions):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            st.markdown(
                f"""<div class="question-card"><div class="question-title">{icon} {q}</div><div style="font-size: 0.82rem; color: #475569; margin-bottom: 4px;">{ans}</div><div class="question-meta">Answered by: <b style="color: #1d4ed8;">{mod}</b></div></div>""",
                unsafe_allow_html=True
            )
