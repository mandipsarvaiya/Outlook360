"""Outlook360 - UI & Landing Page Components Package."""
from app.components.kpi_cards import render_kpi_card, render_kpi_grid
from app.components.charts import (
    create_revenue_trend_chart,
    create_pareto_chart,
    create_pca_cluster_chart,
    create_forecast_chart,
    create_heatmap_chart,
    create_abc_xyz_matrix_chart
)
from app.components.navigation import render_sidebar_header
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

__all__ = [
    "render_kpi_card",
    "render_kpi_grid",
    "create_revenue_trend_chart",
    "create_pareto_chart",
    "create_pca_cluster_chart",
    "create_forecast_chart",
    "create_heatmap_chart",
    "create_abc_xyz_matrix_chart",
    "render_sidebar_header",
    "render_landing_navbar",
    "render_hero_section",
    "render_what_is_section",
    "render_how_it_works",
    "render_platform_capabilities",
    "render_analytics_modules_showcase",
    "render_business_intelligence_grid",
    "render_industries_section",
    "render_business_questions",
    "render_ai_ml_section",
    "render_technical_foundation",
    "render_dashboard_preview",
    "render_footer"
]
