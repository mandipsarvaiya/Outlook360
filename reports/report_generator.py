"""
Outlook360 - Automated Executive Business Intelligence Report Generator
Compiles financial KPIs, Pareto classifications, customer cluster profiles,
forecast summaries, and inventory replenishment schedules into a polished printable HTML/PDF report.
"""
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Ensure project root in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ml_engine.eda_engine import EDAEngine
from ml_engine.rfm_segmentation import RFMSegmentationEngine
from ml_engine.demand_forecaster import DemandForecaster
from ml_engine.inventory_optimizer import InventoryOptimizer
from database.queries import AnalyticsQueries


class ExecutiveReportGenerator:
    """Generates comprehensive executive summary business intelligence reports."""

    def generate_html_report(self, output_path: str = "reports/Executive_BI_Report.html") -> str:
        """Compiles data across all analytics modules into a modern, printable HTML report."""
        eda = EDAEngine()
        kpis = eda.get_kpi_summary()
        curr = kpis.get("currency", "$")
        pareto_df, pareto_meta = eda.get_pareto_analysis()
        monthly_df = eda.get_monthly_growth_trend()

        rfm = RFMSegmentationEngine()
        clustered_df, rfm_meta = rfm.run_kmeans_clustering(4)

        forecaster = DemandForecaster()
        hist_df, fc_df, fc_meta = forecaster.forecast_holt_winters(forecast_horizon=30)

        inv = InventoryOptimizer()
        inv_df, inv_meta = inv.compute_abc_xyz_matrix()

        # Monthly Table HTML rows
        monthly_rows = ""
        if not monthly_df.empty:
            for _, r in monthly_df.iterrows():
                monthly_rows += f"""
                <tr>
                    <td>{r['month_label']}</td>
                    <td>{curr}{r['revenue']:,.2f}</td>
                    <td>{curr}{r['profit']:,.2f}</td>
                    <td>{r['orders']:,}</td>
                    <td>{r['revenue_growth_pct']:+.1f}%</td>
                    <td>{r['profit_margin_pct']:.1f}%</td>
                </tr>
                """

        # Pareto Top 5 Products HTML rows
        pareto_rows = ""
        if not pareto_df.empty:
            for _, r in pareto_df.head(6).iterrows():
                pareto_rows += f"""
                <tr>
                    <td><b>{r['product_name']}</b> ({r['sku']})</td>
                    <td>{r['category_name']}</td>
                    <td>{r['total_units_sold']:,}</td>
                    <td>{curr}{r['total_revenue']:,.2f}</td>
                    <td>{r['cumulative_pct']:.1f}%</td>
                    <td><span style="color: #4f46e5; font-weight: 600;">{r['pareto_class']}</span></td>
                </tr>
                """

        # Cluster Table HTML rows
        cluster_rows = ""
        if rfm_meta and "cluster_summary" in rfm_meta:
            for _, r in rfm_meta["cluster_summary"].iterrows():
                cluster_rows += f"""
                <tr>
                    <td><b>{r['cluster_label']}</b></td>
                    <td>{r['customer_count']:,}</td>
                    <td>{r['avg_recency']:.1f} days</td>
                    <td>{r['avg_frequency']:.1f} orders</td>
                    <td>{curr}{r['avg_monetary']:,.2f}</td>
                    <td>{r['revenue_share_pct']:.1f}%</td>
                </tr>
                """

        report_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Outlook360 - Executive Business Intelligence Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
            background-color: #f8fafc;
            color: #1e293b;
            margin: 0;
            padding: 30px;
        }}
        .report-container {{
            max-width: 950px;
            margin: 0 auto;
            background: #ffffff;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }}
        .header {{
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 20px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .header h1 {{
            margin: 0 0 6px 0;
            color: #0f172a;
            font-size: 26px;
        }}
        .header p {{
            margin: 0;
            color: #64748b;
            font-size: 14px;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 30px;
        }}
        .kpi-card {{
            background: #f1f5f9;
            padding: 18px;
            border-radius: 8px;
            border-left: 4px solid #4f46e5;
        }}
        .kpi-title {{
            font-size: 12px;
            text-transform: uppercase;
            color: #64748b;
            font-weight: 600;
        }}
        .kpi-val {{
            font-size: 22px;
            font-weight: 700;
            color: #0f172a;
            margin-top: 4px;
        }}
        h2 {{
            color: #1e293b;
            font-size: 18px;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 8px;
            margin-top: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 12px;
            font-size: 13px;
        }}
        th, td {{
            padding: 10px 12px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }}
        th {{
            background-color: #f8fafc;
            color: #475569;
            font-weight: 600;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 15px;
            border-top: 1px solid #e2e8f0;
            font-size: 11px;
            color: #94a3b8;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="report-container">
        <div class="header">
            <div>
                <h1>⚡ {kpis['business_name']}</h1>
                <p><b>Executive Business Intelligence & Machine Learning Report</b></p>
            </div>
            <div style="text-align: right;">
                <p><b>Report Date:</b> {datetime.now().strftime('%B %d, %Y')}</p>
                <p><b>Domain:</b> {kpis['domain_key'].upper()}</p>
            </div>
        </div>

        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-title">Gross Revenue</div>
                <div class="kpi-val">{curr}{kpis['gross_revenue']:,.2f}</div>
            </div>
            <div class="kpi-card" style="border-left-color: #10b981;">
                <div class="kpi-title">Net Profit Margin</div>
                <div class="kpi-val">{curr}{kpis['net_profit']:,.2f} ({kpis['profit_margin_pct']:.1f}%)</div>
            </div>
            <div class="kpi-card" style="border-left-color: #f59e0b;">
                <div class="kpi-title">Average Order Value</div>
                <div class="kpi-val">{curr}{kpis['average_order_value']:,.2f}</div>
            </div>
            <div class="kpi-card" style="border-left-color: #8b5cf6;">
                <div class="kpi-title">Active Customers</div>
                <div class="kpi-val">{kpis['active_customers']:,}</div>
            </div>
        </div>

        <h2>📈 Historical Financial Trajectory & MoM Pacing</h2>
        <table>
            <thead>
                <tr>
                    <th>Month</th>
                    <th>Gross Revenue</th>
                    <th>Net Profit</th>
                    <th>Orders</th>
                    <th>MoM Growth</th>
                    <th>Profit Margin</th>
                </tr>
            </thead>
            <tbody>
                {monthly_rows}
            </tbody>
        </table>

        <h2>🏆 Vital Revenue Drivers (Pareto 80/20 Analysis)</h2>
        <table>
            <thead>
                <tr>
                    <th>Product & SKU</th>
                    <th>Category</th>
                    <th>Units Sold</th>
                    <th>Revenue</th>
                    <th>Cumulative %</th>
                    <th>Classification</th>
                </tr>
            </thead>
            <tbody>
                {pareto_rows}
            </tbody>
        </table>

        <h2>👥 Machine Learning Customer Segmentation (K-Means)</h2>
        <table>
            <thead>
                <tr>
                    <th>Customer Segment</th>
                    <th>Customer Count</th>
                    <th>Avg Recency</th>
                    <th>Avg Frequency</th>
                    <th>Avg Spend</th>
                    <th>Revenue Share</th>
                </tr>
            </thead>
            <tbody>
                {cluster_rows}
            </tbody>
        </table>

        <h2>🔮 Predictive Sales Demand Horizon (Holt-Winters Multiplicative)</h2>
        <p style="font-size: 13px; color: #475569;">
            <b>30-Day Forecast Horizon:</b> Model MAE: <b>{curr}{fc_meta['mae']}</b> | MAPE: <b>{fc_meta['mape_pct']}%</b> | Residual Std Dev: <b>{curr}{fc_meta['residual_std']}</b>
        </p>

        <h2>📦 Supply Chain & Inventory Replenishment Priority</h2>
        <p style="font-size: 13px; color: #475569;">
            Total Monitored SKUs: <b>{inv_meta.get('total_skus', 0)}</b> | Target Service Level: <b>{inv_meta.get('service_level', '95%')}</b> | SKUs Needing Reorder: <b>{inv_meta.get('items_needing_reorder', 0)}</b>
        </p>

        <div class="footer">
            Generated automatically by <b>Outlook360 Platform</b> • Universal Business Intelligence & Predictive Analytics Engine
        </div>
    </div>
</body>
</html>
"""
        target_file = BASE_DIR / output_path
        target_file.parent.mkdir(parents=True, exist_ok=True)
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(report_html)

        print(f"[Report] Successfully generated executive report: {target_file}")
        return str(target_file)


if __name__ == "__main__":
    generator = ExecutiveReportGenerator()
    generator.generate_html_report()
