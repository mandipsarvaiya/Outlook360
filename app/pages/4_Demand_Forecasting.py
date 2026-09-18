"""
Outlook360 - Predictive Sales & Demand Forecasting Dashboard
Multi-horizon time-series projections with Holt-Winters Exponential Smoothing and 95% confidence intervals.
"""
import sys
from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.theme import apply_theme
from app.auth_gate import require_auth
from app.components.charts import create_forecast_chart
from app.components.navigation import render_sidebar_header
from ml_engine.demand_forecaster import DemandForecaster
from ml_engine.eda_engine import EDAEngine

st.set_page_config(page_title="Demand Forecasting - Outlook360", page_icon="🔮", layout="wide")
apply_theme()
render_sidebar_header()
user = require_auth(allowed_roles=["owner"])

profile = EDAEngine().get_kpi_summary()
curr = profile.get("currency", "₹")

st.markdown("## 🔮 Predictive Demand & Revenue Forecasting")
st.markdown("Leverages **Holt-Winters Triple Exponential Smoothing** (accounting for level, trend, and weekly 7-day cyclical seasonality) to forecast future revenue & demand volume.")

forecaster = DemandForecaster()

# Forecasting Controls
fcol1, fcol2 = st.columns([2, 2])
with fcol1:
    target_metric = st.selectbox("Target Forecasting Metric", options=[("daily_revenue", "Daily Revenue"), ("daily_quantity", "Daily Unit Demand")], format_func=lambda x: x[1])[0]
with fcol2:
    horizon_days = st.slider("Forecast Horizon (Future Days)", min_value=7, max_value=90, value=30, step=7)

try:
    hist_df, fc_df, metrics = forecaster.forecast_holt_winters(
        target_col=target_metric,
        forecast_horizon=horizon_days,
        test_days=30
    )

    # Model Evaluation Metrics
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    with mcol1:
        st.metric("Model Architecture", "Holt-Winters Multiplicative/Additive")
    with mcol2:
        mae_val = metrics.get("mae", 0.0)
        st.metric("Mean Absolute Error (MAE)", f"{curr}{mae_val:,.2f}" if "revenue" in target_metric else f"{mae_val:.1f} units")
    with mcol3:
        rmse_val = metrics.get("rmse", 0.0)
        st.metric("Root Mean Squared Error (RMSE)", f"{curr}{rmse_val:,.2f}" if "revenue" in target_metric else f"{rmse_val:.1f} units")
    with mcol4:
        mape_val = metrics.get("mape_pct", 0.0)
        st.metric("Mean Abs % Error (MAPE)", f"{mape_val:.1f}%", delta="Accurate" if mape_val < 35 else "Acceptable")

    st.markdown("<br>", unsafe_allow_html=True)

    # Plot Forecast Curve
    metric_label = "Revenue (" + curr + ")" if "revenue" in target_metric else "Units Demanded"
    fig_fc = create_forecast_chart(hist_df, fc_df, target_label=metric_label)
    st.plotly_chart(fig_fc, use_container_width=True)

    # Future Projection Data Table
    with st.expander(f"📅 View Detailed {horizon_days}-Day Forecast Schedule Table", expanded=False):
        st.dataframe(
            fc_df.rename(columns={
                "date": "Date",
                "forecast": f"Forecast ({curr})",
                "lower_bound": f"95% CI Lower Bound ({curr})",
                "upper_bound": f"95% CI Upper Bound ({curr})"
            }).style.format({
                f"Forecast ({curr})": "{:,.2f}",
                f"95% CI Lower Bound ({curr})": "{:,.2f}",
                f"95% CI Upper Bound ({curr})": "{:,.2f}"
            }),
            use_container_width=True
        )

except Exception as e:
    st.error(f"Forecasting Error: {e}")
