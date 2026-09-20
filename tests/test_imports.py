"""
Outlook360 - Deep Import & Component Verification
Imports all backend modules, DB queries, ML engines, and UI components to verify 100% clean execution.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def test_imports():
    print("Verifying all imports...")

    import config.settings
    import config.database_config
    import database.connection
    import database.queries
    import database.auth
    import database.seed_data
    import data_generators.domain_configs
    import data_generators.synthetic_generator
    import ml_engine.eda_engine
    import ml_engine.rfm_segmentation
    import ml_engine.demand_forecaster
    import ml_engine.market_basket
    import ml_engine.inventory_optimizer
    import ml_engine.anomaly_detector
    import app.theme
    import app.auth_gate
    import app.components.charts
    import app.components.kpi_cards
    import app.components.navigation
    import app.components.landing_navbar
    import app.components.hero
    import app.components.what_is_section
    import app.components.how_it_works
    import app.components.platform_capabilities
    import app.components.analytics_modules_showcase
    import app.components.business_intelligence_grid
    import app.components.industries_section
    import app.components.business_questions
    import app.components.ai_ml_section
    import app.components.technical_foundation
    import app.components.dashboard_preview
    import app.components.footer
    
    # Check theme exports
    assert hasattr(app.theme, "apply_theme"), "apply_theme missing"
    assert hasattr(app.theme, "render_custom_css"), "render_custom_css missing"
    assert hasattr(app.theme, "render_header"), "render_header missing"
    assert hasattr(app.theme, "render_metric_card"), "render_metric_card missing"

    # Check auth exports
    assert hasattr(app.auth_gate, "require_auth"), "require_auth missing"
    assert hasattr(app.auth_gate, "init_auth_state"), "init_auth_state missing"
    assert hasattr(app.auth_gate, "login_user"), "login_user missing"
    assert hasattr(app.auth_gate, "render_auth_sidebar"), "render_auth_sidebar missing"

    # Check landing component exports
    assert hasattr(app.components.landing_navbar, "render_landing_navbar"), "render_landing_navbar missing"
    assert hasattr(app.components.hero, "render_hero_section"), "render_hero_section missing"
    assert hasattr(app.components.what_is_section, "render_what_is_section"), "render_what_is_section missing"
    assert hasattr(app.components.how_it_works, "render_how_it_works"), "render_how_it_works missing"
    assert hasattr(app.components.platform_capabilities, "render_platform_capabilities"), "render_platform_capabilities missing"
    assert hasattr(app.components.analytics_modules_showcase, "render_analytics_modules_showcase"), "render_analytics_modules_showcase missing"
    assert hasattr(app.components.business_intelligence_grid, "render_business_intelligence_grid"), "render_business_intelligence_grid missing"
    assert hasattr(app.components.industries_section, "render_industries_section"), "render_industries_section missing"
    assert hasattr(app.components.business_questions, "render_business_questions"), "render_business_questions missing"
    assert hasattr(app.components.ai_ml_section, "render_ai_ml_section"), "render_ai_ml_section missing"
    assert hasattr(app.components.technical_foundation, "render_technical_foundation"), "render_technical_foundation missing"
    assert hasattr(app.components.dashboard_preview, "render_dashboard_preview"), "render_dashboard_preview missing"
    assert hasattr(app.components.footer, "render_footer"), "render_footer missing"

    print("All Python modules and component exports verified successfully!")

if __name__ == "__main__":
    test_imports()
