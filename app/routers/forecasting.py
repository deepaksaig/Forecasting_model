"""Endpoints for running forecasting models."""
from __future__ import annotations

from datetime import timedelta

import pandas as pd
from fastapi import APIRouter, HTTPException

from app.config import DEFAULT_FORECAST_HORIZON
from app.models.schemas import ForecastRequest, ForecastResult
from app.services import external_data_fetcher, feature_engineering, forecasting
from app.utils.storage import data_store

router = APIRouter(prefix="/forecast", tags=["forecast"])


@router.post("/{file_id}", response_model=ForecastResult)
async def run_forecast(file_id: str, body: ForecastRequest) -> ForecastResult:
    if file_id not in data_store.sales:
        raise HTTPException(status_code=404, detail="Upload not found")

    df = data_store.get_sales(file_id)
    regressors = {}
    if body.use_exogenous:
        regressors = external_data_fetcher.fetch_all_regressors(df["date"].min(), df["date"].max())
    merged = feature_engineering.align_regressors(df[["date", body.target_metric]], regressors)
    merged = feature_engineering.add_lag_features(merged, [body.target_metric], [1, 2, 3])
    merged = feature_engineering.add_rolling_features(merged, [body.target_metric], [3, 6])
    merged = feature_engineering.add_calendar_features(merged)
    merged = merged.dropna()

    horizon = body.forecast_horizon or DEFAULT_FORECAST_HORIZON
    result = forecasting.evaluate_models(merged, body.target_metric, horizon)

    start_date = merged["date"].max() + timedelta(days=30)
    dates = pd.date_range(start_date, periods=horizon, freq="M").date.tolist()

    return ForecastResult(
        model_name=result.name,
        metrics=result.metrics,
        forecast=list(map(float, result.forecast)),
        dates=dates,
        used_regressors=result.used_regressors,
        message="Forecast generated with mock models",
    )
