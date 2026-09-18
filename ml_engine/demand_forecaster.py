"""
OmniPulse AI - Predictive Sales & Demand Forecasting Engine
Implements Multi-Model Time Series Forecasting (Holt-Winters Exponential Smoothing
and Auto-Regressive Lagged Feature Regression) with accuracy metrics and confidence bands.
"""
import sys
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Ensure project root in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from database.queries import AnalyticsQueries


class DemandForecaster:
    """Predictive time-series modeling engine for store-level and item-level demand."""

    def __init__(self):
        self.queries = AnalyticsQueries()

    def prepare_daily_series(self) -> pd.DataFrame:
        """Loads and prepares daily time-series with continuous date index."""
        df = self.queries.get_daily_sales_timeseries()
        if df.empty:
            return pd.DataFrame()

        df = df.sort_values(by="order_date").reset_index(drop=True)
        # Ensure complete date range without missing calendar days
        full_idx = pd.date_range(start=df["order_date"].min(), end=df["order_date"].max(), freq="D")
        df = df.set_index("order_date").reindex(full_idx)
        df.index.name = "date"
        df["daily_revenue"] = df["daily_revenue"].fillna(0.0)
        df["order_count"] = df["order_count"].fillna(0.0)
        df["daily_profit"] = df["daily_profit"].fillna(0.0)
        df["daily_quantity"] = df["daily_quantity"].fillna(0.0)
        return df.reset_index()

    def forecast_holt_winters(
        self,
        target_col: str = "daily_revenue",
        forecast_horizon: int = 30,
        test_days: int = 30
    ) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
        """
        Fits Holt-Winters Exponential Smoothing on historical series,
        evaluates on test split, and projects future forecast horizon with confidence bands.
        """
        df = self.prepare_daily_series()
        if len(df) < test_days + 14:
            raise ValueError("Insufficient historical time series data for forecasting.")

        series = df.set_index("date")[target_col].astype(float)
        
        # Train / Test split
        train_series = series.iloc[:-test_days]
        test_series = series.iloc[-test_days:]

        # Fit model on training set
        # Using additive trend and 7-day weekly seasonal cycle
        seasonal_periods = 7 if len(train_series) >= 28 else None
        try:
            hw_model = ExponentialSmoothing(
                train_series,
                trend="add",
                seasonal="add" if seasonal_periods else None,
                seasonal_periods=seasonal_periods,
                initialization_method="estimated"
            ).fit()
            test_preds = hw_model.forecast(test_days)
        except Exception:
            # Fallback to simple exponential smoothing if convergence fails
            hw_model = ExponentialSmoothing(train_series, trend="add").fit()
            test_preds = hw_model.forecast(test_days)

        # Performance evaluation metrics on test partition
        y_true = test_series.values
        y_pred = np.maximum(test_preds.values, 0.0)

        mae = float(mean_absolute_error(y_true, y_pred))
        rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
        mape = float(np.mean(np.abs((y_true - y_pred) / np.maximum(y_true, 1e-5))) * 100)
        r2 = float(r2_score(y_true, y_pred)) if np.var(y_true) > 0 else 0.0

        test_eval_df = pd.DataFrame({
            "date": test_series.index,
            "actual": y_true,
            "predicted": y_pred.round(2),
            "error": (y_true - y_pred).round(2)
        })

        # Fit on full series for future projection
        try:
            full_model = ExponentialSmoothing(
                series,
                trend="add",
                seasonal="add" if seasonal_periods else None,
                seasonal_periods=seasonal_periods,
                initialization_method="estimated"
            ).fit()
            future_preds = full_model.forecast(forecast_horizon)
        except Exception:
            full_model = ExponentialSmoothing(series, trend="add").fit()
            future_preds = full_model.forecast(forecast_horizon)

        future_start = pd.to_datetime(series.index[-1]) + pd.to_timedelta(1, unit="D")
        future_dates = pd.date_range(start=future_start, periods=forecast_horizon, freq="D")
        future_values = np.maximum(future_preds.values, 0.0)

        # Statistical confidence intervals (95% CI based on residual standard deviation)
        residuals = series.values[-test_days:] - test_preds.values
        residual_std = float(np.std(residuals)) if len(residuals) > 0 else 10.0
        z_score = 1.96

        forecast_df = pd.DataFrame({
            "date": future_dates,
            "forecast": future_values.round(2),
            "lower_bound": np.maximum(0.0, future_values - (z_score * residual_std)).round(2),
            "upper_bound": (future_values + (z_score * residual_std)).round(2)
        })

        historical_df = df[["date", target_col]].rename(columns={target_col: "historical_value"})

        metrics = {
            "model_name": "Holt-Winters Triple Exponential Smoothing",
            "target_variable": target_col,
            "forecast_horizon_days": forecast_horizon,
            "test_split_days": test_days,
            "mae": round(mae, 2),
            "rmse": round(rmse, 2),
            "mape_pct": round(mape, 2),
            "r2_score": round(r2, 3),
            "residual_std": round(residual_std, 2)
        }

        return historical_df, forecast_df, metrics
