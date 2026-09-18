"""
Outlook360 - Interactive Plotly Visualizations Component
Provides reusable, highly styled Blue & White chart builders.
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Base Blue & White Theme Layout Settings
BASE_LIGHT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255, 255, 255, 0.8)",
    font=dict(family="Plus Jakarta Sans, Inter, sans-serif", color="#1e293b", size=12),
    margin=dict(l=40, r=40, t=50, b=40)
)

# Export for generic charts
DARK_LAYOUT_TEMPLATE = BASE_LIGHT_LAYOUT


def create_revenue_trend_chart(df: pd.DataFrame, currency: str = "$") -> go.Figure:
    """Creates a line chart with shaded area for daily/monthly revenue & profit."""
    fig = go.Figure()

    # Revenue Line
    fig.add_trace(go.Scatter(
        x=df["order_date"],
        y=df["daily_revenue"],
        mode="lines",
        name="Daily Revenue",
        line=dict(color="#2563eb", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(37, 99, 235, 0.08)",
        hovertemplate="<b>Date:</b> %{x|%Y-%m-%d}<br><b>Revenue:</b> " + currency + "%{y:,.2f}<extra></extra>"
    ))

    # Profit Line
    fig.add_trace(go.Scatter(
        x=df["order_date"],
        y=df["daily_profit"],
        mode="lines",
        name="Net Profit",
        line=dict(color="#059669", width=2),
        hovertemplate="<b>Date:</b> %{x|%Y-%m-%d}<br><b>Profit:</b> " + currency + "%{y:,.2f}<extra></extra>"
    ))

    fig.update_layout(
        **BASE_LIGHT_LAYOUT,
        title="<b>Daily Revenue & Net Profit Trajectory</b>",
        hovermode="x unified",
        height=380,
        xaxis=dict(gridcolor="#f1f5f9", zerolinecolor="#e2e8f0"),
        yaxis=dict(gridcolor="#f1f5f9", zerolinecolor="#e2e8f0")
    )
    return fig


def create_pareto_chart(df: pd.DataFrame, currency: str = "$") -> go.Figure:
    """Creates Pareto 80/20 Dual-Axis Bar & Cumulative Line Chart."""
    fig = go.Figure()

    # Bar chart of individual product revenue
    colors = ["#2563eb" if c == "Vital Few (Top 80%)" else "#94a3b8" for c in df["pareto_class"]]
    fig.add_trace(go.Bar(
        x=df["product_name"],
        y=df["total_revenue"],
        name="Product Revenue",
        marker=dict(color=colors),
        hovertemplate="<b>%{x}</b><br>Revenue: " + currency + "%{y:,.2f}<extra></extra>"
    ))

    # Cumulative Percentage Line (Secondary Y Axis)
    fig.add_trace(go.Scatter(
        x=df["product_name"],
        y=df["cumulative_pct"],
        name="Cumulative Share %",
        mode="lines+markers",
        line=dict(color="#d97706", width=2.5),
        marker=dict(size=6),
        yaxis="y2",
        hovertemplate="<b>Cumulative:</b> %{y:.1f}%<extra></extra>"
    ))

    # 80% Threshold reference line
    fig.add_shape(
        type="line",
        x0=-0.5,
        x1=len(df) - 0.5,
        y0=80,
        y1=80,
        yref="y2",
        line=dict(color="#dc2626", width=1.5, dash="dash")
    )

    fig.update_layout(
        **BASE_LIGHT_LAYOUT,
        title="<b>Product Pareto (80/20) Revenue Distribution</b>",
        height=420,
        xaxis=dict(tickangle=-45, showgrid=False),
        yaxis=dict(title="Revenue (" + currency + ")", gridcolor="#f1f5f9"),
        yaxis2=dict(
            title="Cumulative %",
            overlaying="y",
            side="right",
            range=[0, 105],
            showgrid=False
        ),
        legend=dict(x=0.01, y=0.99)
    )
    return fig


def create_pca_cluster_chart(df: pd.DataFrame, is_3d: bool = False) -> go.Figure:
    """Creates 2D or 3D PCA scatter chart for customer clusters in Blue & White theme."""
    color_map = {
        "Platinum VIPs": "#1d4ed8",          # Deep Blue
        "Regular Active Spenders": "#0284c7", # Sky Blue
        "At-Risk / Lapsed": "#f59e0b",        # Amber
        "Standard Casuals": "#059669"         # Emerald
    }

    hover_col = "customer_name" if "customer_name" in df.columns else ("name" if "name" in df.columns else None)

    if is_3d and "pca_z" in df.columns:
        fig = px.scatter_3d(
            df,
            x="pca_x",
            y="pca_y",
            z="pca_z",
            color="cluster_name",
            hover_name=hover_col,
            hover_data=["customer_code", "city", "tier", "recency", "frequency", "monetary"],
            title="<b>3D Customer Cluster Landscape (PCA Projection)</b>",
            color_discrete_map=color_map
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            scene=dict(
                bgcolor="rgba(248, 250, 252, 0.9)",
                xaxis=dict(backgroundcolor="#ffffff", gridcolor="#e2e8f0"),
                yaxis=dict(backgroundcolor="#ffffff", gridcolor="#e2e8f0"),
                zaxis=dict(backgroundcolor="#ffffff", gridcolor="#e2e8f0")
            ),
            height=500,
            font=dict(family="Plus Jakarta Sans, Inter, sans-serif", color="#0f172a")
        )
    else:
        fig = px.scatter(
            df,
            x="pca_x",
            y="pca_y",
            color="cluster_name",
            hover_name=hover_col,
            hover_data=["customer_code", "city", "tier", "recency", "frequency", "monetary"],
            title="<b>2D Customer Segmentation Landscape (PCA Features)</b>",
            color_discrete_map=color_map
        )
        fig.update_layout(
            **BASE_LIGHT_LAYOUT,
            height=450,
            xaxis=dict(gridcolor="#f1f5f9"),
            yaxis=dict(gridcolor="#f1f5f9")
        )

    return fig


def create_forecast_chart(
    hist_df: pd.DataFrame,
    fc_df: pd.DataFrame,
    target_label: str = "Revenue ($)"
) -> go.Figure:
    """Creates time series forecasting chart with 95% confidence intervals."""
    fig = go.Figure()

    # Historical
    fig.add_trace(go.Scatter(
        x=hist_df["date"],
        y=hist_df["historical_value"],
        mode="lines",
        name="Historical Actual",
        line=dict(color="#64748b", width=2),
        hovertemplate="<b>Actual:</b> %{y:,.2f}<extra></extra>"
    ))

    # Confidence Interval Bounds
    fig.add_trace(go.Scatter(
        x=fc_df["date"],
        y=fc_df["upper_bound"],
        mode="lines",
        line=dict(width=0),
        showlegend=False,
        hoverinfo="none"
    ))
    fig.add_trace(go.Scatter(
        x=fc_df["date"],
        y=fc_df["lower_bound"],
        mode="lines",
        line=dict(width=0),
        fill="tonexty",
        fillcolor="rgba(37, 99, 235, 0.12)",
        name="95% Confidence Interval",
        hoverinfo="none"
    ))

    # Forecast Projected Line
    fig.add_trace(go.Scatter(
        x=fc_df["date"],
        y=fc_df["forecast"],
        mode="lines+markers",
        name="ML Forecast Projection",
        line=dict(color="#2563eb", width=3, dash="dash"),
        marker=dict(size=5, color="#1d4ed8"),
        hovertemplate="<b>Forecast:</b> %{y:,.2f}<extra></extra>"
    ))

    fig.update_layout(
        **BASE_LIGHT_LAYOUT,
        title=f"<b>Predictive Demand & {target_label} Forecasting Horizon</b>",
        hovermode="x unified",
        height=420,
        xaxis=dict(gridcolor="#f1f5f9"),
        yaxis=dict(gridcolor="#f1f5f9")
    )
    return fig


def create_heatmap_chart(pivot_df: pd.DataFrame) -> go.Figure:
    """Creates hourly footfall density heatmap in Blue & White style."""
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=[f"{h:02d}:00" for h in pivot_df.columns],
        y=pivot_df.index,
        colorscale="Blues",
        hovertemplate="<b>Day:</b> %{y}<br><b>Hour:</b> %{x}<br><b>Orders:</b> %{z}<extra></extra>"
    ))
    fig.update_layout(
        **BASE_LIGHT_LAYOUT,
        title="<b>Hourly Transaction Density Heatmap (Day × Hour Footfall)</b>",
        height=320,
        xaxis=dict(title="Hour of Day", showgrid=False),
        yaxis=dict(title="", showgrid=False)
    )
    return fig


def create_abc_xyz_matrix_chart(df: pd.DataFrame) -> go.Figure:
    """Creates 9-box ABC-XYZ Matrix distribution heatmap."""
    categories = ["A", "B", "C"]
    volatilities = ["X", "Y", "Z"]

    matrix = np.zeros((3, 3), dtype=int)
    for i, a in enumerate(categories):
        for j, z in enumerate(volatilities):
            seg = f"{a}{z}"
            matrix[i, j] = len(df[df["abc_xyz_segment"] == seg])

    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=["X (Stable Demand)", "Y (Fluctuating)", "Z (Erratic Demand)"],
        y=["A (High Value 70%)", "B (Moderate 20%)", "C (Low Value 10%)"],
        text=matrix,
        texttemplate="<b>%{text} SKUs</b>",
        textfont={"size": 14, "color": "white"},
        colorscale="Blues",
        showscale=False
    ))

    fig.update_layout(
        **BASE_LIGHT_LAYOUT,
        title="<b>9-Box ABC-XYZ Inventory Matrix Grid</b>",
        height=340,
        xaxis=dict(title="Demand Volatility (XYZ)", showgrid=False),
        yaxis=dict(title="Revenue Contribution (ABC)", showgrid=False)
    )
    return fig
