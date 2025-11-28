"""Forecasting pipeline with simple model selection."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

try:
    from statsmodels.tsa.arima.model import ARIMA
except Exception:  # pragma: no cover - optional dependency
    ARIMA = None


@dataclass
class ModelResult:
    name: str
    forecast: np.ndarray
    metrics: Dict[str, float]
    used_regressors: List[str]


def _compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    return {
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "mape": float(np.mean(np.abs((y_true - y_pred) / np.clip(y_true, a_min=1e-3, a_max=None)))),
    }


def baseline_naive(train: pd.Series, horizon: int) -> np.ndarray:
    return np.repeat(train.iloc[-1], horizon)


def moving_average(train: pd.Series, horizon: int, window: int = 3) -> np.ndarray:
    avg = train.tail(window).mean()
    return np.repeat(avg, horizon)


def fit_arima(train: pd.Series, horizon: int, order: Tuple[int, int, int] = (1, 1, 1)) -> np.ndarray:
    if ARIMA is None:
        return baseline_naive(train, horizon)
    model = ARIMA(train, order=order).fit()
    forecast = model.forecast(steps=horizon)
    return forecast.values


def fit_random_forest(features: pd.DataFrame, target: pd.Series, horizon: int) -> np.ndarray:
    X_train, X_val, y_train, y_val = train_test_split(features, target, test_size=0.2, shuffle=False)
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_val)
    metrics = _compute_metrics(y_val, preds)
    future = features.tail(horizon)
    forecast = model.predict(future)
    return forecast, metrics


def evaluate_models(df: pd.DataFrame, target_col: str, horizon: int) -> ModelResult:
    df = df.sort_values("date")
    target = df[target_col]
    metrics: Dict[str, float] = {}

    naive_fcst = baseline_naive(target, horizon)
    metrics_naive = _compute_metrics(target.tail(horizon), naive_fcst)

    moving_fcst = moving_average(target, horizon)
    metrics_ma = _compute_metrics(target.tail(horizon), moving_fcst)

    arima_fcst = fit_arima(target, horizon)
    metrics_arima = _compute_metrics(target.tail(horizon), arima_fcst)

    model_options = {
        "naive": (naive_fcst, metrics_naive),
        "moving_average": (moving_fcst, metrics_ma),
        "arima": (arima_fcst, metrics_arima),
    }

    best_name = min(model_options, key=lambda k: model_options[k][1]["rmse"])
    forecast, best_metrics = model_options[best_name]

    used_regressors = [col for col in df.columns if col not in {"date", target_col}]
    if used_regressors:
        feature_df = df.dropna().set_index("date")
        forecasts, rf_metrics = fit_random_forest(
            feature_df[used_regressors], feature_df[target_col], horizon
        )
        if rf_metrics["rmse"] < best_metrics["rmse"]:
            best_name = "random_forest"
            forecast = forecasts
            best_metrics = rf_metrics

    return ModelResult(name=best_name, forecast=np.array(forecast), metrics=best_metrics, used_regressors=used_regressors)
