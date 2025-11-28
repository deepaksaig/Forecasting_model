"""Helpers for aligning regressors and building time-series features."""
from __future__ import annotations

from typing import Dict, List

import pandas as pd


def align_regressors(target: pd.DataFrame, regressors: Dict[str, pd.DataFrame], freq: str = "M") -> pd.DataFrame:
    merged = target.copy()
    merged = merged.set_index("date").resample(freq).sum().reset_index()
    for name, df in regressors.items():
        temp = df.copy()
        temp = temp.set_index("date").resample(freq).mean().ffill().reset_index()
        merged = merged.merge(temp, on="date", how="left")
    return merged


def add_lag_features(df: pd.DataFrame, columns: List[str], lags: List[int]) -> pd.DataFrame:
    for col in columns:
        for lag in lags:
            df[f"{col}_lag_{lag}"] = df[col].shift(lag)
    return df


def add_rolling_features(df: pd.DataFrame, columns: List[str], windows: List[int]) -> pd.DataFrame:
    for col in columns:
        for window in windows:
            df[f"{col}_roll_{window}"] = df[col].rolling(window).mean()
    return df


def add_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    df["month"] = df["date"].dt.month
    df["quarter"] = df["date"].dt.quarter
    df["year"] = df["date"].dt.year
    return df


def summarize_regressors(df: pd.DataFrame, target_col: str) -> List[dict]:
    summaries: List[dict] = []
    for col in df.columns:
        if col in {"date", target_col}:
            continue
        summary = {
            "name": col,
            "description": "Mock regressor",
            "coverage_start": df["date"].min().date(),
            "coverage_end": df["date"].max().date(),
            "missing_ratio": float(df[col].isna().mean()),
            "correlation_with_target": float(df[col].corr(df[target_col])) if df[col].count() > 3 else None,
        }
        summaries.append(summary)
    return summaries
